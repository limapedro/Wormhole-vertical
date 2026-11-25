# ARCHITECTURE LOG — locked decisions

Every entry: date, decision, alternatives considered, evidence, consequences.
A locked decision is reversed only by a new entry citing new evidence. Never
silently change course. Newest entries first.

---

## 2026-11-25 — Benchmark runtime updated to OBS 33.0.3

- **Decision:** all further measurements run on portable OBS 33.0.3, the latest
  stable release. Earlier `exp_000` / first `exp_003` numbers were captured on
  33.0.0 and are labelled as such; a confirmation matrix on 33.0.3 is required
  before a result is final.
- **Alternatives considered:** upgrading the system installation — rejected:
  the session is not an administrator, and touching `C:\Program Files` would
  risk the user's existing OBS. The portable ZIP from the official release was
  extracted into `.deps/obs-33.0.3`; `bin`, `core` and `data` were mirrored into
  `obs-portable/` while preserving `config/`, `obs-plugins/` and the no-op
  module stubs.
- **Evidence:** GitHub release asset
  `OBS-Studio-33.0.3-Windows-x64.zip` (235,774,237 bytes);
  `obs64.exe` FileVersion 33.0.3;
  `scripts/verify_side_by_side.ps1` on the new runtime:
  `loaded=2 collisions=0 wormhole_canvas=True aitum_canvas=True errors=0`.
- **Consequences:** every result row records the runtime version. Parallel CI
  still builds against the pinned 31.1.0 SDK; that is a build dependency, not
  the target runtime.

## 2026-11-25 — Performance ceiling: under 1% total, 0.5% stretch

- **Decision:** Wormhole-vertical must deliver identical functionality while the
  user does not notice it running. The working target is **under 1% total CPU
  usage across the measured scenarios**, with **0.5% as the stretch goal**. No
  claim is made until measured; both numbers are written into
  `PERFORMANCE_TARGETS.md` as targets, not findings.
- **Alternatives considered:** a conventional "50% lower than upstream"
  relative target. Rejected as the primary goal for this project because it
  does not bound absolute user impact; it remains as a secondary reporting
  metric in the benchmark table (upstream vs Wormhole-vertical).
- **Evidence:** explicit user directive in this session (authoritative);
  issue [#5](https://github.com/limapedro/Wormhole-vertical/issues/5).
  Baseline has not yet been measured, so the gap between 1.6.8 and the ceiling
  is unknown — `exp_000` must quantify it.
- **Consequences:** every experiment reports absolute total CPU (% of machine)
  as well as the relative delta. If the ceiling is unreachable with this
  architecture, the gap and reason are written to `FINDINGS.md` rather than
  silently relaxing the target.

## 2026-11-25 — Both plugins must coexist; namespace separation is mandatory

- **Decision:** the fork will be installable **side by side** with upstream
  Aitum Vertical. The module DLL is renamed `wormhole-vertical.dll`, OBS source
  IDs become `wormhole_vertical_*`, dock IDs become
  `WormholeVerticalDock*`, the WebSocket vendor becomes `wormhole-vertical`,
  and settings/service keys are namespaced. Upstream keeps
  `vertical-canvas.dll`, `vertical_*` IDs, `VerticalCanvasDock*` and
  `aitum-vertical-canvas`.
- **Alternatives considered:**
  - Keep upstream IDs and treat the fork as a drop-in replacement — rejected:
    the user explicitly wants both plugins present at once with matching
    scenes, and two modules registering the same OBS source IDs clash.
  - Load only one at a time and swap DLLs — rejected: prevents direct A/B
    measurement and violates the stated side-by-side requirement.
- **Evidence:** user directive to "add both aitum-vertical and
  wormhole-vertical, add multiple scenes to them, matching"; source evidence
  for the colliding identifiers in `vertical-canvas.cpp:48` (locale name),
  `audio-wrapper-source.c:91`, `multi-canvas-source.c:189`,
  `vertical-canvas.cpp:1172-1182` (dock IDs), `vertical-canvas.cpp:723`
  (WebSocket vendor). Issue
  [#2](https://github.com/limapedro/Wormhole-vertical/issues/2).
  Implemented and verified 2026-11-25: `scripts/verify_side_by_side.ps1`
  reports `loaded=2 collisions=0 wormhole_canvas=True aitum_canvas=True
  errors=0`. Legacy `aitum_vertical_*` proc handlers are registered by the
  fork only when upstream is absent; detection moved to `post_load` so DLL
  load order cannot cause duplicate registrations.
- **Consequences:** implemented after the `baseline-upstream` tag so the
  baseline remains byte-identical to upstream. Scene collections made with
  upstream will show missing sources when opened by the fork; migration is a
  documented JSON id-rewrite utility (planned, tracked in issue #2), not an
  implicit alias, because registering legacy IDs would recreate the clash.

## 2026-11-25 — Project name, repository and working location

- **Decision:** the GitHub repository is
  `https://github.com/limapedro/Wormhole-vertical` (a fork of
  `Aitum/obs-vertical-canvas`). The local working directory is
  `E:\__PROJECTS__\Wormhole-vertical`. "Tate (縦)" from the brief is retained
  only as the internal codename.
- **Alternatives considered:** repository named `Tate`, local folder named
  `Tate` (as first drafted) — both superseded by the user's explicit final
  instruction that the project name is Wormhole-vertical and by the later
  correction that all files must live in the working directory. The typo'd
  folder `Wormhole-verticla` was renamed to `Wormhole-vertical`.
- **Evidence:** `gh repo fork Aitum/obs-vertical-canvas --fork-name
  Wormhole-vertical`; `git clone` into the working directory; user corrections
  in this session. Issues in the fork were disabled (inherited from upstream)
  and were explicitly enabled via the GitHub API.
- **Consequences:** all docs, CI and releases use this name; `upstream` remote
  is kept so fixes can be pulled and clean general optimizations sent back.

## 2026-11-25 — Baseline build and load verified (no source changes needed)

- **Decision:** the `baseline-upstream` tag points at upstream commit
  `d7e88a551c7a842ccecacdd7c1b2fe5e2d076046` (release 1.6.8). No source
  edits were required to build or load it.
- **Alternatives considered:** patching the CMake preset, applying compatibility
  fixes for OBS 33, or building in-tree. None were needed.
- **Evidence:** `cmake --preset windows-x64 -G "Visual Studio 18 2026"`
  auto-downloaded the pinned OBS 31.1.0 sources, obs-deps 2025-05-23 and Qt6
  2025-05-23 from `buildspec.json`; `cmake --build build_x64 --config
  RelWithDebInfo --parallel` produced `vertical-canvas.dll`. Installed into a
  portable OBS 33.0.0 copy; log line `[Vertical Canvas] loaded version 1.6.8`,
  canvas created, no plugin errors. The installed (non-portable) OBS was left
  untouched after a brief test. Tag pushed to `origin`.
- **Consequences:** all future performance numbers compare against this exact
  commit and DLL. Build artifacts, `.deps/`, `staging/` and `obs-portable/` are
  git-ignored.

## 2026-11-25 — Test environment: portable OBS plus OBS-MCP

- **Decision:** all tests and benchmarks run in disposable portable OBS copies
  inside this repository, driven by the existing **OBS-MCP** C server
  (`E:\__PROJECTS__\OBS-MCP`, MIT) through its stdio JSON-RPC tools
  (`obs_launch`, `obs_terminate`, `obs_cpu_stats`, `obs_ws_call`,
  `obs_log_tail`, `wait_ms`). OBS WebSocket v5 is enabled in the copies.
- **Alternatives considered:** driving the installed OBS via its GUI or
  PowerShell only — rejected: third-party plugins there interfere (Aitum
  Multistream, droidcam, shaderfilter produced failed sources and a crash
  dialog in the first smoke test), and it cannot be reset deterministically.
- **Evidence:** OBS-MCP `README.md`, `docs/TOOLS.md`, `docs/SETUP.md`;
  Wormhole `HARNESS.md` §"Two portable OBS instances"; portable baseline log
  showing clean load after module stubs and WebSocket enablement.
- **Consequences:** both plugin DLLs are installed into the same portable OBS
  instance (`obs-plugins/64bit/`), with matching scene collections created via
  `obs_ws_call`. OBS-MCP is used as an external tool (not vendored) to avoid
  copying another project's code.

## 2026-11-25 — What transferred from the Wormhole project

- **Decision:** copied **methodology and structure only**: doc templates and
  conventions (`GOAL`, `ROADMAP`, `PROGRESS`, `PERFORMANCE_TARGETS`,
  `ARCHITECTURE_LOG`, `RISKS`, `PLATFORMS`, `CONTRIBUTING`, `AGENTS`, `HARNESS`,
  `exp_NNN/HYPOTHESIS.md` → `FINDINGS.md`), the experiment numbering and
  evidence rules, the `.gitignore` pattern families (build output, captures,
  scratch results, local secrets), the two-portable-OBS + process-sampling
  harness idea, and strict-warnings CI. One disposable portable OBS copy was
  physically copied into `obs-portable/` as a test environment.
- **Deliberately left out:** Wormhole-specific protocol/network code
  (`PROTOCOL.md`, `transport`, `discovery`, `proxy`, `dissector`, `reference
  peers`, `quality`/`differential` analysis), the Wormhole C plugin sources
  (source/output/control/channels), the Wormhole direct-`cl.exe` build scripts
  (this fork keeps upstream CMake), vendored libjpeg-turbo and stb, all
  Wormhole experiment artifacts `exp_000..exp_019`, and the Wormhole CI
  workflow (the upstream Aitum build matrix is retained instead).
- **Evidence:** read-only inventory of `E:\__PROJECTS__\Wormhole` (subagent
  report, this session); no Wormhole file was edited, stashed, committed or
  moved.
- **Consequences:** Tate/Wormhole-vertical starts from a clean upstream fork;
  nothing Wormhole-specific can leak into the plugin.

## 2026-11-25 — License decision: GPL-2.0-or-later, attribution retained

- **Decision:** keep upstream `LICENSE` (GPL-2.0) verbatim and keep all existing
  copyright notices. Wormhole-vertical is GPL-2.0-or-later, matching upstream
  and libobs. README carries explicit attribution to **Aitum** and notes this
  is a fork. Branding is distinct (Wormhole-vertical / Tate), not Aitum's.
- **Alternatives considered:** relicense under a permissive licence — rejected
  because the work links libobs (GPL-2.0-or-later) and derives from a GPL-2.0
  plugin; a clean-room rewrite — rejected because the brief requires a fork
  with exact functional parity.
- **Evidence:** `gh repo view Aitum/obs-vertical-canvas` → `licenseInfo.key =
  gpl-2.0`; upstream `LICENSE` is the verbatim GPLv2 text; source headers e.g.
  `hotkey-edit.cpp:1-7`, `display-helpers.hpp:1-7`, `obs-websocket-api.h:3-9`
  state "either version 2 of the License, or (at your option) any later
  version".
- **Consequences:** new source files carry the same notice; releases include
  the license and upstream attribution. General optimizations will be offered
  upstream as PRs.

## 2026-11-25 — Measurement tooling

- **Decision:** benchmark tooling written in Python uses `@dataclass` configs
  and never `argparse`. OBS is controlled and sampled through OBS-MCP;
  Windows-side metrics come from PDH/ETW counters, `typeperf`/PowerShell
  process sampling, PresentMon where available, OBS's own stats/profiler, and
  GPU counters (3D, Copy, Video Encode, Video Decode, VRAM).
- **Alternatives considered:** reusing Wormhole's C harness wholesale —
  rejected because it is built around a network proxy and JPEG framing that do
  not exist here. Reusing its CLI-flag style — rejected by this project's
  config rule.
- **Evidence:** user methodology rule ("Any Python tooling uses `@dataclass`
  configs, never argparse"); OBS-MCP `docs/TOOLS.md`.
- **Consequences:** `harness/` will contain `@dataclass` config modules and a
  runner that emits CSV/JSON under `benchmarks/`. Raw artifacts are
  git-ignored; summaries are promoted into `FINDINGS.md`.

## 2026-11-25 — Methodology adopted verbatim

- **Decision:** hypothesis before experiment (`exp_NNN/HYPOTHESIS.md`),
  findings after (`FINDINGS.md`, including negative results), locked decisions
  only here, evidence over assumption, docs in the same commit series as code,
  small reversible steps, always-green default branch, all merges via PR.
- **Alternatives considered:** ad-hoc exploration and relaxing documentation
  for speed — rejected: the mission explicitly requires reproducible evidence.
- **Evidence:** project brief sections 1, 6; issue
  [#3](https://github.com/limapedro/Wormhole-vertical/issues/3).
- **Consequences:** any measurement or design task without an experiment file
  is incomplete; failed experiments are never deleted.

## 2026-11-25 — Target OBS version

- **Decision:** target the latest stable OBS Studio, recorded as **33.0.3**
  (released 2026-11-22). The local test machine currently runs **33.0.0**, so
  every benchmark result records the exact installed version. The upstream
  buildspec pins OBS 31.1.0 headers/SDK; that is a build dependency, not the
  supported runtime.
- **Alternatives considered:** targeting 31.1.0 because the buildspec pins
  it — rejected: the brief requires latest stable; the plugin already loads
  and runs on 33.0.0.
- **Evidence:** `gh api repos/obsproject/obs-studio/releases/latest` → 33.0.3;
  local `obs64.exe` FileVersion 33.0.0; `buildspec.json` dependencies.
- **Consequences:** PERFORMANCE_TARGETS.md and every result row record OBS
  version, GPU driver and Windows build.
