# Typed benchmark configuration. No argparse: callers pass one config path.
# Copyright (C) 2026 Wormhole-vertical contributors
# SPDX-License-Identifier: GPL-2.0-or-later
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class InstanceConfig:
    name: str = "wormhole"
    ws_host: str = "127.0.0.1"
    ws_port: int = 4455


@dataclass
class ScenarioConfig:
    id: str
    plugins: tuple[str, ...] = ()
    preview_hidden: bool = False
    description: str = ""


@dataclass
class BenchmarkConfig:
    portable_dir: Path = Path("obs-portable")
    mcp_exe: Path = Path("E:/__PROJECTS__/OBS-MCP/build/obs-mcp.exe")
    mcp_config: Path = Path("harness/config/obs-mcp.toml")
    plugin_store: Path = Path("benchmarks/plugins")
    dismiss_script: Path = Path("scripts/dismiss_crash.ps1")
    instance: InstanceConfig = field(default_factory=InstanceConfig)
    warmup_s: int = 10
    window_s: int = 60
    runs: int = 5
    samples: int = 12
    settle_s: int = 8
    scenarios: tuple[ScenarioConfig, ...] = ()

    @classmethod
    def load(cls, path: Path | str) -> "BenchmarkConfig":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        instance = InstanceConfig(**raw.get("instance", {}))
        parsed = []
        for raw_scenario in raw.get("scenarios", []):
            values = dict(raw_scenario)
            if "plugins" in values:
                values["plugins"] = tuple(values["plugins"])
            parsed.append(ScenarioConfig(**values))
        scenarios = tuple(parsed)
        known = {f.name for f in cls.__dataclass_fields__.values()}
        values = {k: v for k, v in raw.items() if k in known and k not in {"instance", "scenarios"}}
        for key in ("portable_dir", "mcp_exe", "mcp_config", "plugin_store", "dismiss_script"):
            if key in values:
                values[key] = Path(values[key])
        return cls(instance=instance, scenarios=scenarios, **values)

    def to_dict(self) -> dict:
        return asdict(self)
