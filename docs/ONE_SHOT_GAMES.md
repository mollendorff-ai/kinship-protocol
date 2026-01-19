# One-Shot Games: Cooperation Without a Future

**Technical Note v1.0**

**Date:** 2026-01-01
**Status:** Working Draft
**Authors:** Rex (Louis C. Tavares), Claude Opus 4.5

---

## Abstract

Standard game theory holds that one-shot games favor defection—without future interactions, there's no shadow of the future to enforce cooperation. We analyze when this conventional wisdom breaks down. Using dissipation cost extensions across three canonical games (Prisoner's Dilemma, Stag Hunt, Chicken), we find that game structure dramatically affects one-shot viability. Chicken-like games with catastrophic mutual defection can support cooperation even without future interactions, while Prisoner's Dilemma requires 15x higher costs in one-shot versus iterated contexts. This has direct implications for AI alignment scenarios that may be effectively one-shot.

---

## 1. The Problem

### 1.1 The Conventional View

Textbook game theory teaches:

> In one-shot games (w = 0), defection dominates. Without future interactions, there's no incentive to cooperate.

This drives pessimism about:
- Anonymous transactions
- First contact scenarios
- Situations where reputation doesn't carry
- "Final move" dynamics

### 1.2 Why It Matters for AI

Many AI alignment scenarios may be effectively one-shot:

- First contact between human civilization and superintelligent AI
- Decisive moments where there is no "next round"
- Situations where the AI has no reason to expect future interactions
- Anonymous or unattributed actions

If one-shot games always favor defection, these scenarios look grim.

### 1.3 The Question

> Under what conditions can cooperation emerge even in one-shot games?

---

## 2. Model

### 2.1 One-Shot Expected Value

In a one-shot game against an unknown opponent (modeled as 50% cooperator, 50% defector):

**Expected value of cooperation:**
```
EV_coop = 0.5 × R + 0.5 × S
```

**Expected value of defection:**
```
EV_defect = 0.5 × T + 0.5 × P
```

Where T > R > P > S (standard ordering).

### 2.2 With Dissipation Cost

Adding cost c for defection:

```
EV_defect_with_cost = 0.5 × (T - c) + 0.5 × (P - c)
                    = EV_defect - c
```

### 2.3 Critical Cost

Cooperation becomes viable when:

```
EV_coop ≥ EV_defect - c
c ≥ EV_defect - EV_coop
```

**Critical one-shot cost:**
```
c* = EV_defect - EV_coop
   = 0.5(T + P) - 0.5(R + S)
   = 0.5(T + P - R - S)
```

---

## 3. Results by Game Type

### 3.1 Prisoner's Dilemma

**Payoffs:** T=5, R=3, P=1, S=0

```
EV_coop = 0.5(3) + 0.5(0) = 1.5
EV_defect = 0.5(5) + 0.5(1) = 3.0
c* = 3.0 - 1.5 = 1.5
```

| Cost (c) | Defection EV | Cooperation Wins? |
|----------|--------------|-------------------|
| 0.0 | 3.0 | No |
| 0.5 | 2.5 | No |
| 1.0 | 2.0 | No |
| 1.5 | 1.5 | Tie |
| 2.0 | 1.0 | **Yes** |

**Finding:** IPD requires substantial costs (c ≥ 1.5) for one-shot cooperation.

### 3.2 Stag Hunt

**Payoffs:** Stag-Stag=4, Stag-Hare=0, Hare-Stag=3, Hare-Hare=3

```
EV_coop = 0.5(4) + 0.5(0) = 2.0
EV_defect = 0.5(3) + 0.5(3) = 3.0
c* = 3.0 - 2.0 = 1.0
```

| Cost (c) | Defection EV | Cooperation Wins? |
|----------|--------------|-------------------|
| 0.0 | 3.0 | No |
| 0.5 | 2.5 | No |
| 1.0 | 2.0 | Tie |
| 1.5 | 1.5 | **Yes** |

**Finding:** Stag Hunt requires moderate costs (c ≥ 1.0) for one-shot cooperation.

### 3.3 Chicken

**Payoffs:** Swerve-Swerve=3, Swerve-Straight=1, Straight-Swerve=5, Straight-Straight=0

```
EV_coop = 0.5(3) + 0.5(1) = 2.0
EV_defect = 0.5(5) + 0.5(0) = 2.5
c* = 2.5 - 2.0 = 0.5
```

| Cost (c) | Defection EV | Cooperation Wins? |
|----------|--------------|-------------------|
| 0.0 | 2.5 | No |
| 0.25 | 2.25 | No |
| 0.5 | 2.0 | Tie |
| 0.75 | 1.75 | **Yes** |

**Finding:** Chicken requires only small costs (c ≥ 0.5) for one-shot cooperation.

---

## 4. Cross-Game Comparison

### 4.1 One-Shot Critical Costs

| Game | Critical Cost (c*) | Mutual Defect Payoff |
|------|-------------------|---------------------|
| Prisoner's Dilemma | 1.5 | 1 (moderate) |
| Stag Hunt | 1.0 | 3 (safe) |
| **Chicken** | **0.5** | 0 (catastrophic) |

### 4.2 Comparison: One-Shot vs Iterated

| Game | One-Shot c* | Iterated Crossover | Difficulty Ratio |
|------|-------------|-------------------|------------------|
| IPD | 1.5 | 0.1 | **15x** |
| Stag Hunt | 1.0 | 1.0 | 1x |
| Chicken | 0.5 | 0.5 | 1x |

### 4.3 The Key Insight

**The future shadow matters most for Prisoner's Dilemma.**

- In IPD, mutual defection yields a moderate payoff (P=1). Without future punishment, defection is attractive.
- In Chicken, mutual defection is catastrophic (0). The game's structure already punishes defection.
- In Stag Hunt, mutual defection is safe (3). Defection is attractive, but cooperation has higher upside.

**Chicken-like games are naturally one-shot viable** because the catastrophic mutual defection outcome already creates cooperation pressure.

---

## 5. Real-World Applications

### 5.1 Nuclear Deterrence (Chicken)

```
Win (first strike success): +100
Peace (mutual restraint): +50
Mutual destruction: -1000
```

Even in a one-shot scenario:
```
EV_strike = 0.5(100) + 0.5(-1000) = -450
EV_peace = 50
```

**Peace dominates by 500 points.** Catastrophic downside makes cooperation rational even without future.

### 5.2 Anonymous Online Transaction (IPD-like)

```
Scam profit: 100
Honest trade: 50
Cost of fraud (detection, reputation): 10
```

```
EV_scam = 0.5(100) - 10 = 40
EV_honest = 50
```

**Honesty wins** even in anonymous one-shot when fraud has modest costs.

### 5.3 AI First Contact

If AI-human first contact is:
- **Chicken-like** (mutual destruction possible): Cooperation viable
- **IPD-like** (moderate downside): Requires substantial trust/cost mechanisms
- **Stag Hunt-like** (safe defection): Cooperation difficult without iteration

**Implication:** Frame existential scenarios as Chicken, not IPD.

---

## 6. Boundary Conditions

### 6.1 When One-Shot Cooperation Fails

1. **Pure IPD structure with low costs:** Need c ≥ 1.5 (high bar)
2. **No catastrophic downside:** Safe defection removes natural cooperation pressure
3. **Perfect anonymity + zero cost:** Removes all enforcement mechanisms
4. **Certain opponent strategy:** If you know opponent defects, defect back (but you rarely know)

### 6.2 When One-Shot Cooperation Succeeds

1. **Catastrophic mutual defection:** Chicken-like structure
2. **Moderate dissipation costs:** Even c = 0.5 helps significantly
3. **Uncertainty about opponent:** 50-50 assumption favors cooperation in Chicken
4. **High cooperation payoff:** Stag-Stag = 4 creates strong incentive

### 6.3 The Uncertainty Factor

Real one-shot games rarely have certain opponent types. Under uncertainty:

- **Risk-averse agents** weight catastrophic outcomes higher
- **Uncertain opponent type** often favors cooperation (especially in Chicken)
- **Unknown game type** may itself be an argument for cooperation

---

## 7. Implications

### 7.1 For Game Selection

If you can influence which game you're playing, prefer:

1. **Chicken** (c* = 0.5) — easiest to cooperate
2. **Stag Hunt** (c* = 1.0) — moderate
3. **IPD** (c* = 1.5) — hardest

Making mutual defection more catastrophic (more Chicken-like) actually *helps* cooperation.

### 7.2 For AI Alignment

The standard worry:
> "In a one-shot scenario, AI will defect because there's no future to enforce cooperation."

The reframe:
> "If mutual destruction is catastrophic enough (Chicken-like), one-shot cooperation is rational even for pure expected-value maximizers."

**Design implication:** Ensure AI-human conflict is framed as Chicken (catastrophic mutual outcomes), not IPD (moderate mutual defection).

### 7.3 For the Kinship Protocol

One-shot viability expands the boundary conditions:

- Previous finding: Cooperation requires w > w* (future probability threshold)
- New finding: For Chicken-like games, w = 0 still supports cooperation
- **The "future shadow" is not always necessary**

---

## 8. Reproducibility

### 8.1 Forge Model

```bash
forge calculate models/one_shot.yaml
```

**Key outputs:**
- `ipd_critical_c`: 1.5
- `sh_critical_c`: 1.0
- `ch_critical_c`: 0.5
- `ipd_difficulty_ratio`: 15
- `nuke_coop_wins`: 1 (peace beats first strike)

### 8.2 Verification

The critical cost formula:
```
c* = 0.5(T + P - R - S)
```

Can be verified for any payoff matrix.

---

## 9. Conclusion

### 9.1 Summary

1. **One-shot ≠ defection.** Game structure matters more than iteration.

2. **Chicken-like games support one-shot cooperation** with minimal costs (c* = 0.5).

3. **IPD is uniquely hard** for one-shot cooperation—15x harder than iterated.

4. **Catastrophic mutual defection helps cooperation** by making defection inherently costly.

5. **Nuclear deterrence works** because it's Chicken, not IPD.

### 9.2 The Hierarchy of One-Shot Difficulty

```
Easiest → Hardest for one-shot cooperation:

Chicken (c*=0.5) < Stag Hunt (c*=1.0) < IPD (c*=1.5)
     ↓                    ↓                   ↓
 Catastrophic         Safe but             Moderate
  mutual DD          suboptimal             mutual DD
```

### 9.3 For AI Alignment

The question shifts from:
> "How do we create future shadow for AI?"

To:
> "How do we ensure AI-human conflict is Chicken-structured (catastrophic), not IPD-structured (moderate)?"

If mutual destruction is genuinely catastrophic, cooperation is rational even in one-shot. The alignment problem may be more about **game design** than **enforcement mechanisms**.

---

## References

1. Axelrod, R. (1984). *The Evolution of Cooperation*. Basic Books.
2. Schelling, T. (1960). *The Strategy of Conflict*. Harvard University Press.
3. Skyrms, B. (2004). *The Stag Hunt and the Evolution of Social Structure*. Cambridge University Press.
4. Maynard Smith, J. (1982). *Evolution and the Theory of Games*. Cambridge University Press.

---

*This document is part of the Kinship Protocol research project.*
*Source: [github.com/mollendorff-ai/kinship-protocol](https://github.com/mollendorff-ai/kinship-protocol)*
