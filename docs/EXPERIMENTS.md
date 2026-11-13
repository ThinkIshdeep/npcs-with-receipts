# Experiments and reproduction

Run `python scripts/evaluate_all.py` from this repository. The report is written to `reports/evaluation-results.json`. This executes real calculations; model quality is separate from test success.

## Recorded baseline

```json
{
  "checks": {
    "private_observation": true,
    "one_hop_rumour": true,
    "distant_character_unaware": true,
    "coin_conservation": true,
    "debt_repaid": true
  },
  "note": "Deterministic world invariants; believability requires a human study."
}
```

## Interpretation

Structured rule-based social agents and TF-IDF memory retrieval. No language-model dialogue or human believability study.

The raw reports describe whether measurements are synthetic benchmarks, controlled regression fixtures or invariants. Do not interpret regression-fixture accuracy as a held-out real-world score. Preserve seeds and splits when comparing changes.
