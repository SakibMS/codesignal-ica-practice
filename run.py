#!/usr/bin/env python3
"""
Runs a practice module's tests, like CodeSignal's "Run" button.

    python3 run.py 1                # module 1, all levels
    python3 run.py 1 --level 2      # module 1, levels 1-2 only
    python3 run.py 1 --solution     # run the reference solution instead of your code
    python3 run.py all --solution   # score summary for every module

A module can be given as 1, 01, or 01_inventory.
"""
import argparse
import importlib.util
import io
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEVELS = 4
MODULES = sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name[:2].isdigit())


def resolve(name):
    for path in MODULES:
        if name in (path.name, path.name[:2], path.name[:2].lstrip("0")):
            return path
    choices = ", ".join(p.name for p in MODULES)
    sys.exit(f"Unknown module {name!r}. Choose one of: {choices}, or 'all'.")


class Result(unittest.TextTestResult):
    """Remembers which tests passed so each level can be scored."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passed = set()

    def addSuccess(self, test):
        super().addSuccess(test)
        self.passed.add(test.id())


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def run_module(module_dir, max_level, use_solution, quiet):
    stub = module_dir / (module_dir.name[3:] + ".py")  # 01_inventory -> inventory.py
    sys.path.insert(0, str(ROOT / "support"))  # local timeout_decorator

    if use_solution:
        spec = importlib.util.spec_from_file_location(
            stub.stem, ROOT / "solutions" / stub.name
        )
        solution = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(solution)
        sys.modules[stub.stem] = solution  # the tests now import the solution

    tests_dir = module_dir / "tests"
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    groups = {}
    files = [("Playground", "basicTests.py")] + [
        (f"Level {n}", f"level{n}Tests.py") for n in range(1, max_level + 1)
    ]
    for label, pattern in files:
        found = loader.discover(str(tests_dir), pattern=pattern, top_level_dir=str(tests_dir))
        suite.addTests(found)
        ids = [test.id() for test in flatten(found)]
        broken = any(i.startswith("unittest.loader") for i in ids)
        if broken:  # the test file couldn't import your code; count its tests as failed
            source = (tests_dir / pattern).read_text(encoding="utf-8")
            ids = ["?"] * len(re.findall(r"^\s*def test_", source, re.M))
        groups[label] = (ids, broken)

    stream = io.StringIO() if quiet else sys.stdout
    runner = unittest.TextTestRunner(
        stream=stream, resultclass=Result, verbosity=1 if quiet else 2
    )
    result = runner.run(suite)

    title = module_dir.name + (" (reference solution)" if use_solution else "")
    print(f"\n=== {title} ===")
    passed = total = 0
    for label, (ids, broken) in groups.items():
        ok = sum(i in result.passed for i in ids)
        if broken:
            note = "(couldn't import your code: check it for errors)"
        elif label == "Playground":
            note = "(not scored)"
        else:
            note = "✓" if ok == len(ids) else ""
        if label != "Playground":
            passed += ok
            total += len(ids)
        print(f"{label}: {ok}/{len(ids)} passed {note}".rstrip())
    print(f"Score: {passed}/{total}")
    return result.wasSuccessful()


def main():
    parser = argparse.ArgumentParser(description="Run CodeSignal-style practice tests.")
    parser.add_argument("module", help="module number or folder name, or 'all'")
    parser.add_argument(
        "--level", type=int, default=LEVELS, choices=range(1, LEVELS + 1),
        help="run levels 1..LEVEL only (default: all levels)",
    )
    parser.add_argument("--solution", action="store_true",
                        help="run the tests against the reference solution")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="only print the score summary")
    args = parser.parse_args()

    if args.module == "all":
        ok = True
        for path in MODULES:
            cmd = [sys.executable, str(Path(__file__).resolve()), path.name,
                   "--level", str(args.level), "--quiet"]
            if args.solution:
                cmd.append("--solution")
            ok = subprocess.run(cmd).returncode == 0 and ok
        sys.exit(0 if ok else 1)

    success = run_module(resolve(args.module), args.level, args.solution, args.quiet)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
