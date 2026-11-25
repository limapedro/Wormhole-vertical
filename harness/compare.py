# Summarise benchmark CSVs: median/min/max/coefficient of variation.
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


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python harness/compare.py <results.csv>")
        return 2
    rows = list(csv.DictReader(Path(sys.argv[1]).open(encoding="utf-8")))
    by_scenario: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_scenario[row["scenario"]].append(row)
    for scenario, scenario_rows in by_scenario.items():
        print(f"=== {scenario} ({len(scenario_rows)} samples) ===")
        for metric in METRICS:
            values = [float(r[metric]) for r in scenario_rows if r.get(metric) not in (None, "")]
            if not values:
                continue
            mean = statistics.mean(values)
            cof = statistics.pstdev(values) / mean if mean else 0.0
            print(f"{metric:18s} median={statistics.median(values):8.4f} "
                  f"min={min(values):8.4f} max={max(values):8.4f} CoV={cof:6.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
