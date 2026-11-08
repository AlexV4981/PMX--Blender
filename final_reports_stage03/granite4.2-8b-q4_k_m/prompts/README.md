# Lap-linked synthetic prompts

Each lap-NN-prompts.json contains shared_prefix, shared_suffix, twenty case tasks, per-case prompt hashes and the actual explicit request settings. Reconstruct exactly as shared_prefix + case.task + shared_suffix, with no added separator or newline. All200 hashes were checked against the validated ledger. Saved actual request bodies were checked wherever a request reached transport.

The twenty prepared lap1 prompts are archived even though only six requests were transmitted and five responses completed; fourteen cases were blocked locally by the now-documented capture-index bug. That distinction is in the case metrics. Later laps transmitted all twenty.

Synthetic prompts are unredacted and contain no private asset identifiers or machine paths. Some original instructions mention other stages; no results outside Stage03 are included. Final API-sheet text is retained as part of lap10. There are no real-character prompts for Granite in this experiment.

Lap8 matches lap4 with only explicit think=false added. Lap9 changes only temperature and repeat_penalty relative to lap8. Lap10 appends only the verified general reference sheet relative to lap9. These equalities were checked across all twenty actual requests. Other lap changes and comparison limits appear in ../analysis-notes.md.
