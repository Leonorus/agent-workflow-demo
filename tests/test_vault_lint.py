from __future__ import annotations

import unittest
from pathlib import Path

from agent_workflow_demo.vault import lint_vault

FIXTURES = Path(__file__).parent / "fixtures"


class VaultLintTests(unittest.TestCase):
    def test_clean_vault_has_no_issues(self) -> None:
        issues = lint_vault(FIXTURES / "vault-clean")
        self.assertEqual(issues, [])

    def test_reports_expected_issue_codes(self) -> None:
        issues = lint_vault(FIXTURES / "vault")
        codes = {issue.code for issue in issues}
        self.assertIn("missing-h1", codes)
        self.assertIn("duplicate-title", codes)
        self.assertIn("unresolved-link", codes)
        self.assertIn("absolute-local-path", codes)

    def test_duplicate_title_points_to_second_note(self) -> None:
        issues = lint_vault(FIXTURES / "vault")
        duplicate = [issue for issue in issues if issue.code == "duplicate-title"]
        self.assertEqual(len(duplicate), 1)
        self.assertEqual(duplicate[0].path, "notes/duplicate-title.md")
        self.assertIn("notes/good-note.md", duplicate[0].message)


if __name__ == "__main__":
    unittest.main()
