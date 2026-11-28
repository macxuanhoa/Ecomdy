import copy
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))
import scope_checker
import task_contract
import validate_execution
import verification_runner


class ExecutionGateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        self.git("init", "-q")
        self.git("config", "user.email", "devharness@example.invalid")
        self.git("config", "user.name", "DevHarness Test")
        (self.root / ".gitignore").write_text(".harness/state/\n", encoding="utf-8")
        (self.root / "allowed.txt").write_text("base\n", encoding="utf-8")
        (self.root / "scripts").mkdir()
        (self.root / "scripts" / "check.py").write_text("print('CHECK-PASS')\n", encoding="utf-8")
        self.git("add", ".")
        self.git("-c", "commit.gpgsign=false", "commit", "-qm", "fixture")
        self.head = self.git("rev-parse", "HEAD").strip()
        self.contract_path = self.base / "contract.json"
        self.contract = {
            "schema_version": "1.0",
            "task_id": "TASK-GATE-001",
            "trace_id": "TRACE-001",
            "objective": "Verify an allowed fixture change.",
            "acceptance_criteria": ["The allowlisted check passes."],
            "route_id": "ROUTE-FEATURE",
            "profile_id": "PROFILE-STANDARD",
            "recipe_id": "RECIPE-001",
            "verification_technique_id": "TECH-038",
            "scope": {
                "allow_paths": ["allowed.txt", "scripts/**"],
                "base_commit": self.head,
                "max_changed_files": 10,
                "max_changed_bytes": 100000,
            },
            "commands": [{
                "id": "CHECK-001",
                "kind": "test",
                "argv": [sys.executable, "scripts/check.py"],
                "criteria": ["The allowlisted check passes."],
                "timeout_seconds": 10,
                "max_output_bytes": 65536,
            }],
            "budgets": {"max_iterations": 1, "max_runtime_minutes": 5, "max_cost_usd": 0, "max_retries": 0},
            "approvals": ["fixture-test-only"],
            "evidence_dir": ".harness/state/evidence",
            "secret_scan_required": False,
        }

    def tearDown(self):
        self.temporary.cleanup()

    def git(self, *args):
        result = subprocess.run(["git", "-C", str(self.root), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, shell=False, check=False)
        if result.returncode != 0:
            self.fail(f"git {' '.join(args)} failed: {result.stderr.decode('utf-8', errors='replace')}")
        return result.stdout.decode("utf-8")

    def write_contract(self):
        self.contract_path.write_text(json.dumps(self.contract), encoding="utf-8")

    def test_clean_and_all_change_states_are_observed(self):
        clean = scope_checker.check_scope(self.contract, self.root)
        self.assertEqual(clean["state"], "PASS")
        self.assertEqual(clean["observations"]["changed_file_count"], 0)
        (self.root / "allowed.txt").write_text("unstaged\n", encoding="utf-8")
        self.git("add", "allowed.txt")
        (self.root / "allowed.txt").write_text("staged and unstaged\n", encoding="utf-8")
        (self.root / "scripts" / "new.py").write_text("print('new')\n", encoding="utf-8")
        result = scope_checker.check_scope(self.contract, self.root)
        self.assertEqual(result["state"], "PASS")
        self.assertEqual(result["observations"]["staged_paths"], ["allowed.txt"])
        self.assertEqual(result["observations"]["unstaged_paths"], ["allowed.txt"])
        self.assertEqual(result["observations"]["untracked_paths"], ["scripts/new.py"])
        self.assertEqual(result["repository"]["changed_paths"], ["allowed.txt"])

    def test_out_of_scope_untracked_file_is_blocked(self):
        (self.root / "outside.txt").write_text("outside\n", encoding="utf-8")
        result = scope_checker.check_scope(self.contract, self.root)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any(item["kind"] == "outside_allowlist" and item["path"] == "outside.txt" for item in result["violations"]))

    def test_protected_paths_cannot_be_enabled_by_empty_deny_list(self):
        self.contract["scope"]["allow_paths"] = ["**"]
        self.contract["scope"]["deny_paths"] = []
        (self.root / ".env").write_text("SECRET=not-real\n", encoding="utf-8")
        result = scope_checker.check_scope(self.contract, self.root)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any(item["kind"] == "denied_path" and item["path"] == ".env" for item in result["violations"]))

    def test_rename_checks_both_old_and_new_paths(self):
        self.git("mv", "allowed.txt", "renamed.txt")
        self.contract["scope"]["allow_paths"] = ["renamed.txt"]
        result = scope_checker.check_scope(self.contract, self.root)
        self.assertEqual(result["state"], "BLOCKED")
        statuses = {item["path"]: item for item in result["observations"]["path_statuses"]}
        self.assertEqual(statuses["renamed.txt"]["previous_path"], "allowed.txt")
        self.assertTrue(any(item["path"] == "allowed.txt" and item["kind"] == "outside_allowlist" for item in result["violations"]))

    def test_file_and_byte_limits_fail_closed(self):
        (self.root / "allowed.txt").write_text("x" * 20, encoding="utf-8")
        self.contract["scope"]["max_changed_files"] = 1
        self.contract["scope"]["max_changed_bytes"] = 10
        result = scope_checker.check_scope(self.contract, self.root)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any(item["kind"] == "max_changed_bytes" for item in result["violations"]))
        (self.root / "scripts" / "new.py").write_text("pass\n", encoding="utf-8")
        result = scope_checker.check_scope(self.contract, self.root)
        self.assertTrue(any(item["kind"] == "max_changed_files" for item in result["violations"]))

    def test_non_git_project_is_blocked(self):
        plain = self.base / "plain"
        plain.mkdir()
        result = scope_checker.check_scope(self.contract, plain)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(result["errors"])
        verification = verification_runner.verify_task(self.contract, plain)
        self.assertEqual(verification["state"], "BLOCKED")
        self.assertEqual(verification["execution_state"], "NOT_EXECUTED")
        self.assertTrue(verification["errors"])

    def test_invalid_contracts_fail_before_execution(self):
        cases = []
        missing = copy.deepcopy(self.contract)
        missing["acceptance_criteria"] = []
        cases.append(missing)
        shell = copy.deepcopy(self.contract)
        shell["commands"][0]["argv"] = ["bash", "-c", "echo unsafe"]
        cases.append(shell)
        inline = copy.deepcopy(self.contract)
        inline["commands"][0]["argv"] = [sys.executable, "-c", "print('unsafe')"]
        cases.append(inline)
        uncovered = copy.deepcopy(self.contract)
        uncovered["acceptance_criteria"].append("No command covers this criterion")
        cases.append(uncovered)
        scan = copy.deepcopy(self.contract)
        scan["commands"][0]["kind"] = "secret_scan"
        scan["commands"][0]["argv"] = ["gitleaks", "detect"]
        cases.append(scan)
        evidence = copy.deepcopy(self.contract)
        evidence["evidence_dir"] = "docs/evidence"
        cases.append(evidence)
        traversal = copy.deepcopy(self.contract)
        traversal["commands"][0]["argv"] = [sys.executable, "../outside.py"]
        cases.append(traversal)
        scan_equals = copy.deepcopy(self.contract)
        scan_equals["commands"][0]["kind"] = "secret_scan"
        scan_equals["commands"][0]["argv"] = ["gitleaks", "detect", "--source=../outside", "--redact"]
        cases.append(scan_equals)
        scan_report = copy.deepcopy(self.contract)
        scan_report["commands"][0]["kind"] = "secret_scan"
        scan_report["commands"][0]["argv"] = ["gitleaks", "detect", "--source", ".", "--redact", "--report-path", "report.json"]
        cases.append(scan_report)
        for index, contract in enumerate(cases):
            with self.subTest(index=index):
                errors = task_contract.validate_task_contract(contract)
                self.assertTrue(errors)
                result = verification_runner.verify_task(contract, self.root)
                self.assertEqual(result["state"], "BLOCKED")
                self.assertTrue(result["input_error"])

    def test_missing_approval_blocks_before_command_execution(self):
        self.contract["approvals"] = []
        result = verification_runner.verify_task(self.contract, self.root)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertEqual(result["execution_state"], "NOT_EXECUTED")
        self.assertTrue(any("approval" in error for error in result["errors"]))

    def test_invalid_base_commit_is_blocked(self):
        self.contract["scope"]["base_commit"] = "0" * 40
        result = scope_checker.check_scope(self.contract, self.root)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any("base_commit" in error for error in result["errors"]))

    def test_post_verification_scope_violation_blocks_success(self):
        (self.root / "scripts" / "check.py").write_text("from pathlib import Path\nPath('outside.txt').write_text('side effect')\nprint('CHECK-PASS')\n", encoding="utf-8")
        result = verification_runner.verify_task(self.contract, self.root)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertEqual(result["execution_state"], "EXECUTED")
        self.assertEqual(result["commands"][0]["status"], "PASS")
        self.assertEqual(result["post_scope"]["state"], "BLOCKED")
        self.assertTrue((self.root / result["post_scope_path"]).is_file())

    def test_command_path_outside_project_is_blocked(self):
        outside = self.base / "outside.py"
        outside.write_text("print('outside')\n", encoding="utf-8")
        self.contract["commands"][0]["argv"] = [sys.executable, "../outside.py"]
        errors = task_contract.validate_task_contract(self.contract)
        self.assertTrue(any("parent-traversal" in error for error in errors))
        result = verification_runner.verify_task(self.contract, self.root)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertEqual(result["execution_state"], "NOT_EXECUTED")
        self.assertTrue(result["input_error"])

    def test_bare_python_script_path_is_checked_before_start(self):
        self.contract["commands"][0]["argv"] = [sys.executable, "missing.py"]
        result = verification_runner.verify_task(self.contract, self.root)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertEqual(result["execution_state"], "NOT_EXECUTED")
        self.assertEqual(result["commands"][0]["status"], "BLOCKED")
        self.assertTrue(any("does not exist" in event.get("reason", "") for event in result["command_events"]))

    def test_allowlisted_verification_captures_valid_trace_and_hashes(self):
        result = verification_runner.verify_task(self.contract, self.root)
        self.assertEqual(result["state"], "PASS")
        self.assertEqual(result["verification_state"], "VERIFIED")
        self.assertEqual(result["execution_state"], "EXECUTED")
        trace_path = self.root / result["trace_path"]
        trace = json.loads(trace_path.read_text(encoding="utf-8"))
        self.assertEqual(validate_execution.validate_document(trace), [])
        self.assertEqual(trace["status"], "COMPLETED")
        self.assertEqual(trace["resources"]["token_usage"], None)
        log_path = self.root / result["commands"][0]["evidence_path"]
        self.assertIn("CHECK-PASS", log_path.read_text(encoding="utf-8"))
        manifest = json.loads((self.root / result["evidence_manifest_path"]).read_text(encoding="utf-8"))
        self.assertTrue(any(item["path"] == result["trace_path"] for item in manifest["files"]))

    def test_failure_stops_later_commands_and_records_failed_trace(self):
        (self.root / "scripts" / "fail.py").write_text("raise SystemExit(7)\n", encoding="utf-8")
        (self.root / "scripts" / "later.py").write_text("from pathlib import Path\nPath('later-ran.txt').write_text('ran')\n", encoding="utf-8")
        self.contract["commands"][0]["argv"] = [sys.executable, "scripts/fail.py"]
        self.contract["commands"].append({
            "id": "CHECK-002", "kind": "test", "argv": [sys.executable, "scripts/later.py"],
            "criteria": ["The allowlisted check passes."], "timeout_seconds": 10, "max_output_bytes": 1024,
        })
        result = verification_runner.verify_task(self.contract, self.root)
        self.assertEqual(result["state"], "FAIL")
        self.assertEqual(result["commands"][0]["exit_code"], 7)
        self.assertEqual(result["commands"][1]["status"], "BLOCKED")
        self.assertFalse((self.root / "later-ran.txt").exists())
        trace = json.loads((self.root / result["trace_path"]).read_text(encoding="utf-8"))
        self.assertEqual(trace["status"], "FAILED")
        self.assertEqual(validate_execution.validate_document(trace), [])

    def test_scope_violation_prevents_command_side_effect(self):
        (self.root / "outside.txt").write_text("outside\n", encoding="utf-8")
        (self.root / "scripts" / "check.py").write_text("from pathlib import Path\nPath('ran.txt').write_text('ran')\n", encoding="utf-8")
        result = verification_runner.verify_task(self.contract, self.root)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertEqual(result["execution_state"], "NOT_EXECUTED")
        self.assertFalse((self.root / "ran.txt").exists())
        self.assertTrue(all(item["status"] == "BLOCKED" for item in result["commands"]))

    def test_timeout_is_recorded_without_exit_code(self):
        (self.root / "scripts" / "slow.py").write_text("import time\ntime.sleep(5)\n", encoding="utf-8")
        self.contract["commands"][0]["argv"] = [sys.executable, "scripts/slow.py"]
        self.contract["commands"][0]["timeout_seconds"] = 1
        result = verification_runner.verify_task(self.contract, self.root)
        self.assertEqual(result["state"], "FAIL")
        self.assertEqual(result["commands"][0]["status"], "TIMEOUT")
        self.assertIsNone(result["commands"][0]["exit_code"])
        trace = json.loads((self.root / result["trace_path"]).read_text(encoding="utf-8"))
        self.assertEqual(validate_execution.validate_document(trace), [])

    def test_output_cap_terminates_and_redacts_sensitive_values(self):
        secret = "token=abcdefghijklmnopqrstuvwxyz0123456789"
        (self.root / "scripts" / "noisy.py").write_text(f"print({secret!r})\nprint('x' * 1000)\n", encoding="utf-8")
        self.contract["commands"][0]["argv"] = [sys.executable, "scripts/noisy.py"]
        self.contract["commands"][0]["max_output_bytes"] = 100
        result = verification_runner.verify_task(self.contract, self.root)
        self.assertEqual(result["state"], "FAIL")
        self.assertEqual(result["command_events"][0]["termination_reason"], "output_cap")
        log = (self.root / result["commands"][0]["evidence_path"]).read_text(encoding="utf-8")
        self.assertNotIn("abcdefghijklmnopqrstuvwxyz0123456789", log)
        self.assertIn("[REDACTED]", log)
        self.assertIn("OUTPUT TRUNCATED", log)

    def test_scope_and_verification_cli_exit_codes(self):
        self.write_contract()
        stdout = StringIO()
        with redirect_stdout(stdout):
            code = scope_checker.main([str(self.contract_path), "--project", str(self.root)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(stdout.getvalue())["state"], "PASS")
        stdout = StringIO()
        with redirect_stdout(stdout):
            code = verification_runner.main([str(self.contract_path), "--project", str(self.root)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(stdout.getvalue())["state"], "PASS")
        self.contract["commands"][0]["argv"] = ["bash", "-c", "echo unsafe"]
        self.write_contract()
        with redirect_stdout(StringIO()):
            self.assertEqual(verification_runner.main([str(self.contract_path), "--project", str(self.root)]), 2)


if __name__ == "__main__":
    unittest.main()
