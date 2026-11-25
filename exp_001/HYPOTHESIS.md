# exp_001 — Cache overlay vertex buffers instead of recreating per frame

**Written before the experiment. Issue
[#8](https://github.com/limapedro/Wormhole-vertical/issues/8).**

## What we expect

When a scene item is selected (or crop handles are visible), the preview
overlay code creates and destroys a `gs_vertbuffer_t` for every line, every
stripe and the rotation handle on every frame. We expect this to show up as
per-frame CPU time and/or driver-side allocations, and that caching one
reusable buffer per shape (updated with `gs_render_start`/`gs_render_save`
only when geometry changes) will reduce OBS CPU measurably with no visual
change.

## Why (source evidence, not yet a finding)

- `DrawStripedLine` loops `ceil(dist / 15)` times and calls
  `gs_render_start`, `gs_render_save`, `gs_load_vertexbuffer` and
  `gs_vertexbuffer_destroy` **per stripe per frame** —
  `vertical-canvas.cpp:2667-2709`.
- `DrawLine` and `DrawRotationHandle` each create and destroy a vertex buffer
  per call — `:2627-2665`, `:2230-2248`.
- `DrawSelectedItem` early-outs when no item is selected (`:2782-2786`), so
  this cost only appears in editor interaction scenarios. An idle benchmark
  will *not* confirm or refute it.

## What would prove us wrong

- A profile with one selected item shows no measurable time in
  `gs_render_start`/`gs_render_save`/`gs_vertexbuffer_destroy`; or
- vertex-buffer allocation rate is flat before and after the change; or
- the CPU delta is smaller than the noise margin measured in `exp_000`.

## Method

1. Confirm with a CPU sampling profile (WPA/xperf or a sampling profiler)
   while a scene item with crop handles is selected in the vertical preview.
2. Add a benchmark scenario with a selected item; run upstream and fork with
   the same scene set.
3. Implement the smallest cache that preserves every drawn pixel: one
   reusable dynamic vertex buffer per shape, rebuilt only when its geometry
   changes.
4. Re-run the matrix, compare with the noise margin, and run the preview/editor
   parity rows (`V53`–`V61`) before merge.
5. Write `FINDINGS.md`, including a negative result if the profile is flat.

No code is changed until step 1 produces evidence.
