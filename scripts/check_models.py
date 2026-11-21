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
  6. The four games added in v0.5.0 (continuation, inspection,
     noisy_tournament, conventions), the five-player public_goods game,
     the one_shot games and the two games of hidden types (hidden_types,
     signalling) are checked by GAME_RESULTS below: what Forge gives in each scenario
     must equal values checked outside Forge (nashpy, Gambit, the axelrod
     library, or by hand), and the docs must still quote them.
  7. `forge goal-seek` must find the flip point of the continuation tournament
     (the w at which AlwaysDefect stops beating GrimTrigger) by playing the
     game, and it must equal the closed form w* = (T-c-R)/(T-P) at three
     costs (check_goal_seek below).
  8. The Bayesian network mistake_or_defection.yaml is run at nine settings
     of the prior and the noise (BAYESIAN below): Forge's chance that the
     partner is a defector, after one, two and three defections, must equal
     Bayes' rule worked out here in exact fractions, and the number of
     defections it takes must be what the docs say.
  9. The models in models/analytics/ (Monte Carlo, tornado, real options,
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
# Key figures may come from an old-format model (assumptions.x) or a game model (kinship.x)
KEY_LINE = re.compile(r"^\s*(?:assumptions|kinship)\.(\S+) = (\S+)\s*$")

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

# The games added in v0.5.0. For each model, per scenario ("" is the base),
# what Forge must give. Equilibria were checked with nashpy, the noisy
# tournament's ranking with the axelrod library (seeded matches), and the
# rest by hand (the formulas are in each model's header). "tornado" is a
# regex on `forge tornado`'s output and the swing it must show. "quotes" is
# text the docs must keep, so the prose cannot drift from the numbers.
GAME_TOL = 1e-6
GAME_RESULTS = {
    "continuation.yaml": {
        "": {"kinship.threshold": 0.5, "kinship.grim_holds": 1, "kinship.agrees": 1,
             "long_run.match.ad.grim": 2.6},
        "short": {"kinship.threshold": 0.5, "kinship.grim_holds": 0, "kinship.agrees": 1,
                  "long_run.match.ad.grim": 3.4},
        "edge": {"kinship.grim_holds": 1, "kinship.agrees": 1, "long_run.match.ad.grim": 3},
        "costly": {"kinship.threshold": 0.375, "kinship.grim_holds": 1, "kinship.agrees": 1,
                   "long_run.match.ad.grim": 2.9},
        "quotes": [("docs/MORE_GAMES.md", "3.4 a round against GrimTrigger's 3"),
                   ("docs/MORE_GAMES.md", "lands on 0.5 at c = 0, 0.375 at c = 0.5 and 0.25 at c = 1")],
    },
    "inspection.yaml": {
        "": {"kinship.pure_equilibria": 0, "kinship.audit_rate": 1 / 3,
             "kinship.cheat_rate": 1 / 3, "kinship.audit_by_hand": 1 / 3,
             "kinship.cheat_by_hand": 1 / 3},
        "harsh": {"kinship.audit_rate": 0.2, "kinship.cheat_rate": 1 / 3},
        "mild": {"kinship.audit_rate": 0.5, "kinship.cheat_rate": 1 / 3},
        "cheap_audits": {"kinship.audit_rate": 1 / 3, "kinship.cheat_rate": 1 / 6},
        "tornado": [(r"inputs\.penalty\s+\|[^|]*\| swing ([\d.]+)", 0.3),
                    (r"inputs\.audit_cost\s+\|[^|]*\| swing ([\d.]+)", 0.0)],
        "quotes": [("README.md", "a harsher penalty makes the human audit less"),
                   ("docs/MORE_GAMES.md", "| 8 | 1 | 0.2 | 1/3 |")],
    },
    "noisy_tournament.yaml": {
        "": {"clean.rank.grim": 1, "clean.rank.tft": 2, "clean.score.grim": 2.711429,
             "noisy.rank.tft": 1, "noisy.rank.tf2t": 2, "noisy.rank.grim": 4,
             "noisy.rank.gtft": 5, "noisy.score.tft": 2.247836,
             "noisy.score.tf2t": 2.247241, "kinship.forgiving_first": 0,
             # Nine strategies (Pavlov and suspicious TitForTat added)
             "clean_wide.rank.tf2t": 1, "clean_wide.rank.tft": 2,
             "kinship.wide_grim_place_clean": 4, "clean_wide.score.tf2t": 2.649583,
             "kinship.grim_vs_suspicious": 1.015,
             "noisy_wide.rank.tf2t": 1, "noisy_wide.rank.wsls": 2,
             "kinship.wide_grim_place_noisy": 7, "noisy_wide.score.tf2t": 2.283023,
             "kinship.wide_forgiving_first": 1},
        "careful": {"noisy.rank.tf2t": 1, "noisy.rank.grim": 4,
                    "noisy.score.tf2t": 2.377545, "kinship.forgiving_first": 1,
                    "noisy_wide.rank.tf2t": 1, "noisy_wide.rank.gtft": 2,
                    "kinship.wide_grim_place_noisy": 7, "kinship.wide_forgiving_first": 1},
        "careless": {"noisy.rank.grim": 1, "noisy.rank.ad": 2,
                     "noisy.score.grim": 2.278385, "kinship.forgiving_first": 0,
                     "noisy_wide.rank.grim": 1, "noisy_wide.rank.ad": 2,
                     "kinship.wide_forgiving_first": 0},
        "quotes": [("docs/MORE_GAMES.md", "| 5% | TitForTat 2.248, TitForTwoTats 2.247 |"),
                   ("docs/MORE_GAMES.md", "GrimTrigger is 4th even without mistakes"),
                   ("blog/content/posts/08-does-forgiveness-pay.md", "GrimTrigger is 4th even without mistakes")],
    },
    "conventions.yaml": {
        "": {"kinship.pure_equilibria": 2, "kinship.insist_rate": 0.6,
             "kinship.insist_by_hand": 0.6, "kinship.miss_rate": 0.52,
             "kinship.mixed_payoff": 1.2},
        "costly": {"kinship.insist_rate": 4 / 7, "kinship.miss_rate": 25 / 49,
                   "kinship.mixed_payoff": 5 / 7},
        "very_costly": {"kinship.insist_rate": 8 / 15, "kinship.miss_rate": 113 / 225,
                        "kinship.mixed_payoff": -19 / 15},
        "quotes": [("docs/MORE_GAMES.md", "they miss each other 52% of the time")],
    },
    # One-shot games. The scenario flags were checked against exact fractions
    # computed without Forge (the average payoff against a 50/50 opponent, and
    # strict dominance in the dilemma). The critical costs are the figures the
    # old hand-typed model stored: 1.5, 1.0, 0.5, and 2 against any opponent.
    "one_shot.yaml": {
        "": {"kinship.ipd_critical_c": 1.5, "kinship.sh_critical_c": 1.0,
             "kinship.ch_critical_c": 0.5, "kinship.ipd_critical_c_any_opponent": 2.0,
             "kinship.viable_without_future": 1, "kinship.catastrophic_games_easier": 1,
             "kinship.anon_defect_ev": 40, "kinship.anon_coop_wins": 1,
             "kinship.nuke_defect_ev": -450, "kinship.nuke_coop_wins": 1,
             "kinship.ipd_coop_wins": 0, "kinship.sh_coop_wins": 0, "kinship.ch_coop_wins": 0},
        "c025": {"kinship.ipd_coop_wins": 0, "kinship.sh_coop_wins": 0, "kinship.ch_coop_wins": 0},
        "c050": {"kinship.ipd_coop_wins": 0, "kinship.sh_coop_wins": 0, "kinship.ch_coop_wins": 0},
        "c075": {"kinship.ipd_coop_wins": 0, "kinship.sh_coop_wins": 0, "kinship.ch_coop_wins": 1},
        "c100": {"kinship.ipd_coop_wins": 0, "kinship.sh_coop_wins": 0, "kinship.ch_coop_wins": 1},
        "c150": {"kinship.ipd_coop_wins": 0, "kinship.sh_coop_wins": 1, "kinship.ch_coop_wins": 1},
        "c200": {"kinship.ipd_coop_wins": 1, "kinship.sh_coop_wins": 1, "kinship.ch_coop_wins": 1,
                 "kinship.ipd_defect_dominated": 0},
        "c250": {"kinship.ipd_defect_dominated": 1, "kinship.ipd_critical_c": 1.5},
        "quotes": [("docs/ONE_SHOT_GAMES.md", "`kinship.ipd_critical_c`: 1.5")],
    },
    # Five players; checked with Gambit (pygambit 16.7, enumpure_solve) and by
    # enumerating the 32 profiles by hand. All five play alike in every
    # equilibrium, so Claude's give rate stands for all of them.
    "public_goods.yaml": {
        "": {"kinship.pure_equilibria": 1, "kinship.give_rate": 0,
             "kinship.equilibrium_payoff": 1, "kinship.give_dominated": 1,
             "kinship.threshold_by_hand": 0.6, "kinship.all_give_payoff": 2},
        "cheap": {"kinship.pure_equilibria": 1, "kinship.give_rate": 0,
                  "kinship.equilibrium_payoff": 0.5, "kinship.give_dominated": 1},
        "edge": {"kinship.pure_equilibria": 32, "kinship.give_dominated": 0,
                 "kinship.keep_dominated": 0},
        "costly": {"kinship.pure_equilibria": 1, "kinship.give_rate": 1,
                   "kinship.equilibrium_payoff": 2, "kinship.keep_dominated": 1},
        "rich": {"kinship.pure_equilibria": 1, "kinship.give_rate": 1,
                 "kinship.equilibrium_payoff": 6, "kinship.keep_dominated": 1},
        "quotes": [("docs/MORE_GAMES.md", "giving dominates once `c > 1 - r/5`"),
                   ("README.md", "all five keep below a cost of conflict of 0.6")],
    },
    # Hidden types (v0.6.3); checked with Gambit (pygambit 16.7,
    # enummixed_solve) and nashpy 0.0.43 (vertex enumeration), from payoffs
    # built outside the model: one equilibrium in each scenario.
    "hidden_types.yaml": {
        "": {"kinship.exploit_rate": 0.5, "kinship.verify_rate": 0.5,
             "kinship.exploited": 0.25, "kinship.human_payoff": 0.5,
             "kinship.p_star": 0.75, "kinship.exploited_by_hand": 0.25,
             "kinship.verify_by_hand": 0.5, "kinship.c_star": 2,
             "oversight.pure_equilibria": 0},
        "rare": {"kinship.exploit_rate": 1 / 3, "kinship.verify_rate": 0.5,
                 "kinship.exploited": 0.25, "kinship.human_payoff": 0.5},
        "common": {"kinship.exploit_rate": 1, "kinship.verify_rate": 0,
                   "kinship.exploited": 0.2, "kinship.exploited_by_hand": 0.2,
                   "kinship.human_payoff": 0.8, "oversight.pure_equilibria": 1},
        "cost1": {"kinship.exploit_rate": 0.5, "kinship.verify_rate": 0.25,
                  "kinship.verify_by_hand": 0.25, "kinship.exploited": 0.25,
                  "kinship.human_payoff": 0.5},
        "costly": {"kinship.exploit_rate": 0, "kinship.verify_rate": 0,
                   "kinship.exploited": 0, "kinship.human_payoff": 2,
                   "oversight.dominated.ai.exploit": 1},
        "quotes": [("README.md", "exploited in a quarter of meetings whatever the prior"),
                   ("docs/MORE_GAMES.md", "| rare | 0.25 | 0 | 1/3 | 0.5 | 0.25 | 0.5 |")],
    },
    # A signalling game (v0.6.3); the same check. Gambit and nashpy also
    # find the far end of a line of equilibria where nobody signals, which
    # Forge leaves out, as it warns for a degenerate game.
    "signalling.yaml": {
        "": {"signal.equilibria": 2, "kinship.pure_equilibria": 2,
             "kinship.separating": 1, "kinship.separates_by_hand": 1,
             "signal.equilibrium_1.human.after_signal": 1,
             "signal.equilibrium_2.ai.neither": 1, "kinship.trust_blind": -1,
             "signal.degenerate": 1},
        "same_cost": {"signal.equilibria": 1, "kinship.separating": 0,
                      "kinship.separates_by_hand": 0, "signal.equilibrium_1.ai.neither": 1,
                      "signal.equilibrium_1.human.never": 1},
        "dear": {"signal.equilibria": 1, "kinship.separating": 0,
                 "kinship.separates_by_hand": 0, "signal.equilibrium_1.ai.neither": 1},
        "cheap": {"signal.equilibria": 2, "kinship.pure_equilibria": 1,
                  "kinship.separates_by_hand": 0,
                  "signal.equilibrium_2.ai.both": 0.5, "signal.equilibrium_2.ai.aligned_only": 0.5,
                  "kinship.misaligned_signal_by_hand": 0.5,
                  "signal.equilibrium_2.human.after_signal": 2 / 3,
                  "kinship.trust_after_signal_by_hand": 2 / 3},
        "conflict": {"signal.equilibria": 2, "kinship.separating": 1,
                     "kinship.separates_by_hand": 1},
        "quotes": [("README.md", "one that costs both the same is bought first by the misaligned AI"),
                   ("docs/MORE_GAMES.md", "| cheap | 0.5 | 2 | 0 | half-sorting: the misaligned AI signals half the time, the human trusts a signal 2/3 of the time |")],
    },
}


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


def check_game_results(path, expected):
    problems = []
    for scenario, wanted in expected.items():
        if scenario in ("tornado", "quotes"):
            continue
        try:
            got = game_values(path, scenario)
        except RuntimeError as err:
            return [f"forge failed: {err}"]
        for key, value in wanted.items():
            seen = got.get(key)
            if seen is None or abs(seen - value) > GAME_TOL:
                problems.append(f"{scenario or 'base'}: {key} is {seen}, expected {value:g}")
    if "tornado" in expected:
        run = subprocess.run([FORGE, "tornado", path], capture_output=True, text=True)
        for pattern, value in expected["tornado"]:
            m = re.search(pattern, run.stdout)
            if run.returncode != 0 or not m:
                problems.append(f"tornado: no match for {pattern}")
            elif abs(float(m.group(1)) - value) > 0.005:
                problems.append(f"tornado: swing {m.group(1)}, expected {value:g}")
    for doc, quote in expected.get("quotes", []):
        doc_path = os.path.join(os.path.dirname(path), "..", doc)
        if not os.path.exists(doc_path):
            problems.append(f"{doc} is missing")
        elif quote not in open(doc_path, encoding="utf-8").read():
            problems.append(f"{doc} no longer contains '{quote}'")
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
            for m in map(KEY_LINE.match, run.stdout.splitlines()) if m}


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


# Mistake or defection? (prior share of defectors, noise, defections it takes
# before "defector" is more likely than not). A tie at exactly 50% does not count.
BAYESIAN = [
    ("1/100", "1/100", 2), ("1/100", "5/100", 2), ("1/100", "10/100", 3),
    ("1/10", "1/100", 1), ("1/10", "5/100", 1), ("1/10", "10/100", 2),
    ("3/10", "1/100", 1), ("3/10", "5/100", 1), ("3/10", "10/100", 1),
]
BAYESIAN_QUOTES = [
    ("docs/MORE_GAMES.md", "| 1 in 100 | 5% | 16.1% | 78.5% | 98.6% | 2 |"),
    ("docs/MORE_GAMES.md", "| 1 in 10 | 5% | 67.9% | 97.6% | 99.9% | 1 |"),
    ("README.md", "one defection is more likely a slip"),
]


def bayes_posterior(path, evidence):
    """Forge's chance that the partner is a defector, given the moves seen."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "out.yaml")
        args = [FORGE, "bayesian", path, "-q", "partner", "-o", out]
        for i, move in enumerate(evidence, 1):
            args += ["-e", f"move_{i}={move}"]
        run = subprocess.run(args, capture_output=True, text=True)
        if run.returncode != 0 or not os.path.exists(out):
            raise RuntimeError((run.stdout + run.stderr).strip()[-200:])
        result = yaml.safe_load(open(out, encoding="utf-8"))
    return float(result["probabilities"][result["states"].index("defector")])


def check_bayesian(path):
    import tempfile
    from fractions import Fraction
    problems = []
    try:
        # The file as it stands: 1 in 10 defectors, 5% noise
        for evidence, wanted in [(["defect"], 0.095 / 0.14),
                                 (["defect", "defect"], 0.09025 / 0.0925),
                                 (["defect", "cooperate"], 0.1)]:
            got = bayes_posterior(path, evidence)
            if abs(got - wanted) > 1e-9:
                problems.append(f"{'-'.join(evidence)}: Forge gives {got:.6f}, Bayes' rule {wanted:.6f}")
        model = yaml.safe_load(open(path, encoding="utf-8"))
        nodes = model["bayesian_network"]["nodes"]
        for prior, noise, needed in BAYESIAN:
            p, e = Fraction(prior), Fraction(noise)
            nodes["partner"]["prior"] = [float(1 - p), float(p)]
            for k in (1, 2, 3):
                nodes[f"move_{k}"]["cpt"] = {"cooperator": [float(1 - e), float(e)],
                                             "defector": [float(e), float(1 - e)]}
            with tempfile.TemporaryDirectory() as tmp:
                variant = os.path.join(tmp, "variant.yaml")
                yaml.safe_dump(model, open(variant, "w", encoding="utf-8"), sort_keys=False)
                first = None
                for k in (1, 2, 3):
                    exact = p * (1 - e) ** k / (p * (1 - e) ** k + (1 - p) * e ** k)
                    got = bayes_posterior(variant, ["defect"] * k)
                    if abs(got - float(exact)) > 1e-9:
                        problems.append(f"prior {prior}, noise {noise}, {k} defections: "
                                        f"Forge {got:.6f}, Bayes' rule {float(exact):.6f}")
                    if first is None and exact > Fraction(1, 2):
                        first = k
                if first != needed:
                    problems.append(f"prior {prior}, noise {noise}: takes {first} defections, "
                                    f"the docs say {needed}")
    except RuntimeError as err:
        return [f"forge failed: {err}"]
    for doc, quote in BAYESIAN_QUOTES:
        if quote not in open(os.path.join(os.path.dirname(path), "..", doc), encoding="utf-8").read():
            problems.append(f"{doc} no longer contains '{quote}'")
    return problems


# The flip point found by playing the tournament must be the formula's w*:
# (cost of conflict, w* by hand). Goal-seek prints w to two or three decimals.
GOAL_SEEK = [(0, 0.5), (0.5, 0.375), (1, 0.25)]


def check_goal_seek(models_dir):
    import tempfile
    problems = []
    source = open(os.path.join(models_dir, "continuation.yaml"), encoding="utf-8").read()
    for cost, expected in GOAL_SEEK:
        text, n = re.subn(r"(?m)^c: 0\b.*$", f"c: {cost}", source)
        if n != 1:
            return ["continuation.yaml: cannot find the line 'c: 0' to set the cost"]
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "continuation.yaml")
            open(path, "w", encoding="utf-8").write(text)
            run = subprocess.run([FORGE, "goal-seek", path, "--target", "defector_edge",
                                  "--value", "0", "--vary", "w", "--min", "0.01",
                                  "--max", "0.99", "--tolerance", "1e-9"],
                                 capture_output=True, text=True)
        m = re.search(r"^\s*w = ([\d.]+) ", run.stdout, re.M)
        if run.returncode != 0 or not m:
            problems.append(f"c = {cost}: goal-seek found no w ({run.stdout.strip()[-80:]})")
        elif abs(float(m.group(1)) - expected) > 0.0006:
            problems.append(f"c = {cost}: goal-seek gives w = {m.group(1)}, the formula gives {expected}")
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
        if name in GAME_MODELS:
            problems = check_game(path, GAME_MODELS[name])
        elif name in GAME_RESULTS:
            problems = check_game_results(path, GAME_RESULTS[name])
        elif name == "mistake_or_defection.yaml":
            problems = check_bayesian(path)
        else:
            problems = check(path)
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
    seek = check_goal_seek(root)
    if seek:
        print("FAIL goal-seek")
        for p in seek:
            print(f"     {p}")
    else:
        print(f"ok   goal-seek ({len(GOAL_SEEK)} flip points found by playing the tournament "
              "equal the formula's w*)")
    return 1 if failed or figures or analytics or seek else 0


if __name__ == "__main__":
    sys.exit(main())
