# Smoke candidates (authored by hand, UNEXECUTED)

`stage03_correct.py` should pass the Stage 03 synthetic oracle and `stage03_wrong.py` should fail it.
Neither has been run in Blender. They exist so the first end-to-end test on a machine with a pinned
Blender image has a known-good and a known-bad candidate. Stage 04-06 smoke candidates are not written yet.
Treat a mismatch (correct fails / wrong passes) as an oracle or sandbox defect to investigate, not as a model result.
