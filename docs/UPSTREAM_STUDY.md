# UPSTREAM STUDY — placeholder (Phase D deliverable)

Issue [#6](https://github.com/limapedro/Wormhole-vertical/issues/6).
This file will be completed from source reading plus profiles before any
optimization is merged. The source-derived feature inventory already lives in
[FEATURE_PARITY.md](../FEATURE_PARITY.md).

## Candidate waste sites identified by source reading (hypotheses, not facts)

| Site | Evidence | Hypothesis |
|---|---|---|
| Per-frame vertex buffer creation for guide/selection lines | `vertical-canvas.cpp:2230-2248`, `:2655-2896` | Redundant GPU resource churn per frame |
| Private text sources updated on stretch | `vertical-canvas.cpp:2285-2587` | Per-frame text re-render |
| Extra texrender pass per canvas in multi-canvas mode | `multi-canvas-source.c:58-126` | Redundant render/scale pass |
| Vestigial `texrender`/`stagesurface` members | `vertical-canvas.hpp:152-153` | No active readback found — confirm |
| 1 s + 4 s polling timers | `vertical-canvas.cpp:1418-1451` | Idle CPU from polling |
| Many `QTimer::singleShot(200-500 ms)` re-entrancy workarounds | multiple | Race-prone state handling, possible extra work |
| Startup libcurl HTTPS thread | `file-updater.c:101-144` | Network I/O on startup |
| Blanket scene-tree updates via queued signals | `source-tree.cpp:304-332`, `vertical-canvas.cpp:8490-8544` | Excess UI work on scene changes |

Each row becomes a hypothesis with a profile before a code change. Negative
results are recorded in `FINDINGS.md` and never deleted.
