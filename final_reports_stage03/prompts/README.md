# Stage03 prompts by lap — Qwen3.5 9B

These prompts accompany the [final Stage03 report](../qwen3.5-9b-stage03-final-report.md). Historical wording and settings are preserved, including obsolete stage references in early synthetic laps. Nothing here changes the frozen private benchmark or launches inference.

| Lap or trial | Prompt archive | Coverage | Fidelity |
|---|---|---|---|
| Synthetic 1 | [lap-01-prompts.json](lap-01-prompts.json) | 20 exact prompts | Reconstructed; hashes match recorded originals |
| Synthetic 2 | [lap-02-prompts.json](lap-02-prompts.json) | 20 exact prompts | Captured request text; hashes match ledger |
| Synthetic 3 | [lap-03-prompts.json](lap-03-prompts.json) | 20 exact prompts | Captured request text; hashes match ledger |
| Synthetic 4 | [lap-04-prompts.json](lap-04-prompts.json) | 20 exact prompts | Captured request text; hashes match ledger |
| Synthetic 5 | [lap-05-prompts.json](lap-05-prompts.json) | 20 exact prompts | Captured request text; hashes match ledger |
| Synthetic 6 | [lap-06-prompts.json](lap-06-prompts.json) | 20 exact prompts | Captured request text; hashes match ledger |
| Synthetic 7 | [lap-07-prompts.json](lap-07-prompts.json) | 20 exact prompts | Captured request text; hashes match ledger |
| Synthetic 8 | [lap-08-prompts.json](lap-08-prompts.json) | 20 exact prompts | Captured request text; hashes match ledger |
| Real first attempt | [real-first-attempt-prompt.txt](real-first-attempt-prompt.txt) | One sanitized prompt | Character mesh and nonstandard material identifiers redacted; not byte-identical |
| Real final assisted retry | [real-final-assisted-prompt.txt](real-final-assisted-prompt.txt) | One sanitized prompt | Character mesh and nonstandard material identifiers redacted; not byte-identical |

Each synthetic JSON contains its lap-specific common prefix, common suffix, all 20 case task strings, request settings and per-case SHA-256. Reconstruct an exact prompt with `shared_prefix + case.task + shared_suffix`, with no extra spaces, separators or newlines. The reconstructed hashes were checked against every corresponding saved proposal and verified ledger attempt. Lap 1 had no saved outgoing request body; its prompt text was reconstructed from the retained fixture and recorded runner, then verified against all 20 original hashes. Later laps use saved request text. The settings listed for lap 1 reconstruct the runner payload; an omitted `think` field means server default.

To reconstruct an Ollama request, copy `request_settings` and add the reconstructed text as its `prompt` field. These are application-level prompts before Ollama applies the native model template. API wrappers, credentials and raw responses are not included.

The two real-character files replace the original mesh identifier with `[CHARACTER_MESH]` and nonstandard material labels with `[MATERIAL_nn]` aliases. Standard technical material labels and input-derived geometry statistics remain. These redactions protect source identifiers, so the public copies are not byte-identical executable reproductions against the private scene. The original prompts and their exact hashes remain local; the frozen benchmark is unchanged. No source checkpoint, texture, private path, raw model output or reference repair implementation is included.

There were eight synthetic laps, followed by one real primary attempt and one real assisted retry. The real trials are not synthetic laps 9/10. The final retry added one sentence about explicit named-mesh selection; it is feedback-assisted evidence and does not replace the primary score. The saved model tag is qwen3.5:9b, Q4_K_M; its digest is recorded in the final report.
