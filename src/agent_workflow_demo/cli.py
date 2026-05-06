"""Command line interface for the demo package."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .calculator import add, divide, format_number
from .vault import build_index, issues_to_json, lint_vault, load_index, write_index


def _float(value: str) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"not a number: {value}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-demo")
    subparsers = parser.add_subparsers(dest="command", required=True)

    calc = subparsers.add_parser("calc", help="small calculator used by debug demo")
    calc_sub = calc.add_subparsers(dest="calc_command", required=True)
    calc_add = calc_sub.add_parser("add", help="add two numbers")
    calc_add.add_argument("left", type=_float)
    calc_add.add_argument("right", type=_float)
    calc_add.set_defaults(func=_cmd_calc_add)

    calc_div = calc_sub.add_parser("div", help="divide two numbers")
    calc_div.add_argument("left", type=_float)
    calc_div.add_argument("right", type=_float)
    calc_div.set_defaults(func=_cmd_calc_div)

    vault = subparsers.add_parser("vault", help="markdown vault ingest/lint demo")
    vault_sub = vault.add_subparsers(dest="vault_command", required=True)

    ingest = vault_sub.add_parser("ingest", help="build a deterministic JSON index")
    ingest.add_argument("root", type=Path)
    ingest.add_argument("--out", type=Path, help="write JSON index to this path")
    ingest.set_defaults(func=_cmd_vault_ingest)

    lint = vault_sub.add_parser("lint", help="lint a markdown vault")
    lint.add_argument("root", type=Path)
    lint.add_argument("--json", action="store_true", help="print machine-readable JSON")
    lint.set_defaults(func=_cmd_vault_lint)

    show = vault_sub.add_parser("show-index", help="print titles from an index JSON")
    show.add_argument("index", type=Path)
    show.set_defaults(func=_cmd_vault_show_index)

    return parser


def _cmd_calc_add(args: argparse.Namespace) -> int:
    print(format_number(add(args.left, args.right)))
    return 0


def _cmd_calc_div(args: argparse.Namespace) -> int:
    try:
        print(format_number(divide(args.left, args.right)))
        return 0
    except ZeroDivisionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


def _cmd_vault_ingest(args: argparse.Namespace) -> int:
    index = build_index(args.root)
    if args.out:
        write_index(index, args.out)
        print(f"indexed {len(index.docs)} markdown files")
        print(f"wrote {args.out.as_posix()}")
    else:
        import json

        print(json.dumps(index.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def _cmd_vault_lint(args: argparse.Namespace) -> int:
    issues = lint_vault(args.root)
    if args.json:
        print(issues_to_json(issues))
    elif not issues:
        print("OK: no vault lint issues")
    else:
        for issue in issues:
            print(issue.to_line())
    return 1 if any(issue.severity == "error" for issue in issues) else 0


def _cmd_vault_show_index(args: argparse.Namespace) -> int:
    index = load_index(args.index)
    docs = index.get("docs", [])
    for doc in docs:
        print(f"{doc['path']}: {doc['title']}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
