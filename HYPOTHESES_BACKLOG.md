# HYPOTHESES BACKLOG — Wormhole-vertical

Candidate ideas that are **not** experiments yet. Nothing here is a finding.
Promote an item to `exp_NNN` only by writing `HYPOTHESIS.md` first and linking
its issue.

| ID | Candidate idea | Source of idea | What would confirm it | Issue |
|---|---|---|---|---|
| H01 | Redundant render/scale passes in the vertical canvas path | Project brief | GPU frame capture shows the same content rendered/scaled more than once per frame | #8 |
| H02 | GPU→CPU readbacks or staging copies every frame | Project brief | Nsight/PresentMon shows a synchronous map/copy on the render thread | #12 |
| H03 | Work done while the dock or preview is hidden | Project brief | CPU/GPU samples with preview hidden are indistinguishable from preview visible | #9 |
| H04 | Per-frame heap allocations on render/UI hot path | Project brief | Allocation sampler shows steady-state allocations per frame | #10 |
| H05 | Polling timers in the Qt UI doing no useful work | Project brief | ETW timer callbacks dominate UI thread samples while idle | #11 |
| H06 | Lock contention between UI and graphics threads | Project brief | ETW/WPA wait analysis shows thread waits on plugin-owned locks | #13 |
| H07 | Avoidable colour/format conversions | Project brief | Frame analysis shows extra conversion passes between canvas texture and display | #14 |
| H08 | Duplicated encoding work shared with the main canvas | Project brief | Two encoders receive equivalent frames; one could be shared | #15 |
| H09 | The file updater / version check runs more often than needed | Source reading (pending `UPSTREAM_STUDY.md`) | Network/timer trace shows repeated checks after startup | — |
| H10 | Dock widget repaints on every frame even when unchanged | Source reading (pending) | Qt paint events per second exceed actual scene changes | — |
| H11 | Multiple source-tree models rebuild on scene change | Source reading (pending) | Profiler shows repeated full model resets | — |
| H12 | WebSocket vendor requests cost CPU while idle | Source reading (pending) | Handler samples without client requests | — |

Negative results belong in `FINDINGS.md` and must not be deleted. An idea that
is measured and rejected is recorded there, not silently removed from this
backlog.
