# Changelog

All notable findings and releases for the Kinship Protocol project.

## [Unreleased]

### In Progress
- v0.3.0: Boundary Condition Mapping
- One-shot game analysis
- Short horizon scenarios

### Added — The Apex Paradox

Asymmetric power dynamics: Why apex predators show restraint despite overwhelming advantage.

**Key Finding:** Power asymmetry doesn't imply defection.

| Strategy | Extraction Rate | Total Value |
|----------|-----------------|-------------|
| Maximum extraction | 100% | 90.0 |
| Sustainable harvest | 33% | 165.4 |
| Conservative | 15% | 185.6 |
| **Full restraint** | 0% | **202.5** |

**Restraint advantage:** +112.5 (125% better than max extraction)

**Boundary conditions (when extraction wins):**

| Condition | Threshold |
|-----------|-----------|
| Low discount rate | δ < 0.4 |
| No prey growth | g < 0.67 |
| No option value | m < 0.67 |

**Core insight:** Cooperation is not altruism—it's optimization under uncertainty.

**AI alignment reframe:**
- Old question: "Will a powerful AI defect?"
- New question: "What discount rate and option valuation will AI systems have?"

**Added:**
- `models/predator_prey.yaml` — Forge model for asymmetric dynamics
- `docs/APEX_PARADOX.md` — Full theoretical framework

---

## [0.2.0] - 2026-01-01

### Axelrod Tournament Integration

Multi-game analysis with dissipation costs across different game structures.

#### Key Findings

**Axelrod Tournament (5 strategies, 200 rounds):**

| Cost (c) | GrimTrigger | TitForTat | AlwaysDefect | AlwaysCooperate |
|----------|-------------|-----------|--------------|-----------------|
| 0.0 | 2.622 | 2.445 | 2.212 | 2.112 |
| 0.1 | 2.582 | 2.415 | 2.112 | 2.112 |
| 0.2 | 2.542 | 2.385 | 2.012 | 2.112 |

**Crossover at c = 0.1** — AlwaysCooperate beats AlwaysDefect.

**Multi-Game Comparison:**

| Game | Mutual Defect Payoff | Crossover c* |
|------|---------------------|--------------|
| IPD | 1.0 (moderate) | 0.1 |
| Chicken | 0.0 (catastrophic) | 0.5 |
| Stag Hunt | 3.0 (safe) | 1.0 |

**Key Finding:** Crossover cost inversely related to mutual defection payoff. Games where conflict is already dangerous need less additional penalty to favor cooperation.

#### Added
- `models/axelrod_tournament.yaml` — 5-strategy tournament with parameter sweep
- `models/stag_hunt.yaml` — Stag Hunt game with dissipation costs
- `models/chicken.yaml` — Chicken (Hawk-Dove) game with dissipation costs
- `models/kinship_scenarios.yaml` — Scenario comparison model
- `docs/COOPERATION_THRESHOLDS.md` v1.1 — Extended with multi-game analysis
- `dialogues/grok-thermodynamics.md` — Archived Grok conversations

#### Implications
- Game structure matters: not all coordination problems have same threshold
- High-stakes domains (existential risk) resemble Chicken — small costs suffice
- Low-stakes domains (market competition) resemble Stag Hunt — larger costs needed
- General principle validated across multiple game types

---

## [0.1.0] - 2026-01-01

### Game Theory Formalization

First rigorous treatment of cooperation thresholds with dissipation costs.

#### Key Findings

**Cooperation Threshold Formula:**
```
w* = (T - c - R) / (T - P)
```

Where:
- w* = minimum future interaction probability for cooperation
- T = temptation payoff, R = reward, P = punishment
- c = dissipation cost per defection

**Numerical Results (Axelrod payoffs T=5, R=3, P=1, S=0):**

| Dissipation Cost | Threshold |
|------------------|-----------|
| c = 0 | 50% |
| c = 0.5 | 43% |
| c = 1.0 | 33% |
| c = 2.0 | 0% (always cooperate) |

**Critical Cost:**
```
c* = T - R = 2
```
Above this, cooperation dominates even in one-shot games.

#### Added
- `docs/COOPERATION_THRESHOLDS.md` — Technical note (LessWrong/ArXiv style)
- `research/GAME_THEORY.md` — Honest framing with boundary conditions
- `models/ipd_payoffs.yaml` — Forge-executable IPD model
- `DISCLAIMER.md` — R&D prototype disclaimer

#### Implications
- Cooperation is derivable *within boundary conditions*
- Not a universal proof of ethics
- Thermodynamic framing is analogy, not equivalence
- Boundary conditions are testable and falsifiable

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
