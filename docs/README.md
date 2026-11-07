# Technical Documentation

Research notes and analysis for the Kinship Protocol project.

## Index

### Cooperation Thresholds

**[COOPERATION_THRESHOLDS.md](COOPERATION_THRESHOLDS.md)**

Closed-form expressions for cooperation thresholds in iterated games with dissipation costs. Derives `w* = (T - c - R) / (T - P)` and critical cost `c* = T - R`. Extended to Stag Hunt and Chicken games in v1.1.

**Key result:** Cooperation threshold decreases monotonically with dissipation cost.

---

### The Apex Paradox

**[APEX_PARADOX.md](APEX_PARADOX.md)**

Why power doesn't imply extraction. Models predator-prey dynamics with option value to explain apex predator restraint. Under the base parameters restraint scores 202.5 against 90 for maximum extraction; with a discount rate below 0.4, extraction wins.

**Key result:** Power asymmetry doesn't predict defection. Discount rate and option value matter more.

---

### One-Shot Games

**[ONE_SHOT_GAMES.md](ONE_SHOT_GAMES.md)**

Cooperation without a future. Analyzes when one-shot games (w=0) can support cooperation. One-shot IPD needs a dissipation cost of 1.5 (against a 50/50 opponent) or 2 (against anyone); Stag Hunt needs 1.0 and Chicken 0.5.

**Key result:** Game structure matters more than iteration. Frame existential scenarios as Chicken, not IPD.

---

### Short Horizons

**[SHORT_HORIZONS.md](SHORT_HORIZONS.md)**

The shadow of the future. Maps cooperation dynamics as time horizons shorten. Finds the defection advantage at short horizons is capped at 2, while the cooperation advantage grows without bound as w → 1.

**Key result:** Horizon extension is high leverage. Any intervention that extends time horizons disproportionately favors cooperation.

---

### Failure Modes

**[FAILURE_MODES.md](FAILURE_MODES.md)**

Where cooperation breaks. Comprehensive taxonomy of seven failure modes with diagnostic criteria and mitigations. Synthesizes boundary conditions from all previous work.

**Key result:** The theory specifies where it fails—short horizons, one-shot IPD, low discount, no option value, zero costs, terminal rounds, anonymity.

---

### Edge Cases

**[EDGE_CASES.md](EDGE_CASES.md)**

Model validation across 18 edge cases. Tests extreme values, boundary conditions, degenerate games, and numerical stability.

**Key result:** All 18 tests pass. Models are robust across the parameter space.

---

## Quick Reference

| Document | Topic | Key Finding |
|----------|-------|-------------|
| COOPERATION_THRESHOLDS | IPD + multi-game thresholds | `c ≥ max(T - R, P - S)` makes cooperation dominant |
| APEX_PARADOX | Asymmetric power dynamics | Restraint > extraction under uncertainty |
| ONE_SHOT_GAMES | One-shot viability | Chicken enables one-shot cooperation |
| SHORT_HORIZONS | Time horizon dynamics | Defection advantage capped; cooperation advantage unbounded as w → 1 |
| FAILURE_MODES | Boundary conditions | 7 failure modes with diagnostics and mitigations |
| EDGE_CASES | Model validation | 18/18 tests pass, models robust |

## Related

- [models/README.md](../models/README.md) — Forge model quick reference
- [research/GAME_THEORY.md](../research/GAME_THEORY.md) — Theoretical framework
- [research/THESIS.md](../research/THESIS.md) — Core hypothesis
