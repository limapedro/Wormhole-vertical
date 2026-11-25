# Summarise benchmark CSVs: median/min/max and the noise margin across runs.
# Usage: python harness/compare.py benchmarks/raw/<file>.csv
# Copyright (C) 2026 Wormhole-vertical contributors
# SPDX-License-Identifier: GPL-2.0-or-later
from __future__ import annotations

import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path

METRICS = ("cpu_percent", "obs_cpu_usage", "obs_render_ms", "working_set_mb",
           "render_skipped", "output_skipped")


def cof(values: list[float]) -> float:
    mean = statistics.mean(values)
    return statistics.pstdev(values) / mean if mean else 0.0


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python harness/compare.py <results.csv>")
        return 2
    rows = list(csv.DictReader(Path(sys.argv[1]).open(encoding="utf-8")))
    by_scenario: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_scenario[row["scenario"]].append(row)
    for scenario, scenario_rows in by_scenario.items():
        runs = sorted({int(r["run"]) for r in scenario_rows})
        print(f"=== {scenario} ({len(runs)} runs, {len(scenario_rows)} samples) ===")
        for metric in METRICS:
            values = [float(r[metric]) for r in scenario_rows if r.get(metric) not in (None, "")]
            if not values:
                continue
            run_means = []
            for run in runs:
                run_values = [float(r[metric]) for r in scenario_rows
                              if int(r["run"]) == run and r.get(metric) not in (None, "")]
                if run_values:
                    run_means.append(statistics.mean(run_values))
            print(f"{metric:18s} median={statistics.median(values):8.4f} "
                  f"min={min(values):8.4f} max={max(values):8.4f} "
                  f"sample_CoV={cof(values):6.2%} run_CoV={cof(run_means):6.2%}")
        # Skip counts are cumulative in OBS stats; report final values only.
        for metric in ("render_skipped", "output_skipped"):
            finals = []
            for run in runs:
                run_rows = [r for r in scenario_rows if int(r["run"]) == run]
                if run_rows:
                    finals.append(float(run_rows[-1][metric]))
            if finals:
                print(f"{metric:18s} final_per_run={finals}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
