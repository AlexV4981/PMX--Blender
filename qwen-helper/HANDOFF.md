# Zero-reasoning Qwen-to-Codex completion handoff

**Only the `Qwen-Local-Helper` branch.** This is a notification mechanism, **not** validation or permission to accept changes.

## What Qwen needs to know

After the local specialist finishes its proposal and the trusted worker writes the proposal JSON, call exactly:

```sh
python qwen-helper/done.py inventory_summary
```

Substitute the registered specialist name: `inventory_summary`, `texture_diagnostics` or `regression_fixtures`. If more than one unfinished proposal exists for that specialist, the runner supplies a task ID:

```sh
python qwen-helper/done.py inventory_summary --task-id TASK_ID
```

**Qwen does not choose a reviewer, execute its own code, accept anything, or decide what happens next.** It merely triggers a durable, local event bound to the original proposal's SHA-256. The existing `dispatch.py propose` wrapper calls this signal automatically on successful proposals; pure Ollama inference cannot execute shell commands by itself.

## Host-side setup (one time per Codex task/session)

The **trusted host**, not Qwen, runs this watcher in a separate terminal while the Qwen worker is active:

```sh
python qwen-helper/done.py --watch --resume-thread YOUR_CODEX_SESSION_UUID
```

Or omit `--resume-thread` to have Codex start a **new** `codex exec` session. An existing session does not magically receive messages when you write a file. Resume only an explicit, idle Codex CLI session; do not race the same active session with two concurrent writers. If your Codex surface is an app without CLI session access, have its external orchestrator poll `qwen-helper/handoffs/pending/` or connect through the official SDK/app-server, rather than claiming this watcher can awaken that app.

The watcher invokes `codex exec` with the original Sol High orchestrator setting and prompts it to ask a real Sol Light reviewer to check Qwen output, run tests, and then either finalize via the existing guarded dispatcher or fall back to the original pipeline. Sol Light availability is checked by Codex at runtime; no model is assumed to exist merely from a name.

To perform a dry run or consume a single event:

```sh
python qwen-helper/done.py --watch --dry-run --once
python qwen-helper/done.py --watch --once --resume-thread YOUR_CODEX_SESSION_UUID
```

For full automation an orchestrating agent starts the watcher at task startup, then launches the local worker. No model needs to reason about handoff procedures. Signaling without a watcher is safe and durable: the pending event stays on disk until a trusted host processes it.

## Guarantees and limits

- Event includes only verified specialist/task IDs, known proposal path, matching SHA-256, and fixed metadata; **never arbitrary shell commands**.
- Script refuses unknown specialist, ambiguous proposals, invalid/duplicate task IDs, unsafe branch, changed/invalid proposal, or a second notification for the same task.
- Watcher re-verifies the event and proposal digest, then invokes a fixed `codex exec` command **without a shell**.
- Completion does not approve Qwen. All actual deterministic testing, qualified-model checks, real Sol Light review and fallback continue in the original process. No automatic stage/human acceptance.
- At most one watcher wake-up per event. Failed Codex invocation moves the event into `handoffs/failed/` with local logs; an agent investigates instead of blindly retrying.
- Pending events, logs and proposals are excluded from Git. Do not commit local task contents, credentials, model adapters or runtime logs.
- The Codex CLI must be installed and authenticated on the watcher machine; using the CLI can consume Codex usage. No separate process can awaken an unavailable session. The watcher needs permission to run `codex exec`; it never assumes access.

## Example workflow

1. Host verifies `Qwen-Local-Helper`, then checks qualifications and `dispatch.py plan`.
2. Host starts `done.py --watch` in another terminal, passing the intended Codex CLI thread UUID.
3. Host runs `dispatch.py propose --task TASK.json`. The wrapper writes its proposal and signals `done.py` **automatically**; alternatively an external specialist runs the one-line signal.
4. Watcher sees `handoffs/pending/TASK_ID.json`, launches Codex once, and moves the event to finished/failed.
5. Codex reads the untrusted proposal, invokes Sol Light if actually available, checks tests, and either finalizes or falls back to the full original pipeline (no second local attempt).
