# exp_000 — Baseline and noise margin — FINDINGS

**Date:** 2026-11-25
**Hypothesis:** [HYPOTHESIS.md](HYPOTHESIS.md)
**Raw data:** `benchmarks/raw/run_20261125T130255Z.csv` (git-ignored; regenerate
with `python harness/run_benchmark.py benchmarks/config/noise.json`)
**Summary command:** `python harness/compare.py <csv>`
**Machine:** i5-12400F, GTX 1660 SUPER driver 32.0.16.2101, Windows 10 Pro
26300.10075, OBS Studio 33.0.0 (portable), 30 fps, 1280x720 main, 1080x1920
vertical canvases, matching 3-scene sets in both plugins. 5 runs per scenario,
8 s warm-up, 30 s measurement window, 6 samples per run.

## What happened

The harness completed S0-none, S0-upstream and S0-fork (5 runs each) and 4 of
5 runs of S0-both before the process was stopped by the 15-minute shell timeout.
The four S0-both runs are enough to estimate noise; the missing fifth run is
recorded here rather than silently ignored.

| Scenario | OBS `cpuUsage` median | run CoV | render ms median | run CoV | working set | skipped frames |
|---|---|---|---|---|---|---|
| S0-none (OBS only) | 0.6168% | 12.84% | 0.6017 | 3.36% | 491.7 MB | 0 / 0 |
| S0-upstream (aitum-vertical 1.6.8) | 0.7904% | 9.32% | 0.6845 | 4.68% | 495.9 MB | 0 / 0 |
| S0-fork (Wormhole-vertical baseline) | 0.7679% | 9.31% | 0.6958 | 15.98%* | 496.1 MB | 0 / 0 |
| S0-both (4 runs) | 0.7900% | 7.01% | 0.6852 | 21.07%* | ~496 MB | 0 / 0 |

\* Render-time CoV is inflated by rare single-frame spikes (2.16 ms and 1.88 ms)
in one run each. Excluding those outliers the run CoV is ~4–5%, consistent with
the other scenarios. Outliers are recorded, not dropped.

Process-level CPU from OBS-MCP (`obs_cpu_stats`) is noisier (run CoV 15–18%)
because it samples a 1 s window; it is retained as a secondary metric only.

## Noise margin (the finding)

- **OBS `GetStats.cpuUsage`:** run-to-run CoV is **7–13%**. Use **10%** as the
  acceptance margin: a CPU reduction smaller than 10% is not a finding.
- **OBS `averageFrameRenderTime`:** ~4–5% excluding one-frame spikes. Use **5%**.
- **Working set:** <0.2% — essentially deterministic.
- **Dropped/skipped frames:** zero in every sample of every scenario.

The harness is therefore sensitive enough to detect the planned 50% relative
gains, but not 1–2% differences. The hypothesis that 50% is "far outside the
noise band" is **confirmed**; the expectation of CoV below 10% for CPU is
**confirmed at the low end but not strictly** (12.84% on S0-none) — recorded as
a partial result.

## Baseline observations (not optimization findings)

1. One vertical plugin adds ~0.17 percentage points of OBS CPU over the empty
   OBS baseline (0.6168% → ~0.79%).
2. The fork at baseline is **not measurably faster** than upstream: 0.7679%
   vs 0.7904% median, a 2.8% difference, below the 10% noise margin. This is a
   **negative result** for any claim of a speedup from the namespace-only
   changes.
3. Loading **both** plugins (0.7900%) costs essentially the same as loading
   upstream alone (0.7904%) — the second canvas's idle cost is below the noise
   margin. This is a useful result for the side-by-side requirement.
4. **The 0.5% stretch CPU target is below the measured empty-OBS floor of
   0.6168%.** It is therefore unattainable as "total OBS CPU" on this machine
   with any plugin. Recorded as gap R12; the 1% ceiling is achievable at idle.
5. No render or output frames were skipped in any scenario.

## Consequences

- Set the acceptance margin in `PERFORMANCE_TARGETS.md` to 10% (CPU) and 5%
  (render time).
- `exp_002` and `exp_003` must show >10% CPU reduction to be merged; otherwise
  they are negative results.
- Use `GetStats.cpuUsage` as the headline metric; process CPU is secondary.
- Add GPU-engine and VRAM collectors before claiming those targets — this
  baseline only measured CPU, render time, RAM and skipped frames. Recording
  that limitation is required by the methodology.
