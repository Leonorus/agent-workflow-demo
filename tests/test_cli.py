from __future__ import annotations

import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from agent_workflow_demo.cli import main


class CliTests(unittest.TestCase):
    def run_cli(self, args: list[str]) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(args)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_calc_add(self) -> None:
        code, stdout, stderr = self.run_cli(["calc", "add", "2", "3"])
        self.assertEqual(code, 0)
        self.assertEqual(stdout.strip(), "5")
        self.assertEqual(stderr, "")

    def test_calc_div(self) -> None:
        code, stdout, stderr = self.run_cli(["calc", "div", "10", "2"])
        self.assertEqual(code, 0)
        self.assertEqual(stdout.strip(), "5")
        self.assertEqual(stderr, "")

    def test_calc_division_by_zero(self) -> None:
        code, stdout, stderr = self.run_cli(["calc", "div", "10", "0"])
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("division by zero", stderr)


if __name__ == "__main__":
    unittest.main()
