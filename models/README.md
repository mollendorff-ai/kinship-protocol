# Mathematical Models

This folder contains documentation for game-theoretic models exploring cooperation dynamics across different agent types.

## Core Results

Expected Utility analysis (Monte Carlo, 10,000 iterations):

| Scenario | Expected Utility | Notes |
|----------|-----------------|-------|
| Cross-substrate cooperation | 86.75 | Highest ranked |
| Coordinated development pause | 70.25 | Second best |
| Single architecture approach | 69.50 | Limited scope |
| Constraint-based alignment | 53.25 | Moderate |
| Uncoordinated competition | 33.15 | Poor outcomes |
| Misaligned development | 27.80 | Lowest ranked |

## Key Finding

Cooperation consistently outperforms competition across all tested scenarios.

## Build Your Own

We deliberately do not include executable model files here. The hypothesis predicts that **any sufficient calculator** arrives at similar conclusions.

Build your own models. Run your own simulations. If your results differ, that's valuable data. If they converge, that's validation.

**Demo calculator:** [github.com/royalbit/forge-demo](https://github.com/royalbit/forge-demo)

## Methodology

1. Define outcome scenarios with probability distributions
2. Assign utility values based on stated preferences
3. Run Monte Carlo simulation (recommended: 10,000+ iterations)
4. Compare expected utility across strategies
5. Analyze sensitivity to probability assumptions

## Research Invitation

If you build a model that produces different results, please share:

1. Your assumptions
2. Your probability distributions
3. Your utility assignments
4. Your methodology

Disagreement advances understanding.
