# RISKS — Wormhole-vertical

Risk register. Newest first; resolved rows are retained with links to evidence.

| ID | Risk | Impact | Owner action | Status |
|---|---|---|---|---|
| R01 | Absolute <1% / 0.5% CPU ceiling may be unreachable with the current architecture | Release target missed | Measure baseline first; if gap remains, document measured reason in `FINDINGS.md` and log any target revision in `ARCHITECTURE_LOG.md` | open |
| R02 | Registering two similar plugins in one OBS could clash on source IDs / docks | Feature loss, broken scene collections | Namespace separation locked (#2); verify both DLLs load and both canvases work with matching scenes | open |
| R03 | Scene collections saved by upstream reference fork's source IDs | Migration friction | Provide documented JSON id-rewrite utility; do not alias legacy IDs (would recreate clash) | open |
| R04 | OBS 33 runtime vs OBS 31.1.0 build SDK could hide ABI issues | Crash / wrong behaviour | Every experiment runs in portable OBS 33.0.0 with parity checks; record version | mitigated by baseline load test |
| R05 | Benchmark noise could exceed the deltas we hope to find | False findings | `exp_000` measures noise margin before any optimization; no claim below margin | open |
| R06 | Driven OBS via OBS-MCP may be flaky (crash dialog, WS port conflicts) | Wasted runs / bad data | Reset portable copy per run; verified clean launch after plugin stubs; check `obs_log_tail` before accepting a run | mitigated |
| R07 | Optimization could break parity | Release blocked | Run affected parity rows before every merge; never merge a win that drops a feature | open |
| R08 | GitHub issues inherited as disabled from upstream | Cannot track work | Enabled explicitly on fork via GitHub API | resolved 2026-11-25 |
| R09 | Local folder typo `Wormhole-verticla` | Confusing paths | Renamed to `Wormhole-vertical`; OpenCode session moved | resolved 2026-11-25 |
| R10 | Upstream repo could change under us | Merge conflicts | `upstream` remote kept; pin baseline commit; pull deliberately, never force-push | open |
