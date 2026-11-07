# Lap-linked prompts

Laps 01–06: each JSON file contains shared_prefix, shared_suffix, twenty case tasks and explicit request settings. Reconstruct exactly as shared_prefix + case.task + shared_suffix, with no added separators. Each reconstructed hash was checked against the original ledger. These synthetic prompts are unredacted, including historical cross-stage cautions present in the original request; no results outside Stage03 are included.

Laps 07–10: real-lapNN-prompt.txt contains the identifier-redacted real exam prompt for that lap. Redactions follow the existing Qwen public archive. Request settings and public prompt hashes appear in ../analysis-data.json. These texts are not byte-identical to private requests because of identifier substitutions.

Prompt sequence and comparison limits are explained in ../analysis-notes.md. No generated candidate code or raw completions are included.
