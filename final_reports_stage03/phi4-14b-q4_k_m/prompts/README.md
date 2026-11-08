# Lap-linked prompts and request controls

Synthetic01–03: exact unredacted prompts, factorized as shared_prefix + case.task + shared_suffix without extra separators. All60 prompt hashes and actual transmitted bodies checked against frozen/validated evidence.02/03 requests and final response texts matched for every case.02 helper derives from the original project's Qwen API appendix plus scalar-weight clarification; no complete solution supplied.

Real04–10: established public mesh/material placeholders replace private identifiers. Public prompt hashes identify redacted text; these are not byte-identical private requests. Original task, input-derived numeric summary, API guidance, all appended instructions and explicit settings are otherwise preserved.04 uses original frozen real-exam controls;05 adds identification help;06 BMesh guidance;07/08 initial prompts match06;09 adds brief API review;10 changes only temperature to0.2.

07/08 repair templates retain settings and feedback descriptions but exclude the previous generated answer embedded in the actual request. Full prompts containing code remain private.07's generic-footer feedback limitation is documented;08 received the specific exception.09/10 did not invoke repair because code ran and failed state verification, outside the syntax/runtime repair policy.

Context/output numbers are token limits, not GB. Synthetic controls:temperature0/context4096/output1536; optional thinking/seed/repetition omitted as in baseline. Real controls:context8192/output4096, thinkfalse, seed0, repeat_penalty1, presence_penalty0; temperature0 until10 (0.2). Native backend defaults can differ where omitted. Brief review is not native thinking.
