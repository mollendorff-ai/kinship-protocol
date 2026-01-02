# Changelog

All notable findings and releases for the Kinship Protocol project.

## [Unreleased]

*Consolidation phase — assessing findings before next milestone.*

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
```
w* = (T - c - R) / (T - P)
```

**Critical Cost:**
```
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
