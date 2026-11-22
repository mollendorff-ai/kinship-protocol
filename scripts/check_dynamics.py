#!/usr/bin/env python3
"""Check the two models of strategies that spread outside Forge.

models/spread.yaml (GrimTrigger and AlwaysDefect) and models/ecology.yaml
(nine strategies with mistakes) let Forge follow a population by the
discrete replicator equation, x'_i = x_i f_i / f_bar. This script works the
same numbers out without Forge's arithmetic:

  1. spread.yaml: each match payoff and the barrier x* in exact fractions
     from T, R, P, S, w and c, and every generation's shares against the
     replicator equation at 60 digits (mpmath) and against egttools' own
     replicator gradient (x_i (f_i - f_bar), divided by f_bar for one
     discrete step).
  2. ecology.yaml: every share of every generation, in each scenario,
     against the replicator equation at 60 digits, from the match scores
     Forge reports (those were checked against the axelrod library in
     v0.6.0).
  3. With --axelrod: the axelrod library plays its own noisy tournament
     (seeded, sampled matches) and runs its own Ecosystem; the strategy with
     the largest share after 500 generations must be Forge's.

It needs packages that CI does not install:
    python3 -m venv venv && venv/bin/pip install mpmath numpy egttools==0.2.1 axelrod==4.14.0 pyyaml
    venv/bin/python scripts/check_dynamics.py [--axelrod]     (forge on PATH, or FORGE=...)
Exit code 0 when everything agrees, 1 otherwise.
"""
import json
import os
import subprocess
import sys
import tempfile
from fractions import Fraction as F

import numpy as np
import yaml
from mpmath import mp, mpf

mp.dps = 60
FORGE = os.environ.get("FORGE", "forge")
SHARE_TOL = 1e-9
NINE = ["grim", "tft", "ad", "ac", "rand", "gtft", "tf2t", "wsls", "stft"]
failures = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


def forge_json(model, scenario):
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "out.json")
        cmd = [FORGE, "game", model, "-o", out] + (["--scenario", scenario] if scenario else [])
        subprocess.run(cmd, check=True, capture_output=True)
        with open(out, encoding="utf-8") as fh:
            return {g["game"]: g for g in json.load(fh)}


def scalars(model, scenario):
    with open(model, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    values = {k: v for k, v in doc.items() if isinstance(v, (int, float))}
    values.update(doc.get("dilemma_payoffs", {}))
    if scenario:
        values.update(doc["scenarios"][scenario]["scalars"])
    return {k: F(str(v)) for k, v in values.items()}


def exact(v):
    return mpf(v.numerator) / v.denominator if isinstance(v, F) else mpf(v)


def replicate(matrix, start, generations):
    """Every generation of x'_i = x_i f_i / f_bar, at 60 digits."""
    n = len(start)
    a = [[exact(v) for v in row] for row in matrix]
    x = [exact(v) for v in start]
    path = [x]
    for _ in range(generations):
        f = [sum(a[i][j] * x[j] for j in range(n)) for i in range(n)]
        f_bar = sum(x[i] * f[i] for i in range(n))
        x = [x[i] * f[i] / f_bar for i in range(n)]
        path.append(x)
    return path


def worst_gap(forge_path, path, names):
    return max(abs(float(path[g][i]) - forge_path[g]["shares"][s])
               for g in range(len(path)) for i, s in enumerate(names))


def check_spread():
    model = "models/spread.yaml"
    for scenario in ["", "many", "costly", "ruinous", "short", "long"]:
        v = scalars(model, scenario)
        T, R, P, S, w, c = (v[k] for k in ("T", "R", "P", "S", "w", "c"))
        gg, dd = R, P - c
        gd = (1 - w) * S + w * (P - c)
        dg = (1 - w) * (T - c) + w * (P - c)
        matrix = [[gg, gd], [dg, dd]]
        games = forge_json(model, scenario)
        name = scenario or "base"
        m = games["matches"]["matches"]
        check(all(abs(float(matrix[i][j]) - m[a][b]) < SHARE_TOL
                  for i, a in enumerate(["grim", "ad"]) for j, b in enumerate(["grim", "ad"])),
              f"spread {name}: the four match payoffs are the formulas")
        if gg > dg:
            barrier = (dd - gd) / ((gg - dg) + (dd - gd))
            found = [e for e in games["population"]["equilibria"] if e["kind"] == "mixed"]
            if barrier > 0:
                share = found[0]["players"]["me"]["strategies"]["grim"] if found else None
                check(share is not None and abs(share - float(barrier)) < SHARE_TOL,
                      f"spread {name}: x* = {barrier} (Forge {share})")
            else:
                check(not found, f"spread {name}: x* = 0, no mixed equilibrium")
        else:
            barrier = F(1)
            check(len(games["population"]["equilibria"]) == 1,
                  f"spread {name}: below w*, one equilibrium (everyone defects)")
        dyn = games["population"]["dynamics"]
        last = dyn["path"][-1]["shares"]
        start = [v["start"], 1 - v["start"]]
        path = replicate(matrix, start, len(dyn["path"]) - 1)
        check(worst_gap(dyn["path"], path, ["grim", "ad"]) < SHARE_TOL,
              f"spread {name}: every generation equals the replicator equation at 60 digits")
        # egttools: one discrete step is x + gradient / f_bar
        from egttools.analytical import replicator_equation
        x = np.array([float(s) for s in start])
        a = np.array([[float(e) for e in row] for row in matrix])
        for _ in range(len(dyn["path"]) - 1):
            f_bar = float(x @ a @ x)
            x = x + replicator_equation(x, a) / f_bar
        check(abs(x[0] - last["grim"]) < 1e-9,
              f"spread {name}: the last share equals egttools' ({x[0]:.6f})")
        spreads = last["grim"] > 0.5
        check(spreads == (v["start"] > barrier),
              f"spread {name}: cooperation {'spreads' if spreads else 'dies out'} from {float(v['start'])}, "
              f"as x* = {float(barrier):.6f} says")


def check_ecology():
    model = "models/ecology.yaml"
    for scenario in ["", "clean", "careful", "careless", "careful_long"]:
        games = forge_json(model, scenario)
        m = games["noisy_wide"]["matches"]
        matrix = [[m[a][b] for b in NINE] for a in NINE]
        dyn = games["ecology"]["dynamics"]
        path = replicate(matrix, [mpf(1) / 9] * 9, len(dyn["path"]) - 1)
        gap = worst_gap(dyn["path"], path, NINE)
        check(gap < SHARE_TOL, f"ecology {scenario or 'base'}: every share of every generation "
              f"equals the replicator equation at 60 digits (largest gap {gap:.1e})")


def check_axelrod():
    import warnings
    warnings.filterwarnings("ignore")
    import axelrod as axl

    def roster():
        return [axl.Grudger(), axl.TitForTat(), axl.Defector(), axl.Cooperator(),
                axl.Random(0.5), axl.GTFT(p=1 / 3), axl.TitFor2Tats(),
                axl.WinStayLoseShift(), axl.SuspiciousTitForTat()]

    for scenario, noise in [("clean", 0), ("careful", 0.01), ("", 0.05), ("careless", 0.1)]:
        tournament = axl.Tournament(roster(), turns=200, repetitions=100, noise=noise, seed=1)
        ecosystem = axl.Ecosystem(tournament.play(progress_bar=False, processes=None))
        ecosystem.reproduce(500)
        theirs = dict(zip(NINE, ecosystem.population_sizes[-1]))
        ours = forge_json("models/ecology.yaml", scenario)["ecology"]["dynamics"]["path"][-1]["shares"]
        if noise == 0:
            dead = ["ad", "rand", "stft"]
            check(all(theirs[s] < 1e-3 and ours[s] < 1e-3 for s in dead),
                  "ecology clean: AlwaysDefect, Random and suspicious TitForTat die out in both")
        else:
            top = max(ours, key=ours.get)
            check(max(theirs, key=theirs.get) == top,
                  f"ecology {scenario or 'base'}: axelrod's Ecosystem's largest share is {top}, as Forge's "
                  f"({theirs[top]:.3f} against {ours[top]:.3f})")


if __name__ == "__main__":
    check_spread()
    check_ecology()
    if "--axelrod" in sys.argv:
        check_axelrod()
    print(f"\n{len(failures)} failed" if failures else "\nall agree")
    sys.exit(1 if failures else 0)
