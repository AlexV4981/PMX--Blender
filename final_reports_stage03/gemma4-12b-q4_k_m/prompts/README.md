# Lap-linked prompts and controls

Laps01–06 contain exact synthetic prompts, factorized as shared_prefix + case.task + shared_suffix with no added separator. All120 hashes were checked against validated first-attempt events and all120 actual requests matched frozen requests. Lap06's initial requests equal lap05 exactly; its separate repair request includes original generated code and is kept private. A redacted repair prompt template and policy are in ../repair-analysis.json.

Laps07–10 contain real-task prompts with only the established public character/material placeholders. Public prompt hashes identify sanitized text, not the private raw request. The original API/task semantics, general guidance and explicit request settings are retained. Lap08 adds only general Geometry Nodes guidance; lap09 matches08 exactly; lap10 changes only think=false totrue. The08/09 final response text was identical, but raw generated answers are excluded.

Context and output limits are token counts. Thinking shares the output limit with final text. Seed0 applies to real trials; synthetic seed was omitted. Optional omitted settings use backend defaults, so omission is not an asserted numeric value. Native thinking default was enabled in lap01; it was explicitly off in02–09 and on in10. Prompt/API guidance is a proposal aid, not proof of a correct Blender solution.
