# Stage 00 — GPU qualification (V4.2 / V4.3)

A saved UI preference, driver version, device enumeration or default CPU scene is not sufficient to establish actual rendering capability or incompatibility. `--factory-startup` can bypass saved preferences. Run the following from the same agent execution environment and trusted pinned Blender binary before making a GPU support claim. Do not load the PMX or an approved .blend. The utility changes only temporary in-process preferences and a disposable factory scene.

    python3 "$PACK/scripts/gpu_qualification.py" --blender /path/to/pinned/blender --output "$RUN/audit/gpu-001"

The output directory must be new and private. Stop other GPU workloads first. The NVIDIA-specific probe tries OptiX then CUDA only when necessary, each in a fresh process with a 120-second default timeout and a 512×512, 128-sample synthetic scene. It explicitly enables exactly one matching device and disables CPU and other devices. Multiple matching devices require an operator-selected ID from the inventory: use `--backend CUDA --device-id ID` or the corresponding OPTIX option. The synthetic fixture is not a hard RAM/VRAM resource limiter; retain the existing workload ceilings and monitor the host independently. No automatic install, driver changes, system preference changes or CPU fallback.

Interpret `gpu-qualification.json` and individual worker logs:

- `gpu_render_verified` (exit 0): completed output from a GPU-only configuration plus positive NVIDIA process-specific compute activity overlapping the render. This corroborates device execution, not every kernel or target performance.
- `gpu_render_completed_unverified` (exit 3): GPU-configured render completed but telemetry is unavailable, unsupported or missed the short render. Do not label GPU unsupported. Obtain an independent live witness on the same binary and session, or record blocked qualification.
- `device_selection_required`: select an appropriate device explicitly.
- `no_usable_device_detected_in_test_session`: configuration or enumeration did not find a usable device. This is not proof that the machine or OS cannot use the GPU.
- `gpu_qualification_blocked`: process, configuration, render, timeout or evidence failure. Inspect actual worker status/log; one bounded distinguishing test at a time.

An existing successful manual GPU render is useful positive evidence: compare the exact binary/build, backend, enabled device, execution identity, preferences and GPU visibility. Do not repeatedly reinstall drivers or downgrade Blender based on CPU defaults or version assumptions. Run the probe outside a sandbox that intentionally hides the GPU only when authorized; never weaken unrelated isolation to force a pass. If direct telemetry is unavailable, a separately recorded manual GPU-render witness with matching process and device may qualify the environment. If GPU operation remains unknown, block the GPU claim and dependent GPU benchmark; continue independent preparation. An explicitly approved CPU-only path is not GPU qualification.

Record the selected backend and device ID, binary hash, worker results, driver, OS and configuration in the existing environment-lock/capability-spec evidence. Keep paths and logs outside the public repository. Apply and verify the selected configuration in later fresh Blender sessions; the disposable probe does not save preferences. Reuse qualification only with matching environment and runtime identity. A driver, Blender build, device or execution-boundary change requires requalification. Do not mistake this tiny headless render for actual Cycles Rendered viewport FPS or character/physics qualification. The existing performance and quality requirements remain unchanged.
