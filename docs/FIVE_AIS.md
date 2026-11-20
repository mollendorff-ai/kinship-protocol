# Five AIs in One Game: Public Goods

**Technical Note v1.0**

**Date:** 2026-11-20
**Status:** Working Draft

---

## Abstract

The README's five sessions (Claude, two Groks, two Copilots) put in one game, as a [Forge](https://github.com/mollendorff-ai/forge) model: [five_ais.yaml](../models/five_ais.yaml). Each AI starts with 1 and gives it to a common pot or keeps it. There are two versions of the game, and Forge finds every pure equilibrium of each (Forge 10.0.0-rc.30 or later).

| Game | What it shows | Status |
|------|---------------|--------|
| Linear: the pot is tripled and shared | Nobody gives, though all five would get three times as much if all gave | Textbook (the linear public goods game; Ledyard, 1995) |
| Threshold: a good exists only if three give | Three give and two free ride, or nobody gives; which three, the game does not say | Textbook (step-level public goods, Palfrey and Rosenthal, 1984) |

Both are one-shot games: the five choose once, at the same time. None of this is new. What it adds is the project's cost of conflict c, paid here by each AI that keeps.

**Checked:** outside Forge, by trying every unilateral deviation in all 32 cells of each game, in exact fractions. `scripts/check_models.py` checks every figure below against Forge in every scenario.

**Not covered:** mixed equilibria (Forge looks for them only in two-player games), repeated play, and strategies that spread over generations (replicator dynamics, still parked for v0.6.0).

---

## 1. The Linear Game

Each AI gives its 1 or keeps it. What is given is multiplied by 3 and shared by all five. With k givers:

- a giver gets `3k/5`;
- a keeper gets `1 - c + 3k/5`.

Each unit an AI gives comes back to it as 3/5. So keeping pays `1 - c - 3/5` more than giving, whatever the others do: 0.4 with no cost. Keeping is the better choice for each AI until c reaches 0.4.

| c | Pure equilibria | In them | Each gets |
|---|-----------------|---------|-----------|
| 0 | 1 | Nobody gives | 1 |
| 0.4 | 32 | Every cell (everyone is indifferent) | — |
| 0.5 | 1 | Everyone gives | 3 |

With no cost, the only equilibrium is that nobody gives and each gets 1. If all five gave, each would get 3. That gap is the textbook social dilemma, with five players instead of two.

A cost of conflict of 0.5 flips it: now giving pays more whatever the others do, and everyone gives. That is less of a result than it looks. A cost paid by whoever keeps is a fine on keeping, and a large enough fine makes anyone give. The question is who levies it.

---

## 2. The Threshold Game

Now the pot is not shared. A good worth 2 to every AI exists only if at least 3 give, and what is given is used up. With k givers:

- a giver gets 2 if k is at least 3, otherwise 0;
- a keeper gets `1 - c`, plus 2 if k is at least 3.

| c | Pure equilibria | In them |
|---|-----------------|---------|
| 0 | 11 | Nobody gives, or exactly 3 give |
| 0.5 | 11 | Nobody gives, or exactly 3 give |
| 1 | 22 | Ties: nobody, 1, 3, 4 or all 5 give |
| 1.5 | 1 | Everyone gives |

With exactly 3 givers, each giver is needed: if one stops, the good is gone. Each keeper is not: giving would add nothing. So the 3 givers get 2 each and the 2 keepers get 3 each. Nobody giving is an equilibrium too, because one AI giving alone gets nothing back.

There are 10 ways to pick the 3 givers, and the game does not say which. Forge lists the cells in table order, so its first equilibrium has Claude and the two Groks giving and the two Copilots keeping (each Copilot gets 3, each giver 2). That is the order of the columns, not a prediction about Copilot.

Three givers is also the best the five can do between them: 12 with no cost, against 10 if all give (two of the gifts are wasted) and 5 if nobody does.

A small cost of conflict changes nothing: at c = 0.5 the equilibria are the same 11. Only when keeping costs more than the endowment (c above 1) does everyone give, though three would be enough.

---

## For the Project

The README's table says five AIs, asked about cooperation, each answered "cooperation optimal". In a one-shot public goods game, the textbook answer is the opposite: nobody gives, unless keeping is fined. In the threshold version some give, but the ones who do best are the ones who do not.

So "cooperation optimal" needs more than game theory and a calculator. It needs repeated play, a fine on free riding, or a way to agree on who gives. This model has none of them. The repeated version, and strategies that spread over generations, are what v0.6.0 still waits on Forge for.

---

## References

1. Ledyard, J.O. (1995). Public goods: a survey of experimental research. In Kagel and Roth (eds.), *The Handbook of Experimental Economics*. Princeton University Press.
2. Palfrey, T.R. and Rosenthal, H. (1984). Participation and the provision of discrete public goods: a strategic analysis. *Journal of Public Economics*, 24(2), 171-193.

---

*This document is part of the Kinship Protocol research project.*
*Source: [github.com/mollendorff-ai/kinship-protocol](https://github.com/mollendorff-ai/kinship-protocol)*
