# Qwen3.5 9B Q4_K_M — Stage03 analysis package

Model tag: `qwen3.5:9b`. Pinned digest: `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`.

- [Final report](qwen3.5-9b-stage03-final-report.md): all eight synthetic development laps and the separate real primary and assisted trials.
- [Prompts by lap and trial](prompts/README.md): 160 exact synthetic prompts and two redacted real-character prompts.
- [Additional analysis notes](analysis-notes.md): native defaults and overrides, generation-stop evidence, repeated-output checks and interpretation limits.
- [Per-case analysis data](analysis-data.json): all 160 synthetic case records, selected safe model metadata and extra real-trial observations.
- [SHA-256 checksums](SHA256SUMS): integrity of this public package; the checksum file excludes itself.

This folder records a finalized result snapshot for this exact model digest. The report being finalized does not mean the model or a character repair was accepted. Later development should use separate run identifiers and preserve primary scores. No inference is started by opening these files.

Only allowlisted text and numeric fields are published. Personal and machine identifiers, local/network paths, credentials, raw model code and reasoning, continuation-token arrays, logs, private assets, original asset fingerprints, unreleased reference repair details and all results outside Stage03 are excluded. The real prompts retain the clearly documented identifier redactions. Full reproduction against private assets remains limited.
