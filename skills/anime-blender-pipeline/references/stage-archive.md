# Stage-based archival (optional, V4.2 and V4.3)

The existing mandatory storage subgate is copy-on-write extent deduplication, not hardlinking or cloud backup. It preserves all paths. The ledger verifies every approved working bundle, submitted snapshot and recorded evidence on later commands. Do not delete or substitute these files with remote placeholders. This extension does not change policy, gate evidence, approval hashes or the existing subgate.

## Setup once

Install and configure rclone locally with a private Google Drive remote using your own account. Keep OAuth credentials out of the repository and run reports. Use a dedicated folder per run, e.g. `REMOTE:PROJECT/RUN-ID`. Test with a separate local directory on an external disk using `--local-store /path/to/external-archive/RUN-ID` instead of `--remote`. Never use a folder inside the workspace. On a fresh run stage original source files under RUN/source before init so the ledger records relative paths. External sources still use pinned absolute paths; existing absolute records remain unchanged, and must be accessible at their original paths. Do not rewrite historical ledgers. Blender internal absolute texture/library/cache paths are not rewritten by this tool: inventory these in the stage dependency review; pack or make project-relative using qualified Blender operations only on authorized private derivatives. Keep their transitive dependencies local. The archive cannot establish that dependency inventory is complete.

## After every completed stage, before beginning the next

Stop Blender, background jobs, sync and all writers. Check ledger validity. Make a private plan JSON (never publish model assets or private reports):

    {"paths":["work/02","audit/02","candidates/02"],
     "retired":["work/02/old-private-diagnostic.blend"],
     "keep":["work/02/required-textures"],
     "dependencies_reviewed":true,
     "reason":"Retired private draft; no active consumer after dependency review"}

Only include paths that actually exist. paths may be explicit files or directories under work, audit, candidates or checkpoints; archived contents are regular files only, symlinks are skipped/refused. Include checkpoint directories for backup if desired, but never evict them. Plan lists must not be guessed. Use empty retired if no eligible file. If dependency review is incomplete, archive only. For long-running sessions the orchestrator should invoke the following command after the actual complete/delivery action, not before. Record the returned manifest ID in the compact handoff; the local index and remote manifest are content-addressed. A failed upload is a storage warning/blocker for cleanup, not a change to model qualification. Never retry blindly.

    python3 "$PACK/scripts/stage_archive.py" "$RUN" archive --stage 02 --plan /private/plan.json --remote REMOTE:PROJECT/RUN-ID --quiescent

Each unique content SHA-256 becomes its own gzip object; upload is immutable, readback decompresses and verifies original size/hash. Duplicate bytes share one remote object. This enables individual retrieval without fetching a full stage tarball; many tiny files may incur request overhead. One compressed object is staged locally at a time, requiring headroom up to roughly the largest file plus overhead. A manifest is published only after all objects verify. The receipt does not guarantee perpetual cloud availability; retain a second backup for irreplaceable evidence.

## Find and restore

    python3 "$PACK/scripts/stage_archive.py" "$RUN" list --manifest MANIFEST_SHA --remote REMOTE:PROJECT/RUN-ID
    python3 "$PACK/scripts/stage_archive.py" "$RUN" restore --manifest MANIFEST_SHA --path work/02/old-private-diagnostic.blend --remote REMOTE:PROJECT/RUN-ID --quiescent

Query .stage-archive/*.json locally for exact relative paths; list recovers a lost local manifest by ID and verifies remote identity. Keep IDs separately in handoff/backup. The restore installs verified bytes at original relative paths, refuses collisions, path traversal and symlinks, and uses an atomic no-overwrite temporary link (no permanent writable aliases). A filesystem that cannot perform this operation fails safely. It does not recreate symlinks, empty directories or original timestamps. Keep required source, registered candidates, all submission snapshots and all ledger evidence local; the ledger is intentionally strict. Restore retired dependencies before tools/scripts that explicitly need them. If a restored file is absent or remote unavailable, block dependent work rather than manufacture evidence.

## Optional local reclamation

Not automatic by design. First qualify actual Google Drive round-trip on a disposable run and obtain explicit operator authorization for this plan. Use the same plan's exact retired list and keep list, with reviewed dependencies and reason.

    python3 "$PACK/scripts/stage_archive.py" "$RUN" evict --manifest MANIFEST_SHA --plan /private/plan.json --remote REMOTE:PROJECT/RUN-ID --quiescent

All listed paths must be from the archived stage under work, audit or candidates; any path recorded in the current ledger, at archival, or under checkpoints is protected. Local bytes and actual remote bytes must match; no deletion if any preflight fails. Only regular files are removed. Quiescence and dependency completeness cannot be proven by this script. Do not evict any unreviewed Blender texture, library, cache, script input, approval or active artifact. A partial interruption can leave some retired files removed; restore them from the verified manifest. No remote delete command. Local space recovered may be lower than logical size due to extent sharing. Keep exact registered assets even if this limits savings. Automatic remote-aware ledger validation and fully automatic dependency discovery are deliberately out of scope; never bypass the ledger to reclaim more space.

Tests use a local store and synthetic data only. Live Drive credentials, API behavior, actual Blender dependency completeness and real disk savings must be qualified locally. This is a shared extension usable by either agent, not an automatic scheduler or new human gate. Existing V3 runs must keep its pinned tools and approval ledger.
