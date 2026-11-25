# exp_003 — Deferred canvas video mix — FINDINGS

**Date:** 2026-11-25
**Hypothesis:** [HYPOTHESIS.md](HYPOTHESIS.md)
**Baseline:** `benchmarks/raw/run_20261125T130255Z.csv` (S0-fork, 5 runs)
**After:** `benchmarks/raw/run_20261125T131825Z.csv` (S0-fork, 4 complete runs;
the fifth aborted on an empty OBS-MCP `GetStats` response, data up to that
point was preserved by incremental CSV writes)
**Runtime for these numbers:** OBS Studio 33.0.0 portable. A 33.0.3 confirmation
run is pending (see below).

## What happened

`EnsureCanvas()` creates the canvas with `obs_frontend_add_canvas(name,
nullptr, PROGRAM)` and registers the keyer/channel exactly as before, but does
**not** call `obs_canvas_reset_video()`. `LoadScenes()` now uses
`EnsureCanvas()`; every output start path still calls `StartVideo()`, which
creates the video mix only when an output actually needs it.

| Metric (S0-fork idle) | Before | After | Delta | Noise margin | Verdict |
|---|---|---|---|---|---|
| OBS `cpuUsage` median | 0.7679% | 0.6501% | **−15.3%** | 10% | **win** |
| `averageFrameRenderTime` median | 0.6958 ms | 0.6342 ms | **−8.9%** | 5% | **win** |
| Working set median | 496.1 MB | 495.35 MB | −0.15% | 0.2% | marginal |
| Skipped render/output frames | 0 / 0 | 0 / 0 | none | — | parity |

Both headline deltas exceed their measured noise margins, so this is a
finding, not noise. No frame regressions were observed.

## Parity checks (all passed)

- `scripts/verify_side_by_side.ps1`:
  `loaded=2 collisions=0 wormhole_canvas=True aitum_canvas=True errors=0`.
- OBS WebSocket `GetCanvasList` shows `Main`, `Wormhole Vertical` and
  `Aitum Vertical`; both vertical canvases keep their three matching scenes.
- Vendor API through OBS-MCP:
  - `wormhole-vertical` / `version` → `{"success":true,"version":"1.6.8"}`
  - `wormhole-vertical` / `status` → all four output flags false, success true
  - `aitum-vertical-canvas` / `version` → success, 1.6.8
- Preview still calls `obs_canvas_render()`; the canvas exists even though
  `obs_canvas_has_video()` is false at idle.

## Known limitation / next step

These numbers were captured on OBS 33.0.0. The user asked to move to the
latest stable OBS (33.0.3). A confirmation matrix on 33.0.3 is required before
this result is treated as final; record it in this file when complete. Output
paths (stream/record/backtrack/vcam) still call `StartVideo()`, so their video
mix behaviour is unchanged, but an explicit output-start parity run is still
outstanding (tracked in issue #7).

## Decision

Merge the code change (measured win, no parity loss observed). Keep the
aborted fifth run and this limitation in the record; do not present the result
as a 33.0.3 finding. Candidate for an upstream PR: the same deferral applies
to Aitum Vertical 1.6.8 and is a clean, general optimization.
