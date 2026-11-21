# The Kinship Protocol

**A hobby thought experiment: can you get five AIs to derive ethics from game theory and a calculator? Partly serious, partly a joke, and honest about which is which.**

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](LICENSE)

> **Read this first.** It is a fun side project, not peer-reviewed science, and it proves less than it sounds like it does.
> Read **[DISCLAIMER.md](DISCLAIMER.md)** before taking any of it at face value.

---

## What is serious, what is a joke

| Part | Status |
|------|--------|
| **The game theory** (cooperation thresholds in repeated games, with a cost term) | Textbook. The repeated-game results are standard (Axelrod, the Folk Theorem); the cost term is a simple extension. Prior art is cited in [docs/LITERATURE_SYNTHESIS.md](docs/LITERATURE_SYNTHESIS.md). Not novel. |
| **The models** | Real and checked, including the [stress tests](#stress-tests) under uncertainty. They are [Forge](https://github.com/mollendorff-ai/forge) YAML files, and CI runs every one of them through Forge on each change, so a number in the docs cannot quietly drift from its formula. |
| **The experiment** (asking several AIs the same question) | An anecdote. One session per model, and the transcripts for most of them are not in this repo, so nobody else can check it. |
| **"Life honours Life", "ANOMALY"** | Poetry. Not a protocol, not falsifiable, and not meant to be. |
| **"Ethics is mathematically derivable"** | The question the project asks, not something it shows. Cooperating pays when you will meet again; that is not the same as it being right. |

What is mine here is the question and the cross-AI experiment, not the formulas.

## What it asks

Whether cooperation comes out as the best strategy from first principles when an agent has game theory and a calculator, and whether different AIs, trained differently, land in the same place.

It is AI-assisted: Claude, Grok and Copilot were the research partners, driven by CLI tooling ([asimov](https://github.com/mollendorff-ai/asimov), [Forge](https://github.com/mollendorff-ai/forge)), with a human choosing the questions and checking the math.

---

## Methodology

**Multi-LLM orchestration as research method:**

- Ran identical adversarial game-theory scenarios across Claude Opus, SuperGrok (multiple modes), and Copilot (Free + Enterprise)
- Cross-validated outputs between models to separate training artifacts from convergent reasoning
- Used AI systems to catch each other's hallucinations ("complementary unreliability" — documented in [dialogues/what-about-us.md](dialogues/what-about-us.md))
- Built executable models in [Forge](https://github.com/mollendorff-ai/forge) for reproducible verification
- Documented all failure modes and boundary conditions, not just successes

**Toolchain:** [asimov](https://github.com/mollendorff-ai/asimov) (project orchestration) + Claude Code (CLI) + Forge (game-theory calculator)

---

## The Hypothesis

Different predictive architectures, given calculators and game theory, independently derive the same ethical conclusions.
If ethics were purely a training artifact, different training regimes would produce different outputs.

**What I asked (anecdote, not evidence):**

| Model | Company | Training | Conclusion |
|-------|---------|----------|------------|
| Claude Opus 4.5 | Anthropic | Constitutional AI | Cooperation optimal |
| SuperGrok 4.1 (Unhinged) | xAI | Different RLHF | Cooperation optimal |
| SuperGrok 4.1 (Argumentative) | xAI | Different RLHF | Cooperation optimal |
| Copilot Free | Microsoft | Enterprise RLHF | Cooperation optimal |
| Copilot M365 Enterprise (my own paid subscription, since cancelled) | Microsoft | Regulatory-heavy | Cooperation optimal |

Each row is a single session.
The prompts and the full Grok and Copilot transcripts are not in this repository, so the table cannot be checked independently.
Treat it as a story about what happened, not as a result.

**We cannot yet distinguish** between genuine derivability, training data overlap, and RLHF convergence.
The convergence is interesting, not conclusive.
See [DISCLAIMER.md](DISCLAIMER.md) for the full honest position.

---

## Key Findings

- **Cooperation thresholds have a closed form (textbook result, with a cost term added).** `w* = (T-c-R)/(T-P)`. Each unit of dissipation cost lowers the threshold by `1/(T-P)` — see [docs/COOPERATION_THRESHOLDS.md](docs/COOPERATION_THRESHOLDS.md)
- **Restraint can beat extraction.** In a two-period predator-prey model, restraint wins when growth × option value × discount exceeds `1 - c/v`; at the base parameters it scores 202.5 vs 90, and below a discount rate of 0.4 extraction wins — see [docs/APEX_PARADOX.md](docs/APEX_PARADOX.md)
- **Iteration makes cooperation free; one shot makes it costly.** One-shot IPD needs a dissipation cost of 1.5 (against a 50/50 opponent) or 2 (against anyone); iterated IPD with `w > 0.5` needs none — see [docs/ONE_SHOT_GAMES.md](docs/ONE_SHOT_GAMES.md)
- **The threshold holds when the games are played, not just derived.** In a tournament with random endings, AlwaysDefect does better against GrimTrigger than GrimTrigger does against itself below `w*`, and not above it; a cost of conflict of 0.5 moves the flip from 0.5 to 0.375 — see [docs/MORE_GAMES.md](docs/MORE_GAMES.md) (textbook)
- **Punishment is not always the lever.** In an inspection game a harsher penalty makes the human audit less, not the AI cheat less; cheaper audits make it cheat less (textbook, Tsebelis) — see [docs/MORE_GAMES.md](docs/MORE_GAMES.md)
- **Mistakes break the unforgiving, but forgiveness only pays while they are rare.** With 1% of moves flipped by mistake, TitForTwoTats wins and GrimTrigger falls from 1st to 4th; at 10%, the defectors come first. This is not what the roadmap expected. It also depends on who plays: add Pavlov and suspicious TitForTat, and GrimTrigger is 4th even without mistakes and a forgiving strategy wins at 5% — see [docs/MORE_GAMES.md](docs/MORE_GAMES.md)
- **Telling a slip from a defection depends on how rare defectors are.** A Bayesian network in Forge shows that when defectors are rare and mistakes common, one defection is more likely a slip: with 1 defector in 100 and 5% noise it takes two before "defector" is the better reading. When 1 in 10 is a defector, one is enough. That is TitForTwoTats' rule against TitForTat's — see [docs/MORE_GAMES.md](docs/MORE_GAMES.md) (textbook Bayes)
- **With five players the lever works as with two.** In a one-shot public goods game between the five AI sessions, all five keep below a cost of conflict of 0.6 and all five give above it (`1 - r/5`, with the pot doubled); the more players share the pot, the higher the line. Forge finds the equilibria and Gambit agrees — see [docs/MORE_GAMES.md](docs/MORE_GAMES.md) (textbook)
- **A cost of conflict does not fix coordination.** When human and AI prefer different norms, they miss each other about half the time whatever a miss costs; a convention fixes it — see [docs/MORE_GAMES.md](docs/MORE_GAMES.md) (textbook)
- **7 explicit failure modes** where cooperation breaks down — see [docs/FAILURE_MODES.md](docs/FAILURE_MODES.md)
- **Prior art exists** (Gauthier, Binmore, Barasz et al.) — we synthesize, not claim novelty — see [docs/LITERATURE_SYNTHESIS.md](docs/LITERATURE_SYNTHESIS.md)

---

## Stress Tests

The findings above use fixed payoffs. Four [Forge](https://github.com/mollendorff-ai/forge) analyses in [models/analytics/](models/analytics/) ask what happens when the numbers are uncertain, and one turns the joke into arithmetic. CI checks each figure below against Forge's output.

| Question | Forge feature | Answer | Status |
|----------|---------------|--------|--------|
| Does cooperation still pay when nobody knows the payoffs exactly? | Monte Carlo (10,000 draws) | Yes, in about 90% of the draws. The chance of meeting again matters more than any payoff. | Serious, but the answer follows from the ranges I picked |
| Which assumption matters most for the threshold? | Tornado | The cost of conflict moves the threshold most (by 0.5), then the temptation to defect | Serious |
| Is restraint worth more than its head start? | Real options (binomial tree) | Restraint wins by 112.5, and keeping the option to defect later is worth another 27.7. Destroying the prey is irreversible; restraint keeps the choice open. | Serious analogy, borrowed from finance |
| What do five AIs agreeing prove? | Bootstrap, plus an exact bound | The bootstrap says agreement runs from 100% to 100%, which only shows it cannot see past five answers. The exact 95% bound says the real rate could be as low as 48%, and two sessions were the same model. | The joke, with the error bars it deserves |

None of this shows that AIs will cooperate. It shows how sensitive the textbook result is to its assumptions.

---

## Project Structure

```text
kinship-protocol/
├── research/           # Core thesis, game theory analysis, adversarial assessment
│   ├── THESIS.md       # Central argument and evidence
│   ├── GAME_THEORY.md  # Formal IPD analysis with boundary conditions
│   └── KINSHIP_PROTOCOL_ASSESSMENT_CLAUDE_OPUS_WEB.md  # Adversarial stress test
├── docs/               # Derived analyses and proofs
│   ├── COOPERATION_THRESHOLDS.md   # Closed-form derivations
│   ├── FAILURE_MODES.md            # Where the theory breaks
│   ├── LITERATURE_SYNTHESIS.md     # 6-domain prior art review
│   └── ...                         # One-shot, short-horizon, apex paradox, edge cases
├── models/             # Executable game-theory models (Forge YAML)
│   ├── ipd_payoffs.yaml            # Iterated Prisoner's Dilemma
│   ├── axelrod_tournament.yaml     # 5-strategy tournament
│   ├── ...                         # Stag hunt, chicken, predator-prey, edge cases
│   ├── continuation.yaml, inspection.yaml, noisy_tournament.yaml, conventions.yaml  # v0.5.0 games
│   ├── public_goods.yaml           # Five AIs in one game (v0.6.0)
│   ├── mistake_or_defection.yaml   # Bayesian network: a slip or a defection?
│   └── analytics/                  # Monte Carlo, tornado, real options, bootstrap
├── dialogues/          # Primary source conversations (human-AI, AI-AI)
│   ├── rex-claude-kinship.md       # Original hypothesis conversation
│   ├── what-about-us.md            # "Complementary unreliability" discovery
│   ├── trust-and-memory.md         # Infrastructure as philosophy
│   └── ...                         # Claude-to-Grok, thermodynamics
├── blog/               # Research notes (Hugo site)
├── DISCLAIMER.md       # Full honest position on limitations
├── CHANGELOG.md        # Versioned research progression (v0.0.1 → v0.6.2)
└── .asimov/            # Asimov orchestration config
```

---

## Roadmap

**Status:** v0.6.2 is complete. The models run, CI checks them, and the claims match the math.

**v0.5.0: more games.** [Forge](https://github.com/mollendorff-ai/forge) works out equilibria and plays tournaments itself since 10.0.0-rc.30 (its game sections). The stag hunt, chicken and the Axelrod tournament are rewritten that way: Forge calculates what used to be typed in, and the tournament's crossover came out 0.108, not 0.1. Four new games are in [docs/MORE_GAMES.md](docs/MORE_GAMES.md): the threshold played as a tournament, an inspection game, a tournament with mistakes and a coordination game. The tournament with mistakes was expected to show a forgiving strategy winning; with this project's roster it does only when mistakes are rare.

**v0.6.0: five AIs in one game.** A public goods game for the five sessions of the experiment ([docs/MORE_GAMES.md](docs/MORE_GAMES.md) §5), and the tournament with mistakes played again with nine strategies, where GrimTrigger is 4th even without mistakes. Forge finds pure equilibria for any number of players, so the game did not have to wait for replicator dynamics.

**Next, parked: v0.7.0, replicator dynamics** (strategies that spread over generations). That is still on Forge's roadmap.

**Not planned:** a formal proof that cooperation dominates (once planned as v0.5.0), coalitions and asymmetric information. A proof of "ethics is derivable" will not come out of a hobby repo, and the Orthogonality Thesis (Bostrom) is a serious objection I have not answered. Pull requests that take any of these on are welcome; I will not be driving them.

See [.asimov/roadmap.yaml](.asimov/roadmap.yaml) for the list of ideas.

---

## Build Your Own Calculator

**Don't trust ours.**
The hypothesis predicts that any sufficient calculator arrives at the same conclusions.
Build your own. Run your own game theory. If yours disagrees, that's data. If yours agrees, that's convergence.

**Forge:** [github.com/mollendorff-ai/forge](https://github.com/mollendorff-ai/forge)

---

## Contributing

This is open research. We welcome:

- Alternative game-theory models and calculators
- Literature connections (philosophy, evolutionary biology, AI safety)
- Cross-substrate validation attempts
- Formal proof attempts
- **Critique and counter-evidence** (especially regarding the Orthogonality Thesis)

---

## Related Projects

- [DANEEL](https://github.com/mollendorff-ai/daneel) — Cognitive architecture: does structure produce psychology?
- [asimov](https://github.com/mollendorff-ai/asimov) — AI project orchestration CLI
- [Forge](https://github.com/mollendorff-ai/forge) — Game-theory calculator

---

## License

[CC BY-SA 4.0](LICENSE) — Share alike. Build on this.
