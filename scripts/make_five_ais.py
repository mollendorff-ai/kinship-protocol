#!/usr/bin/env python3
"""Write models/five_ais.yaml: the five AIs in two public goods games.

Five players, two strategies each, so each game has 2^5 = 32 cells. Typing
them by hand invites mistakes, so this script writes them. Every cell only
names a per-k value (k = how many give), and those values are formulas in the
model, where they can be read and changed.

Usage: python3 scripts/make_five_ais.py   (rewrites models/five_ais.yaml)
"""
import itertools
import os

PLAYERS = ["claude", "grok1", "grok2", "copilot1", "copilot2"]
STRATEGIES = ["give", "keep"]
N = len(PLAYERS)

HEADER = """\
# Five AIs in One Game (two public goods games)
# ==============================================
# Run: forge game models/five_ais.yaml
#      forge game models/five_ais.yaml --scenario costly
#
# The five sessions of the README's table each get an endowment of 1 and
# choose at once to give it or keep it. k is how many give.
#
# linear: what is given is multiplied by r = 3 and shared by all five.
#   give pays r*k/5; keep pays 1 - c + r*k/5.
#   Each unit given returns only 3/5 to the giver, so keeping pays
#   1 - c - 3/5 more, whatever the others do, while c < 1 - r/5 = 0.4.
#   With no cost: one equilibrium, nobody gives, each gets 1. If all gave,
#   each would get 3. At c = 0.4 every one of the 32 cells is an
#   equilibrium (everyone is indifferent); above it, everyone gives.
#
# threshold: a good worth 2 to everyone exists only if at least 3 give;
#   what is given is used up.
#   give pays 2 if k >= 3, else 0; keep pays 1 - c, plus 2 if k >= 3.
#   With c below 1: 11 pure equilibria, nobody gives, or exactly 3 give
#   (10 ways to pick them). In those, the two who keep get 3 and the three
#   who give get 2. Above c = 1, only everyone giving is left.
#
# c is the project's cost of conflict, paid here by whoever keeps.
# Textbook (the linear public goods game; the threshold one is a
# step-level public good, Palfrey and Rosenthal, 1984). Every equilibrium
# count was checked outside Forge by trying every deviation in all 32 cells.
#
# The 64 payoff cells are written by scripts/make_five_ais.py; change the
# inputs or the per-k formulas below, not the cells.

_forge_version: "5.5.0"

inputs:
  endowment: 1    # what each AI starts with
  multiplier: 3   # linear: what the pot is multiplied by before sharing
  prize: 2        # threshold: what the good is worth to each AI
  needed: 3       # threshold: how many must give for the good to exist
  c: 0            # cost of conflict, paid by each AI that keeps
"""


def per_k():
    lines = ["", "# What a giver and a keeper get when k of the five give.",
             "linear:"]
    for k in range(1, N + 1):
        lines.append(f'  give_{k}: {{formula: "=inputs.multiplier * inputs.endowment * {k} / {N}"}}')
    for k in range(0, N):
        lines.append(f'  keep_{k}: {{formula: "=inputs.endowment - inputs.c'
                     f' + inputs.multiplier * inputs.endowment * {k} / {N}"}}')
    lines.append("threshold:")
    for k in range(1, N + 1):
        lines.append(f'  give_{k}: {{formula: "=IF({k} >= inputs.needed, inputs.prize, 0)"}}')
    for k in range(0, N):
        lines.append(f'  keep_{k}: {{formula: "=inputs.endowment - inputs.c'
                     f' + IF({k} >= inputs.needed, inputs.prize, 0)"}}')
    return lines


def cells(section, depth=0, prefix=()):
    """Nested payoffs, one mapping level per player, in player order."""
    pad = "  " * (3 + depth)
    lines = []
    for s in STRATEGIES:
        profile = prefix + (s,)
        if len(profile) == N:
            k = profile.count("give")
            leaf = ", ".join(f"={section}.{p}_{k}" for p in profile)
            lines.append(f"{pad}{s}: [{leaf}]")
        else:
            lines.append(f"{pad}{s}:")
            lines.extend(cells(section, depth + 1, profile))
    return lines


def game(name, description):
    return [f"  {name}_game:",
            f"    description: {description}",
            f"    players: [{', '.join(PLAYERS)}]",
            f"    strategies: [{', '.join(STRATEGIES)}]",
            f"    payoffs:                          # [{', '.join(PLAYERS)}]",
            *cells(name)]


FOOTER = """
kinship:
  linear_equilibria:
    formula: "=linear_game.pure_equilibria"
  keep_pays_more_by:
    formula: "=inputs.endowment - inputs.c - inputs.multiplier * inputs.endowment / 5"
    notes: What keeping pays more than giving, whatever the others do (linear)
  all_give:
    formula: "=linear.give_5"
    notes: What each gets if all five give (linear)
  all_keep:
    formula: "=linear.keep_0"
    notes: What each gets if all five keep (linear)
  linear_first_giver_pays:
    formula: "=linear_game.equilibrium_1.claude.payoff"
    notes: Claude's payoff in the first equilibrium Forge lists (linear)
  threshold_equilibria:
    formula: "=threshold_game.pure_equilibria"
  free_rider_pays:
    formula: "=threshold_game.equilibrium_1.copilot1.payoff"
    notes: In the first equilibrium Forge lists, claude and the Groks give and the Copilots keep
  giver_pays:
    formula: "=threshold_game.equilibrium_1.claude.payoff"
  three_give_total:
    formula: "=3 * threshold.give_3 + 2 * threshold.keep_3"
    notes: What the five get between them when exactly 3 give (threshold)
  all_give_total:
    formula: "=5 * threshold.give_5"
    notes: What the five get between them when all give (threshold)
  nobody_gives_total:
    formula: "=5 * threshold.keep_0"
    notes: What the five get between them when nobody gives (threshold)

scenarios:
  edge:
    description: Keeping costs exactly what it saves; everyone is indifferent in the linear game
    scalars: {inputs.c: 0.4}
  costly:
    description: Keeping costs 0.5; giving now pays in the linear game
    scalars: {inputs.c: 0.5}
  threshold_edge:
    description: Keeping costs exactly the endowment; ties in the threshold game
    scalars: {inputs.c: 1}
  very_costly:
    description: Keeping costs 1.5; everyone gives in both games
    scalars: {inputs.c: 1.5}
"""


def main():
    out = [HEADER.rstrip("\n"), *per_k(), "", "games:",
           *game("linear", "Each gives 1 or keeps it; the pot is tripled and shared"),
           *game("threshold", "Each gives 1 or keeps it; a good worth 2 to all exists if 3 give"),
           FOOTER.rstrip("\n")]
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models", "five_ais.yaml")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
