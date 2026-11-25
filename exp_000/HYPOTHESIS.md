# exp_000 — Baseline harness and noise margin

**Written before the experiment. Issue [#4](https://github.com/limapedro/Wormhole-vertical/issues/4).**

## What we expect

Repeated runs of the *same* scenario with no code change will produce a CPU
measurement with a small but non-zero spread. We expect the relative
coefficient of variation (CoV) over 5 runs of a 60 s idle scenario to be below
10%, and we expect the 5-run median to be stable enough that a 50% reduction
(a plausible optimization win) is far outside the noise band.

## Why

The project requires that no finding be smaller than the measurement noise.
Without a measured margin, a 1–2% difference could be misreported as an
improvement. The harness must also prove it starts from a clean, identical OBS
state every run; OBS-MCP's `obs_log_tail` and process checks are used to reject
contaminated runs.

## What would prove us wrong

- CoV above 10% for total CPU on the idle scenario: the harness is too noisy
  for the planned experiments, and we must either lengthen the window, increase
  the run count, isolate the machine further, or change the metric.
- Two runs with visibly different plugin state (missing canvas, absent dock,
  crash dialog): the fixture setup is not deterministic.
- Measured CPU of the "no vertical canvas" scenario is not clearly below the
  "dock open" scenario: the scenario definitions do not isolate the plugin.

## Method

1. Set up the portable OBS copy from `benchmarks/fixtures/` with matching
   multi-scene sets for both plugins.
2. For each of 5 runs: launch through OBS-MCP, check the log, warm up 10 s,
   sample process CPU plus OBS stats for 60 s, terminate, record.
3. Compute median/min/max and CoV per metric with `harness/compare.py`.
4. Store raw data in `benchmarks/raw/` and the summary in `FINDINGS.md`.

No plugin code is changed in this experiment.
