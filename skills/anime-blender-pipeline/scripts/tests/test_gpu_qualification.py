import sys
from pathlib import Path
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gpu_qualification as g


class FakePrefs:
    def __init__(self, types):
        self.devices = [SimpleNamespace(type=t, name=t, id=str(i), use=True)
                        for i, t in enumerate(types)]
        self.compute_device_type = "NONE"

    def refresh_devices(self):
        pass


class GPUQualificationTests(unittest.TestCase):
    def test_gpu_config_explicitly_disables_cpu_and_other_backend(self):
        prefs = FakePrefs(["CPU", "OPTIX", "CUDA"])
        state, devices = g.configure_gpu(prefs, "OPTIX")
        self.assertEqual(state, "gpu_configured")
        self.assertEqual([d["type"] for d in devices if d["enabled"]], ["OPTIX"])

    def test_no_matching_device_is_not_success(self):
        state, devices = g.configure_gpu(FakePrefs(["CPU"]), "CUDA")
        self.assertEqual(state, "no_matching_gpu")
        self.assertFalse(any(d["enabled"] for d in devices))

    def test_multiple_devices_require_explicit_selection(self):
        prefs = FakePrefs(["CPU", "CUDA", "CUDA"])
        self.assertEqual(g.configure_gpu(prefs, "CUDA")[0], "device_selection_required")
        state, devices = g.configure_gpu(prefs, "CUDA", "2")
        self.assertEqual(state, "gpu_configured")
        self.assertEqual([d["id"] for d in devices if d["enabled"]], ["2"])

    def test_pmon_rejects_memory_only_other_pid_and_graphics_only(self):
        sample = "# gpu pid type sm mem\n0 42 C 0 90\n0 41 C 99 1\n0 42 G 90 1\n0 42 C - 1\n0 42 C+G 25 1\n"
        self.assertEqual(g.parse_pmon(sample, 42),
                         [{"gpu_index": 0, "pid": 42, "sm_percent": 25}])

    def setUp(self):
        self.result = {"status": "gpu_render_completed", "backend": "CUDA",
                       "pid": 42, "render_start": 10, "render_end": 20,
                       "devices": [{"type": "CUDA", "enabled": True},
                                   {"type": "CPU", "enabled": False}]}
        self.witness = {"start": 12, "end": 13, "exit_code": 0,
                        "matches": [{"pid": 42, "sm_percent": 23}]}

    def check(self, samples=(), **kwargs):
        return g.classify(self.result, kwargs.get("rc", 0), kwargs.get("timeout", False),
                          samples, kwargs.get("image", True), kwargs.get("pid", 42))

    def test_success_requires_overlapping_pid_witness(self):
        self.assertEqual(self.check([self.witness]), "gpu_render_verified")
        self.assertEqual(self.check([]), "gpu_render_completed_unverified")
        self.assertEqual(self.check([{**self.witness, "start": 0, "end": 1}]),
                         "gpu_render_completed_unverified")
        self.assertEqual(self.check([{**self.witness, "exit_code": 1}]),
                         "gpu_render_completed_unverified")

    def test_cpu_fallback_and_invalid_image_not_accepted(self):
        self.assertEqual(self.check([self.witness], image=False), "render_evidence_invalid")
        self.result["devices"][1]["enabled"] = True
        self.assertEqual(self.check([self.witness]), "render_evidence_invalid")

    def test_timeout_process_failure_and_wrong_pid(self):
        self.assertEqual(self.check([self.witness], timeout=True), "probe_timeout")
        self.assertEqual(self.check([self.witness], rc=2), "probe_process_failed")
        self.assertEqual(self.check([self.witness], pid=43), "probe_process_failed")

    def test_missing_witness_not_no_gpu(self):
        self.assertEqual(g.summarize([{"status": "gpu_render_completed_unverified"}]),
                         "gpu_render_completed_unverified")
        self.assertEqual(g.summarize([{"status": "backend_configuration_unavailable"},
                                      {"status": "no_matching_gpu"}]),
                         "no_usable_device_detected_in_test_session")
        self.assertEqual(g.summarize([{"status": "render_failed"}]),
                         "gpu_qualification_blocked")


if __name__ == "__main__":
    unittest.main()
