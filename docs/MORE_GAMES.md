# More Games: Horizons, Audits, Mistakes, Norms, the Commons and Hidden Types

**Technical Note v1.4**

**Date:** 2026-11-21
**Status:** Working Draft

---

## Abstract

More games, each a [Forge](https://github.com/mollendorff-ai/forge) model that works out its own equilibria or plays its own tournament (Forge 10.0.0-rc.30 or later). Each result is checked outside Forge: equilibria with nashpy or Gambit, the noisy tournament with the Python axelrod library, and everything else by hand. `scripts/check_models.py` checks every figure below on each change.

| Game | Model | What it shows | Status |
|------|-------|---------------|--------|
| When cooperation holds | [continuation.yaml](../models/continuation.yaml) | The threshold `w* = (T-c-R)/(T-P)` the project derives by formula is where a real tournament flips | Textbook, now played rather than derived |
| Audit the AI | [inspection.yaml](../models/inspection.yaml) | A harsher penalty makes the human audit less, not the AI cheat less; cheaper audits make it cheat less | Textbook (Tsebelis, 1989) |
| Does forgiveness pay? | [noisy_tournament.yaml](../models/noisy_tournament.yaml) | With mistakes, never forgiving is what falls apart; forgiving wins only while mistakes are rare, and which forgiving strategy wins depends on who else plays | Checked; it contradicts what the roadmap expected |
| Mistake or defection? | [mistake_or_defection.yaml](../models/mistake_or_defection.yaml) | When defectors are rare and mistakes common, one defection is more likely a slip: it takes two or three before "defector" is the better reading | Textbook Bayes' rule; added in v0.6.2 |
| Whose conventions? | [conventions.yaml](../models/conventions.yaml) | When human and AI prefer different norms, a cost of conflict hardly helps; giving way does | Textbook (Luce and Raiffa, 1957) |
| Five AIs in one game | [public_goods.yaml](../models/public_goods.yaml) | With five players the cost of conflict works as it does with two: below a line all five keep, above it all five give | Textbook (Ledyard, 1995); added in v0.6.0 |
| Aligned or not? | [hidden_types.yaml](../models/hidden_types.yaml) | When the human cannot tell which AI it faces, more aligned AIs do not make it safer until it stops checking; a cost of conflict that makes exploiting dominated means nobody needs to know | Textbook (Tsebelis, 1989, with a type); added in v0.6.3 |
| Can an AI show it is aligned? | [signalling.yaml](../models/signalling.yaml) | A signal sorts aligned from misaligned AIs only if it is dearer for the misaligned one; one that costs both the same is bought first by the misaligned AI | Textbook (Spence, 1973); added in v0.6.3 |

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

**Checked:** by the closed form above, which gives the same four numbers. Forge also finds the flip point without the formula: `forge goal-seek models/continuation.yaml --target defector_edge --value 0 --vary w` plays the tournament at each w and lands on 0.5 at c = 0, 0.375 at c = 0.5 and 0.25 at c = 1, exactly `w*`.

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

### 3.2 Mistake or Defection?

**Model:** [mistake_or_defection.yaml](../models/mistake_or_defection.yaml), a Bayesian network (`forge bayesian`). Added in v0.6.2.

The tournaments above end on a condition: cooperation needs each side to tell a slip from a defection. This model asks how many defections it takes before "this partner is a defector" is the better reading.

A partner either means to cooperate every round or means to defect every round. A share p of partners are defectors. Each move is flipped by mistake with the chance `noise`. Forge works out the chance that the partner is a defector, given the moves seen. By Bayes' rule, each defection multiplies the odds of "defector" by `(1 - noise) / noise`, and each cooperation divides them by the same:

`odds after k defections = p / (1 - p) × ((1 - noise) / noise)^k`

So a defection followed by a cooperation leaves you where you started.

| Defectors | Noise | After 1 defection | After 2 | After 3 | Defections it takes |
|-----------|-------|-------------------|---------|---------|---------------------|
| 1 in 100 | 1% | 50.0% | 99.0% | 99.99% | 2 |
| 1 in 100 | 5% | 16.1% | 78.5% | 98.6% | 2 |
| 1 in 100 | 10% | 8.3% | 45.0% | 88.0% | 3 |
| 1 in 10 | 1% | 91.7% | 99.9% | 100.0% | 1 |
| 1 in 10 | 5% | 67.9% | 97.6% | 99.9% | 1 |
| 1 in 10 | 10% | 50.0% | 90.0% | 98.8% | 2 |
| 3 in 10 | 1% | 97.7% | 99.98% | 100.0% | 1 |
| 3 in 10 | 5% | 89.1% | 99.4% | 99.97% | 1 |
| 3 in 10 | 10% | 79.4% | 97.2% | 99.7% | 1 |

"Defections it takes" is the first count at which "defector" is more likely than not; exactly 50% does not count.

- **When defectors are rare, one defection is more likely a slip.** At 1 in 100 with 5% noise, one defection says 16%; it takes two. At 10% noise it takes three.
- **When defectors are common, one is enough.** At 3 in 10, a single defection points to a defector at every noise level here.
- **That is the difference between TitForTat and TitForTwoTats.** TitForTat strikes back after one defection; TitForTwoTats after two. Which rule reads the evidence better depends on how rare defectors are and how noisy the moves are. This is consistent with the tournaments above, where TitForTwoTats did well in rosters with a few exploiters and some noise. It does not explain them: the tournament scores depend on far more than this.

**Left out:** partners who answer your moves. Against TitForTat, a defection may be its reply to your own slip, and this network does not model that. Nor does it model a partner who is a defector only some of the time.

**Checked:** `scripts/check_models.py` runs the network at all nine settings and compares Forge's chances after one, two and three defections with Bayes' rule in exact fractions (all agree to 1e-9), and checks the count in the last column.

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

## 6. Hidden Types

Every game above assumes each side knows what the other is. Here the human does not: the AI may be aligned or misaligned, and only the AI knows which. The human's belief that it is aligned, before anything happens, is the prior `p`. Forge has no move by chance, so both games are written in normal form with payoffs expected over the AI's type (Harsanyi, 1967). Both were added in v0.6.3.

### 6.1 Aligned or Not?

**Model:** [hidden_types.yaml](../models/hidden_types.yaml).

An aligned AI always honours the human's trust: it is a committed type, as in Kreps, Milgrom, Roberts and Wilson (1982), and does not choose. A misaligned AI honours or exploits. The human relies on the AI, or verifies its work at a cost v, which blocks an exploit; a misaligned AI caught exploiting loses f. Whoever exploits pays the cost of conflict c.

| | Rely | Verify |
|---|---|---|
| **Honour** | b, h | b, h - v |
| **Exploit** | e - c, p h - (1-p) l | -f - c, p (h - v) - (1-p) v |

Payoffs are (misaligned AI, human), with h = 2, l = 4, v = 1, b = 1, e = 3 and f = 1. The human's payoffs are expected over the type: an exploit costs it l only when the AI is in fact misaligned.

- **Above `p* = 1 - v/l`** (0.75 here) the human relies without checking, and every misaligned AI exploits.
- **Below `p*`** both mix. The human verifies at `(e - c - b) / (e + f)`, which does not depend on p. A misaligned AI exploits at `(v/l) / (1 - p)`, so the human is exploited in `v/l` of all meetings, whatever p is.
- **From `c* = e - b`** (2 here) exploiting is dominated: every AI honours and the human relies.

| Scenario | p | c | Misaligned AI exploits | Human verifies | Human exploited | Human gets |
|----------|---|---|------------------------|----------------|-----------------|------------|
| base | 0.5 | 0 | 0.5 | 0.5 | 0.25 | 0.5 |
| rare | 0.25 | 0 | 1/3 | 0.5 | 0.25 | 0.5 |
| common | 0.8 | 0 | 1 | 0 | 0.2 | 0.8 |
| cost1 | 0.5 | 1 | 0.5 | 0.25 | 0.25 | 0.5 |
| costly | 0.5 | 2.5 | 0 | 0 | 0 | 2 |

Going from a quarter of AIs aligned to half does not make the human any safer: it is exploited in a quarter of meetings either way and gets 0.5 either way. When aligned AIs are more common, each misaligned one exploits more often, because the human's checks are set by the misaligned AI's payoffs, not by how many there are. Only above `p*`, where the human stops checking, does the share of aligned AIs matter, and then every misaligned AI exploits. A cost of conflict below `c*` does no better: at c = 1 the human checks half as often and is exploited just as often. At c = 2.5 nobody exploits, and the human gets the full 2 without knowing which AI is which.

**For the project:** this is the inspection game of [§2](#2-audit-the-ai) with a type written in, and the same lesson comes back sharper: a penalty-like cost that stops short of making the bad act dominated changes how much checking is needed, not how often the human is harmed. Past `c*` the cost of conflict does more than lower a threshold: it makes the type irrelevant. Kinship's question was whether cooperation needs the AI to share the human's values. In this model it does not, once conflict costs enough; below that, it would need the human to know.

**Checked:** Gambit (pygambit 16.7, `enummixed_solve`) and nashpy 0.0.43 (vertex enumeration), from payoffs built outside the model, find the same single equilibrium in all five scenarios.

### 6.2 Can an AI Show It Is Aligned?

**Model:** [signalling.yaml](../models/signalling.yaml).

Before the human decides whether to trust it, the AI may send a signal, such as opening itself to an audit, that costs an aligned AI `s_aligned` and a misaligned one `s_misaligned`. Trusted, an aligned AI gets b = 1 and the human h = 2; a misaligned AI exploits, gets `e - c` (e = 3) and the human loses l = 4. Not trusted, nobody gets anything. With p = 0.5, trusting every AI would give the human -1, so without a signal it trusts none.

The types choose only whether to signal, so a strategy is a plan for each type: the AI plays both, aligned_only, misaligned_only or neither (which types signal), and the human always, after_signal, after_none or never (when it trusts).

The signal sorts the types, the aligned AI signalling and the misaligned one not, only when `s_aligned <= b` and `s_misaligned >= e - c`: it has to be worth it to the aligned AI and not to the misaligned one (Spence, 1973).

| Scenario | s_aligned | s_misaligned | c | Besides "nobody signals" | "Nobody signals" survives the Intuitive Criterion |
|----------|-----------|--------------|---|--------------------------|---------------------------------------------------|
| base | 0.5 | 4 | 0 | sorting: only the aligned AI signals, and the human trusts a signal and nothing else | no |
| same_cost | 0.5 | 0.5 | 0 | nothing | yes |
| dear | 2 | 2 | 0 | nothing | yes |
| cheap | 0.5 | 2 | 0 | half-sorting: the misaligned AI signals half the time, the human trusts a signal 2/3 of the time | yes |
| conflict | 0.5 | 2 | 1.5 | sorting, as in base | no |

A signal that costs both types the same never sorts them here: one that costs both the same is bought first by the misaligned AI, because it gains more from being trusted (3 against 1). At 0.5 both would pay it, so it says nothing; at 2 the aligned AI will not pay it, and the misaligned one alone would mark itself by signalling. A signal that is dearer for the misaligned AI, but still below its gain (`cheap`), half works: the misaligned AI signals half the time, just often enough that the human, trusting a signal 2/3 of the time, is indifferent. A cost of conflict of 1.5 (`conflict`) brings the misaligned AI's gain down to 1.5, below the signal's cost of 2, and the same signal sorts them again. The signal's cost and the cost of conflict add up: what matters is whether the signal costs the misaligned AI more than exploiting gains it.

"Nobody signals, nobody is trusted" is an equilibrium in every scenario, held up by what the human would do after a signal nobody sends. In `base` and `conflict` that is not credible: a misaligned AI could never gain by signalling, so a signal can only come from an aligned AI, and the human should trust it (the Intuitive Criterion, Cho and Kreps, 1987). Forge finds Nash equilibria and does not apply the criterion; the last column is worked out by hand.

**For the project:** if an AI's alignment is to be shown rather than assumed, the evidence has to be dearer for an AI that is not aligned: an audit a misaligned AI is likely to fail, not a statement any AI can make. Cheap talk sorts nothing. And the cost of conflict helps here too, by lowering what a misaligned AI gains from being trusted. This is an analogy, not a model of real audits: neither the costs nor the types of real AIs are known.

**Checked:** Gambit (pygambit 16.7, `enummixed_solve`) and nashpy 0.0.43 (vertex enumeration), from payoffs built outside the model, find every equilibrium Forge finds in all five scenarios. The game is degenerate (a tie off the path of play), and both also find the far end of a line of equilibria where nobody signals and the human trusts a signal with some chance, up to `min(s_aligned / b, s_misaligned / (e - c))`. Forge lists one end of that line, as it warns it may.

---

## References

1. Axelrod, R. (1984). *The Evolution of Cooperation*. Basic Books.
2. Cho, I.-K. and Kreps, D.M. (1987). Signaling games and stable equilibria. *Quarterly Journal of Economics*, 102(2), 179-221.
3. Harsanyi, J.C. (1967). Games with incomplete information played by "Bayesian" players, Part I. *Management Science*, 14(3), 159-182.
4. Kreps, D.M., Milgrom, P., Roberts, J. and Wilson, R. (1982). Rational cooperation in the finitely repeated prisoners' dilemma. *Journal of Economic Theory*, 27(2), 245-252.
5. Ledyard, J.O. (1995). Public goods: a survey of experimental research. In Kagel, J.H. and Roth, A.E. (eds), *The Handbook of Experimental Economics*. Princeton University Press.
6. Luce, R.D. and Raiffa, H. (1957). *Games and Decisions*. Wiley.
7. Nowak, M.A. and Sigmund, K. (1992). Tit for tat in heterogeneous populations. *Nature*, 355, 250-253.
8. Nowak, M.A. and Sigmund, K. (1993). A strategy of win-stay, lose-shift that outperforms tit-for-tat in the Prisoner's Dilemma game. *Nature*, 364, 56-58.
9. Spence, M. (1973). Job market signaling. *Quarterly Journal of Economics*, 87(3), 355-374.
10. Tsebelis, G. (1989). The abuse of probability in political analysis: the Robinson Crusoe fallacy. *American Political Science Review*, 83(1), 77-91.

---

*This document is part of the Kinship Protocol research project.*
*Source: [github.com/mollendorff-ai/kinship-protocol](https://github.com/mollendorff-ai/kinship-protocol)*
