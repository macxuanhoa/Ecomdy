import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import context_compiler


class ContextCompilerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "docs").mkdir()
        (self.root / "docs" / "a.md").write_text("alpha", encoding="utf-8")
        (self.root / "docs" / "b.md").write_text("beta", encoding="utf-8")

    def tearDown(self):
        self.temporary.cleanup()

    def request(self, **updates):
        value = {"include_paths": ["docs"], "max_files": 10, "max_bytes": 1024}
        value.update(updates)
        return value

    def test_manifest_hashes_local_files_without_embedding_content(self):
        result = context_compiler.compile_context(self.request(), self.root)
        self.assertEqual(result["state"], "COMPILED")
        self.assertEqual(result["summary"]["file_count"], 2)
        self.assertTrue(all(not item["content_included"] for item in result["files"]))
        self.assertNotIn("alpha", json.dumps(result))
        self.assertEqual(result["policy"]["network_enabled"], False)

    def test_duplicate_content_is_deduplicated_with_provenance(self):
        (self.root / "docs" / "b.md").write_text("alpha", encoding="utf-8")
        result = context_compiler.compile_context(self.request(), self.root)
        self.assertEqual(result["summary"]["file_count"], 2)
        self.assertEqual(result["summary"]["unique_content_count"], 1)
        self.assertEqual(result["summary"]["deduplicated_bytes"], 5)
        self.assertEqual(len(result["content_pool"][0]["paths"]), 2)

    def test_file_and_byte_limits_fail_closed(self):
        files = context_compiler.compile_context(self.request(max_files=1), self.root)
        byte_cap = context_compiler.compile_context(self.request(max_bytes=4), self.root)
        self.assertEqual(files["state"], "BLOCKED")
        self.assertEqual(files["limit_violation"]["kind"], "max_files")
        self.assertEqual(byte_cap["state"], "BLOCKED")
        self.assertEqual(byte_cap["limit_violation"]["kind"], "max_bytes")

    def test_absolute_and_parent_paths_are_rejected(self):
        for value in ("../outside", "C:/outside", "/outside", "https://example.invalid/file"):
            with self.subTest(value=value):
                result = context_compiler.compile_context(self.request(include_paths=[value]), self.root)
                self.assertEqual(result["state"], "BLOCKED")

    def test_originals_are_excluded_unless_explicitly_allowed(self):
        original = self.root / "docs" / "00-original"
        original.mkdir()
        (original / "private.txt").write_text("private-source", encoding="utf-8")
        excluded = context_compiler.compile_context(self.request(include_paths=["docs/00-original"]), self.root)
        included = context_compiler.compile_context(self.request(include_paths=["docs/00-original"], include_originals=True), self.root)
        self.assertEqual(excluded["state"], "BLOCKED")
        self.assertTrue(any("Original source" in item["reason"] for item in excluded["excluded"]))
        self.assertEqual(included["state"], "COMPILED")
        self.assertNotIn("private-source", json.dumps(included))

    def test_exclude_rules_and_git_metadata_are_not_loaded(self):
        (self.root / ".git").mkdir()
        (self.root / ".git" / "config").write_text("git-data", encoding="utf-8")
        result = context_compiler.compile_context(self.request(include_paths=["."], exclude_paths=["docs/b.md"]), self.root)
        paths = {item["path"] for item in result["files"]}
        self.assertEqual(paths, {"docs/a.md"})
        self.assertNotIn("git-data", json.dumps(result))

    def test_glob_include_is_supported(self):
        result = context_compiler.compile_context(self.request(include_paths=["docs/*.md"]), self.root)
        self.assertEqual(result["summary"]["file_count"], 2)

    def test_glob_non_regular_match_is_blocked(self):
        special = self.root / "docs" / "special.md"
        special.mkdir()
        original_is_file = Path.is_file
        original_is_dir = Path.is_dir

        def is_file(path):
            return False if Path(path) == special else original_is_file(path)

        def is_dir(path):
            return False if Path(path) == special else original_is_dir(path)

        with patch.object(Path, "is_file", is_file), patch.object(Path, "is_dir", is_dir):
            result = context_compiler.compile_context(self.request(include_paths=["docs/*.md"]), self.root)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any("non-regular path" in error for error in result["errors"]))

    def test_direct_symlink_is_rejected(self):
        link = self.root / "docs" / "link.md"
        try:
            link.symlink_to(self.root / "docs" / "a.md")
        except OSError as exc:
            self.skipTest(f"Symlink creation unavailable: {exc}")
        result = context_compiler.compile_context(self.request(include_paths=["docs/link.md"]), self.root)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any("symlink" in error.lower() for error in result["errors"]))

    def test_symlink_detection_fails_closed_when_host_blocks_creation(self):
        link = self.root / "docs" / "link.md"
        link.write_text("alpha", encoding="utf-8")
        original = Path.is_symlink

        def is_symlink(path):
            return Path(path) == link or original(path)

        with patch.object(Path, "is_symlink", is_symlink):
            result = context_compiler.compile_context(self.request(include_paths=["docs/link.md"]), self.root)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any("symlink" in error.lower() for error in result["errors"]))

    def test_baseline_delta_reports_added_changed_and_unchanged(self):
        baseline = context_compiler.compile_context(self.request(), self.root)
        baseline_path = self.root / "baseline.json"
        baseline_path.write_text(json.dumps(baseline), encoding="utf-8")
        (self.root / "docs" / "a.md").write_text("changed", encoding="utf-8")
        (self.root / "docs" / "c.md").write_text("new", encoding="utf-8")
        result = context_compiler.compile_context(self.request(baseline_manifest="baseline.json"), self.root)
        self.assertEqual(result["delta"]["added_paths"], ["docs/c.md"])
        self.assertEqual(result["delta"]["changed_paths"], ["docs/a.md"])
        self.assertEqual(result["delta"]["unchanged_paths"], ["docs/b.md"])

    def test_missing_path_and_invalid_request_are_blocked(self):
        missing = context_compiler.compile_context(self.request(include_paths=["missing"]), self.root)
        invalid = context_compiler.compile_context({"include_paths": ["docs"], "max_files": True, "max_bytes": 10}, self.root)
        self.assertEqual(missing["state"], "BLOCKED")
        self.assertEqual(invalid["state"], "BLOCKED")

    def test_compilation_is_deterministic(self):
        first = context_compiler.compile_context(self.request(), self.root)
        second = context_compiler.compile_context(dict(reversed(list(self.request().items()))), self.root)
        self.assertEqual(first, second)
        self.assertEqual(first["summary"]["token_measurement_status"], "not_measured")

    def test_cli_writes_manifest_and_blocked_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            request_path = Path(directory) / "request.json"
            output_path = Path(directory) / "manifest.json"
            request_path.write_text(json.dumps(self.request()), encoding="utf-8")
            stdout = StringIO()
            with redirect_stdout(stdout):
                code = context_compiler.main([str(request_path), "--project", str(self.root), "--output", str(output_path)])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8")), json.loads(stdout.getvalue()))
            with redirect_stdout(StringIO()):
                self.assertEqual(context_compiler.main([str(request_path), "--project", str(self.root), "--output", str(output_path)]), 0)
            request_path.write_text(json.dumps(self.request(include_paths=["../outside"])), encoding="utf-8")
            with redirect_stdout(StringIO()):
                self.assertEqual(context_compiler.main([str(request_path), "--project", str(self.root)]), 3)


if __name__ == "__main__":
    unittest.main()
