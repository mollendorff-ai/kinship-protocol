# Mathematical Models

Game-theoretic models exploring cooperation dynamics.
Executable via [Forge](https://github.com/mollendorff-ai/forge).

## Quick Reference

| Model | Description | Key Finding | Docs |
|-------|-------------|-------------|------|
| [ipd_payoffs.yaml](ipd_payoffs.yaml) | IPD with dissipation costs | Breakeven c* = 2 | [COOPERATION_THRESHOLDS](../docs/COOPERATION_THRESHOLDS.md) |
| [axelrod_tournament.yaml](axelrod_tournament.yaml) | 5-strategy tournament, played by Forge | Crossover at c = 0.108 (typed in as 0.1) | [COOPERATION_THRESHOLDS](../docs/COOPERATION_THRESHOLDS.md) |
| [stag_hunt.yaml](stag_hunt.yaml) | Stag Hunt with costs, equilibria found by Forge | Crossover at c = 1.0 | [COOPERATION_THRESHOLDS](../docs/COOPERATION_THRESHOLDS.md) |
| [chicken.yaml](chicken.yaml) | Chicken with costs, equilibria found by Forge | Crossover at c = 0.5 | [COOPERATION_THRESHOLDS](../docs/COOPERATION_THRESHOLDS.md) |
| [continuation.yaml](continuation.yaml) | Tournament with random endings | GrimTrigger holds from w* = 0.5 (0.375 with c = 0.5), as the formula says | [MORE_GAMES](../docs/MORE_GAMES.md) |
| [inspection.yaml](inspection.yaml) | Audit the AI (inspection game) | Harsher penalty: less auditing, same cheating (1/3); cheaper audits: cheating 1/6 | [MORE_GAMES](../docs/MORE_GAMES.md) |
| [noisy_tournament.yaml](noisy_tournament.yaml) | Seven strategies, moves flipped by mistake | GrimTrigger 1st → 4th; TitForTwoTats wins at 1% noise, defectors at 10% | [MORE_GAMES](../docs/MORE_GAMES.md) |
| [conventions.yaml](conventions.yaml) | Human and AI prefer different norms | Mixed play misses 52% of the time; a cost of conflict hardly helps | [MORE_GAMES](../docs/MORE_GAMES.md) |
| [public_goods.yaml](public_goods.yaml) | Five AIs give to a common pot or keep | All keep below c = 0.6, all give above it (`1 - r/5`); checked with Gambit | [MORE_GAMES](../docs/MORE_GAMES.md) |
| [predator_prey.yaml](predator_prey.yaml) | Asymmetric power dynamics | Restraint wins when g·m·δ > 1 - c/v (202.5 vs 90 at base parameters) | [APEX_PARADOX](../docs/APEX_PARADOX.md) |
| [one_shot.yaml](one_shot.yaml) | One-shot game analysis | One-shot c*: IPD 1.5, Stag Hunt 1.0, Chicken 0.5 (50/50 opponent) | [ONE_SHOT_GAMES](../docs/ONE_SHOT_GAMES.md) |
| [short_horizon.yaml](short_horizon.yaml) | Time horizon sweep | Defection advantage capped at 2; cooperation advantage unbounded as w → 1 | [SHORT_HORIZONS](../docs/SHORT_HORIZONS.md) |
| [edge_cases.yaml](edge_cases.yaml) | Model validation | 18/18 tests pass | [EDGE_CASES](../docs/EDGE_CASES.md) |
| [kinship_scenarios.yaml](kinship_scenarios.yaml) | Scenario comparison | Kinship +314 over chaos (follows from the assumed defection rates and costs) | — |

## Stress Tests (models/analytics/)

These use Forge's analysis commands instead of `forge calculate`. Each run is seeded, so the numbers repeat.

| Model | Command | Result |
|-------|---------|--------|
| [cooperation_monte_carlo.yaml](analytics/cooperation_monte_carlo.yaml) | `forge simulate` | Cooperation pays in 90.3% of 10,000 draws; the chance of meeting again is the biggest driver |
| [cooperation_tornado.yaml](analytics/cooperation_tornado.yaml) | `forge tornado` | Cost of conflict swings the threshold by 0.5, temptation by 0.33, reward by 0.25, punishment by 0.10 |
| [restraint_option.yaml](analytics/restraint_option.yaml) | `forge real-options` | The option to defect later adds 27.70 to restraint's 112.5 lead (American put, 100-step binomial tree) |
| [five_ais_bootstrap.yaml](analytics/five_ais_bootstrap.yaml) | `forge bootstrap` | Bootstrap interval 100% to 100%; exact 95% lower bound 47.8% |

Forge labels real-options values in dollars and years because it is a finance tool; here they are payoff units and rounds.
All four results were also recomputed independently in Python (NumPy, a separate binomial tree, SciPy's beta distribution) and agree.

## Running Models

Install Forge 10.0.0-rc.30 or later from [crates.io](https://crates.io/crates/mollendorff-forge): `cargo install mollendorff-forge --version 10.0.0-rc.31`.
Forge has no stable release yet, so cargo needs the `--version`. rc.30 is the first release with game sections, which the game models need; CI runs rc.31.
Use `--dry-run` to print results without touching the file.
Without it, `forge calculate` writes the results back into the model and keeps a `.bak` copy.

```bash
# Preview all formulas (no file changes)
forge calculate models/<model>.yaml --dry-run

# Example
forge calculate models/ipd_payoffs.yaml --dry-run
```

The game models (`stag_hunt.yaml`, `chicken.yaml`, `axelrod_tournament.yaml`, `continuation.yaml`, `inspection.yaml`, `noisy_tournament.yaml`, `conventions.yaml`) also run with `forge game`, which prints the equilibria or the tournament table. Each cost is a scenario:

```bash
forge game models/axelrod_tournament.yaml
forge game models/stag_hunt.yaml --scenario c3
forge tornado models/inspection.yaml   # which input moves the audit rate
```

## Checking for Drift

`scripts/check_models.py` runs every model through Forge and fails if any stored value no longer matches its formula (values rounded to 2 decimals pass). It also checks the headline figures quoted in the README and docs against Forge's output, including the stress-test figures, and the results of the v0.5.0 games in each scenario (each checked outside Forge with nashpy, the Python axelrod library, or by hand).
It runs automatically in CI on every push and pull request that touches `models/`, the README or `docs/`.

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

The Axelrod-tournament crossover (c = 0.108 in `axelrod_tournament.yaml`; the hand-typed table gave 0.1) is when AlwaysCooperate's average tournament payoff overtakes AlwaysDefect's; it is a different measure from the costs above.

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
cargo install mollendorff-forge --version 10.0.0-rc.31  # or see github.com/mollendorff-ai/forge

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
