#!/usr/bin/env python3
"""Check every Forge model for drift between stored values and their formulas.

For each models/*.yaml file:
  1. `forge calculate <file> --dry-run` must succeed (schema and formulas valid).
  2. Every stored `value:` of an entry that has a `formula:` must match what
     Forge computes, within TOLERANCE. Hand-typed values rounded to 2 decimals
     pass; a value that no longer follows from its formula fails.
  3. In edge_cases.yaml, tests_passed must equal total_tests.

Usage: python3 scripts/check_models.py            (uses `forge` on PATH)
       FORGE=/path/to/forge python3 scripts/check_models.py
Exit code 0 when everything passes, 1 otherwise.
"""
import glob
import os
import re
import subprocess
import sys

import yaml

TOLERANCE = 0.006  # allows values typed to 2 decimals (max rounding error 0.005)
FORGE = os.environ.get("FORGE", "forge")
LINE = re.compile(r"^\s*assumptions\.(\S+) = (\S+)\s*$")


def check(path):
    problems = []
    run = subprocess.run([FORGE, "calculate", path, "--dry-run"],
                         capture_output=True, text=True)
    if run.returncode != 0:
        tail = (run.stdout + run.stderr).strip().splitlines()[-3:]
        return [f"forge failed: {' | '.join(line[:200] for line in tail)}"]

    computed = {}
    for line in run.stdout.splitlines():
        m = LINE.match(line)
        if m:
            computed[m.group(1)] = float(m.group(2))

    entries = yaml.safe_load(open(path, encoding="utf-8"))["assumptions"]
    for key, entry in entries.items():
        if "formula" not in entry:
            continue
        stored = entry.get("value")
        if key not in computed:
            problems.append(f"{key}: Forge printed no value")
        elif stored is None:
            problems.append(f"{key}: no stored value (Forge gives {computed[key]:g})")
        elif abs(float(stored) - computed[key]) > TOLERANCE:
            problems.append(f"{key}: stored {stored:g}, formula gives {computed[key]:g}")

    if os.path.basename(path) == "edge_cases.yaml":
        passed, total = computed.get("tests_passed"), computed.get("total_tests")
        if passed is None or total is None or passed != total:
            problems.append(f"edge cases: tests_passed = {passed}, total_tests = {total}")
    return problems


def main():
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models")
    files = sorted(glob.glob(os.path.join(root, "*.yaml")))
    if not files:
        print("no models found")
        return 1
    failed = 0
    for path in files:
        name = os.path.basename(path)
        problems = check(path)
        if problems:
            failed += 1
            print(f"FAIL {name}")
            for p in problems:
                print(f"     {p}")
        else:
            print(f"ok   {name}")
    print(f"\n{len(files) - failed}/{len(files)} models pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
