# PROGRESS — Wormhole-vertical

Running log. Newest entries first. Updated on every merge and every experiment.

## Current status (2026-11-25)

- **Phase:** A complete; B in progress; C/D not started.
- **Repo:** https://github.com/limapedro/Wormhole-vertical
- **Baseline tag:** `baseline-upstream` → `d7e88a5` (upstream 1.6.8), pushed.
- **Environment:** local folder `E:\__PROJECTS__\Wormhole-vertical`; portable
  OBS 33.0.0 under `obs-portable/`; OBS-MCP at
  `E:\__PROJECTS__\OBS-MCP` (MIT, used as an external tool).
- **Numbers:** none claimed yet. No experiment has run. The <1% / 0.5% CPU
  ceiling is a target, not a result.

## Done

- **Namespace separation (#2)** — fork DLL renamed to `wormhole-vertical.dll`;
  source IDs, dock IDs, hotkey names, canvas name, WebSocket vendor, output/
  encoder/service names and manifest/buildspec metadata namespaced. Official
  upstream 1.6.8 binary installed beside it in portable OBS. Automated check
  passes: `loaded=2 collisions=0 wormhole_canvas=True aitum_canvas=True
  errors=0`. Three matching scenes with deterministic colour sources created
  in both vertical canvases via OBS-MCP (`scripts/setup_matching_scenes.ps1`).
- **First OBS-MCP telemetry (not a benchmark run)** — idle portable OBS with
  both plugins loaded and matching scenes: OBS `GetStats` reported
  `cpuUsage = 0.8476%`, `averageFrameRenderTime = 0.719 ms`, 0 skipped render
  and 0 skipped output frames; OBS-MCP process sampling reported 0.65% CPU
  and 496.2 MB working set. Raw response captured in session evidence; a
  repeatable matrix comes from `exp_000`.
- **Phase A1** — inventoried `E:\__PROJECTS__\Wormhole` read-only. Transfers
  and exclusions recorded in [ARCHITECTURE_LOG.md](ARCHITECTURE_LOG.md).
- **Phase A3** — verified upstream `Aitum/obs-vertical-canvas`, GPL-2.0, latest
  release 1.6.8 (2026-11-18), latest stable OBS 33.0.3.
- **Phase A4** — forked upstream as `Wormhole-vertical`; `upstream` remote kept;
  issues enabled; labels, 6 milestones and 17 issues created.
- **Phase A5** — license finding logged; original `LICENSE` kept.
- **Phase A6** — namespace separation locked (both plugins coexist).
- **Phase A7** — unmodified fork built with CMake + VS 18 generator override
  and loaded in portable OBS (`[Vertical Canvas] loaded version 1.6.8`);
  tagged `baseline-upstream`.
- **Phase B** — planning docs being written; issues #1–#17 created.

## Next

1. Finish Phase B docs, including `FEATURE_PARITY.md` from source reading.
2. Implement the namespace rename so both DLLs load together (issue #2).
3. Install upstream `aitum-vertical` and `wormhole-vertical` into portable OBS;
   create matching multi-scene sets through OBS-MCP.
4. Write `exp_000/HYPOTHESIS.md`, then build the harness and measure noise.
5. Run the upstream baseline matrix; write numeric targets.

## Blocked / risks

See [RISKS.md](RISKS.md). Nothing currently blocks Phase B.
