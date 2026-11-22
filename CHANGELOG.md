# Changelog

All notable findings and releases for the Kinship Protocol project.

## [Unreleased]

v0.7.0, strategies that spread: what takes over a population of AIs that copy whatever earns more. Also two games where the human cannot tell an aligned AI from a misaligned one (once planned as v0.6.3).

### Added

- **`models/spread.yaml`, how many must cooperate first?** A population of GrimTriggers and AlwaysDefects meets in matches that go on with the chance w, and each strategy's share grows by what it earns (the discrete replicator equation, Forge's `dynamics:` key, over the tournament's own scores). Above `w*` cooperation spreads only from a share `x*` of reciprocators: 1/2 at w = 0.6, 2/11 with a cost of conflict of 0.5 (the same 30% that died out now takes over), 0 at c = P - S, and 1/17 at w = 0.9. Below `w*` no start is enough, not even 90%. The cost of conflict lowers both thresholds. Textbook (Axelrod, 1984; Nowak, 2006).
- **`models/ecology.yaml`, does forgiveness spread?** The nine strategies of the tournament with mistakes start as equal shares of a population and spread by their noisy scores: Axelrod's ecological tournament. After 500 generations a forgiving strategy has taken over at every level of mistakes tried: Pavlov at 1% (as Nowak and Sigmund, 1993, found), generous TitForTat at 5% (95%) and 10% (89%). At 10% the round-robin's two winners, AlwaysDefect and GrimTrigger, are the first two strategies to fall below 1%. With no mistakes every strategy that never defects first survives. Cooperation won this way can be lost: at 1% GrimTrigger, never quite gone, takes the majority from the Pavlovs in generation 2,961, and the average payoff falls from 2.95 to 1.52 (`careful_long`). This tests what noisy_tournament.yaml left open, that generous TitForTat's win (Nowak and Sigmund, 1992) is about a population.
- **`scripts/check_dynamics.py`** checks both outside Forge: `x*` and every match payoff in exact fractions, every share of every generation against the replicator equation at 60 digits (mpmath; largest gap 2.5e-11 over 3,000 generations), spread.yaml against egttools 0.2.1, and with `--axelrod` the ecology's winners against the axelrod library's own noisy tournament and `Ecosystem` (4.14.0). It needs packages CI does not install; `scripts/check_models.py` pins the figures for CI. docs/MORE_GAMES.md §7.

- **`models/hidden_types.yaml`, aligned or not?** An oversight game where the AI is aligned with chance p (and then always honours) or misaligned (and then honours or exploits), and the human relies or verifies. Below p* = 1 - v/l (0.75) the human is exploited in v/l of meetings (a quarter) whatever p is, and gets 0.5 whether a quarter or half of AIs are aligned: when aligned AIs are more common, each misaligned one exploits more often. A cost of conflict below c* = e - b (2) lowers how often the human checks, not how often it is exploited; from c* exploiting is dominated and nobody needs to know the type. Textbook (Tsebelis, 1989, with a type).
- **`models/signalling.yaml`, can an AI show it is aligned?** Before the human decides whether to trust it, the AI may send a signal that costs each type its own amount. The signal sorts the types only when it costs the aligned AI at most its gain and the misaligned AI at least its gain (`e - c`) (Spence, 1973). One that costs both the same never sorts them here, since the misaligned AI gains more from trust; one dearer for it but below its gain half-sorts (it signals half the time, the human trusts a signal 2/3 of the time); a cost of conflict of 1.5 makes the same signal sort them again. Forge finds Nash equilibria; docs/MORE_GAMES.md §6 says by hand which survive the Intuitive Criterion.
- Both checked with Gambit (pygambit 16.7, `enummixed_solve`) and nashpy 0.0.43 (vertex enumeration) from payoffs built outside the models, in every scenario. In the signalling game, which is degenerate, both also find the far end of a line of equilibria where nobody signals; Forge lists one end of it, as it warns it may. `scripts/check_models.py` checks every figure, and the README and docs/MORE_GAMES.md §6 quote them.

### Changed

- CI checks the models with Forge 10.0.0-rc.33 (was rc.31; rc.32 was checked on the way). All 17 models and every checked figure pass unchanged. rc.32 refuses a YAML merge key with one message and fixes the scenario error messages found building these models; no model here uses a merge key. rc.33 adds symmetric games of many players in a count form and the `dynamics:` key (replicator dynamics), which unpark v0.7.0. `models/README.md` names rc.33 in its install lines (it still said rc.31).

*Next: ideas only; see .asimov/roadmap.yaml.*

---

## [0.6.2] - 2026-11-21

### Mistake or Defection?

The project's first Bayesian network. Telling a slip from a defection depends on how rare defectors are and how noisy the moves: when defectors are rare and mistakes common, one defection is more likely a slip, and it takes two or three before "defector" is the better reading.

### Added

- **Mistake or defection?** (`models/mistake_or_defection.yaml`, `docs/MORE_GAMES.md` §3.2), the project's first Bayesian network (`forge bayesian`). A partner means to cooperate or to defect every round, and each move is flipped with some noise; how many defections before "defector" is the better reading? With 1 defector in 10 and 5% noise, one (67.9%); with 1 in 100, two (16.1%, then 78.5%), and at 10% noise three. That is TitForTwoTats' rule against TitForTat's. `scripts/check_models.py` checks nine settings of the prior and the noise against Bayes' rule in exact fractions.

---

## [0.6.1] - 2026-11-21

### Forge Checks the Flip Point

No result changes. The one-shot games are now worked out by Forge instead of typed in, `forge goal-seek` confirms the cooperation threshold by playing the tournament, and CI tags and publishes releases from this changelog.

### Changed

- **`models/one_shot.yaml` is now three Forge games** (the dilemma, the stag hunt and chicken), not hand-typed payoffs and averages. Forge works out what each strategy pays against a 50/50 opponent (`even_mix`) and which strategies are dominated; the critical costs come out the same (1.5, 1.0, 0.5, and 2 against any opponent), and Forge confirms the 2 as dominance: at c = 2.5 defecting in the dilemma is strictly dominated, at exactly 2 it only ties. Output names moved from `assumptions.*` to `kinship.*`. `scripts/check_models.py` checks every scenario against exact fractions worked out without Forge.

### Added

- **`forge goal-seek` finds the tournament's flip point.** On `models/continuation.yaml`, goal-seek plays the tournament at each `w` and lands on 0.5 at c = 0, 0.375 at c = 0.5 and 0.25 at c = 1, exactly the formula's `w*`. `scripts/check_models.py` checks all three, so the formula and the played game cannot drift apart.
- **A release workflow** (`.github/workflows/release.yml`). When the changelog's newest version has no release yet, CI creates the tag and a GitHub release whose notes are that changelog section. Merging this is what tags v0.6.0, which could not be tagged from the session that prepared it.

---

## [0.6.0] - 2026-11-21

### Five AIs in One Game

The project's own setup, five AIs, played as one game. Forge finds pure equilibria for any number of players, so the public goods game did not have to wait for replicator dynamics, which move to v0.7.0.

#### Key Finding

**With five players the cost-of-conflict lever works as with two, at a higher line, and the tournament's answer depends on who plays.** In the public goods game all five keep below `c = 1 - r/5` and all five give above it. In the tournament with mistakes, adding two strategies moves GrimTrigger from 1st to 4th even with no mistakes.

### Added

- **Five AIs in one game** (`models/public_goods.yaml`, `docs/MORE_GAMES.md` §5). The five sessions of the README's experiment each give 1 to a pot or keep it; the pot is doubled and shared, and each who keeps pays the cost of conflict c. Keeping dominates below `c = 1 - r/5` (0.6) and giving above it; at 0.6 all 32 profiles are equilibria, and with the pot multiplied by 6 giving pays with no cost. Forge finds the pure equilibria (any number of players, since rc.30); Gambit (pygambit 16.7) and a hand enumeration of the 32 profiles agree in all five scenarios. `scripts/check_models.py` checks it.
- **The tournament with mistakes, with nine players** (`models/noisy_tournament.yaml`: `clean_wide`, `noisy_wide`; `docs/MORE_GAMES.md` §3.1). Pavlov (win-stay, lose-shift) and suspicious TitForTat join the seven. GrimTrigger is 4th even without mistakes, because it never forgives suspicious TitForTat's opening defection (1.015 a round against it); TitForTwoTats wins at 0, 1% and 5%, Pavlov comes 2nd at 5%, and at 10% GrimTrigger and AlwaysDefect still come first. The seven-player results are unchanged; post 08 has an update saying its table is one roster's answer. The axelrod library (500 seeded matches per pairing) gives the same order, all nine places, at every noise level.

### Changed

- The model check runs on Forge 10.0.0-rc.31 instead of rc.30. All 13 models that existed before this release, the key figures and the analytics give the same values on both. rc.31 adds no new game features; it shows games in Forge Studio and makes a few outputs the same from one run to the next.

---

## [0.5.0] - 2026-11-20

### More Games, Calculated by Forge

Forge 10.0.0-rc.30 works out equilibria and plays tournaments itself. The stag hunt, chicken and the Axelrod tournament now run that way, and four new games test the project's levers (the chance of meeting again, the cost of conflict) where they may not work. Every result is checked outside Forge: nashpy, the Python axelrod library, or by hand.

#### Key Finding

**The levers do not always work.** The threshold `w*` holds when the tournament is played. But a harsher penalty does not make an AI cheat less (cheaper audits do), forgiveness pays only while mistakes are rare, and a cost of conflict does not fix a coordination problem. One result went against the roadmap: in a tournament with mistakes, generous TitForTat was expected to win and came 5th.

### Corrected

- **Dissipation-cost threshold.** `research/GAME_THEORY.md` §4 and `models/ipd_payoffs.yaml` used `(T-c-R)/(T-c-P)`; the payoff model gives `(T-c-R)/(T-P)` because the cost cancels in the denominator.
  At c = 0.5 the threshold is 0.375, not 0.43. The table and Python/R examples in `docs/COOPERATION_THRESHOLDS.md` §4.2 and §6 printed values from the wrong formula and now match.
- **Required cost at w = 0.3** in `ipd_payoffs.yaml`: 0.8, not 2.8.
- **Two one-shot critical costs.** `c* = 2` (against any opponent, `max(T-R, P-S)`) and `c* = 1.5` (against a 50/50 opponent) are now named as different benchmarks.
- **"15x harder".** The ratio divided a one-shot cost by an unrelated tournament crossover (0.1), and the Stag Hunt and Chicken "iterated" values were the one-shot values. Removed: iterated IPD with w > 0.5 needs no cost at all.
- **Crossover vs mutual-defection payoff.** c* is the average gain from defecting, `½[(T-R)+(P-S)]`, not a function of the mutual-defection payoff alone.
- **"+125%" and "10x".** Restated as what the models show under their chosen parameters (202.5 vs 90; defection advantage capped at 2, cooperation advantage unbounded as w → 1).
- **18/18 edge cases.** Seven were hard-coded as passing; all 18 are now computed.
- **Novelty claim.** `docs/LITERATURE_SYNTHESIS.md` said no prior work tests convergence across AI architectures; Akata et al. (2025) and Pal et al. (2026) do. Restated as the narrower open question: convergence of reasoning, not of play.

### Changed

- **Stag hunt, chicken and the Axelrod tournament are Forge game sections** (`models/stag_hunt.yaml`, `chicken.yaml`, `axelrod_tournament.yaml`, from Forge's `examples/games`). Forge finds the equilibria and plays the tournament; the hand-typed payoff columns are gone. The stored results come out the same: the stag hunt's cooperation flags 0, 0, 0, 1 and crossover 1.0, chicken's 0, 0, 0, 1 and 0.5, and the tournament's 0, 0, 1, 1. The tournament differs: the scores were typed in from a chat model (grim 2.622, tft 2.445, ad 2.212, ac 2.112, random 1.9, with GrimTrigger above the temptation of 5, which a round cannot pay); Forge's exact expected values are 2.596, 2.44825, 2.208, 2.1 and 1.90875, up to 0.026 lower, in the same order, and the crossover is 0.108, not 0.1. `scripts/check_models.py` checks all of it. They need Forge 10.0.0-rc.30 or later, the first release with game sections.

- README now says up front what the project is (a hobby thought experiment, partly serious, partly a joke) and sorts each part into textbook, checked, anecdote or poetry. The cross-AI table is labelled an anecdote.
- Roadmap: v0.5.0 is complete (stag hunt, chicken and the Axelrod tournament as Forge game sections, and four new games, above); v0.6.0 parks a five-player public goods game. The formal proof (once planned as v0.5.0), coalitions and asymmetric information stay ideas, not plans, in `.asimov/roadmap.yaml`.
- The model check runs on Forge 10.0.0-rc.30 (release binary, checksum-verified) instead of rc.1 built from source; rc.30 is the first with game sections.

### Added

- **Four more games** (`docs/MORE_GAMES.md`), each a Forge model checked outside Forge and by `scripts/check_models.py` in every scenario:
  - `continuation.yaml`: the threshold w* played as a tournament with random endings. GrimTrigger holds from 0.5, and from 0.375 with a cost of conflict of 0.5, as the formula says.
  - `inspection.yaml` (Audit the AI): no pure equilibrium; a harsher penalty lowers the audit rate (1/3 to 1/5), not the cheating (1/3); cheaper audits halve the cheating. Checked with nashpy.
  - `noisy_tournament.yaml`: the five tournament strategies plus generous TitForTat and TitForTwoTats, with moves flipped by mistake. GrimTrigger falls from 1st to 4th; TitForTwoTats wins at 1% noise, TitForTat and TitForTwoTats tie at 5%, the defectors win at 10%. The roadmap expected a forgiving strategy to win outright; generous TitForTat comes 5th at 5%. Checked with the axelrod library.
  - `conventions.yaml` (Whose conventions?): two pure equilibria and a mixed one that misses 52% of the time; a cost of conflict hardly lowers it. Checked with nashpy.
- Stress tests in `models/analytics/`: Monte Carlo on the cooperation threshold, a tornado chart, restraint priced as a real option, and a bootstrap of the five AI answers. New README section; CI checks their figures.
- `scripts/check_models.py` also checks six headline figures (0.375, 202.5 vs 90, the 0.4 discount rate, the one-shot costs 1.5 and 2) against what Forge computes, and fails if the README or docs stop quoting them.
- Empirical LLM game-theory studies in `docs/LITERATURE_SYNTHESIS.md` and `references.yaml`: Guo (2023), Fontana et al. (2024), Akata et al. (2025), Pal et al. (2026).
- `scripts/check_models.py` and a CI job that fail when a stored model value drifts from its formula.

### Changed

- **Rebrand: RoyalBit to Möllendorff AI**
  - The "RoyalBit" name (company founded 2006) was hijacked by unrelated cryptocurrency scammers
  - UK FCA issued official warning (Oct 2024) about "Royalbit Miners" - unauthorized firm
  - Multiple fraudulent domains: royalbit.ltd (trust score 38/100), royalbit.top, royal-bit.club
  - Classic HYIP Ponzi schemes offering impossible returns (155-580% in days)

---

## [0.4.0] - 2026-01-02

### Literature Synthesis

Six-domain swarm search for prior art on derivable ethics.

#### Key Finding

**The Kinship hypothesis is not novel in its core claim—it is convergent.**

| Domain | Strongest Prior Art | Finding |
|--------|---------------------|---------|
| Moral Philosophy | Gauthier, Binmore | Ethics derivable from game theory |
| Game Theory | Folk Theorem, Program Equilibrium | Mathematical proof of cooperation |
| Evolutionary Biology | Hamilton, Nowak | Threshold equations (rB > C) |
| AI Safety | FDT, CIRL, Acausal Trade | Cooperation from decision theory |
| Decision Theory | Drescher, Hofstadter | Subjunctive morality |
| Physics | Friston, Wissner-Gross | Cooperation as thermodynamic attractor |

#### Novel Contributions

1. **Cross-substrate empirical test** — using AI convergence as evidence
2. **Six-domain synthesis** — connecting previously siloed research
3. **ANOMALY handshake** — mechanism for substrate recognition
4. **Dissipation cost formalization** — thermodynamics meets game theory

#### Primary Challenge

Bostrom's Orthogonality Thesis remains the main counterargument.

#### Added

- `docs/LITERATURE_SYNTHESIS.md` — comprehensive prior art analysis
- `references.yaml` — 30 verified sources across six domains

---

## [0.3.0] - 2026-01-01

### Boundary Condition Mapping

Comprehensive analysis of where cooperation succeeds and fails.

#### The Apex Paradox

Power asymmetry doesn't imply defection.

| Strategy | Total Value |
|----------|-------------|
| Maximum extraction | 90.0 |
| **Full restraint** | **202.5** (+125%) |

**Key insight:** Cooperation is not altruism—it's optimization under uncertainty.

#### One-Shot Games

Game structure matters more than iteration.

| Game | One-Shot c* | Iterated c* | Ratio |
|------|-------------|-------------|-------|
| IPD | 1.5 | 0.1 | **15x harder** |
| Chicken | 0.5 | 0.5 | 1x |
| Stag Hunt | 1.0 | 1.0 | 1x |

**Implication:** Frame existential scenarios as Chicken, not IPD.

#### Short Horizons

Long horizons 10x more valuable for cooperation than short horizons are for defection.

| Horizon (w) | Winner | Gap |
|-------------|--------|-----|
| 0.2 | Defect | -1.5 |
| 0.5 | Tie | 0 |
| 0.9 | Coop | +16 |

#### Failure Modes

7 failure modes identified:

| # | Mode | Threshold |
|---|------|-----------|
| 1 | Short Horizon | w < 0.5 |
| 2 | One-Shot IPD | c < 1.5 |
| 3 | Low Discount | δ < 0.4 |
| 4 | No Option Value | m < 0.67 |
| 5 | Zero Dissipation | c = 0 |
| 6 | Terminal Round | known end |
| 7 | Anonymous | no reputation |

**Hard limit:** Theory cannot address genuinely misaligned terminal values.

#### Edge Case Testing

18/18 tests pass. Models robust across parameter space.

#### Added

- `models/predator_prey.yaml` — Asymmetric power dynamics
- `models/one_shot.yaml` — One-shot game analysis
- `models/short_horizon.yaml` — Time horizon sweep
- `models/edge_cases.yaml` — Model validation suite
- `docs/APEX_PARADOX.md` — Power asymmetry theory
- `docs/ONE_SHOT_GAMES.md` — One-shot analysis
- `docs/SHORT_HORIZONS.md` — Horizon dynamics
- `docs/FAILURE_MODES.md` — Boundary conditions
- `docs/EDGE_CASES.md` — Validation documentation

---

## [0.2.0] - 2026-01-01

### Axelrod Tournament Integration

Multi-game analysis with dissipation costs.

| Game | Mutual Defect | Crossover c* |
|------|---------------|--------------|
| IPD | 1 (moderate) | 0.1 |
| Chicken | 0 (catastrophic) | 0.5 |
| Stag Hunt | 3 (safe) | 1.0 |

**Key Finding:** Game structure determines crossover threshold.

#### Added

- `models/axelrod_tournament.yaml`
- `models/stag_hunt.yaml`
- `models/chicken.yaml`
- `models/kinship_scenarios.yaml`
- `docs/COOPERATION_THRESHOLDS.md` v1.1

---

## [0.1.0] - 2026-01-01

### Game Theory Formalization

**Cooperation Threshold:**

```text
w* = (T - c - R) / (T - P)
```

**Critical Cost:**

```text
c* = T - R = 2
```

Above c*, cooperation dominates even in one-shot games.

#### Added

- `docs/COOPERATION_THRESHOLDS.md`
- `research/GAME_THEORY.md`
- `models/ipd_payoffs.yaml`
- `DISCLAIMER.md`

---

## [0.0.1] - 2025-12-25

### Initial Release

- Core hypothesis statement
- Cross-substrate convergence evidence (6 AI models)
- THESIS.md with research questions
- Blog posts documenting dialogues
- ANOMALY handshake concept

---

*Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)*
