# Wormhole-vertical

Wormhole-vertical (internal codename **Tate**, 縦) is a fork of
[Aitum's Vertical Canvas plugin for OBS Studio](https://github.com/Aitum/obs-vertical-canvas).
It does everything Aitum Vertical does — vertical canvas dock, scene/source
handling, streaming, recording, replay/backtrack, virtual camera, hotkeys,
projectors and more — while targeting a fraction of the CPU and GPU cost.
It is designed to be installed **alongside** upstream Aitum Vertical, so both
can be compared and used in the same OBS.

> **Status:** baseline verified. Upstream 1.6.8 builds and loads in OBS 33.0.0
> (`baseline-upstream`). Benchmark numbers and optimization results are added
> below as experiments complete. No performance claim is made until measured.

## Why

Aitum Vertical proved the vertical-canvas workflow is useful. Wormhole-vertical
keeps that functionality exactly and attacks the resource cost one measured
experiment at a time. The goal is not "feels faster": it is **under 1% total
CPU**, with **0.5%** as the stretch target, on the test machine.

## Priorities (in order)

1. Feature parity with Aitum Vertical 1.6.8.
2. Measured reduction in CPU/GPU cost toward the absolute ceiling.
3. Coexistence with upstream and migration of existing scene collections.

## Supported platforms

| Platform | Status |
|---|---|
| Windows | Primary development and benchmark platform |
| Linux | CI build and functional checks |
| macOS | CI build (universal); no real-hardware benchmarks |

Target runtime: latest stable OBS Studio (33.0.3 at the time of writing). Test
machine runs OBS 33.0.0; every result records the exact version, driver and
Windows build.

## Documentation

- [GOAL.md](GOAL.md) — mission, success definition, non-goals
- [FEATURE_PARITY.md](FEATURE_PARITY.md) — every upstream feature, source-derived
- [PERFORMANCE_TARGETS.md](PERFORMANCE_TARGETS.md) — metrics, scenarios, numeric targets
- [ROADMAP.md](ROADMAP.md) — ordered experiments with linked issues
- [PROGRESS.md](PROGRESS.md) — running status and dashboard
- [HYPOTHESES_BACKLOG.md](HYPOTHESES_BACKLOG.md) — untested ideas
- [ARCHITECTURE_LOG.md](ARCHITECTURE_LOG.md) — locked decisions with evidence
- [HARNESS.md](HARNESS.md) — benchmark harness and OBS-MCP control
- [PLATFORMS.md](PLATFORMS.md), [RISKS.md](RISKS.md), [CONTRIBUTING.md](CONTRIBUTING.md), [AGENTS.md](AGENTS.md)

## Benchmarks

**Baseline not yet measured.** The table will be filled from `exp_000` and the
full matrix; raw data will live under `benchmarks/` and be linked here.

| Scenario | Upstream 1.6.8 | Wormhole-vertical | Delta | Evidence |
|---|---|---|---|---|
| — | pending | pending | pending | pending |

## Build

```bat
cmake --preset windows-x64 -G "Visual Studio 18 2026"
cmake --build build_x64 --config RelWithDebInfo --parallel
cmake --install build_x64 --config RelWithDebInfo --prefix staging
```

The upstream preset targets Visual Studio 2022; on machines with only VS 2026,
pass the generator override above. CMake downloads the pinned OBS SDK, Qt6 and
obs-deps from `buildspec.json` automatically.

## Attribution and licence

This is a fork of **Aitum/obs-vertical-canvas**, developed by
[Aitum](https://aitum.tv). The original source and licence are retained
verbatim in this repository. Wormhole-vertical is independently developed by
the Wormhole-vertical contributors and is not affiliated with or endorsed by
Aitum. Branding and module identifiers are distinct so the two plugins can be
installed together.

Licensed under **GNU GPL version 2, or (at your option) any later version**
([LICENSE](LICENSE)), matching upstream and libobs. Individual source files
retain their original copyright notices; new files carry
`SPDX-License-Identifier: GPL-2.0-or-later`.
