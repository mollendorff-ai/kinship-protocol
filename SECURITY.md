# Security Policy

## Important context

The Kinship Protocol is exploratory game-theory research: Markdown notes, dialogues, Forge models and a blog. It has no server and no installable software, so its security surface is small. Read [DISCLAIMER.md](DISCLAIMER.md) for what the research does and does not claim.

## Supported versions

Research is paused at v0.4.0. Only the latest commit on `main` is maintained.

## Reporting a vulnerability

Please do not open a public issue for a security problem.

Email **security@mollendorff.ai** with:

- what you found and what it lets someone do,
- steps that reproduce it,
- the file or workflow involved.

You can also use GitHub's private vulnerability reporting, under the **Security** tab of this repository, if it is enabled.

This is a small project kept up on a best-effort basis. I aim to reply within 14 days, and I will tell you what I plan to do about the report. Please give me reasonable time to ship a fix before you share the details publicly. I am glad to credit you if you want that.

## What is in scope

- The GitHub Actions workflows (`hugo.yml` and `models.yml`), including their permissions and how they handle pull requests.
- The scripts in `scripts/`.
- The blog's build and the theme it pulls in as a submodule.
- Personal or private information that appears in the repository, including its history.

## What is not in scope

- The research claims themselves. A wrong argument or a flawed model is a disagreement with the research, not a security problem: please open a normal issue for those.
- Vulnerabilities in Forge, Hugo or the PaperMod theme: report those to their own projects.
