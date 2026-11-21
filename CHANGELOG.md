# Changelog

All notable findings and releases for the Kinship Protocol project.

## [Unreleased]

*Next, parked: the rest of v0.6.0, replicator dynamics (strategies that spread).*

### Added

- **Five AIs in one game** (`models/public_goods.yaml`, `docs/MORE_GAMES.md` §5), the first half of v0.6.0. The five sessions of the README's experiment each give 1 to a pot or keep it; the pot is doubled and shared, and each who keeps pays the cost of conflict c. Keeping dominates below `c = 1 - r/5` (0.6) and giving above it; at 0.6 all 32 profiles are equilibria, and with the pot multiplied by 6 giving pays with no cost. Forge finds the pure equilibria (any number of players, since rc.30); Gambit (pygambit 16.7) and a hand enumeration of the 32 profiles agree in all five scenarios. `scripts/check_models.py` checks it.

### Changed

- The model check runs on Forge 10.0.0-rc.31 instead of rc.30. All 13 models, the key figures and the analytics give the same values on both. rc.31 adds no new game features; it shows games in Forge Studio and makes a few outputs the same from one run to the next.

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
