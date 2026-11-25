# CONTRIBUTING — Wormhole-vertical

## Workflow

- `main` is always buildable with passing CI. Never force-push `main`, never
  rewrite published history.
- Work on short-lived branches: `feat/...`, `fix/...`, `exp/NNN-short-name`,
  `docs/...`, `perf/...`.
- Every merge to `main` goes through a PR, even for solo work. The PR states
  what changed, which issue it closes, and which experiment/benchmark backs it.
  Squash-merge unless history is clean and meaningful.
- Update [PROGRESS.md](PROGRESS.md) on every merge.
- Every roadmap item is a GitHub issue in milestones `0`–`5`. Labels: `docs`,
  `harness`, `perf`, `parity`, `exp`, `platform:windows`, `platform:linux`,
  `platform:macos`, `blocked`, `research`. Close issues only when acceptance
  criteria and linked evidence exist.
- `gh` commands must target `--repo limapedro/Wormhole-vertical`: this fork
  inherits upstream's disabled issues, so unqualified `gh issue` resolves to
  the upstream repository.

## Commit conventions

Small, atomic, imperative mood, typed prefix: `feat:`, `fix:`, `perf:`,
`docs:`, `test:`, `ci:`, `exp:`, `refactor:`. Reference the issue when one
exists, e.g. `perf(canvas): remove redundant scale pass (#8)`.

## Experiments

For any measurement or design question:

1. Create `exp_NNN/` with a zero-padded sequential number.
2. Write `HYPOTHESIS.md` **before** running anything: what you expect, why, and
   what result would prove you wrong.
3. Run the experiment on a branch. Write `FINDINGS.md` with raw numbers, what
   happened and what you learned. Negative results get the same care. **Never
   delete a failed experiment.**
4. Link the experiment from `PROGRESS.md` and, where relevant,
   `PERFORMANCE_TARGETS.md` / `ARCHITECTURE_LOG.md`.
5. Locked decisions go in `ARCHITECTURE_LOG.md` with date, decision,
   alternatives, evidence, consequences. Reversal requires a new entry with
   new evidence.
6. Parity checks for affected features run before merge. A speedup that drops
   a feature does not count.

## Configuration

Python tooling uses `@dataclass` configs with explicit defaults and never
`argparse`. OBS-MCP and harness tools take a typed config path. Keep personal
paths and secrets out of committed configs.

## Tests and benchmarks

- Every scenario in `PERFORMANCE_TARGETS.md` is runnable from a single script
  against a fresh portable OBS copy.
- Unit tests for the harness config loader and metric aggregation.
- Every bug fix lands with a regression test or a linked experiment.
- Strict compiler warnings in CI; upstream source keeps its existing style.
- Raw CSV/JSON under `benchmarks/` is git-ignored; small summaries are
  promoted into `FINDINGS.md`.

## Licence

Derived from Aitum/obs-vertical-canvas, GPL-2.0-or-later. Keep upstream
copyright notices and the verbatim `LICENSE`. New files carry:

```
Copyright (C) 2026 Wormhole-vertical contributors
SPDX-License-Identifier: GPL-2.0-or-later
```

General optimizations are candidates for a PR back to upstream.
