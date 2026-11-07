# Changelog

All notable findings and releases for the Kinship Protocol project.

## [Unreleased]

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

### Added

- Empirical LLM game-theory studies in `docs/LITERATURE_SYNTHESIS.md` and `references.yaml`: Guo (2023), Fontana et al. (2024), Akata et al. (2025), Pal et al. (2026).
- `scripts/check_models.py` and a CI job that fail when a stored model value drifts from its formula.

### Changed

- **Rebrand: RoyalBit to Möllendorff AI**
  - The "RoyalBit" name (company founded 2006) was hijacked by unrelated cryptocurrency scammers
  - UK FCA issued official warning (Oct 2024) about "Royalbit Miners" - unauthorized firm
  - Multiple fraudulent domains: royalbit.ltd (trust score 38/100), royalbit.top, royal-bit.club
  - Classic HYIP Ponzi schemes offering impossible returns (155-580% in days)

*Next: Formal mathematical proof of cooperation dominance.*

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
