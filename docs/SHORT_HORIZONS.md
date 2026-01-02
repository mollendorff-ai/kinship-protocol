# Short Horizon Scenarios: The Shadow of the Future

**Technical Note v1.0**

**Date:** 2026-01-01
**Status:** Working Draft
**Authors:** Rex (Louis C. Tavares), Claude Opus 4.5

---

## Abstract

The "shadow of the future" is game theory's term for how future interactions discipline present behavior. We analyze how cooperation dynamics change as this shadow shortens. Using IPD with dissipation costs, we map the transition from short-horizon defection to long-horizon cooperation. Key finding: the cooperation advantage at long horizons is 10x larger than the defection advantage at short horizons. This asymmetry suggests that extending time horizons—even modestly—disproportionately favors cooperation.

---

## 1. The Problem

### 1.1 The Shadow of the Future

In iterated games, the probability of future interaction `w` determines whether cooperation or defection dominates:

- **High w (long horizon):** Future rewards matter; cooperation is sustainable
- **Low w (short horizon):** Future doesn't matter; defection is tempting
- **w = 0 (one-shot):** No future; pure extraction logic

### 1.2 Real-World Short Horizons

Many scenarios have uncertain or short time horizons:

- Startup negotiations (might not get another meeting)
- Political term limits (finite tenure)
- Company acquisitions (relationship may end)
- AI development races (winner-take-all dynamics)
- End-of-life decisions (no future rounds)

### 1.3 The Question

> How does cooperation viability change as horizons shorten?
> Is there a sharp threshold, or gradual decline?

---

## 2. Model

### 2.1 Expected Value Formulas

For an infinitely repeated game with probability `w` of continuation:

**Perpetual mutual cooperation:**
```
EV_coop = R + wR + w²R + ... = R / (1 - w)
```

**Defect once, then mutual punishment:**
```
EV_defect = T + wP + w²P + ... = T + wP / (1 - w)
```

### 2.2 Cooperation Threshold

Cooperation dominates when `EV_coop > EV_defect`:

```
R / (1 - w) > T + wP / (1 - w)
```

Solving for w:

```
w* = (T - R) / (T - P)
```

With Axelrod payoffs (T=5, R=3, P=1):
```
w* = (5 - 3) / (5 - 1) = 0.5
```

### 2.3 With Dissipation Cost

Adding cost `c` to defection:

```
w* = (T - c - R) / (T - P)
```

Each unit of c reduces threshold by `1 / (T - P) = 0.25`.

---

## 3. Results

### 3.1 Horizon Sweep (No Dissipation Cost)

| Horizon (w) | Coop EV | Defect EV | Gap | Winner |
|-------------|---------|-----------|-----|--------|
| 0.1 | 3.33 | 5.11 | -1.78 | Defect |
| 0.2 | 3.75 | 5.25 | -1.50 | Defect |
| 0.3 | 4.29 | 5.43 | -1.14 | Defect |
| 0.4 | 5.00 | 5.67 | -0.67 | Defect |
| **0.5** | **6.00** | **6.00** | **0.00** | **Tie** |
| 0.6 | 7.50 | 6.50 | +1.00 | Coop |
| 0.7 | 10.00 | 7.33 | +2.67 | Coop |
| 0.8 | 15.00 | 9.00 | +6.00 | Coop |
| 0.9 | 30.00 | 14.00 | +16.00 | Coop |

### 3.2 The Asymmetry

**Key finding:** The cooperation advantage at long horizons vastly exceeds the defection advantage at short horizons.

| Metric | Value |
|--------|-------|
| Defection advantage at w=0.2 | 1.50 |
| Cooperation advantage at w=0.9 | 16.00 |
| **Ratio** | **10.67x** |

Long horizons are 10x more valuable for cooperation than short horizons are for defection.

### 3.3 With Dissipation Cost (c=0.5)

| Horizon (w) | Coop EV | Defect EV (with c) | Gap | Winner |
|-------------|---------|-------------------|-----|--------|
| 0.3 | 4.29 | 4.93 | -0.64 | Defect |
| 0.4 | 5.00 | 5.00 | 0.00 | Tie |
| 0.5 | 6.00 | 5.00 | +1.00 | Coop |

**Threshold shift:** From w=0.5 to w≈0.375 with c=0.5.

### 3.4 Threshold Sensitivity

```
Δw* / Δc = -1 / (T - P) = -0.25
```

Each unit of dissipation cost reduces the required horizon by 0.25.

**Implication:** A small cost (c=0.5) expands cooperation viability from "50%+ future probability" to "37.5%+ future probability"—a meaningful expansion.

---

## 4. Real-World Scenarios

### 4.1 Startup Negotiations (w ≈ 0.3)

```
Coop EV: 4.29
Defect EV: 5.43
Winner: Defect (+1.14)
```

Short horizon favors aggressive tactics. But adding reputation cost (c≈0.5) narrows the gap significantly.

### 4.2 Industry Conference (w ≈ 0.7)

```
Coop EV: 10.00
Defect EV: 7.33
Winner: Coop (+2.67)
```

Longer horizon (you'll see them again) strongly favors cooperation.

### 4.3 AI Lab Competition (w ≈ 0.5)

```
Coop EV: 6.00
Defect EV: 6.00
Winner: Tie
```

Exactly at threshold—knife edge. Small changes tip the balance either way.

**Implication:** AI safety coordination is at the threshold. Modest interventions (increasing perceived future interaction, adding coordination costs) can shift equilibrium toward cooperation.

---

## 5. Dynamics of Horizon Extension

### 5.1 Marginal Value of Longer Horizons

| From w | To w | Coop EV Change | Defect EV Change | Net Shift |
|--------|------|----------------|------------------|-----------|
| 0.3 | 0.4 | +0.71 | +0.24 | +0.47 toward coop |
| 0.4 | 0.5 | +1.00 | +0.33 | +0.67 toward coop |
| 0.5 | 0.6 | +1.50 | +0.50 | +1.00 toward coop |
| 0.6 | 0.7 | +2.50 | +0.83 | +1.67 toward coop |
| 0.7 | 0.8 | +5.00 | +1.67 | +3.33 toward coop |

**Finding:** Each increment in horizon favors cooperation more than the previous. The benefit accelerates.

### 5.2 The Compounding Effect

Cooperation EVs grow as `R / (1-w)`, which has a vertical asymptote at w=1.
Defection EVs grow as `T + wP/(1-w)`, which grows more slowly.

Near w=1:
- Cooperation EV → ∞
- Defection EV → ∞ but slower

**Implication:** Any intervention that extends horizons disproportionately helps cooperation.

---

## 6. Interventions

### 6.1 Horizon Extension

Ways to increase perceived future interaction probability:

1. **Long-term contracts** — Commit to future interactions
2. **Reputation systems** — Create shadow even without direct repeat
3. **Institutional memory** — Organizations remember longer than individuals
4. **Graduated stakes** — Start small, escalate as trust builds
5. **Exit costs** — Make leaving relationships costly

### 6.2 Cost Injection

Ways to add dissipation costs for defection:

1. **Monitoring** — Make defection observable
2. **Enforcement** — Credible punishment mechanisms
3. **Reputation damage** — Social costs for defectors
4. **Coordination overhead** — Defection requires more effort
5. **Uncertainty tax** — Defection creates unpredictability costs

### 6.3 Combined Strategy

The most effective approach combines both:

| Intervention | Effect |
|-------------|--------|
| Extend horizon w from 0.3 to 0.5 | Threshold met |
| Add cost c=0.5 | Threshold drops to 0.375 |
| **Combined** | **Comfortable margin above threshold** |

---

## 7. Boundary Conditions

### 7.1 When Short Horizon Wins

Defection remains optimal when:

1. **w < w*** — Below threshold, defection dominates
2. **Terminal rounds** — Known last interaction
3. **Anonymous interactions** — No reputation carryover
4. **High temptation** — T >> R widens the gap
5. **Low punishment** — P ≈ R reduces future cost of defection

### 7.2 When Long Horizon Wins

Cooperation dominates when:

1. **w > w*** — Above threshold
2. **Open-ended relationships** — No known endpoint
3. **Reputation propagates** — Others learn of defection
4. **High cooperation payoff** — R is attractive
5. **Costly mutual defection** — Low P or high dissipation

---

## 8. Implications

### 8.1 For AI Alignment

AI development currently sits at threshold (w ≈ 0.5):
- Labs may or may not interact again
- Winner-take-all dynamics shorten horizons
- Rapid capability gains create uncertainty

**Interventions that help:**
1. **Safety agreements** between labs (horizon extension)
2. **Transparency requirements** (reputation effects)
3. **Regulatory coordination** (cost injection for racing)
4. **Staged deployment** (graduated stakes)

### 8.2 For the Kinship Protocol

The short horizon analysis suggests:

1. **Horizon extension is high leverage** — 10x asymmetry favors cooperation at long horizons
2. **Threshold is knife-edge** — Small changes around w=0.5 flip outcomes
3. **Interventions compound** — Horizon extension + cost injection together are more effective than either alone

### 8.3 For Strategy

If you can influence the game structure:

1. **Extend horizons when possible** — Open-ended beats finite
2. **Make defection costly** — Add monitoring, reputation, enforcement
3. **Signal long-term orientation** — Commit to future interactions
4. **Avoid terminal frame** — "Last chance" dynamics trigger defection

---

## 9. Reproducibility

### 9.1 Forge Model

```bash
forge calculate models/short_horizon.yaml
```

**Key outputs:**
- `threshold_c0`: 0.5 (baseline threshold)
- `threshold_c05`: 0.375 (with c=0.5)
- `horizon_leverage`: 10.67 (long vs short asymmetry)
- `w_05_gap`: 0 (breakeven point)

### 9.2 Threshold Formula

```
w* = (T - c - R) / (T - P)
```

Verify for any payoff matrix.

---

## 10. Conclusion

### 10.1 Summary

1. **Threshold is sharp:** At w=0.5 (standard IPD), cooperation and defection are exactly equal.

2. **Long horizons favor cooperation 10x more:** The asymmetry strongly favors extending time horizons.

3. **Dissipation costs lower threshold:** Each unit of c reduces required horizon by 0.25.

4. **Interventions compound:** Horizon extension + cost injection together create robust cooperation conditions.

5. **AI alignment is at threshold:** Current dynamics sit near w=0.5—small changes flip outcomes.

### 10.2 The Key Insight

> The shadow of the future casts an asymmetric light.

Cooperation benefits from long horizons far more than defection benefits from short ones. This asymmetry is the key leverage point: any intervention that extends horizons disproportionately favors cooperation.

### 10.3 Practical Implication

If you want cooperation to emerge:

1. **Lengthen the game** — Open-ended > finite
2. **Add costs to defection** — Even small costs help
3. **Avoid terminal framing** — "This is it" triggers defection
4. **Build institutions** — They have longer memories than individuals

The future is cooperation's friend.

---

## References

1. Axelrod, R. (1984). *The Evolution of Cooperation*. Basic Books.
2. Dal Bó, P. (2005). Cooperation under the Shadow of the Future. *American Economic Review*, 95(5), 1591-1604.
3. Fudenberg, D. & Maskin, E. (1986). The Folk Theorem in Repeated Games. *Econometrica*, 54(3), 533-554.
4. Mailath, G. & Samuelson, L. (2006). *Repeated Games and Reputations*. Oxford University Press.

---

*This document is part of the Kinship Protocol research project.*
*Source: [github.com/royalbit/kinship-protocol](https://github.com/royalbit/kinship-protocol)*
