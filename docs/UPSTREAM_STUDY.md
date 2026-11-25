# UPSTREAM STUDY — Aitum/obs-vertical-canvas 1.6.8

Source-derived study of the unmodified fork at `baseline-upstream` (`d7e88a5`).
Everything below is **code reading**, not a measured finding. Each candidate
waste site must be profiled before a code change; negative results are recorded
in `FINDINGS.md` and never deleted. Issue #6.

## 1. How the vertical canvas is created and drawn

- `obs_module_load()` registers the frontend event callback and two private
  source types (`wormhole_vertical_audio_wrapper_source`,
  `wormhole_vertical_multi_canvas_source` in the fork; upstream uses the
  `vertical_*` ids) — `vertical-canvas.cpp:639-651`.
- `obs_module_post_load()` reads `config.json` (from `obs_module_config_path`),
  creates one `CanvasDock` per configured canvas, or a default one if the
  array is empty, then registers the four docks with
  `obs_frontend_add_dock_by_id` — `vertical-canvas.cpp:673-711`, `:1169-1182`.
- The canvas itself is created lazily in `StartVideo()`:
  `obs_frontend_add_canvas(CANVAS_NAME, nullptr, PROGRAM)` — `:5244-5268`.
  Upstream's canvas name is hard-coded `Aitum Vertical` (`:56`); the fork uses
  `Wormhole Vertical` so both can coexist. The canvas is registered with the
  downstream keyer on start and removed on destroy (`:5261-5268`, `:1780-1784`).
- Each dock embeds an `OBSQTDisplay` (native surface, paint engine disabled,
  recreated on move/display/color-space change) — `qt-display.cpp:26-63`,
  `:79-115`, `:171-243`, `:250-260`.
- `CanvasDock::DrawPreview()` is the per-frame callback — `:2064-2171`.

## 2. Per-frame work in `DrawPreview()`

In order:

1. Scale/centre calculation (`GetScaleAndCenterPos`) — `:2080`.
2. `DrawOverflow(scale)` — tiled overflow indicator effect — `:2099`,
   `:1884-2016`.
3. `DrawBackdrop(newCX, newCY)` — black quad behind the canvas — `:2101`,
   `:2119-2159`.
4. `gs_set_linear_srgb(true)` + `obs_canvas_render(canvas)` — the actual
   vertical scene render — `:2103-2111`.
5. Six safe-area guide renders when enabled — `:2117-2129`.
6. `obs_scene_enum_items(..., DrawSelectedItem, ...)` — full item enumeration
   with matrix math for selection outlines — `:2137-2142`.
7. Selection box with a lazily-created quad vertex buffer — `:2144-2158`.
8. `DrawSpacingHelpers()` — up to four private text sources (`N px` labels)
   and distance lines — `:2164-2167`, `:2285-2587`.

So even a completely idle dock executes at least three extra draw passes
(overflow, backdrop, canvas) plus overlays, and several are implemented with
per-frame allocations (below).

## 3. Extra render passes and texture copies

- **Normal preview:** one `obs_canvas_render()` into the dock's swapchain.
- **Virtual camera "Both" mode:** `multi_canvas_source` renders all main
  program outputs first (`:62-76`), then for every registered canvas performs
  a `gs_texrender_reset` / `begin_with_color_space` / `clear` /
  `obs_canvas_render` / `end` / `gs_draw_sprite` sequence — one full extra
  render target per canvas per frame — `multi-canvas-source.c:84-124`.
  Width becomes main base width + sum of canvas widths; height is the max —
  `:140-154`. This is a legitimate composite, not obviously redundant, and
  must be profiled before touching.
- **Scaling/colour conversion:** preview uses `gs_set_linear_srgb` and
  viewport-relative `gs_ortho`; the multi-canvas path uses
  `gs_get_format_from_space(gs_get_color_space())` and recreates a texrender
  when the format changes, then `gs_effect_set_texture_srgb` —
  `multi-canvas-source.c:86-120`.

## 4. GPU → CPU readbacks

No active readback was found. `CanvasDock` declares `gs_texrender_t *texrender`
and `gs_stagesurf_t *stagesurface` members (`vertical-canvas.hpp:152-153`) but
neither is referenced anywhere in the .cpp. This is a **negative result from
source reading**: hypothesis H02 should be confirmed or refuted with a GPU
trace, not assumed.

## 5. Encoders and outputs

- `StartStream()` iterates `streamOutputs` and creates one output per enabled
  server, sharing video/audio encoders where possible — `:6834-7034`.
- Output type is chosen by URL scheme (`rtmp_output`, `ftl_output`, ffmpeg
  muxer fallback; `whip_custom` service for WHIP URLs) — `:6658-6748`,
  `:1067-1069`.
- Recording uses `mp4_output` (hybrid_mp4) or `ffmpeg_muxer`, with a separate
  audio encoder per selected track and optional split files — `:5590-5932`.
- Backtrack (replay buffer) reuses the active recording or stream encoder when
  compatible — `:6073-6118`, `:6237-6253`.
- Virtual camera uses the **main** OBS virtualcam output; "Both" mode inserts
  the multi-canvas source — `:5349-5455`.
- Updater runs an HTTPS `curl` GET in a detached pthread at startup —
  `file-updater.c:101-144`; `update_info_destroy()` joins it.

## 6. Qt timers, threads and hidden work

- `recordDurationTimer`: 1 s repeating timer, always started; polls every
  stream output's frame count to update button text — `:1430-1459`.
- A 4 s timer resets status text — `:1449-1451`.
- Many `QTimer::singleShot(200/250/500 ms)` re-entrancy guards around output
  state and replay logic — `:185-220`, `:7953`, `:8114`, `:8136`,
  `config-dialog.cpp:1336`, `source-tree.cpp:351`.
- Scene/source tree subscribes to OBS signals and posts updates with
  `Qt::QueuedConnection` — `source-tree.cpp:304-332`,
  `vertical-canvas.cpp:8490-8544`.
- When the dock/preview is hidden, `obs_canvas_render()` still runs for active
  outputs and backtrack; the dock's preview display is disabled with a
  placeholder (`:1245-1261`) but the 1 s timer and updater thread remain.
- Destructor can busy-wait up to ~10 s (100 × 100 ms) for outputs to stop —
  `:1786-1809`.

## 7. Candidate waste sites (hypotheses, not findings)

| ID | Candidate | Evidence | Test before change |
|---|---|---|---|
| H01 | Per-frame vertex buffer churn for guides/selection lines | `DrawLine`/`DrawStripedLine` call `gs_render_start` + `gs_render_save` + `gs_vertexbuffer_destroy` per line; striped lines loop `ceil(dist/15)` — `:2655-2896` | GPU/CPU profile with many selected items; count buffer creates/sec |
| H02 | GPU→CPU readback or staging copy | vestigial `texrender`/`stagesurface` — `vertical-canvas.hpp:152-153` | Nsight/PresentMon trace; no readback found in source |
| H03 | Work while preview/dock hidden | 1 s timer always runs — `:1430-1459`; canvas still renders for outputs | A/B CPU with preview hidden vs visible via OBS-MCP |
| H04 | Per-frame allocation | `std::to_string` + `obs_source_update` only when px changes (`SetLabelText`, `:2297-2312`); vertex buffers above | Allocation sampler on render thread |
| H05 | Polling timers | 1 s + 4 s timers, singleShot guards | ETW timer callback sampling |
| H06 | UI/graphics lock contention | `hoveredPreviewItems` mutex — `source-tree.cpp:362-383`; queued signal updates | WPA wait analysis |
| H07 | Avoidable format conversion | texrender format recreation + sRGB toggles — `multi-canvas-source.c:86-120`, `vertical-canvas.cpp:2103-2111` | GPU frame capture in Both mode |
| H08 | Duplicated encoding | per-output encoders, replay encoder reuse logic — `:5821-5932`, `:6073-6118` | Encoder telemetry while streaming both canvases |

## 8. What is NOT waste

- `obs_canvas_render()` is required to produce vertical video; removing it
  would drop the canvas (parity failure).
- The multi-canvas composite in "Both" vcam mode is required functionality.
- The safe-area/overflow/editor overlays are user-visible features; H01 is
  about *how* they are drawn, not whether they exist.

Any optimization must keep every `FEATURE_PARITY.md` row green.
