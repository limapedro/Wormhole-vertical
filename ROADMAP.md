# ROADMAP — Wormhole-vertical

Phased plan. Each phase is a GitHub milestone; each item below links to its
issue. Work follows the loop in [CONTRIBUTING.md](CONTRIBUTING.md): read
[PROGRESS.md](PROGRESS.md), pick the highest-priority open issue, write a
hypothesis first when measurement or design is involved, work on a short-lived
branch, record findings, update docs, open a PR, merge.

## Phase 0 — Bootstrap (milestone `0 - Bootstrap`) — DONE

- [x] [#1](https://github.com/limapedro/Wormhole-vertical/issues/1) Fork
      upstream, verify license, build unmodified 1.6.8, verify load in portable
      OBS, tag `baseline-upstream`.
- [x] [#2](https://github.com/limapedro/Wormhole-vertical/issues/2) Decide and
      lock namespace separation for side-by-side installation and scene
      migration.

**Acceptance:** baseline tag pushed; fork loads cleanly; decision logged.

## Phase 1 — Planning (milestone `1 - Planning`) — IN PROGRESS

- [x] [#3](https://github.com/limapedro/Wormhole-vertical/issues/3) Write all
      Phase B planning documents, including a source-derived feature parity
      checklist and the OBS-MCP driven measurement plan.

**Acceptance:** every planning doc has real content; every roadmap item below
has an issue; no optimization merged before the baseline exists.

## Phase 2 — Baseline and harness (milestone `2 - Baseline and Harness`)

- [ ] [#4](https://github.com/limapedro/Wormhole-vertical/issues/4) Design the
      benchmark harness with `@dataclass` configs; implement matching multi-
      scene sets; measure run-to-run noise before optimizing (`exp_000`).
- [ ] [#5](https://github.com/limapedro/Wormhole-vertical/issues/5) Install
      `aitum-vertical` and `wormhole-vertical` side by side, run unmodified
      upstream through the full matrix with OBS-MCP, store raw data in
      `benchmarks/`, and set numeric targets including the <1% / 0.5%
      absolute-CPU ceiling.

**Acceptance:** repeated runs land within the recorded noise margin; baseline
table exists; targets are numbers, not adjectives.

## Phase 3 — Upstream study (milestone `3 - Upstream Study`)

- [ ] [#6](https://github.com/limapedro/Wormhole-vertical/issues/6) Write
      `docs/UPSTREAM_STUDY.md`: canvas creation/render path, extra passes and
      copies, scaling and colour conversion, readbacks, encoders/outputs,
      dock drawing, Qt timers/threads, and work done while hidden.
- [ ] [#7](https://github.com/limapedro/Wormhole-vertical/issues/7) Turn every
      parity row into a repeatable test; verify both plugins with the same
      scene set.

**Acceptance:** every hypothesis in the brief is either confirmed by profile
or recorded as a negative result before code is touched.

## Phase 4 — Experiments (milestone `4 - Experiments`)

Each item: `HYPOTHESIS.md` → branch `exp-NNN-short-name` → smallest change →
benchmark matrix → parity checks → `FINDINGS.md` → merge only on a measured win
without parity loss. Update `PROGRESS.md` after every experiment.

| Order | Issue | Experiment | Candidate cause (unconfirmed) |
|---|---|---|---|
| 1 | [#8](https://github.com/limapedro/Wormhole-vertical/issues/8) | `exp_001` | Redundant render/scale passes |
| 2 | [#9](https://github.com/limapedro/Wormhole-vertical/issues/9) | `exp_002` | Work done while dock/preview hidden |
| 3 | [#10](https://github.com/limapedro/Wormhole-vertical/issues/10) | `exp_003` | Per-frame allocations |
| 4 | [#11](https://github.com/limapedro/Wormhole-vertical/issues/11) | `exp_004` | Polling timers / Qt UI work |
| 5 | [#12](https://github.com/limapedro/Wormhole-vertical/issues/12) | `exp_005` | GPU→CPU readbacks / staging copies |
| 6 | [#13](https://github.com/limapedro/Wormhole-vertical/issues/13) | `exp_006` | UI/graphics lock contention |
| 7 | [#14](https://github.com/limapedro/Wormhole-vertical/issues/14) | `exp_007` | Avoidable format conversions |
| 8 | [#15](https://github.com/limapedro/Wormhole-vertical/issues/15) | `exp_008` | Duplicated encoding shared with main canvas |

The order is a starting point; profiles may reorder it. Clean, general wins
are noted as candidates to send upstream as PRs.

## Phase 5 — Release (milestone `5 - Release`)

- [ ] [#16](https://github.com/limapedro/Wormhole-vertical/issues/16) CI builds
      on Windows (required) and Linux/macOS on every PR; Windows release zip
      drops into the OBS plugins folder; semantic tags; notes include benchmark
      deltas.
- [ ] [#17](https://github.com/limapedro/Wormhole-vertical/issues/17) README
      benchmark table (upstream vs Wormhole-vertical), methodology and raw
      data links; every parity row green; every target met or gap documented.

## Definition of done (per release)

1. Every row in `FEATURE_PARITY.md` passes.
2. Every target in `PERFORMANCE_TARGETS.md` is met, or the gap is documented
   with the reason in `FINDINGS.md`.
3. README shows the benchmark table with methodology and raw data linked.
