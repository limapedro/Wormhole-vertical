# exp_003 — Do not create a canvas video mix until an output needs one

**Written before the experiment. Issue
[#9](https://github.com/limapedro/Wormhole-vertical/issues/9).**

## What we expect

At startup `OBS_FRONTEND_EVENT_FINISHED_LOADING` calls `CanvasDock::LoadScenes()`,
which calls `StartVideo()` (`vertical-canvas.cpp:154-168`, `:7336`, `:7356`).
`StartVideo()` calls `obs_canvas_reset_video()` when
`obs_canvas_has_video()` is false (`:5293-5302`), which creates a video mix
and a continuously running 30 fps render path even when no stream, recording,
replay buffer or virtual camera is active. We expect that creating only the
canvas (with `ovi = nullptr`, which creates no mix —
`libobs/obs-canvas.c:162-174`) and deferring `obs_canvas_reset_video()` to the
output start paths (which already call `StartVideo()`) will cut the plugin's
idle CPU substantially.

## Why (source evidence, not yet a finding)

- `obs_frontend_add_canvas(name, nullptr, PROGRAM)` creates no mix
  (`obs-canvas.c:162-174`), so a canvas by itself is cheap.
- `StartVideo()` is called from every output start path (vcam `:5388`,
  recording `:5704`, backtrack `:6086`, per-output stream `:6544`,
  stream `:6874`) — those calls still create the mix when actually needed.
- `LoadScenes()` (`:7356`) and the projector open path (`:8774`) call it
  without any output active.

## What would prove us wrong

- Idle CPU does not drop by more than the `exp_000` noise margin (about 12%
  CoV on OBS's own CPU metric); or
- OBS still creates a mix for the canvas through another path; or
- Streaming/recording/backtrack/vcam parity fails, or the preview stops
  rendering, or scene hotkeys/linked scenes break.

## Method

1. Baseline: the `exp_000` run already contains 5 idle `S0-fork` runs with the
   unmodified fork DLL.
2. Split `StartVideo()` into `EnsureCanvas()` (canvas creation, keyer
   registration, channel 0, no mix) and `StartVideo()` (EnsureCanvas +
   `obs_canvas_reset_video`). Use `EnsureCanvas()` in `LoadScenes()` and in
   the projector path; leave every output start path on `StartVideo()`.
3. Build, restage, re-run the idle scenario 5 times with the same fixture.
4. Run parity checks: canvas/scene list, preview draw, WS vendor `version`,
   start/stop stream, record, backtrack and vcam.
5. Write `FINDINGS.md` with measured before/after and a decision to merge or
   revert. A negative result is kept.
