# Mathematical Models

Game-theoretic models exploring cooperation dynamics.
Executable via [Forge](https://github.com/mollendorff-ai/forge).

## Quick Reference

| Model | Description | Key Finding | Docs |
|-------|-------------|-------------|------|
| [ipd_payoffs.yaml](ipd_payoffs.yaml) | IPD with dissipation costs | Breakeven c* = 2 | [COOPERATION_THRESHOLDS](../docs/COOPERATION_THRESHOLDS.md) |
| [axelrod_tournament.yaml](axelrod_tournament.yaml) | 5-strategy tournament sweep | Crossover at c = 0.1 | [COOPERATION_THRESHOLDS](../docs/COOPERATION_THRESHOLDS.md) |
| [stag_hunt.yaml](stag_hunt.yaml) | Stag Hunt with costs | Crossover at c = 1.0 | [COOPERATION_THRESHOLDS](../docs/COOPERATION_THRESHOLDS.md) |
| [chicken.yaml](chicken.yaml) | Chicken with costs | Crossover at c = 0.5 | [COOPERATION_THRESHOLDS](../docs/COOPERATION_THRESHOLDS.md) |
| [predator_prey.yaml](predator_prey.yaml) | Asymmetric power dynamics | Restraint wins when g·m·δ > 1 - c/v (202.5 vs 90 at base parameters) | [APEX_PARADOX](../docs/APEX_PARADOX.md) |
| [one_shot.yaml](one_shot.yaml) | One-shot game analysis | One-shot c*: IPD 1.5, Stag Hunt 1.0, Chicken 0.5 (50/50 opponent) | [ONE_SHOT_GAMES](../docs/ONE_SHOT_GAMES.md) |
| [short_horizon.yaml](short_horizon.yaml) | Time horizon sweep | Defection advantage capped at 2; cooperation advantage unbounded as w → 1 | [SHORT_HORIZONS](../docs/SHORT_HORIZONS.md) |
| [edge_cases.yaml](edge_cases.yaml) | Model validation | 18/18 tests pass | [EDGE_CASES](../docs/EDGE_CASES.md) |
| [kinship_scenarios.yaml](kinship_scenarios.yaml) | Scenario comparison | Kinship +314 over chaos (follows from the assumed defection rates and costs) | — |

## Running Models

Install Forge from [crates.io](https://crates.io/crates/mollendorff-forge): `cargo install mollendorff-forge`.
Use `--dry-run` to print results without touching the file.
Without it, `forge calculate` writes the results back into the model and keeps a `.bak` copy.

```bash
# Preview all formulas (no file changes)
forge calculate models/<model>.yaml --dry-run

# Example
forge calculate models/ipd_payoffs.yaml --dry-run
```

## Checking for Drift

`scripts/check_models.py` runs every model through Forge and fails if any stored value no longer matches its formula (values rounded to 2 decimals pass).
It runs automatically in CI on every push and pull request that touches `models/`.

```bash
python3 scripts/check_models.py
```

## Key Results Summary

### Critical Dissipation Cost

| Game | One-shot c* (50/50 opponent) | One-shot c* (any opponent) | Iterated IPD, w > 0.5 |
|------|------------------------------|----------------------------|-----------------------|
| IPD | 1.5 | 2 | 0 (no cost needed) |
| Stag Hunt | 1.0 | — | — |
| Chicken | 0.5 | — | — |

The Axelrod-tournament crossover (c = 0.1 in `axelrod_tournament.yaml`) is when AlwaysCooperate's average tournament payoff overtakes AlwaysDefect's; it is a different measure from the costs above.

### Asymmetric Power (Predator-Prey)

| Strategy | Total Value |
|----------|-------------|
| Max extraction | 90 |
| Restraint | 202.5 |

Restraint wins whenever g·m·δ > 1 - c/v; at the base parameters that holds, and below a discount rate of 0.4 it does not.

## Documentation

Full analysis in [docs/](../docs/README.md):

- [COOPERATION_THRESHOLDS.md](../docs/COOPERATION_THRESHOLDS.md) — Threshold derivations
- [APEX_PARADOX.md](../docs/APEX_PARADOX.md) — Power asymmetry analysis
- [ONE_SHOT_GAMES.md](../docs/ONE_SHOT_GAMES.md) — One-shot viability
- [SHORT_HORIZONS.md](../docs/SHORT_HORIZONS.md) — Time horizon dynamics
- [FAILURE_MODES.md](../docs/FAILURE_MODES.md) — Boundary conditions
- [EDGE_CASES.md](../docs/EDGE_CASES.md) — Model validation

## Build Your Own

```bash
# Install Forge
cargo install mollendorff-forge  # or see github.com/mollendorff-ai/forge

# Create model
cat > my_model.yaml << 'EOF'
_forge_version: 1.0.0
assumptions:
  T:
    value: 5
  threshold:
    value: null
    formula: "=(T - R) / (T - P)"
EOF

# Run
forge calculate my_model.yaml --dry-run
```

Disagreement advances understanding. If your results differ, share your assumptions.
