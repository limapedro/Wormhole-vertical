# PERFORMANCE TARGETS — Wormhole-vertical

Metrics, methodology, baseline and targets. **No baseline has been measured
yet.** Every value marked `target` is a hypothesis until `exp_000` produces a
measured baseline and the full matrix is run. Targets change only with evidence
and a corresponding [ARCHITECTURE_LOG.md](ARCHITECTURE_LOG.md) entry.

## Measurement machine (recorded 2026-11-25)

| Item | Value |
|---|---|
| CPU | Intel Core i5-12400F, 6 cores / 12 logical threads |
| Memory | 34,197,749,760 bytes (31.85 GiB reported) |
| OS | Windows 10 Pro, build `26300.10075` |
| GPU | NVIDIA GeForce GTX 1660 SUPER (6 GB) |
| GPU driver | `32.0.16.2101` |
| OBS runtime under test | Studio **33.0.0**, installed at `C:\Program Files\obs-studio` |
| Target stable OBS (per brief) | Studio **33.0.3**, released 2026-11-22 |
| Toolchain | Visual Studio 18 Community / MSVC 19.51.36257.0, CMake 4.3.3 |
| Test environment | disposable portable OBS under `obs-portable/`, driven by OBS-MCP |
| Plugins under test | upstream `aitum-vertical` 1.6.8 (`baseline-upstream`) and Wormhole-vertical |

CI numbers from other OSes are never compared to this machine without
normalization. Every result row records OBS version, GPU driver and Windows
build.

## Metrics

Collected per scenario, for the whole OBS process and, where possible, per
plugin (by loading one plugin at a time and by ETW attribution):

1. **CPU** — process total % of machine, plus per-thread and per-plugin where
   attributable. This is the headline metric for the <1% ceiling.
2. **OBS render time per frame** — from OBS stats/profiler; mean and p99.
3. **GPU engine utilization** — 3D, Copy, Video Encode, Video Decode via PDH
   `GPU Engine` counters / NVIDIA tooling.
4. **VRAM** and **system RAM** (working set / committed).
5. **Encoder lag** and dropped / skipped / missed frames from OBS stats.
6. **OBS WebSocket telemetry** via OBS-MCP (`obs_ws_call`), including
   `GetStats`, scene/source state and active-canvas queries.

## Benchmark scenarios (minimum)

| ID | Scenario | Vertical canvas | Encoding |
|---|---|---|---|
| S1 | OBS only, no vertical canvas | none | software |
| S2 | Vertical dock open, idle | visible | software |
| S3 | Vertical preview hidden | hidden | software |
| S4 | Vertical streaming only | visible | software |
| S5 | Horizontal + vertical streaming at once | visible | software |
| S6 | Recording both canvases | visible | software |
| S7 | Vertical streaming with NVENC | visible | NVENC |
| S8 | Horizontal + vertical streaming with NVENC | visible | NVENC |
| S9 | Both plugins loaded, matching multi-scene sets, idle | visible | software |
| S10 | Both plugins loaded, streaming both | visible | software |

Scenarios S9 and S10 exist because the user requires both plugins to be
installed together; they measure per-plugin contribution directly.

## Deterministic fixtures

- A scene collection and profile are shipped under `benchmarks/fixtures/` and
  installed into the portable OBS copy by `scripts/setup_benchmark_obs.ps1`.
- Sources are deterministic: colour-bar/image sources, a media file loop, and
  one fixed browser source. Both plugin canvases receive **matching multi-scene
  sets** so comparisons are apples-to-apples.
- Warm-up 10 s, measurement window 60 s, 5 runs per scenario. Report median
  with min/max; outliers are recorded, never silently dropped.

## Noise margin

**Not yet measured.** `exp_000` runs the same scenario repeatedly with no code
change and records the coefficient of variation. Until then no delta smaller
than that margin will be claimed.

## Baseline — upstream 1.6.8

**Not yet measured.** The baseline DLL is the unmodified `baseline-upstream`
build. No numeric baseline is claimed here.

## Targets

| ID | Metric | Target | Status |
|---|---|---|---|
| T1 | Total CPU, scenario S2 (idle dock visible) | **< 1.0%** of machine; 0.5% stretch | target, unmeasured |
| T2 | Total CPU, scenario S3 (preview hidden) | **< 0.5%**; 0.25% stretch | target, unmeasured |
| T3 | Total CPU, all other scenarios | **< 1.0%**; 0.5% stretch | target, unmeasured |
| T4 | CPU reduction vs upstream, equal scene set | ≥ 50% lower (secondary metric) | target, unmeasured |
| T5 | OBS render-thread stalls attributable to plugin | zero | target, unmeasured |
| T6 | Dropped/skipped/missed frames | zero at 1080p30 fixtures | target, unmeasured |
| T7 | GPU Copy engine utilization added by plugin | < 0.5% absolute | target, unmeasured |
| T8 | VRAM added by plugin | < 64 MB | target, unmeasured |
| T9 | Feature parity | 100% of `FEATURE_PARITY.md` rows verified | target, unmeasured |

A target is promoted from `target` to `measured` only when a linked result file
under `benchmarks/` supports it and the baseline and method are documented. If
a target proves unrealistic, it is replaced with an evidence-backed value and
the change is logged — never silently dropped.
