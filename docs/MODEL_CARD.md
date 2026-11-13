# Model and simulator card — NPCs With Receipts

## Intended use

A bounded social world where character knowledge has sources and private actions propagate through limited rumour paths.

## Implemented methods

- Eight agents with goals, locations, trust and private memories
- Validated loan and repayment actions with a conserved coin ledger
- Direct observations separated from reported memories
- One-hop daily rumour propagation and trust updates
- TF-IDF retrieval over each character’s available memories

Some projects use deterministic simulators and rules rather than trained neural models. Those distinctions are retained in this card and the source.

## Evaluation

See `docs/EXPERIMENTS.md` and the machine-readable reports. No pretrained foundation-model weights or real-world efficacy certification are included. Parameters, splits and synthetic generators are visible in source.

## Limitations

Structured rule-based social agents and TF-IDF memory retrieval. No language-model dialogue or human believability study.

## Extensions not implemented in this release

- Generative dialogue and hierarchical learned planning
- Blinded player studies and persistent branching replay
