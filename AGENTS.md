# AGENTS — standing instructions for AI agents in Wormhole-vertical

Read the root documents before acting: [GOAL.md](GOAL.md),
[ROADMAP.md](ROADMAP.md), [PROGRESS.md](PROGRESS.md),
[PERFORMANCE_TARGETS.md](PERFORMANCE_TARGETS.md),
[ARCHITECTURE_LOG.md](ARCHITECTURE_LOG.md), [FEATURE_PARITY.md](FEATURE_PARITY.md),
[HYPOTHESES_BACKLOG.md](HYPOTHESES_BACKLOG.md), [HARNESS.md](HARNESS.md),
[PLATFORMS.md](PLATFORMS.md), [RISKS.md](RISKS.md),
[CONTRIBUTING.md](CONTRIBUTING.md).

## Working loop

1. Read PROGRESS.md and ROADMAP.md; pick the highest-priority open issue.
2. If it involves measurement or a design question, write
   `exp_NNN/HYPOTHESIS.md` first, on a branch.
3. Do the work on a short-lived branch; keep every merge through a PR.
4. Run the benchmark matrix and the parity checks; write
   `exp_NNN/FINDINGS.md` (including failures and negative results).
5. Update FEATURE_PARITY.md, PERFORMANCE_TARGETS.md, PROGRESS.md and
   ARCHITECTURE_LOG.md as relevant, in the same commit series.
6. Open a PR linking the issue and the evidence; CI must pass; merge.
7. Update the milestone; pick the next item.

## Key commands

- `gh auth status` — verify access (account `limapedro`).
- Always pass `--repo limapedro/Wormhole-vertical` to `gh issue`/`gh label`
  unless you have confirmed git's resolved repo is the fork.
- `git checkout -b exp/NNN-short-name|feat/...|fix/...|docs/...|perf/...`
- `cmake --preset windows-x64 -G "Visual Studio 18 2026"` — configure.
- `cmake --build build_x64 --config RelWithDebInfo --parallel` — build.
- `cmake --install build_x64 --config RelWithDebInfo --prefix staging` — stage.
- OBS control and telemetry: the external OBS-MCP C server at
  `E:\__PROJECTS__\OBS-MCP`, launched with
  `build\obs-mcp.exe --config <our config.toml>` and driven by one JSON-RPC
  request per line on stdin.
- Python tooling: `@dataclass` configs only, never `argparse`.

## Configuration and evidence conventions

- Typed config objects with explicit defaults; no flag sprawl.
- Every performance claim links to a committed result under `benchmarks/` or
  a summary in `exp_NNN/FINDINGS.md`.
- "Faster" or "should be" is not a finding. Negative results are findings.
- Locked decisions only in ARCHITECTURE_LOG.md with date, decision,
  alternatives, evidence, consequences.
- Raw captures, logs, `.deps/`, `staging/`, `obs-portable/` and `build_x64/`
  are git-ignored; promote small structured summaries into the repo.

## Never do these

- Edit, stash, commit, move or delete anything in `E:\__PROJECTS__\Wormhole`
  (read-only reference) or `E:\__PROJECTS__\OBS-MCP`.
- Force-push `main` or rewrite published history.
- Commit secrets, tokens, personal paths or large binaries.
- Claim parity or a CPU/GPU gain without linked evidence.
- Block OBS's render or audio threads from plugin code.
- Delete failed experiments or negative results.
- Drop a feature to gain speed.
- Guess upstream behaviour — read the source and profile it.
