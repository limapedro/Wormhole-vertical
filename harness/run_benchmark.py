# Repeatable OBS resource benchmark driven by OBS-MCP.
# Usage: python harness/run_benchmark.py benchmarks/config/noise.json
# No argparse: the single positional argument is the typed config path.
# Copyright (C) 2026 Wormhole-vertical contributors
# SPDX-License-Identifier: GPL-2.0-or-later
from __future__ import annotations

import csv
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from bench_config import BenchmarkConfig
from mcp import ObsMcp

PLUGIN_DLLS = ("vertical-canvas.dll", "wormhole-vertical.dll")
FIELDS = (
    "scenario", "run", "sample", "timestamp_utc", "cpu_percent", "working_set_mb",
    "obs_cpu_usage", "obs_render_ms", "render_skipped", "render_total",
    "output_skipped", "output_total", "active_fps", "memory_usage_mb", "log",
)


def kill_obs() -> None:
    subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "Get-Process obs64 -ErrorAction SilentlyContinue | Stop-Process -Force"],
        check=False, capture_output=True,
    )


def install_plugins(cfg: BenchmarkConfig, plugins: tuple[str, ...]) -> None:
    portable = cfg.portable_dir
    plugin_dir = portable / "obs-plugins" / "64bit"
    data_dir = portable / "data" / "obs-plugins"
    plugin_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    for dll in PLUGIN_DLLS:
        (plugin_dir / dll).unlink(missing_ok=True)
    for name in ("vertical-canvas", "wormhole-vertical"):
        target = data_dir / name
        if target.exists():
            subprocess.run(["cmd", "/c", "rmdir", "/S", "/Q", str(target)], check=False)
    for name in plugins:
        source_dll = cfg.plugin_store / f"{name}.dll"
        source_data = cfg.plugin_store / name
        (plugin_dir / f"{name}.dll").write_bytes(source_dll.read_bytes())
        if source_data.exists():
            subprocess.run(
                ["robocopy", str(source_data), str(data_dir / name), "/E", "/NFL", "/NDL", "/NJH", "/NJS", "/NP"],
                check=False, capture_output=True,
            )


def clear_logs(cfg: BenchmarkConfig) -> None:
    log_dir = cfg.portable_dir / "config" / "obs-studio" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    for log in log_dir.glob("*.txt"):
        log.unlink(missing_ok=True)


def dismiss_crash(cfg: BenchmarkConfig, root: Path) -> None:
    subprocess.run(["powershell", "-NoProfile", "-File", str(root / cfg.dismiss_script)],
                   check=False, capture_output=True)
    time.sleep(1)


def sample(mcp: ObsMcp, cfg: BenchmarkConfig, scenario: str, run: int, index: int) -> dict:
    cpu_text = json.loads(mcp.tool("obs_cpu_stats", {
        "name": cfg.instance.name, "window_ms": 1000,
    }))
    stats = mcp.ws(cfg.instance.name, "GetStats", 100 + index)
    return {
        "scenario": scenario,
        "run": run,
        "sample": index,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "cpu_percent": cpu_text.get("cpu_percent"),
        "working_set_mb": cpu_text.get("working_set_mb"),
        "obs_cpu_usage": stats.get("cpuUsage"),
        "obs_render_ms": stats.get("averageFrameRenderTime"),
        "render_skipped": stats.get("renderSkippedFrames"),
        "render_total": stats.get("renderTotalFrames"),
        "output_skipped": stats.get("outputSkippedFrames"),
        "output_total": stats.get("outputTotalFrames"),
        "active_fps": stats.get("activeFps"),
        "memory_usage_mb": stats.get("memoryUsage"),
        "log": "",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python harness/run_benchmark.py <config.json>")
        return 2
    root = Path(__file__).resolve().parent.parent
    cfg = BenchmarkConfig.load(root / sys.argv[1])
    out_dir = root / "benchmarks" / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = out_dir / f"run_{stamp}.csv"
    handle = output.open("w", newline="", encoding="utf-8")
    writer = csv.DictWriter(handle, fieldnames=FIELDS)
    writer.writeheader()
    handle.flush()
    mcp = ObsMcp(cfg.mcp_exe, cfg.mcp_config, root)
    try:
        for scenario in cfg.scenarios:
            for run in range(1, cfg.runs + 1):
                kill_obs()
                install_plugins(cfg, scenario.plugins)
                clear_logs(cfg)
                mcp.tool("obs_launch", {"name": cfg.instance.name})
                time.sleep(cfg.settle_s)
                dismiss_crash(cfg, root)
                time.sleep(cfg.warmup_s)
                for index in range(1, cfg.samples + 1):
                    writer.writerow(sample(mcp, cfg, scenario.id, run, index))
                    handle.flush()
                    if index < cfg.samples:
                        time.sleep(max(1, cfg.window_s // cfg.samples))
                mcp.tool("obs_terminate", {"name": cfg.instance.name})
                time.sleep(2)
                print(f"{scenario.id} run {run}/{cfg.runs} complete", flush=True)
    finally:
        mcp.close()
        handle.close()
    print(f"wrote results to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
