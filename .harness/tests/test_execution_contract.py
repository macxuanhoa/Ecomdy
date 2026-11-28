import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_execution


class ExecutionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trace = validate_execution.load(validate_execution.TRACE_EXAMPLE)
        cls.checkpoint = validate_execution.load(validate_execution.CHECKPOINT_EXAMPLE)

    def test_example_documents_are_valid_but_not_run_evidence(self):
        self.assertEqual(validate_execution.validate_document(self.trace), [])
        self.assertEqual(validate_execution.validate_document(self.checkpoint), [])
        self.assertTrue(any("not evidence" in item for item in self.trace["limitations"]))

    def test_selected_step_cannot_claim_attempt(self):
        changed = copy.deepcopy(self.trace)
        changed["steps"][0]["timestamps"]["attempted_at"] = "2026-11-28T00:01:00Z"
        errors = validate_execution.validate_document(changed)
        self.assertTrue(any("SELECTED cannot have attempted_at" in error for error in errors))

    def test_attempted_step_cannot_claim_execution(self):
        changed = copy.deepcopy(self.trace)
        changed["steps"][1]["timestamps"]["executed_at"] = "2026-11-28T00:02:00Z"
        errors = validate_execution.validate_document(changed)
        self.assertTrue(any("ATTEMPTED cannot have executed_at" in error for error in errors))

    def test_executed_step_cannot_claim_verification(self):
        changed = copy.deepcopy(self.trace)
        changed["steps"][2]["timestamps"]["verified_at"] = "2026-11-28T00:03:00Z"
        errors = validate_execution.validate_document(changed)
        self.assertTrue(any("EXECUTED cannot have verified_at" in error for error in errors))

    def test_verified_step_requires_evidence(self):
        changed = copy.deepcopy(self.trace)
        changed["steps"][3]["outputs"] = []
        errors = validate_execution.validate_document(changed)
        self.assertTrue(any("VERIFIED requires output or PASS command evidence" in error for error in errors))

    def test_completed_trace_requires_verified_steps_and_pass_results(self):
        changed = copy.deepcopy(self.trace)
        changed["status"] = "COMPLETED"
        changed["steps"][0]["status"] = "FAILED"
        errors = validate_execution.validate_document(changed)
        self.assertTrue(any("COMPLETED requires every step VERIFIED or SKIPPED" in error for error in errors))

    def test_unknown_measurements_cannot_contain_token_or_cost_values(self):
        changed = copy.deepcopy(self.trace)
        changed["resources"]["token_usage"] = {"input": 100, "output": 20, "total": 120}
        errors = validate_execution.validate_document(changed)
        self.assertTrue(any("unknown measurement cannot contain" in error for error in errors))

    def test_command_status_must_match_exit_code(self):
        changed = copy.deepcopy(self.trace)
        changed["steps"][2]["commands"][0]["exit_code"] = 1
        errors = validate_execution.validate_document(changed)
        self.assertTrue(any("PASS requires exit_code 0" in error for error in errors))

    def test_shell_wrapped_command_is_rejected(self):
        changed = copy.deepcopy(self.trace)
        changed["steps"][2]["commands"][0]["argv"] = ["bash", "-c", "python .harness/scripts/validate.py"]
        errors = validate_execution.validate_document(changed)
        self.assertTrue(any("must not wrap commands in a shell" in error for error in errors))

    def test_malformed_command_argv_fails_without_exception(self):
        changed = copy.deepcopy(self.trace)
        changed["steps"][2]["commands"][0]["argv"] = {"bad": "shape"}
        errors = validate_execution.validate_document(changed)
        self.assertTrue(any("must be a non-empty array of non-empty strings" in error for error in errors))

    def test_budget_enforcement_remains_advisory(self):
        changed = copy.deepcopy(self.trace)
        changed["budgets"]["enforcement"] = "runtime"
        errors = validate_execution.validate_document(changed)
        self.assertTrue(any("budgets.enforcement must remain advisory" in error for error in errors))

    def test_output_truncation_must_be_explicit(self):
        changed = copy.deepcopy(self.trace)
        changed["steps"][2]["commands"][0]["output_truncated"] = "false"
        errors = validate_execution.validate_document(changed)
        self.assertTrue(any("output_truncated must be a boolean" in error for error in errors))

    def test_step_sequences_must_be_contiguous(self):
        changed = copy.deepcopy(self.trace)
        changed["steps"][1]["sequence"] = 4
        errors = validate_execution.validate_document(changed)
        self.assertTrue(any("sequences must be contiguous from 1" in error for error in errors))

    def test_blocked_checkpoint_requires_blocker(self):
        changed = copy.deepcopy(self.checkpoint)
        changed["blockers"] = []
        errors = validate_execution.validate_document(changed)
        self.assertTrue(any("BLOCKED requires at least one blocker" in error for error in errors))

    def test_ready_checkpoint_requires_pending_steps_and_resume_conditions(self):
        changed = copy.deepcopy(self.checkpoint)
        changed["status"] = "READY_TO_RESUME"
        changed["blockers"] = []
        changed["pending_step_ids"] = []
        errors = validate_execution.validate_document(changed)
        self.assertTrue(any("READY_TO_RESUME requires" in error for error in errors))

    def test_complete_checkpoint_cannot_have_pending_steps(self):
        changed = copy.deepcopy(self.checkpoint)
        changed["status"] = "COMPLETE"
        errors = validate_execution.validate_document(changed)
        self.assertTrue(any("COMPLETE cannot contain pending steps or blockers" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
