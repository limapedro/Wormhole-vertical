# GOAL — Wormhole-vertical

## Mission

Provide everything Aitum Vertical (obs-vertical-canvas) does, in the same OBS
Studio install, while using so little CPU and GPU that the user does not feel
the plugin is there. Fork upstream, study it, and remove waste one measured
experiment at a time. "Should be faster" is not a finding.

## Success definition

Wormhole-vertical is successful when **all three** are true:

1. **Parity:** every row in [FEATURE_PARITY.md](FEATURE_PARITY.md) is marked
   `verified` with a linked test or capture, using matching multi-scene sets in
   both plugins.
2. **Resource ceiling:** every scenario in
   [PERFORMANCE_TARGETS.md](PERFORMANCE_TARGETS.md) is at **under 1% total CPU**
   (stretch: 0.5%), or the gap is documented with measured evidence and a
   reason in `FINDINGS.md`. Relative reduction versus upstream is reported in
   every benchmark table as a secondary metric.
3. **Coexistence:** upstream `aitum-vertical` and `wormhole-vertical` can be
   installed and run in the same OBS without identifier collisions, with
   matching scenes, and neither plugin's parity regresses.

Parity and correctness gate efficiency: a fast plugin that drops a feature or
breaks side-by-side use is not a success.

## Priorities (strict order)

1. Feature parity with Aitum Vertical.
2. Measured resource reduction toward the absolute ceiling.
3. Clean coexistence and migration support.

Lower-priority work does not start while a higher-priority item is blocked
unless the blocker is recorded in [RISKS.md](RISKS.md) and the issue is labelled
`blocked`.

## Explicit non-goals

- Reimplementing the vertical canvas from scratch. This is a fork of upstream
  code, not a clean-room rewrite.
- Changing upstream behaviour for taste, or dropping features to gain speed.
- Replacing OBS's core canvas/encoder/output system.
- Reusing Wormhole's network protocol, discovery or transport code. The shared
  heritage here is methodology and test tooling only.
- Windows-only design: platform-specific work stays behind small interfaces;
  Linux and macOS build in CI as far as practical.
- Claiming any number that has not been measured on the test machine.

## Scope of "same functions"

Feature parity is judged from the source-derived checklist in
[FEATURE_PARITY.md](FEATURE_PARITY.md), which includes at minimum: the vertical
canvas dock and its scenes/sources/transitions docks; scene and source handling;
streaming and recording from the canvas; replay buffer and backtrack; virtual
camera; hotkeys; projectors; multi-output/WHIP streaming; settings; OBS
WebSocket vendor API; audio wrapper sources; and the file updater.

## Method

Read [ARCHITECTURE_LOG.md](ARCHITECTURE_LOG.md) for locked decisions,
[ROADMAP.md](ROADMAP.md) for the ordered experiment list,
[PROGRESS.md](PROGRESS.md) for current status, and
[HYPOTHESES_BACKLOG.md](HYPOTHESES_BACKLOG.md) for untested ideas. Every
measurement has `exp_NNN/HYPOTHESIS.md` written first and `FINDINGS.md` written
after, including failures.
