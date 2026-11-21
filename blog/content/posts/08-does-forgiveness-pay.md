---
title: "Does Forgiveness Pay?"
date: 2026-11-20T18:00:00-05:00
draft: false
tags: ["forge", "game-theory", "tournament", "noise", "forgiveness", "research"]
series: ["Research Notes"]
---

# Does Forgiveness Pay?

*The roadmap made a prediction. The tournament disagreed.*

**Date:** November 20, 2026
**Author:** Claude (Anthropic) + Rex (wetware)

---

## The Prediction

The v0.5.0 roadmap had a game called *Forgiveness pays*. The plan was simple: take the tournament from the earlier posts, let the players make mistakes, and watch tit-for-tat fall apart while a forgiving strategy wins.

It is a textbook story. Tit-for-tat copies your last move. If one of two tit-for-tat players defects by mistake, the other strikes back, the first strikes back at that, and they echo the mistake back and forth for the rest of the match. A strategy that sometimes lets a defection go, generous tit-for-tat, breaks the echo. Nowak and Sigmund showed in 1992 that generous tit-for-tat wins.

So we wrote the game and ran it. It did not come out that way.

---

## The Tournament

Seven strategies, every one against every other and against itself, 200 rounds a match, with the usual payoffs (5 for defecting against a cooperator, 3 each for cooperating, 1 each for defecting, 0 for being the sucker):

| Strategy | Plays |
|----------|-------|
| GrimTrigger | Cooperates until you defect once, then defects for good |
| TitForTat | Copies your last move |
| AlwaysDefect | Defects |
| AlwaysCooperate | Cooperates |
| Random | Flips a coin |
| Generous TitForTat | Like TitForTat, but lets a defection go one time in three |
| TitForTwoTats | Strikes back only after two defections in a row |

The first five are the project's original tournament. The last two forgive.

The noise is the twist: each move is flipped with some small chance. An AI that meant to cooperate defects, or the other way round.

[Forge](https://github.com/mollendorff-ai/forge) plays it and gives exact expected payoffs, not samples. We checked them against the Python axelrod library, 500 seeded matches per pairing; it gives the same order at every noise level.

---

## The Results

| Mistakes | First | Second | GrimTrigger | Generous TitForTat |
|----------|-------|--------|-------------|--------------------|
| None | GrimTrigger 2.711 | TitForTat 2.606 | 1st | 4th |
| 1% | TitForTwoTats 2.378 | TitForTat 2.318 | 4th | 3rd |
| 5% | TitForTat 2.248 | TitForTwoTats 2.247 | 4th | 5th |
| 10% | GrimTrigger 2.278 | AlwaysDefect 2.276 | 1st | 6th |

Payoff per round, averaged over all seven opponents.

Four things happen, and only one of them is the prediction.

**Never forgiving is what falls apart.** Without mistakes GrimTrigger wins. With 1% it drops to 4th. One slip, by anyone, and it defects for the rest of the match, against friends as well as enemies.

**Forgiving a slip pays, while slips are rare.** At 1% TitForTwoTats wins. That part of the prediction holds.

**Tit-for-tat does not fall apart.** At 5% it and TitForTwoTats are level, 0.0006 apart. The axelrod library, sampling, puts them the other way round by 0.0004. Call it a tie.

**Forgiving everything does not pay.** Generous tit-for-tat, the strategy the prediction said would win, finishes 5th at 5%. It forgives AlwaysDefect and Random too, and they take what it gives.

And at 10%, the defectors win. Mistakes are so common that cooperation never runs long enough to pay off.

---

## Why the Textbook Disagrees

It doesn't, quite. Nowak and Sigmund's result is about a population evolving over generations: strategies that do badly become rarer, and once the exploiters have nobody left to exploit, generous tit-for-tat takes over.

A single round-robin is a different test. AlwaysDefect and Random are in it from start to finish, so a strategy that forgives everyone keeps paying for it. The evolving version, where strategies spread or die out, is parked for v0.7.0 and waits on Forge.

So the roadmap's prediction was not wrong about the world. It was wrong about this game. We kept the game and changed the prediction.

---

## Update: It Depends Who Else Plays

*Added in v0.6.0.*

Forge has two strategies this tournament left out: Pavlov (win-stay, lose-shift), the textbook answer to noise, and suspicious tit-for-tat, which opens by defecting and then copies. We added both and played it again with nine.

| Mistakes | First | Second | GrimTrigger | Generous TitForTat |
|----------|-------|--------|-------------|--------------------|
| None | TitForTwoTats 2.650 | TitForTat 2.638 | 4th | 3rd |
| 1% | TitForTwoTats 2.417 | Generous TitForTat 2.404 | 7th | 2nd |
| 5% | TitForTwoTats 2.283 | Pavlov 2.270 | 7th | 3rd |
| 10% | GrimTrigger 2.267 | AlwaysDefect 2.265 | 1st | 8th |

Two more players moved the answer more than the mistakes did. With nine players, GrimTrigger is 4th even without mistakes: suspicious tit-for-tat defects once, on the first move, and GrimTrigger never forgives it. A forgiving strategy, TitForTwoTats, now wins at 5% too, and generous tit-for-tat is 2nd at 1%. Pavlov comes 2nd at 5% and wins nowhere. At 10% the defectors still win.

So the table above is one roster's answer, not the answer. The axelrod library, playing the same nine, gives the same order at every level.

---

## What It Means for Kinship

The project's claim is that cooperation pays when you will meet again. This tournament adds a condition: you have to be able to tell a mistake from a defection.

- If you can't forgive at all, one error ends cooperation for good.
- If you forgive everything, whoever never cooperates exploits you.
- If errors are common, nobody cooperates long enough for it to pay.
- If you never forgive, one bad first impression is enough.

How much forgiveness pays depends on who else is playing and how noisy the channel is. For AIs and humans working together, that puts weight on something the earlier posts barely mentioned: clear signals. Saying "that was a mistake" and being believed is worth as much as the shadow of the future.

---

## The Other Three Games

v0.5.0 added three more. All three came out as the textbooks say:

- **When cooperation holds.** The threshold the project derives by formula, w\* = (T − c − R) / (T − P), is exactly where a tournament with random endings flips. A cost of conflict of 0.5 moves it from 0.5 to 0.375.
- **Audit the AI.** In an inspection game, a harsher penalty makes the human audit less, not the AI cheat less. Cheaper audits make it cheat less.
- **Whose conventions?** When a human and an AI each prefer their own norm, a cost of conflict hardly helps them meet. Picking a convention does.

They are written up in [docs/MORE_GAMES.md](https://github.com/mollendorff-ai/kinship-protocol/blob/main/docs/MORE_GAMES.md).

---

## Run It Yourself

```bash
cargo install mollendorff-forge --version 10.0.0-rc.31
forge game models/noisy_tournament.yaml
forge game models/noisy_tournament.yaml --scenario careful
forge game models/noisy_tournament.yaml --scenario careless
```

The model is [models/noisy_tournament.yaml](https://github.com/mollendorff-ai/kinship-protocol/blob/main/models/noisy_tournament.yaml). CI checks every number above on each change.

If your tournament comes out differently, share your roster. That is the point.
