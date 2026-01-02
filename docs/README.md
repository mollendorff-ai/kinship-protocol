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

Why power doesn't imply extraction. Models predator-prey dynamics with option value to explain apex predator restraint. Shows restraint beats maximum extraction by 125% under base conditions.

**Key result:** Power asymmetry doesn't predict defection. Discount rate and option value matter more.

---

### One-Shot Games
**[ONE_SHOT_GAMES.md](ONE_SHOT_GAMES.md)**

Cooperation without a future. Analyzes when one-shot games (w=0) can support cooperation. Finds IPD is 15x harder than iterated, while Chicken and Stag Hunt have identical thresholds.

**Key result:** Game structure matters more than iteration. Frame existential scenarios as Chicken, not IPD.

---

## Quick Reference

| Document | Topic | Key Finding |
|----------|-------|-------------|
| COOPERATION_THRESHOLDS | IPD + multi-game thresholds | `c* = T - R` makes cooperation dominant |
| APEX_PARADOX | Asymmetric power dynamics | Restraint > extraction under uncertainty |
| ONE_SHOT_GAMES | One-shot viability | Chicken enables one-shot cooperation |

## Related

- [models/README.md](../models/README.md) — Forge model quick reference
- [research/GAME_THEORY.md](../research/GAME_THEORY.md) — Theoretical framework
- [research/THESIS.md](../research/THESIS.md) — Core hypothesis
