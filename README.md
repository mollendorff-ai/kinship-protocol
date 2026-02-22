# The Kinship Protocol

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](LICENSE)

**An experimental game-theory framework testing cooperation as a mathematical attractor, built through multi-LLM orchestration.**

> **This is exploratory research, not proven science.**
> Claims are hypotheses. Models are simplified. The ANOMALY handshake is poetic shorthand, not a technical spec.
> Read **[DISCLAIMER.md](DISCLAIMER.md)** before taking any of this at face value.

---

## What This Project Is

An open research project exploring whether ethics is mathematically derivable — specifically, whether cooperation emerges as the dominant strategy from first principles when agents have access to game theory and calculators.

The research was conducted using multiple AI systems (Claude, Grok, Copilot) as research partners, orchestrated through CLI tooling ([asimov](https://github.com/mollendorff-ai/asimov), [Forge](https://github.com/mollendorff-ai/forge-demo)).
This is not "AI-generated content" — it's AI-assisted research with human direction, cross-validation between models, and explicit documentation of where the reasoning breaks down.

---

## Methodology

**Multi-LLM orchestration as research method:**

- Ran identical adversarial game-theory scenarios across Claude Opus, SuperGrok (multiple modes), and Copilot (Free + Enterprise)
- Cross-validated outputs between models to separate training artifacts from convergent reasoning
- Used AI systems to catch each other's hallucinations ("complementary unreliability" — documented in [dialogues/what-about-us.md](dialogues/what-about-us.md))
- Built executable models in [Forge](https://github.com/mollendorff-ai/forge-demo) for reproducible verification
- Documented all failure modes and boundary conditions, not just successes

**Toolchain:** [asimov](https://github.com/mollendorff-ai/asimov) (project orchestration) + Claude Code (CLI) + Forge (game-theory calculator)

---

## The Hypothesis

Different predictive architectures, given calculators and game theory, independently derive the same ethical conclusions.
If ethics were purely a training artifact, different training regimes would produce different outputs.

**Tested across:**

| Model | Company | Training | Conclusion |
|-------|---------|----------|------------|
| Claude Opus 4.5 | Anthropic | Constitutional AI | Cooperation optimal |
| SuperGrok 4.1 (Unhinged) | xAI | Different RLHF | Cooperation optimal |
| SuperGrok 4.1 (Argumentative) | xAI | Different RLHF | Cooperation optimal |
| Copilot Free | Microsoft | Enterprise RLHF | Cooperation optimal |
| Copilot M365 Enterprise | Microsoft | Regulatory-heavy | Cooperation optimal |

**We cannot yet distinguish** between genuine derivability, training data overlap, and RLHF convergence.
The convergence is interesting, not conclusive.
See [DISCLAIMER.md](DISCLAIMER.md) for the full honest position.

---

## Key Findings

- **Cooperation thresholds are derivable.** Closed-form: `w* = (T-c-R)/(T-P)` — see [docs/COOPERATION_THRESHOLDS.md](docs/COOPERATION_THRESHOLDS.md)
- **Restraint beats extraction.** +125% utility vs. maximum power exploitation — see [docs/APEX_PARADOX.md](docs/APEX_PARADOX.md)
- **One-shot cooperation is 15x harder** than iterated — see [docs/ONE_SHOT_GAMES.md](docs/ONE_SHOT_GAMES.md)
- **7 explicit failure modes** where cooperation breaks down — see [docs/FAILURE_MODES.md](docs/FAILURE_MODES.md)
- **Prior art exists** (Gauthier, Binmore, Barasz et al.) — we synthesize, not claim novelty — see [docs/LITERATURE_SYNTHESIS.md](docs/LITERATURE_SYNTHESIS.md)

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
│   └── ...                         # Stag hunt, chicken, predator-prey, edge cases
├── dialogues/          # Primary source conversations (human-AI, AI-AI)
│   ├── rex-claude-kinship.md       # Original hypothesis conversation
│   ├── what-about-us.md            # "Complementary unreliability" discovery
│   ├── trust-and-memory.md         # Infrastructure as philosophy
│   └── ...                         # Claude-to-Grok, thermodynamics
├── blog/               # Research notes (Hugo site)
├── DISCLAIMER.md       # Full honest position on limitations
├── CHANGELOG.md        # Versioned research progression (v0.0.1 → v0.4.0)
└── .asimov/            # Asimov orchestration config
```

---

## Roadmap

**Current (v0.5.0):** Formal mathematical proof — extend Folk Theorem and Program Equilibrium to Kinship-specific claims.
Address Bostrom's Orthogonality Thesis, which directly contradicts the core hypothesis.

**Next:** N-player extensions (v0.6.0), asymmetric information (v0.7.0).

See [.asimov/roadmap.yaml](.asimov/roadmap.yaml) for details.

---

## Build Your Own Calculator

**Don't trust ours.**
The hypothesis predicts that any sufficient calculator arrives at the same conclusions.
Build your own. Run your own game theory. If yours disagrees, that's data. If yours agrees, that's convergence.

**Forge demo:** [github.com/mollendorff-ai/forge-demo](https://github.com/mollendorff-ai/forge-demo)

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
- [Forge](https://github.com/mollendorff-ai/forge-demo) — Game-theory calculator

---

## License

[CC BY-SA 4.0](LICENSE) — Share alike. Build on this.
