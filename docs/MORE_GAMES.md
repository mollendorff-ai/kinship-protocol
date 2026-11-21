# More Games: Horizons, Audits, Mistakes, Norms and the Commons

**Technical Note v1.2**

**Date:** 2026-11-21
**Status:** Working Draft

---

## Abstract

Five more games, each a [Forge](https://github.com/mollendorff-ai/forge) model that works out its own equilibria or plays its own tournament (Forge 10.0.0-rc.30 or later). Each result is checked outside Forge: equilibria with nashpy or Gambit, the noisy tournament with the Python axelrod library, and everything else by hand. `scripts/check_models.py` checks every figure below on each change.

| Game | Model | What it shows | Status |
|------|-------|---------------|--------|
| When cooperation holds | [continuation.yaml](../models/continuation.yaml) | The threshold `w* = (T-c-R)/(T-P)` the project derives by formula is where a real tournament flips | Textbook, now played rather than derived |
| Audit the AI | [inspection.yaml](../models/inspection.yaml) | A harsher penalty makes the human audit less, not the AI cheat less; cheaper audits make it cheat less | Textbook (Tsebelis, 1989) |
| Does forgiveness pay? | [noisy_tournament.yaml](../models/noisy_tournament.yaml) | With mistakes, never forgiving is what falls apart; forgiving wins only while mistakes are rare, and which forgiving strategy wins depends on who else plays | Checked; it contradicts what the roadmap expected |
| Whose conventions? | [conventions.yaml](../models/conventions.yaml) | When human and AI prefer different norms, a cost of conflict hardly helps; giving way does | Textbook (Luce and Raiffa, 1957) |
| Five AIs in one game | [public_goods.yaml](../models/public_goods.yaml) | With five players the cost of conflict works as it does with two: below a line all five keep, above it all five give | Textbook (Ledyard, 1995); added in v0.6.0 |

None of these are new results. What they add is that the project's levers (the cost of conflict, the chance of meeting again) are put into games where they do not always work.

The games that contain a prisoner's dilemma use the Axelrod payoffs: T = 5, R = 3, P = 1, S = 0.

---

## 1. When Cooperation Holds

**Model:** [continuation.yaml](../models/continuation.yaml), adapted from Forge's `examples/games/continuation.yaml`.

[COOPERATION_THRESHOLDS.md](COOPERATION_THRESHOLDS.md) derives `w* = (T - c - R) / (T - P)`: the chance of meeting again above which cooperation can hold. Here a tournament checks it. Matches end at random: after each round, the match goes on with the chance w. GrimTrigger, TitForTat and AlwaysDefect play everyone, themselves included.

Against GrimTrigger, AlwaysDefect gets T - c once and P - c in every round after, an average of `(1 - w)(T - c) + w (P - c)` a round. GrimTrigger gets R against itself. GrimTrigger is collectively stable (nothing in the roster does better against it than it does against itself) exactly when `w >= w*`.

| Scenario | w | c | w* | AlwaysDefect vs GrimTrigger | GrimTrigger holds |
|----------|---|---|----|-----------------------------|-------------------|
| short | 0.4 | 0 | 0.5 | 3.4 | No |
| edge | 0.5 | 0 | 0.5 | 3.0 (a tie) | Yes |
| base | 0.6 | 0 | 0.5 | 2.6 | Yes |
| costly | 0.4 | 0.5 | 0.375 | 2.9 | Yes |

At w = 0.4 a defector gets 3.4 a round against GrimTrigger's 3, so it pays to defect. Add a cost of conflict of 0.5 and the same short horizon holds: the threshold falls to 0.375, the corrected figure in COOPERATION_THRESHOLDS.md §4.2. The tournament and the formula agree in every scenario (`kinship.agrees` is 1 in all four).

**Checked:** by the closed form above, which gives the same four numbers.

---

## 2. Audit the AI

**Model:** [inspection.yaml](../models/inspection.yaml), adapted from Forge's `examples/games/inspection.yaml`.

An AI complies or cheats; a human audits or trusts.

| | Audit | Trust |
|---|---|---|
| **Comply** | 0, -audit_cost | 0, 0 |
| **Cheat** | -penalty, -audit_cost | gain, -harm |

Payoffs are (AI, human), with gain 2, penalty 4, audit cost 1 and harm 3.

No cell is an equilibrium: if the AI complies the human stops auditing, and then the AI cheats, and then the human audits, and then the AI complies. In the only equilibrium both mix, and each side's mix is set by the other side's payoffs:

- The human audits just often enough that the AI is indifferent: `gain / (gain + penalty)`.
- The AI cheats just often enough that the human is indifferent: `audit_cost / harm`.

| Penalty | Audit cost | Human audits | AI cheats |
|---------|------------|--------------|-----------|
| 2 | 1 | 0.5 | 1/3 |
| 4 | 1 | 1/3 | 1/3 |
| 8 | 1 | 0.2 | 1/3 |
| 4 | 0.5 | 1/3 | 1/6 |

Doubling the penalty does not make the AI cheat less. It lets the human audit less, because a smaller chance of being caught is enough to deter. What makes the AI cheat less is cheaper audits: at half the audit cost, it cheats half as often. Forge's tornado (`forge tornado models/inspection.yaml`) shows the same thing from the human's side: the penalty swings the audit rate by 0.3, and the audit cost does not move it at all.

**For the project:** the cost of conflict lowers the cooperation threshold in the prisoner's dilemma, but in an inspection game punishment is not the lever. If the aim is an AI that cheats less, oversight that is cheap to run matters more than penalties that are harsh. This is a textbook result about policing (Tsebelis, 1989), with the obvious caveat that a real AI is not a payoff-maximising row player.

**Checked:** nashpy finds the same single mixed equilibrium in all four scenarios.

---

## 3. Does Forgiveness Pay?

**Model:** [noisy_tournament.yaml](../models/noisy_tournament.yaml), adapted from Forge's `examples/games/noisy-tournament.yaml`.

The roadmap expected this game to show tit-for-tat falling apart under mistakes and a forgiving strategy winning. In this project's roster it does not, quite.

The five strategies of [axelrod_tournament.yaml](../models/axelrod_tournament.yaml) (GrimTrigger, TitForTat, AlwaysDefect, AlwaysCooperate, Random) play with two that forgive: generous TitForTat, which forgives a defection with chance 1/3, and TitForTwoTats, which strikes back only after two defections in a row. Matches are 200 rounds, everyone against everyone and themselves. Each move is flipped with the chance `noise`, so an AI that meant to cooperate defects by mistake, or the other way round. The scores are exact expected values, not samples.

| Noise | Winner (payoff per round) | GrimTrigger | Generous TitForTat |
|-------|---------------------------|-------------|--------------------|
| 0 | GrimTrigger 2.711, then TitForTat 2.606 | 1st | 4th |
| 1% | TitForTwoTats 2.378, then TitForTat 2.318 | 4th | 3rd |
| 5% | TitForTat 2.248, TitForTwoTats 2.247 | 4th | 5th |
| 10% | GrimTrigger 2.278, AlwaysDefect 2.276 | 1st | 6th |

What the tournament shows:

- **Never forgiving is what falls apart.** GrimTrigger wins without mistakes and drops to 4th at 1% and 5%: one slip and it defects for the rest of the match, against friends as well as enemies.
- **Forgiving a slip pays while slips are rare.** At 1% TitForTwoTats wins. At 5% it and TitForTat are level (0.0006 apart, a tie in effect).
- **Forgiving everything does not pay here.** Generous TitForTat forgives AlwaysDefect and Random too, and they take advantage; it finishes 5th at 5%.
- **When mistakes are common, nobody cooperates.** At 10% the two strategies that defect most come first; cooperation never gets going long enough to pay.

The textbook result that generous TitForTat wins under noise (Nowak and Sigmund, 1992) is about a population evolving over generations, where strategies that do badly die out and stop feeding the exploiters. A single round-robin with AlwaysDefect and Random in it is a different test. Replicator dynamics, which would show the evolving version, are parked for v0.7.0.

**For the project:** "cooperation pays" needs the other side to be able to tell a mistake from a defection. With noisy signals, the right amount of forgiveness depends on who else is playing and how noisy the channel is.

**Checked:** with the axelrod library (version 4.14), playing 500 seeded matches of each pairing at each noise level. It gives the same order at every level and scores within 0.01 of Forge's, except that at 5% it puts TitForTwoTats a hair ahead of TitForTat (2.2452 against 2.2448), the other way round from Forge's exact 2.2472 against 2.2478. That is inside the sampling error, and it is why the table calls 5% a tie.

| Noise | axelrod library, top three |
|-------|----------------------------|
| 0 | GrimTrigger 2.710, TitForTat 2.605, TitForTwoTats 2.552 |
| 1% | TitForTwoTats 2.377, TitForTat 2.319, generous TitForTat 2.283 |
| 5% | TitForTwoTats 2.245, TitForTat 2.245, Random 2.219 |
| 10% | GrimTrigger 2.277, AlwaysDefect 2.274, TitForTat 2.242 |

### 3.1 With Nine Players

Added in v0.6.0. Forge has two more strategies the roster above leaves out: Pavlov (win-stay, lose-shift: repeat a move that paid, switch one that did not), the textbook answer to noise (Nowak and Sigmund, 1993), and suspicious TitForTat, which opens by defecting and then copies. The model's `clean_wide` and `noisy_wide` games play all nine; the seven-player results above are unchanged.

| Noise | Winner (payoff per round) | Second | GrimTrigger | Pavlov | Generous TitForTat |
|-------|---------------------------|--------|-------------|--------|--------------------|
| 0 | TitForTwoTats 2.650 | TitForTat 2.638 | 4th | 5th | 3rd |
| 1% | TitForTwoTats 2.417 | generous TitForTat 2.404 | 7th | 3rd | 2nd |
| 5% | TitForTwoTats 2.283 | Pavlov 2.270 | 7th | 2nd | 3rd |
| 10% | GrimTrigger 2.267 | AlwaysDefect 2.265 | 1st | 3rd | 8th |

Two more players change the answer more than the noise does:

- **GrimTrigger is 4th even without mistakes.** Suspicious TitForTat's opening defection is one defection, and GrimTrigger never forgives it: it gets 1.015 a round in that match, where TitForTwoTats gets 2.985. A single bad first impression costs the unforgiving strategy what a 1% error rate cost it before.
- **A forgiving strategy now wins at 5% noise.** TitForTwoTats is first at 0, 1% and 5%, and generous TitForTat climbs to 2nd at 1% and 3rd at 5%. Both new players reciprocate, so the players that exploit forgiveness, AlwaysDefect and Random, are now two in nine rather than two in seven.
- **Pavlov is good, not best.** It comes 2nd at 5% and 3rd at 10%, and wins nowhere. It does badly against AlwaysDefect, which it keeps trying to cooperate with every other round.
- **At 10% the defectors still win.** That result did not depend on the roster.

So the seven-player table above is one roster's answer. "Does forgiveness pay?" depends on how noisy the channel is and on who else is playing, and the second matters at least as much as the first.

**Checked:** with the axelrod library (version 4.14), 500 seeded matches of each pairing at each noise level. It gives the same order as Forge, all nine places, at every level, and scores within 0.01 of Forge's.

| Noise | axelrod library, top three |
|-------|----------------------------|
| 0 | TitForTwoTats 2.650, TitForTat 2.638, generous TitForTat 2.626 |
| 1% | TitForTwoTats 2.417, generous TitForTat 2.397, Pavlov 2.344 |
| 5% | TitForTwoTats 2.282, Pavlov 2.269, generous TitForTat 2.261 |
| 10% | GrimTrigger 2.268, AlwaysDefect 2.267, Pavlov 2.250 |

---

## 4. Whose Conventions?

**Model:** [conventions.yaml](../models/conventions.yaml), adapted from Forge's `examples/games/battle-of-the-sexes.yaml`.

A human and an AI both want to work to the same norm, but each prefers its own. Missing each other pays nothing, less the cost of conflict c that each side pays.

| | Human's norm | AI's norm |
|---|---|---|
| **Human's norm** | 3, 2 | -c, -c |
| **AI's norm** | -c, -c | 2, 3 |

Payoffs are (human, AI).

There are two pure equilibria, one on each norm, and a mixed one in which each side insists on its own norm with `(3 + c) / (5 + 2c)`.

| c | Each insists | They miss each other | Each expects |
|---|--------------|----------------------|--------------|
| 0 | 0.6 | 52% | 1.2 |
| 1 | 4/7 | 51% | 5/7 |
| 5 | 8/15 | 50.2% | -19/15 |

With no cost, they miss each other 52% of the time and each expects 1.2, less than the 2 either side gets by giving way. A cost of conflict, the lever that makes cooperation pay in the prisoner's dilemma, hardly helps: they still miss about half the time, and each now expects less, because every miss costs more. The miss rate can never fall below 50% in the mixed equilibrium, whatever the cost.

**For the project:** a coordination problem is not solved by making conflict expensive. It is solved by a convention: a precedent, a rule, or one side giving way. Whose norm becomes the convention is a question of power and fairness that game theory states but does not answer.

**Checked:** nashpy finds the same three equilibria at c = 0, 1 and 5, and the same miss rates and payoffs.

---

## 5. Five AIs in One Game

**Model:** [public_goods.yaml](../models/public_goods.yaml). Added in v0.6.0.

The README's experiment asked five AI sessions the same question. Here the five play one game. Each holds 1 and, at the same moment as the others, gives it to a common pot or keeps it. The pot is multiplied by r and shared equally by all five, keepers included. Each one who keeps pays the cost of conflict c.

If k of the five give:

- a giver gets `r k / 5`
- a keeper gets `1 - c + r k / 5`

Switching from keep to give changes an AI's own payoff by `r/5 - (1 - c)`, whatever the other four do. So keeping dominates while `c < 1 - r/5`, and giving dominates once `c > 1 - r/5`. The game has 32 profiles, and Forge finds every pure equilibrium of it (Forge finds pure equilibria for any number of players; mixed ones only for two).

| Scenario | r | c | Equilibria | What all five do | Each gets |
|----------|---|---|------------|------------------|-----------|
| base | 2 | 0 | 1 | keep | 1 (all giving would pay 2) |
| cheap | 2 | 0.5 | 1 | keep | 0.5 |
| edge | 2 | 0.6 | all 32 | anything: each is indifferent | between 0.4 and 2 |
| costly | 2 | 0.7 | 1 | give | 2 |
| rich | 6 | 0 | 1 | give | 6 |

With r = 2, all five keep below a cost of conflict of 0.6 and all five give above it. Below the line it is the prisoner's dilemma with five players: all five giving pays each 2, but each does better by keeping, so they end on 1. A cost of conflict of 0.5 does not help, it only makes the bad outcome worse (each gets 0.5). At 0.6 exactly, every profile is an equilibrium. With a pot worth six times what goes in, more than the number of players, each AI's own share of its own gift is worth more than the gift, and giving pays without any cost.

**For the project:** the lever works with five players as with two, and the line has the same shape: the cost has to cover what keeping gains, `1 - r/5`. What changes with more players is that the line moves up: each giver's share of its own gift is `r/n`, so the more AIs share the pot, the larger the cost of conflict that cooperation needs. And this is a game played once. The repeated version, where the chance of meeting again does the work, is the [continuation](#1-when-cooperation-holds) game's territory, and strategies that spread over generations (replicator dynamics, parked for v0.7.0) still wait on Forge.

Two of the five sessions were the same model (SuperGrok 4.1) in two modes. The players are named after the sessions to tie the game to the experiment, not because they would play differently: in this game all five have the same payoffs.

**Checked:** Gambit (pygambit 16.7, `enumpure_solve`) finds the same pure equilibria in all five scenarios: one, one, 32, one and one. So does checking each of the 32 profiles by hand, in exact fractions.

---

## References

1. Axelrod, R. (1984). *The Evolution of Cooperation*. Basic Books.
2. Luce, R.D. and Raiffa, H. (1957). *Games and Decisions*. Wiley.
3. Nowak, M.A. and Sigmund, K. (1992). Tit for tat in heterogeneous populations. *Nature*, 355, 250-253.
4. Nowak, M.A. and Sigmund, K. (1993). A strategy of win-stay, lose-shift that outperforms tit-for-tat in the Prisoner's Dilemma game. *Nature*, 364, 56-58.
5. Ledyard, J.O. (1995). Public goods: a survey of experimental research. In Kagel, J.H. and Roth, A.E. (eds), *The Handbook of Experimental Economics*. Princeton University Press.
6. Tsebelis, G. (1989). The abuse of probability in political analysis: the Robinson Crusoe fallacy. *American Political Science Review*, 83(1), 77-91.

---

*This document is part of the Kinship Protocol research project.*
*Source: [github.com/mollendorff-ai/kinship-protocol](https://github.com/mollendorff-ai/kinship-protocol)*
