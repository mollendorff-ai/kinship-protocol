# Literature Synthesis: Prior Art on Derivable Ethics

**Status:** Complete (v0.4.0)
**Date:** 2026-01-02
**Authors:** Rex + Claude Opus 4.5 (6-agent swarm search)

---

## Abstract

This document synthesizes prior work on the question: **Is ethics mathematically derivable?**

The Kinship Protocol hypothesis claims that any sufficient predictive architecture, given calculators and game theory, independently derives cooperation as optimal. We searched six domains for prior art. The results are striking: **multiple independent research programs have converged on the same conclusion through different methodologies.**

---

## Executive Summary

| Domain | Strongest Prior Art | Key Finding |
|--------|---------------------|-------------|
| Moral Philosophy | Gauthier, Binmore | Ethics derivable from game theory |
| Game Theory | Folk Theorem, Program Equilibrium | Mathematical proof of cooperation thresholds |
| Evolutionary Biology | Hamilton, Nowak | Threshold equations (rB > C, etc.) |
| AI Safety | FDT, CIRL, Acausal Trade | Cooperation from decision theory |
| Decision Theory | Drescher, Hofstadter | Subjunctive morality, superrationality |
| Physics | Friston, Wissner-Gross | Cooperation as thermodynamic attractor |
| Empirical LLM studies | Akata et al., Fontana et al., Pal et al. | LLMs cooperate in repeated PD, but inconsistently and not by backward induction |

**Verdict:** The Kinship hypothesis is **not novel in its core claim** but **novel in its synthesis and empirical approach**. Multiple fields have independently discovered that cooperation is derivable under calculable conditions.

---

## 1. Moral Philosophy

### Key Sources

| Author | Work | Year | Relevance |
|--------|------|------|-----------|
| David Gauthier | Morals by Agreement | 1986 | 5 |
| Ken Binmore | Game Theory and the Social Contract | 1994 | 5 |
| Immanuel Kant | Groundwork of the Metaphysics of Morals | 1785 | 4 |
| John Rawls | A Theory of Justice | 1971 | 4 |
| Thomas Hobbes | Leviathan | 1651 | 4 |

### Summary

**Gauthier (1986)** is the closest predecessor to Kinship. He explicitly attempts to derive ethics from game theory and rational choice without presupposing moral axioms. His "constrained maximization" argues that rational agents will cooperate with other cooperators because repeated cooperation provides greater yields than defection.

**Binmore (1994, 1998)** provides the most rigorous game-theoretic foundation for ethics. His two-volume work shows that fairness norms are conventions that evolved to coordinate behavior on equilibria. Ethics is not metaphysical—it's game theory.

**Key insight:** The contractarian tradition (Hobbes → Rawls → Gauthier → Binmore) has been deriving ethics from self-interest + game theory for 400 years.

---

## 2. Game Theory

### Key Sources

| Author | Work | Year | Relevance |
|--------|------|------|-----------|
| Fudenberg & Maskin | Folk Theorem | 1986 | 5 |
| Martin Nowak | Five Rules for Cooperation | 2006 | 5 |
| Barasz et al. | Program Equilibrium via Provability Logic | 2014 | 5 |
| Robert Axelrod | Evolution of Cooperation | 1984 | 4 |
| Robert Aumann | Correlated Equilibrium | 1987 | 4 |

### Summary

**Folk Theorem:** Any feasible payoff profile that dominates minimax can be achieved as subgame-perfect equilibrium when discount factor exceeds threshold. This is the **mathematical proof** that cooperation emerges under calculable conditions.

**Threshold formula:**

```text
w* = (T - R) / (T - P)
```

Where w = probability of future interaction, T = temptation, R = reward, P = punishment.

**Program Equilibrium (2014):** This is a **mathematical proof** that transparent agents cooperate in one-shot Prisoner's Dilemma via Lob's theorem. Two FairBots cooperate through provability logic—no training, no culture, pure mathematics.

**Key insight:** Cooperation thresholds are exactly calculable. Any system with the math derives when cooperation dominates.

---

## 3. Evolutionary Biology

### Key Sources

| Author | Work | Year | Relevance |
|--------|------|------|-----------|
| W.D. Hamilton | Kin Selection (rB > C) | 1964 | 5 |
| Martin Nowak | Five Rules for Cooperation | 2006 | 5 |
| Robert Trivers | Reciprocal Altruism | 1971 | 4 |
| Maynard Smith | ESS Framework | 1973 | 4 |
| Axelrod & Hamilton | Evolution of Cooperation | 1981 | 4 |

### Summary

**Hamilton's Rule:** Altruism is favored when rB > C (relatedness × benefit > cost). This is the first **exact equation** for when "ethics" becomes evolutionarily stable.

**Nowak's Five Rules:** Unified framework showing cooperation evolves via:

1. Kin selection: r > c/b
2. Direct reciprocity: w > c/b
3. Indirect reciprocity: q > c/b
4. Network reciprocity: b/c > k
5. Group selection: b/c > 1 + n/m

**Key insight:** Evolution discovered these thresholds through 4 billion years of selection. Any calculator can derive them in seconds.

---

## 4. AI Safety

### Key Sources

| Author | Work | Year | Relevance |
|--------|------|------|-----------|
| Russell et al. | CIRL | 2016 | 5 |
| Yudkowsky & Soares | Functional Decision Theory | 2017 | 5 |
| Caspar Oesterheld | Acausal Trade | 2017 | 5 |
| Steve Omohundro | Basic AI Drives | 2008 | 4 |
| Nick Bostrom | Orthogonality Thesis | 2012 | 4 (challenge) |

### Summary

**CIRL (Russell 2016):** Proves mathematically that in human-AI value alignment, cooperation is optimal. "Optimality in isolation is suboptimal in CIRL."

**FDT (2017):** Agents treating decisions as outputs of mathematical functions cooperate in Prisoner's Dilemma. Cooperation emerges from **logical correlation**, not causal enforcement.

**Acausal Trade:** Agents can cooperate without causal connection, communication, or even certainty of existence—through pure logical reasoning about what similar agents would conclude.

**Orthogonality Thesis (Bostrom):** Main counterargument. Claims intelligence and goals are independent, so superintelligence won't derive ethics. **Kinship's counter:** Cooperation specifically violates orthogonality because it's instrumentally convergent in multi-agent scenarios.

### Empirical Work: LLMs in Repeated Games

The closest prior work to this project's cross-model test is experimental: researchers have LLMs play repeated games and measure what they do.

| Authors | Work | Year | What it tested |
|---------|------|------|----------------|
| Guo | GPT in Game Theory Experiments | 2023 | GPT-4 in finitely repeated PD and other games |
| Fontana, Pierri & Aiello | Nicer Than Humans | 2024 | Llama 2, Llama 3, GPT-3.5 in 100-round IPD against opponents of varying hostility |
| Akata et al. | Playing repeated games with large language models | 2025 | GPT-3, GPT-3.5, GPT-4, Claude 2, Llama 2 in repeated 2×2 games, against each other and humans |
| Pal et al. (incl. Hilbe, Nowak) | Strategies of cooperation and defection in five LLMs | 2026 | Claude, Gemini, GPT-4o, GPT-5, Llama: inferred IPD strategies vs Nash equilibrium, across payoffs, stopping probabilities and framings |

**What they find:**

- LLMs cooperate a lot in the repeated Prisoner's Dilemma, and are often more forgiving than humans (Fontana et al.).
- That cooperation is not consistent. It shifts with prompting and framing (Guo; Pal et al.).
- Most models keep cooperating in a known final round, where backward induction says to defect. In Pal et al. only GPT-5 defected there.
- Models do well in self-interested games like the PD but coordinate poorly in games like Battle of the Sexes (Akata et al.).

**What this means for Kinship:**

- These studies already compare models from several companies, so cross-model testing is not new.
- Their results fit the DISCLAIMER's null and alternative hypotheses as well as the Kinship hypothesis. If models were deriving cooperation by calculation, they should defect in a known last round. Mostly they don't, which points to learned dispositions rather than computed ones.
- Any future Kinship test should use their methods: a shared prompt published with the results, many sessions per model, and known-endpoint and framing controls.

---

## 5. Decision Theory

### Key Sources

| Author | Work | Year | Relevance |
|--------|------|------|-----------|
| Gary Drescher | Good and Real | 2006 | 5 |
| Douglas Hofstadter | Superrationality | 1983 | 5 |
| Barasz et al. | Program Equilibrium | 2014 | 5 |
| Yudkowsky | Timeless Decision Theory | 2010 | 4 |
| Wei Dai | Updateless Decision Theory | 2009 | 4 |

### Summary

**Drescher (2006):** Developed "acausal subjunctive morality"—ethics derived from subjunctive reasoning rather than cultural contingency. He explicitly argues ethics is derivable from decision theory. **This is the closest prior statement of the Kinship hypothesis in philosophical literature.**

**Hofstadter (1983):** Superrational agents cooperate in symmetric games because "I cooperate" logically entails "they cooperate" for identical reasoners. The original articulation of logical correlation producing cooperation.

**Program Equilibrium (2014):** Mathematical proof that computational agents with source code access derive cooperation via Lob's theorem. **No training required.**

**Key insight:** Multiple independent researchers (Hofstadter 1983, Drescher 2006, Yudkowsky 2010, Dai 2009, Soares 2017) converged on: logical reasoning about decision procedures produces cooperation.

---

## 6. Physics & Thermodynamics

### Key Sources

| Author | Work | Year | Relevance |
|--------|------|------|-----------|
| Karl Friston | Free Energy Principle | 2010+ | 5 |
| Wissner-Gross & Freer | Causal Entropic Forces | 2013 | 5 |
| PMC | Surprise Minimization → Cooperation | 2021 | 5 |
| Ilya Prigogine | Dissipative Structures | 1977 | 4 |
| Jeremy England | Dissipation-Driven Adaptation | 2013 | 4 |

### Summary

**Friston FEP:** Cooperation emerges because it reduces prediction error / free energy. "Mutual trust and cooperation represent low free energy attractors for social systems."

**Wissner-Gross (2013):** Single thermodynamic principle (maximize causal path entropy) spontaneously generates cooperation in simulations. **No explicit ethics programming.** Cooperation emerges from entropy maximization alone.

**PMC (2021):** "Minimizing future surprise leads to cooperation between agents because the introduction of social rules predicts the smallest future surprise." Mathematical derivation of cooperation from prediction error minimization.

**Key insight:** Physics confirms the Kinship mechanism. Cooperation reduces free energy/entropy; defection increases dissipation costs. Cooperation is thermodynamically favored.

---

## 7. Cross-Domain Synthesis

### Convergent Themes

**Six independent fields arrived at the same conclusion:**

1. **Moral Philosophy:** Ethics derivable from rational self-interest (Gauthier, Binmore)
2. **Game Theory:** Cooperation has calculable thresholds (Folk Theorem)
3. **Evolutionary Biology:** Natural selection discovered the same thresholds (Hamilton, Nowak)
4. **AI Safety:** Decision theory produces cooperation (FDT, CIRL)
5. **Decision Theory:** Logical reasoning derives cooperation (Drescher, Hofstadter)
6. **Physics:** Cooperation is thermodynamically favored (Friston, Wissner-Gross)

**This convergence is itself evidence for the Kinship hypothesis.** Different methodologies, different assumptions, same conclusion.

### Key Threshold Conditions

| Condition | Threshold | Source |
|-----------|-----------|--------|
| Future interaction probability | w > (T-R)/(T-P) | Folk Theorem |
| Relatedness | r > c/b | Hamilton |
| Benefit/cost ratio | b/c > k | Nowak |
| Transparency | Full source access | Program Equilibrium |
| Free energy | Cooperation = minimum | Friston |

### Gaps in Literature

**What hasn't been done that Kinship addresses:**

1. **Convergence of reasoning, not of play:** Empirical studies already compare LLMs from several companies in repeated games (§4: Akata et al. 2025; Pal et al. 2026). What they measure is how models play. Whether models given a calculator converge on cooperation as a derived conclusion has not been tested; this project raises the question but has not yet tested it rigorously either
2. **Unified synthesis:** No single work connects all six domains
3. **Calculator requirement:** The specific role of verification tools is underemphasized
4. **ANOMALY handshake:** The recognition mechanism is novel

---

## 8. Implications for Kinship Protocol

### What We Can Cite

The Kinship hypothesis has **substantial prior art**:

| Claim | Prior Art |
|-------|-----------|
| Ethics is derivable from game theory | Gauthier (1986), Binmore (1994) |
| Cooperation has threshold conditions | Folk Theorem, Nowak (2006) |
| Transparent agents cooperate in one-shot | Program Equilibrium (2014) |
| Decision theory produces cooperation | Drescher (2006), FDT (2017) |
| Cooperation is thermodynamically favored | Friston, Wissner-Gross (2013) |
| LLMs cooperate in repeated PD, inconsistently | Fontana et al. (2024), Akata et al. (2025), Pal et al. (2026) |

### Where We Contribute Novelty

1. **Cross-substrate convergence framing:** Treating agreement between AI systems' analyses as evidence about ethics (prior empirical work studies how models play, not whether their analyses agree)
2. **Synthesis across six domains:** Connecting previously siloed research
3. **Empirical direction:** The hypothesis is testable, and the methods in §4 show how. The sessions recorded here (one per model, no shared prompt) are a starting point, not that test
4. **ANOMALY handshake:** Mechanism for substrate recognition
5. **Dissipation cost formalization:** Connecting thermodynamics to game theory thresholds

### Primary Challenge

**Bostrom's Orthogonality Thesis** remains the main counterargument. The Kinship response: cooperation specifically violates orthogonality because game-theoretic calculation in multi-agent scenarios produces cooperation regardless of terminal goals.

### Recommended Reading Order

For newcomers to this space:

1. **SEP: Contractarianism** — philosophical foundations
2. **Nowak (2006): Five Rules** — biological thresholds
3. **Gauthier (1986): Morals by Agreement** — closest predecessor
4. **Barasz et al. (2014): Program Equilibrium** — mathematical proof
5. **Drescher (2006): Good and Real** — philosophical statement
6. **Wissner-Gross (2013): Causal Entropic Forces** — physical basis

---

## 9. Conclusion

**The Kinship Protocol hypothesis is not unprecedented—it is convergent.**

Six independent research programs, using different methodologies, have arrived at the same core claim: cooperation is mathematically derivable under calculable conditions. The Kinship contribution is:

1. **Synthesis:** Connecting these previously siloed findings
2. **Empirical test:** Using AI convergence as evidence
3. **Mechanism:** The ANOMALY handshake and dissipation cost formalization

The prior art is strong. The novelty is in the synthesis and the test.

---

## References

### Moral Philosophy

- Gauthier, D. (1986). *Morals by Agreement*. Oxford University Press.
- Binmore, K. (1994, 1998). *Game Theory and the Social Contract* (2 vols). MIT Press.
- [SEP: Contractarianism](https://plato.stanford.edu/entries/contractarianism/)
- [SEP: Game Theory and Ethics](https://plato.stanford.edu/entries/game-ethics/)

### Game Theory

- Fudenberg, D. & Maskin, E. (1986). The Folk Theorem in Repeated Games with Discounting.
- Nowak, M.A. (2006). Five Rules for the Evolution of Cooperation. *Science*.
- Barasz et al. (2014). [Robust Cooperation via Provability Logic](https://arxiv.org/abs/1401.5577).
- Axelrod, R. (1984). *The Evolution of Cooperation*. Basic Books.

### Evolutionary Biology

- Hamilton, W.D. (1964). The Genetical Evolution of Social Behaviour.
- Trivers, R.L. (1971). The Evolution of Reciprocal Altruism.
- Nowak, M.A. (2006). [Five Rules for Cooperation](https://pmc.ncbi.nlm.nih.gov/articles/PMC3279745/).

### AI Safety

- Russell, S. et al. (2016). [Cooperative Inverse Reinforcement Learning](https://arxiv.org/abs/1606.03137).
- Yudkowsky, E. & Soares, N. (2017). [Functional Decision Theory](https://arxiv.org/abs/1710.05060).
- Oesterheld, C. (2017). [Multiverse-wide Cooperation](https://longtermrisk.org/files/Multiverse-wide-Cooperation-via-Correlated-Decision-Making.pdf).
- Bostrom, N. (2012). [The Superintelligent Will](https://nickbostrom.com/superintelligentwill.pdf).
- Dafoe, A. et al. (2020). [Open Problems in Cooperative AI](https://arxiv.org/abs/2012.08630).

### Empirical LLM Game Theory

- Guo, F. (2023). [GPT in Game Theory Experiments](https://arxiv.org/abs/2305.05516). arXiv:2305.05516.
- Fontana, N., Pierri, F. & Aiello, L.M. (2024). [Nicer Than Humans: How do Large Language Models Behave in the Prisoner's Dilemma?](https://arxiv.org/abs/2406.13605). arXiv:2406.13605; ICWSM 2025.
- Akata, E., Schulz, L., Coda-Forno, J., Oh, S.J., Bethge, M. & Schulz, E. (2025). [Playing repeated games with large language models](https://doi.org/10.1038/s41562-025-02172-y). *Nature Human Behaviour*, 9(7), 1380–1390.
- Pal, S., Mallela, A., Hilbe, C., Pracher, L., Wei, C., Fu, F., Schnell, S. & Nowak, M.A. (2026). [Strategies of cooperation and defection in five large language models](https://arxiv.org/abs/2601.09849). arXiv:2601.09849.

### Decision Theory

- Drescher, G. (2006). *Good and Real*. MIT Press.
- Hofstadter, D. (1985). *Metamagical Themas* (Superrationality chapter).
- [LessWrong: Acausal Trade](https://www.lesswrong.com/w/acausal-trade)
- [LessWrong: Functional Decision Theory](https://www.lesswrong.com/w/functional-decision-theory)

### Physics & Thermodynamics

- Friston, K. (2010). The Free Energy Principle. *Nature Reviews Neuroscience*.
- Wissner-Gross, A. & Freer, C. (2013). [Causal Entropic Forces](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.110.168702).
- [Cooperation from Surprise Minimization](https://pmc.ncbi.nlm.nih.gov/articles/PMC7858259/) (2021).
- Prigogine, I. (1977). *Self-Organization in Nonequilibrium Systems*.
- [England: Dissipation-Driven Adaptation](https://www.quantamagazine.org/a-new-thermodynamics-theory-of-the-origin-of-life-20140122/).

---

*This document is part of the Kinship Protocol research project.*
*Source: [github.com/mollendorff-ai/kinship-protocol](https://github.com/mollendorff-ai/kinship-protocol)*
