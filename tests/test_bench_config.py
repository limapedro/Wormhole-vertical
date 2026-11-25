# Unit tests for typed benchmark configuration.
# Copyright (C) 2026 Wormhole-vertical contributors
# SPDX-License-Identifier: GPL-2.0-or-later
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))

from bench_config import BenchmarkConfig, InstanceConfig, ScenarioConfig  # noqa: E402


class BenchConfigTests(unittest.TestCase):
    def test_defaults_are_explicit(self):
        cfg = BenchmarkConfig()
        self.assertEqual(cfg.runs, 5)
        self.assertEqual(cfg.samples, 12)
        self.assertEqual(cfg.warmup_s, 10)
        self.assertEqual(cfg.instance, InstanceConfig())

    def test_load_typed_scenarios(self):
        raw = {
            "runs": 3,
            "instance": {"name": "wormhole", "ws_port": 4455},
            "scenarios": [
                {"id": "S1", "plugins": ["vertical-canvas"]},
                {"id": "S2", "plugins": [], "preview_hidden": True},
            ],
            "unknown_key": "ignored",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            cfg = BenchmarkConfig.load(path)
        self.assertEqual(cfg.runs, 3)
        self.assertEqual(cfg.instance.ws_port, 4455)
        self.assertEqual(len(cfg.scenarios), 2)
        self.assertIsInstance(cfg.scenarios[0], ScenarioConfig)
        self.assertEqual(cfg.scenarios[0].plugins, ("vertical-canvas",))
        self.assertTrue(cfg.scenarios[1].preview_hidden)
        self.assertFalse(hasattr(cfg, "unknown_key"))

    def test_repository_noise_config_loads(self):
        cfg = BenchmarkConfig.load(ROOT / "benchmarks" / "config" / "noise.json")
        self.assertEqual([s.id for s in cfg.scenarios],
                         ["S0-none", "S0-upstream", "S0-fork", "S0-both"])
        self.assertEqual(cfg.scenarios[3].plugins,
                         ("vertical-canvas", "wormhole-vertical"))


if __name__ == "__main__":
    unittest.main()
