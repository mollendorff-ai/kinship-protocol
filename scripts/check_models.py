#!/usr/bin/env python3
"""Check every Forge model for drift between stored values and their formulas.

For each models/*.yaml file:
  1. `forge calculate <file> --dry-run` must succeed (schema and formulas valid).
  2. Every stored `value:` of an entry that has a `formula:` must match what
     Forge computes, within TOLERANCE. Hand-typed values rounded to 2 decimals
     pass; a value that no longer follows from its formula fails.
  3. In edge_cases.yaml, tests_passed must equal total_tests.
  4. The headline figures quoted in the README and docs (KEY_FIGURES below) must
     equal what Forge computes, and must still appear in the text that quotes them.
  5. The three game models (stag_hunt, chicken, axelrod_tournament) are checked
     by GAME_MODELS below: what Forge works out for each cost must equal what the
     models stored before Forge could play the games, or the difference listed.
  6. The models in models/analytics/ (Monte Carlo, tornado, real options,
     bootstrap) must run, and the figures the README quotes from them
     (ANALYTICS below) must match Forge's output. Runs are seeded, so the
     numbers are the same every time.

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

# Figures the prose quotes: (model, key, expected value, file, text that must
# appear in that file). If a model changes and a figure moves, this fails until
# the prose is updated, so it cannot drift from the math.
KEY_FIGURES = [
    ("ipd_payoffs.yaml", "threshold_medium_cost", 0.375,
     "docs/COOPERATION_THRESHOLDS.md", "| 0.5 | 0.375 |"),
    ("predator_prey.yaml", "rest_total", 202.5, "README.md", "202.5 vs 90"),
    ("predator_prey.yaml", "max_total", 90.0, "README.md", "202.5 vs 90"),
    ("predator_prey.yaml", "breakeven_discount", 0.4, "README.md", "discount rate of 0.4"),
    ("one_shot.yaml", "ipd_critical_c", 1.5, "README.md", "dissipation cost of 1.5"),
    ("one_shot.yaml", "ipd_critical_c_any_opponent", 2.0, "README.md", "or 2 (against anyone)"),
]

# (command, model, regex on Forge's output, expected value, tolerance,
#  file, text that must appear in that file)
ANALYTICS = [
    ("simulate", "cooperation_monte_carlo.yaml",
     r"P\(assumptions\.margin > 0\) = ([\d.]+)%", 90.28, 0.05,
     "README.md", "in about 90% of the draws"),
    ("tornado", "cooperation_tornado.yaml",
     r"assumptions\.dissipation_cost\s+\|[^|]*\| swing ([\d.]+)", 0.5, 1e-9,
     "README.md", "moves the threshold most (by 0.5)"),
    ("tornado", "cooperation_tornado.yaml",
     r"Tornado Diagram:\s+Base value: [\d.]+\s+assumptions\.(\w+)", "dissipation_cost", None,
     "README.md", "moves the threshold most (by 0.5)"),
    ("real-options", "restraint_option.yaml",
     r"Adds over the traditional NPV: \$([\d.]+)", 27.70, 0.005,
     "README.md", "worth another 27.7"),
    ("bootstrap", "five_ais_bootstrap.yaml",
     r"95% CI: \[([\d.]+), [\d.]+\]", 1.0, 1e-9,
     "README.md", "from 100% to 100%"),
    ("calculate", "five_ais_bootstrap.yaml",
     r"assumptions\.exact_lower_95 = ([\d.]+)", 0.478, 0.0005,
     "README.md", "as low as 48%"),
]


# The game models: Forge works out their equilibria and tournament itself. For
# each, the scenarios (base is c = 0, then c1, c2, c3) and the results the
# models stored when they were typed in by hand: coop_wins per scenario, and the
# crossover cost. DIFFERENT lists what Forge gives that the old file did not:
# the tournament's crossover is 0.108, not 0.1 (typed averages of 2.112 for
# AlwaysCooperate and 2.212 for AlwaysDefect came from a chat model, and had
# GrimTrigger at 5.244 a round, above the temptation of 5).
GAME_SCENARIOS = ["", "c1", "c2", "c3"]
GAME_MODELS = {
    "stag_hunt.yaml": {
        "coop_wins": [0, 0, 0, 1],
        "crossover_c": (1.0, 1e-9),
        "also": {"stag_share": [0.75, 0.625, 0.5, 0.375]},
    },
    "chicken.yaml": {
        "coop_wins": [0, 0, 0, 1],
        "crossover_c": (0.5, 1e-9),
        "also": {"swerve_share": [1 / 3, 5 / 12, 0.5, 2 / 3]},
    },
    "axelrod_tournament.yaml": {
        "coop_wins": [0, 0, 1, 1],
        "crossover_c": (0.108, 0.0005),  # the old file said 0.1
        "also": {"grim_defect_rate": [0.397] * 4},
        "scores": {  # c = 0, exact expected values; the old file typed 2.622...
            "grim": 2.596, "tft": 2.44825, "ad": 2.208, "ac": 2.1, "rand": 1.90875,
        },
    },
}
SCALAR = re.compile(r"^\s*(\S+) = (\S+)\s*$")


def game_values(path, scenario):
    args = [FORGE, "calculate", path, "--dry-run"] + (["--scenario", scenario] if scenario else [])
    run = subprocess.run(args, capture_output=True, text=True)
    if run.returncode != 0:
        tail = (run.stdout + run.stderr).strip().splitlines()[-3:]
        raise RuntimeError(" | ".join(line[:200] for line in tail))
    return {m.group(1): float(m.group(2))
            for m in map(SCALAR.match, run.stdout.splitlines()) if m}


def check_game(path, expected):
    problems = []
    try:
        runs = [game_values(path, s) for s in GAME_SCENARIOS]
    except RuntimeError as err:
        return [f"forge failed: {err}"]
    for i, name in enumerate(["base"] + GAME_SCENARIOS[1:]):
        got = runs[i]
        flag = got.get("kinship.coop_wins")
        if flag != expected["coop_wins"][i]:
            problems.append(f"{name}: coop_wins is {flag}, was stored as {expected['coop_wins'][i]}")
        value, tol = expected["crossover_c"]
        crossover = got.get("kinship.crossover_c")
        if crossover is None or abs(crossover - value) > tol:
            problems.append(f"{name}: crossover_c is {crossover}, expected {value:g}")
        for key, wanted in expected["also"].items():
            seen = got.get("kinship." + key)
            if seen is None or abs(seen - wanted[i]) > 1e-9:
                problems.append(f"{name}: {key} is {seen}, expected {wanted[i]:g}")
    for who, wanted in expected.get("scores", {}).items():
        seen = runs[0].get(f"axelrod.score.{who}")
        if seen is None or abs(seen - wanted) > 1e-9:
            problems.append(f"score {who} is {seen}, expected {wanted:g}")
    # A value stored in the file must still be what Forge computes
    entries = yaml.safe_load(open(path, encoding="utf-8")).get("kinship", {})
    for key, entry in entries.items():
        stored = entry.get("value")
        if stored is not None and abs(float(stored) - runs[0].get("kinship." + key, float("nan"))) > TOLERANCE:
            problems.append(f"kinship.{key}: stored {stored:g}, Forge gives {runs[0].get('kinship.' + key)}")
    return problems


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


def computed_values(path):
    run = subprocess.run([FORGE, "calculate", path, "--dry-run"],
                         capture_output=True, text=True)
    return {m.group(1): float(m.group(2))
            for m in map(LINE.match, run.stdout.splitlines()) if m}


def check_key_figures(models_dir):
    problems = []
    cache = {}
    for model, key, expected, doc, quote in KEY_FIGURES:
        if model not in cache:
            cache[model] = computed_values(os.path.join(models_dir, model))
        got = cache[model].get(key)
        if got is None:
            problems.append(f"{model}: {key} not printed by Forge")
        elif abs(got - expected) > 1e-9:
            problems.append(f"{model}: {key} is {got:g}, README says {expected:g}")
        text = open(os.path.join(models_dir, "..", doc), encoding="utf-8").read()
        if quote not in text:
            problems.append(f"{doc} no longer contains '{quote}' ({model}: {key})")
    return problems


def check_analytics(models_dir):
    problems = []
    for cmd, model, pattern, expected, tol, doc, quote in ANALYTICS:
        path = os.path.join(models_dir, "analytics", model)
        args = [FORGE, cmd, path] + (["--dry-run"] if cmd == "calculate" else [])
        run = subprocess.run(args, capture_output=True, text=True)
        out = run.stdout + run.stderr
        m = re.search(pattern, out)
        if run.returncode != 0 or not m:
            tail = out.strip().splitlines()[-2:]
            problems.append(f"{model}: forge {cmd} gave no match ({' | '.join(tail)})")
        elif tol is None:
            if m.group(1) != expected:
                problems.append(f"{model}: got {m.group(1)}, README says {expected}")
        elif abs(float(m.group(1)) - expected) > tol:
            problems.append(f"{model}: got {m.group(1)}, README says {expected:g}")
        text = open(os.path.join(models_dir, "..", doc), encoding="utf-8").read()
        if quote not in text:
            problems.append(f"{doc} no longer contains '{quote}' ({model})")
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
        problems = check_game(path, GAME_MODELS[name]) if name in GAME_MODELS else check(path)
        if problems:
            failed += 1
            print(f"FAIL {name}")
            for p in problems:
                print(f"     {p}")
        else:
            print(f"ok   {name}")
    print(f"\n{len(files) - failed}/{len(files)} models pass")

    figures = check_key_figures(root)
    if figures:
        print("FAIL key figures")
        for p in figures:
            print(f"     {p}")
    else:
        print(f"ok   key figures ({len(KEY_FIGURES)} checked against Forge)")

    analytics = check_analytics(root)
    if analytics:
        print("FAIL analytics")
        for p in analytics:
            print(f"     {p}")
    else:
        print(f"ok   analytics ({len(ANALYTICS)} figures from Monte Carlo, tornado, "
              "real options and bootstrap)")
    return 1 if failed or figures or analytics else 0


if __name__ == "__main__":
    sys.exit(main())
