# FEATURE PARITY — Wormhole-vertical vs Aitum Vertical 1.6.8

Built by reading the source of the unmodified fork at `baseline-upstream`
(`d7e88a5`, upstream release 1.6.8), **not** from memory. Every row has a
file:line citation and a test method. Legend:
`unverified` (default) | `confirmed` (source-derived) | `verified` (confirmed
with executed test evidence linked). Parity is a hard requirement: a speedup
that drops a row does not count.

Both plugins are installed side by side in the test OBS; each row must pass for
`aitum-vertical` and `wormhole-vertical` with the same scene set. A shared test
fixture is described in [HARNESS.md](HARNESS.md).

| ID | Area | Feature | Evidence | Test method | Status |
|---|---|---|---|---|---|
| V01 | Canvas lifecycle | Module load guard: refuses to load if `aitum-stream-suite` is installed | `vertical-canvas.cpp:639-644` | Simulate suite present, load plugin, check log; no docks appear | confirmed |
| V02 | Canvas lifecycle | Registers `vertical_audio_wrapper_source` and `vertical_multi_canvas_source` plus frontend event callback | `vertical-canvas.cpp:646-651`, `audio-wrapper-source.c:90-100`, `multi-canvas-source.c:188-198` | Enumerate source types via API; both IDs present | confirmed |
| V03 | Canvas lifecycle | Canvas created at `obs_module_post_load` from `config.json`; default dock `VerticalCanvas` if empty | `vertical-canvas.cpp:673-711`, `data/manifest.json:1-16` | Delete config.json, restart; one dock appears and config written | confirmed |
| V04 | Canvas lifecycle | Multiple canvas docks from config array | `vertical-canvas.cpp:700-710` | Seed 2 canvas entries; confirm 2 docks (note shared-canvas caveat) | confirmed |
| V05 | Canvas naming | Canvas name hard-coded `Aitum Vertical`; no rename UI | `vertical-canvas.cpp:56`, `:5250-5260`, `:1780-1784` | Confirm no rename control; `obs_enum_canvases()` name constant | confirmed |
| V06 | Canvas lifecycle | Restores settings incl. default 1080×1920, odd dims rounded up, first-run backtrack=true | `vertical-canvas.cpp:1020-1057`, `:1099-1101` | Fresh install → 1080×1920 + backtrack on; odd config dims round up | confirmed |
| V07 | Canvas lifecycle | Destructor removes projectors, unregisters 9 hotkeys, releases outputs/encoders/services, removes canvas, frees GPU buffers | `vertical-canvas.cpp:1651-1865` | Close OBS while streaming/recording; assert clean shutdown | confirmed |
| V08 | Persistence | `save_canvas()` writes docks to config.json with tmp/bak safe write | `vertical-canvas.cpp:92-122`, `:5470-5480`, `:7896` | Change setting, close OBS, inspect config.json | confirmed |
| V09 | Persistence | Scene-collection save callback stores per-scene `order` and `canvas_active` | `vertical-canvas.cpp:9137-9171`, `:1648`, `:1653` | Reorder scenes, save/reload, verify order and active scene | confirmed |
| V10 | Docks | Companion docks `VerticalCanvasDockScenes`, `...Sources`, `...Transitions` | `vertical-canvas.cpp:1169-1182` | View → Dock list; 4 vertical docks, visibility persists | confirmed |
| V11 | Docks | First-run layout splits docks around main docks then saves config | `vertical-canvas.cpp:7811-7897` | Fresh config → docks docked right and split | confirmed |
| V12 | Docks | Optional inline scenes combo with linked-scene toggle and add/remove (`scenes_row`) | `vertical-canvas.cpp:975-1011`, `:1166-1168` | Enable setting, restart, exercise combo | confirmed |
| V13 | Docks | Scenes grid mode toggle persisted as `grid_mode` | `scenes-dock.cpp:13-38`, `vertical-canvas.cpp:7173` | Right-click → Grid mode; restart; persists | confirmed |
| V14 | Docks | Preview disable with placeholder/Enable button, context menu and hotkey | `vertical-canvas.cpp:1099`, `:1245-1261`, `:3583-3588`, `:8314-8349` | Disable via right-click, restart, re-enable via button/hotkey | confirmed |
| V15 | Scenes | Add scene with unique name, hotkey, rename hook, switches to it | `vertical-canvas.cpp:798-865` | Add scene with duplicate name; auto-suffix and selection | confirmed |
| V16 | Scenes | Duplicate scene with `OBS_SCENE_DUP_REFS` | `vertical-canvas.cpp:822-828`, `scenes-dock.cpp:45-51` | Duplicate; sources are shared refs | confirmed |
| V17 | Scenes | Remove scene with confirmation | `vertical-canvas.cpp:867-888`, `scenes-dock.cpp:52-58` | Cancel then confirm; list updated only on confirm | confirmed |
| V18 | Scenes | Rename via `NameDialog` (170 char max, trim, uniqueness loop), F2/Return | `name-dialog.cpp:40-53`, `scenes-dock.cpp:59-82`, `:284-315` | Rename to existing name repeats; trim spaces; F2 | confirmed |
| V19 | Scenes | Rename propagation to linked main scenes and labels | `vertical-canvas.cpp:7679-7735` | Rename linked scene; link target string updates | confirmed |
| V20 | Scenes | Scene reorder via context menu and toolbar up/down/top/bottom | `scenes-dock.cpp:83-91`, `:362-369`, `:379-407` | Reorder, save/reload, verify `order` | confirmed |
| V21 | Scenes | Switch scene on list selection and combo | `scenes-dock.cpp:264-273`, `vertical-canvas.cpp:979` | Click scene; preview and tree switch | confirmed |
| V22 | Scenes | `SwitchScene`: override resolution, duration fallback, transition_stop, vendor event | `vertical-canvas.cpp:7496-7624` | Set 500 ms override; switch; watch WS event | confirmed |
| V23 | Scenes | Linked scenes per main scene stored in `canvas` array | `scenes-dock.cpp:171-217`, `vertical-canvas.cpp:890-927`, `:8140-8184` | Link A→X, B→Y; switch main; verify vertical follows | confirmed |
| V24 | Scenes | "Show on main canvas" action | `scenes-dock.cpp:219-235` | Right-click vertical scene; main preview/program changes | confirmed |
| V25 | Scenes | Per-scene `show_in_multiview` private setting | `scenes-dock.cpp:237-244` | Toggle; inspect private settings | confirmed |
| V26 | Scenes | Scene filters dialog and screenshot | `scenes-dock.cpp:93-114`, `:346-360` | Add filter; take screenshot | confirmed |
| V27 | Scenes | Transition Override submenu, duration 50–20000 ms | `scenes-dock.cpp:116-169` | Set override; verify private settings | confirmed |
| V28 | Scenes | Scene migration adopts main custom-size scenes, removes groups, preserves order | `vertical-canvas.cpp:7423-7486` | Create legacy scene, reload, verify moved | confirmed |
| V29 | Scenes | Scene cleanup on collection change; auto-add default scene if empty | `vertical-canvas.cpp:137-156`, `:7294-7309`, `:7737-7789` | Switch collections; empty canvas gets default scene | confirmed |
| V30 | Scenes | Diagnostic `LogScenes()` | `vertical-canvas.cpp:9173-9273` | Trigger collection change; inspect log block | confirmed |
| V31 | Sources | Add-source popup with categories, deprecated, scenes, groups, existing sources | `vertical-canvas.cpp:5157-5206`, `:5065-5124` | Open Add menu; verify categories and ordering | confirmed |
| V32 | Sources | Canvas-requiring sources under per-canvas submenus; existing source adds reference | `vertical-canvas.cpp:5100-5109`, `:5126-5129`, `:5225-5236` | Add existing main source into vertical scene; verify shared | confirmed |
| V33 | Sources | New source with unique numbered name and properties dialog | `vertical-canvas.cpp:5208-5242` | Create two Color Sources; names increment | confirmed |
| V34 | Sources | Remove source with confirmation incl. group subitems | `sources-dock.cpp:83-154`, `:215-225` | Select 2 sources; verify multi-remove message | confirmed |
| V35 | Sources | Rename via F2/Return `NameDialog` with canvas-aware uniqueness | `sources-dock.cpp:36-67`, `vertical-canvas.cpp:3322-3345` | Rename to existing name loops; verify | confirmed |
| V36 | Sources | Toolbar: Add, Remove, Filters, Properties, Move Up/Down | `sources-dock.cpp:71-193` | Exercise each toolbar button | confirmed |
| V37 | Sources | Context menu aggregate: Add, Copy/Paste, Rename, Remove, Order, Transform, Scale, Blending, Transitions, Projector, Screenshot, Filters, Properties | `sources-dock.cpp:204-212`, `vertical-canvas.cpp:3319-3572` | Right-click source; verify all submenus | confirmed |
| V38 | Sources | Transform submenu: edit/reset/rotate/flip/fit/stretch/center | `vertical-canvas.cpp:3372-3466` | Apply each; verify transform state | confirmed |
| V39 | Sources | Scale filtering: Disable, Point, Bilinear, Bicubic, Lanczos, Area | `vertical-canvas.cpp:3470-3495` | Set each; get scale filter | confirmed |
| V40 | Sources | Blending modes and methods | `vertical-canvas.cpp:3497-3544` | Set each; verify OBS state | confirmed |
| V41 | Sources | Show/Hide transitions with duration and properties shortcut | `vertical-canvas.cpp:8890-8970` | Assign show transition; hide/show item | confirmed |
| V42 | Sources | Copy / Paste Reference / Paste Duplicate via OBS ≥32.2 dynamic lookup | `vertical-canvas.cpp:9332-9371` | Copy and paste both ways on OBS 33 | confirmed |
| V43 | Source tree | Tree with group expand/collapse, drag reorder and move into groups | `source-tree.cpp:913-1027`, `:1142-1431` | Drag onto group and collapsed group | confirmed |
| V44 | Source tree | Group/Ungroup helpers implemented | `source-tree.cpp:899-978`, `:1582-1598` | **Uncertain UI wiring** — verify via context menu or direct slot call | unverified |
| V45 | Source tree | Visibility and lock checkboxes with accessibility names | `source-tree.cpp:128-190`, `:244-262` | Toggle eye/lock; verify preview item state | confirmed |
| V46 | Source tree | Reacts to OBS signals (remove, visible, locked, select, rename, reorder) | `source-tree.cpp:304-332`, `:224-302` | Change each via API; tree updates live | confirmed |
| V47 | Source tree | Hover highlights item in vertical preview (mutex-protected) | `source-tree.cpp:362-383`, `vertical-canvas.cpp:2757-2768` | Hover rows; observe outline | confirmed |
| V48 | Source tree | Double-click opens properties; Windows snap-to workaround | `source-tree.cpp:334-360` | Enable snap-to; double-click; no hang | confirmed |
| V49 | Source tree | Color labels from private settings and 8 theme colors | `source-tree.cpp:88-101`, `:1052-1060` | Set label; verify row tint | confirmed |
| V50 | Source tree | Empty-state "No Sources" message | `source-tree.cpp:1600-1648` | Remove all; verify text | confirmed |
| V51 | Source tree | Add/reorder/refresh signals queue model updates; removal logs and saves | `vertical-canvas.cpp:8490-8544`, `source-tree.cpp:1569-1580` | Add/reorder/remove; verify order and log | confirmed |
| V52 | Source tree | Source-type icons incl. group/scene | `source-tree.cpp:29-78`, `vertical-canvas.cpp:8387-8436` | Add each type; verify icons | confirmed |
| V53 | Preview | Draw callback: letterboxed render, black backdrop, linear-sRGB, overflow, safe areas, selection | `vertical-canvas.cpp:2052-2159`, `:1884-2050` | Resize preview; verify overlays | confirmed |
| V54 | Preview | Safe-area guides 3.5/5/16.25%, toggle | `display-helpers.hpp:59-113`, `vertical-canvas.cpp:2105-2117` | Enable setting; verify 6 lines | confirmed |
| V55 | Preview | Pixel spacing helpers with live labels via private text sources | `vertical-canvas.cpp:2285-2400`, `:2418-2588` | Select item; verify labels while stretching | confirmed |
| V56 | Preview | Overflow indicator honoring three user config modes | `vertical-canvas.cpp:1884-2016`, `:1500-1509` | Toggle OBS overflow settings | confirmed |
| V57 | Preview | Selection/crop/hover colors respect Accessibility overrides | `vertical-canvas.cpp:2898-2928` | Enable overrides; verify colors | confirmed |
| V58 | Preview | Mouse editor: select, Ctrl-toggle, box, move, stretch, Alt-crop, rotate+snap | `vertical-canvas.cpp:3018-3091`, `:3574-3682`, `:4039-4288` | Exercise gestures | confirmed |
| V59 | Preview | Snapping to edges/center/items, Ctrl disables | `vertical-canvas.cpp:4290-4383`, `:4546-4591` | Drag near edges; verify snap | confirmed |
| V60 | Preview | Arrow nudge 1 px / Shift 10 px; Delete removes with confirm | `vertical-canvas.cpp:1202-1240`, `:8595-8620` | Press keys; verify movement/dialog | confirmed |
| V61 | Preview | Right-click menu: disable preview, projectors, lock, screenshot, add, copy/paste, item menu | `vertical-canvas.cpp:3574-3618` | Open menu with/without selection | confirmed |
| V62 | Toolbar | Stream all, per-output multi-menu, Record, Save backtrack, Backtrack on/off, Virtual camera, status, settings, links | `vertical-canvas.cpp:1263-1496` | Hover/click each; verify tooltips/actions | confirmed |
| V63 | Toolbar | Live duration timers (1 s and 4 s) | `vertical-canvas.cpp:1418-1451` | Start record/stream; watch counters | confirmed |
| V64 | Toolbar | Multi-output dropdown per-output and all start/stop | `vertical-canvas.cpp:6496-6524` | Configure 2 outputs; use menu | confirmed |
| V65 | Errors | Record/stream error dialogs incl. bad path, encode, no-space, TikTok, HDR, disconnect | `vertical-canvas.cpp:7962-7993`, `:8031-8115` | Force failures; verify messages | confirmed |
| V66 | Errors | Auto-remux integration via `RecordingFileChanged` | `vertical-canvas.cpp:7908-7943`, `:7995-8016` | Record mkv with AutoRemux; confirm notification | confirmed |
| V67 | Streaming | `StartVideo()` canvas creation, downstream keyer registration, channel 0, reset | `vertical-canvas.cpp:5244-5289` | Start stream; verify canvas dims and keyer | confirmed |
| V68 | Streaming | `StartStream()` all enabled outputs with shared encoders; no-output warning | `vertical-canvas.cpp:6834-7034` | Disable all outputs; verify dialog | confirmed |
| V69 | Streaming | Per-output advanced settings via aitum-multistream (encoder, frame divisor, GPU scaling) | `vertical-canvas.cpp:6526-6656`, `:6875-6976` | With plugin installed; set settings | confirmed |
| V70 | Streaming | Output type selection rtmp/ftl/ffmpeg by URL scheme | `vertical-canvas.cpp:6658-6748` | Use rtmp/ftl/https URLs; verify IDs | confirmed |
| V71 | Streaming | WHIP service for URLs containing "whip" (3 paths) | `vertical-canvas.cpp:1067-1069`, `:9046-9047`, `config-dialog.cpp:1354-1355` | Enter whip URL; verify service | confirmed |
| V72 | Streaming | Stream delay enable/duration/preserve per output | `vertical-canvas.cpp:6733-6741`, `:1393-1406` | Set 5 s; verify delayed output | confirmed |
| V73 | Streaming | Bind IP / IP family copied from main profile | `vertical-canvas.cpp:6725-6731`, `:7014-7019` | Set bind IP; verify output settings | confirmed |
| V74 | Streaming | Aitum Multistream proc integration and warning in Streaming tab | `vertical-canvas.cpp:243-275`, `:536-549`, `config-dialog.cpp:329`, `:1188-1207` | Install plugin; verify controls hidden/warning | confirmed |
| V75 | Streaming | Per-output start/stop/query and runtime key/server update procs | `vertical-canvas.cpp:277-320`, `:8874-8888` | Call procs; verify output | confirmed |
| V76 | Recording | Output selection: `mp4_output` hybrid else `ffmpeg_muxer`; simple clones main | `vertical-canvas.cpp:5590-5677` | Set hybrid_mp4 then mkv; verify IDs | confirmed |
| V77 | Recording | Filename `-vertical` suffix, extension map, dir creation, split limits | `vertical-canvas.cpp:5710-5761` | Start record; verify filename/split settings | confirmed |
| V78 | Recording | Audio encoders per track; simple clones main and force-inits | `vertical-canvas.cpp:5821-5932` | Set 3 tracks; verify 3 AAC encoders | confirmed |
| V79 | Recording | Signals, pause/unpause, chapter, split | `vertical-canvas.cpp:5783-5811`, `:8284-8312`, `:8351-8385` | Trigger via hotkeys; verify segments/markers | confirmed |
| V80 | Backtrack | Auto-start when main/vertical stream, record, replay or vcam active; always-on; hotkeys | `vertical-canvas.cpp:948-973`, `:1341-1396`, `:8438-8488` | Start main stream; verify backtrack starts | confirmed |
| V81 | Backtrack | Advanced duration/path/format vs cloning main; `Replay`→`Backtrack` rewrite + `-backtrack` | `vertical-canvas.cpp:5956-6067` | Start both modes; verify filename/duration | confirmed |
| V82 | Backtrack | Encoder reuse from recording output or multitrack stream encoder | `vertical-canvas.cpp:6073-6118`, `:6237-6253` | Record then backtrack; verify shared encoder | confirmed |
| V83 | Backtrack | Save with optional filename, `get_last_replay`, status and events | `vertical-canvas.cpp:5482-5511`, `:7995-8016`, `:475-490` | Save via button and WS with filename | confirmed |
| V84 | Virtual camera | Modes Vertical, Main, Both (composite `vertical_multi_canvas_source`) | `vertical-canvas.cpp:5349-5455`, `vertical-canvas.hpp:33-35` | Test each mode; verify resolution/layout | confirmed |
| V85 | Virtual camera | Uses main OBS vcam output, first-use warning, signals/events, cleanup | `vertical-canvas.cpp:5352-5365`, `:5291-5311`, `:5457-5468` | Start/stop; verify no stale source | confirmed |
| V86 | Multi-canvas source | Renders main program then each canvas into texrender, translates, color-space aware | `multi-canvas-source.c:58-126` | Enable Both vcam; verify composite frame | confirmed |
| V87 | Multi-canvas source | Add/remove canvas, dedupe, size recomputation | `multi-canvas-source.c:140-186` | Add 2 canvases; verify get_width/height | confirmed |
| V88 | Audio wrapper | Forwards target audio mix with mask/timestamp; enumerates as child | `audio-wrapper-source.c:23-65`, `:67-88` | Verify audio not double-mixed | confirmed |
| V89 | Audio wrapper | Private+muted, bound to transition source, occupies free program channel, removed on destroy | `vertical-canvas.cpp:1633-1646`, `:7325-7332`, `:1668-1678` | Inspect program channels; shutdown | confirmed |
| V90 | Outputs | Activity queries for status and replay logic | `vertical-canvas.cpp:7140-7163`, `:441-457` | Call status in each output state | confirmed |
| V91 | Hotkeys | Backtrack start/stop + save | `vertical-canvas.cpp:1348-1381`, `:1610-1626` | Assign/fire; verify | confirmed |
| V92 | Hotkeys | Virtual camera start/stop | `vertical-canvas.cpp:1521-1532`, `:8186-8214` | Assign/fire; verify | confirmed |
| V93 | Hotkeys | Recording start/stop | `vertical-canvas.cpp:1534-1545`, `:8216-8244` | Assign/fire; verify | confirmed |
| V94 | Hotkeys | Streaming start/stop | `vertical-canvas.cpp:1547-1558`, `:8246-8282` | Assign/fire with 2 outputs | confirmed |
| V95 | Hotkeys | Pause/unpause recording | `vertical-canvas.cpp:1560-1573`, `:8284-8312` | Fire while recording | confirmed |
| V96 | Hotkeys | Show/hide preview | `vertical-canvas.cpp:1575-1588`, `:8314-8349` | Fire; verify placeholder | confirmed |
| V97 | Hotkeys | Add chapter marker | `vertical-canvas.cpp:1590-1599`, `:8351-8367` | Fire while recording; verify chapter | confirmed |
| V98 | Hotkeys | Split recording file | `vertical-canvas.cpp:1601-1608`, `:8369-8385` | Fire while recording; verify segment | confirmed |
| V99 | Hotkeys | Per-scene SelectScene hotkeys | `vertical-canvas.cpp:836-850`, `:7372-7392` | Assign and fire; verify switch | confirmed |
| V100 | Hotkey UI | Multi-combo widget, add/remove/clear/revert, duplicate warning, keyboard+mouse capture | `hotkey-edit.cpp:28-52`, `:206-230`, `:295-390` | Bind mouse/modifier; check warning and save | confirmed |
| V101 | Projectors | Preview projector windowed/fullscreen, Esc/close | `vertical-canvas.cpp:8782-8857`, `projector.cpp:54-111` | Open both; press Esc | confirmed |
| V102 | Projectors | Aspect-preserving letterboxed projector render | `projector.cpp:16-36`, `:149-177` | Resize window; verify letterbox | confirmed |
| V103 | Projectors | Context menu: fullscreen monitors, windowed, resize, always-on-top, close | `projector.cpp:122-147`, `:179-211`, `:284-355` | Toggle each option | confirmed |
| V104 | Projectors | Source projector fullscreen per monitor + window | `vertical-canvas.cpp:3552-3561`, `:8859-8872` | Open both; verify | confirmed |
| V105 | Projectors | Monitor enumeration with friendly names | `vertical-canvas.cpp:8813-8851`, `projector.cpp:357-434` | Open menu; verify labels | confirmed |
| V106 | Projectors | Multiview flag per scene (OBS core renders multiview) | `scenes-dock.cpp:237-244` | Toggle flag; verify OBS multiview | confirmed |
| V107 | Settings | 5 tabs General/Streaming/Recording/Help/Support, min 983×480 | `config-dialog.cpp:30-117`, `:945-986` | Open gear; verify tabs/resize | confirmed |
| V108 | Settings | Resolution combo with 7 presets + custom | `config-dialog.cpp:140-150` | Enter 900×1600; verify resize | confirmed |
| V109 | Settings | Audio bitrate 64–320 (default 160) | `config-dialog.cpp:152-165` | Set 256; verify encoder | confirmed |
| V110 | Settings | Virtual camera mode and Draw Safe Areas | `config-dialog.cpp:167-176` | Change; verify preview/vcam | confirmed |
| V111 | Settings | Backtrack group: enable, duration, path, hotkeys, guide | `config-dialog.cpp:178-274` | Browse path; set duration/hotkeys | confirmed |
| V112 | Settings | Streaming server rows incl. YouTube presets, enabled, password show/hide | `config-dialog.cpp:329-355`, `:1086-1140` | Add 3 servers; toggle show key | confirmed |
| V113 | Settings | Streaming bitrate + match-main, start/stop hotkeys | `config-dialog.cpp:357-397` | Change bitrate; enable match | confirmed |
| V114 | Settings | Streaming delay group with reactive enable | `config-dialog.cpp:401-432` | Toggle Enable; verify dependents | confirmed |
| V115 | Settings | Streaming advanced: use main, tracks 1–6, encoder combo with dynamic properties | `config-dialog.cpp:434-531`, `:1613-1937` | Choose each encoder; verify widgets | confirmed |
| V116 | Settings | Multistream warning and multitrack-video status label | `config-dialog.cpp:536-556`, `:1176-1186` | Toggle multitrack; reopen settings | confirmed |
| V117 | Settings | Recording path, bitrate, match-main, split by time/size | `config-dialog.cpp:582-644` | Set both limits; verify output | confirmed |
| V118 | Settings | Recording hotkeys start/stop, pause, chapter, split | `config-dialog.cpp:646-740` | Assign all; verify saved | confirmed |
| V119 | Settings | Recording advanced filename formatting, illegal-char filter, file formats | `config-dialog.cpp:744-816` | Enter illegal chars; verify stripped | confirmed |
| V120 | Settings | Recording advanced tracks 1–6 and encoder + "Use stream encoder" | `config-dialog.cpp:818-880` | Select tracks/encoder; verify config | confirmed |
| V121 | Settings | Help/Support tab URLs | `config-dialog.cpp:889-943` | Click buttons; verify URLs | confirmed |
| V122 | Settings | OK vs Cancel, version/ attribution footer, new-version warning | `config-dialog.cpp:945-984`, `:1144-1147` | Cancel unchanged; OK changed | confirmed |
| V123 | Settings | Resolution change side effects: stop replay, reset video, resize transition, reload scenes | `config-dialog.cpp:1261-1290` | Change while backtrack active | confirmed |
| V124 | Settings | Live bitrate updates without restart | `config-dialog.cpp:1296-1323`, `:1504-1523` | Change bitrate; inspect encoders | confirmed |
| V125 | Settings | Settings disabled while outputs active | `config-dialog.cpp:1149-1156` | Start recording; verify disabled | confirmed |
| V126 | Updater | Async HTTPS version check with GUID to Aitum API; callback on UI thread | `vertical-canvas.cpp:713-720`, `file-updater.c:125-144` | Mock endpoint; verify thread joins | confirmed |
| V127 | Updater | Semantic version comparison, tinted button and new-version label | `vertical-canvas.cpp:8654-8675` | Serve newer version; verify UI | confirmed |
| V128 | Updater | Update prompt with Update/Remind/Skip, 14-day block | `vertical-canvas.cpp:9275-9330` | Serve newer version; click Skip; restart | confirmed |
| V129 | Updater | Partner promo blocks (link/button/image) with 14-day suppression | `vertical-canvas.cpp:8678-8731`, `:9389-9423` | Serve partnerBlocks; close; restart | confirmed |
| V130 | Platform | CMake in/out-of-tree, Qt6, libcurl, GuiPrivate, source list | `CMakeLists.txt:1-97` | Configure/build both modes | confirmed |
| V131 | Platform | Resources: Aitum logo + 8 SVG icons under `/aitum` | `resources.qrc:1-13` | Inspect binary resources/icons | confirmed |
| V132 | Platform | 10 locale files bundled | `data/locale/*.ini` | Switch OBS language; verify strings | confirmed |
| V133 | WS vendor API | Vendor `aitum-vertical-canvas` registered/unregistered | `vertical-canvas.cpp:722-748`, `:753-775` | GetVendorRequests; verify vendor | confirmed |
| V134 | WS request | `version` → PROJECT_VERSION | `vertical-canvas.cpp:377-382` | Call; assert 1.6.8 | confirmed |
| V135 | WS request | `switch_scene` all docks, error if missing | `vertical-canvas.cpp:384-397` | Call with name and empty | confirmed |
| V136 | WS request | `current_scene` with optional width/height filter | `vertical-canvas.cpp:399-417` | Call with/without dims | confirmed |
| V137 | WS request | `get_scenes` array of `{name}` | `vertical-canvas.cpp:419-439` | Compare to dock list | confirmed |
| V138 | WS request | `status` booleans | `vertical-canvas.cpp:441-457` | Start each output; call | confirmed |
| V139 | WS request | `start_streaming` | `vertical-canvas.cpp:733`, `:6834` | Call; confirm outputs | confirmed |
| V140 | WS request | `stop_streaming` | `vertical-canvas.cpp:734`, `:7036` | Call; confirm stop | confirmed |
| V141 | WS request | `toggle_streaming` | `vertical-canvas.cpp:735`, `:6481` | Call twice | confirmed |
| V142 | WS request | `start_recording` | `vertical-canvas.cpp:736`, `:5590` | Call; confirm record | confirmed |
| V143 | WS request | `stop_recording` | `vertical-canvas.cpp:737`, `:5774` | Call; confirm stop | confirmed |
| V144 | WS request | `toggle_recording` | `vertical-canvas.cpp:738`, `:5581` | Call twice | confirmed |
| V145 | WS request | `start_backtrack` | `vertical-canvas.cpp:739`, `:5956` | Call; confirm | confirmed |
| V146 | WS request | `stop_backtrack` | `vertical-canvas.cpp:740`, `:6452` | Call; confirm | confirmed |
| V147 | WS request | `save_backtrack` with optional filename | `vertical-canvas.cpp:475-490`, `:741` | Call with filename; verify clip | confirmed |
| V148 | WS request | `start_virtual_camera` | `vertical-canvas.cpp:742`, `:5349` | Call; confirm | confirmed |
| V149 | WS request | `stop_virtual_camera` | `vertical-canvas.cpp:743`, `:5457` | Call; confirm | confirmed |
| V150 | WS request | `update_stream_key` at index | `vertical-canvas.cpp:492-519`, `:744` | Call; verify next stream | confirmed |
| V151 | WS request | `update_stream_server` at index | `vertical-canvas.cpp:521-549`, `:745` | Call with whip URL | confirmed |
| V152 | WS request | `add_chapter` | `vertical-canvas.cpp:551-577`, `:746` | Call while recording | confirmed |
| V153 | WS request | `pause_recording` | `vertical-canvas.cpp:579-598`, `:747` | Call while recording | confirmed |
| V154 | WS request | `unpause_recording` | `vertical-canvas.cpp:600-619`, `:748` | Call while paused | confirmed |
| V155 | WS event | `switch_scene` with width/height/old/new | `vertical-canvas.cpp:7602-7610` | Subscribe; switch; inspect payload | confirmed |
| V156 | WS event | 4 streaming events, stopped includes code/last_error | `vertical-canvas.cpp:7006`, `:7056`, `:7047`, `:7070` | Subscribe; start/stop; verify order | confirmed |
| V157 | WS event | 4 recording events | `vertical-canvas.cpp:5763`, `:5787`, `:5778`, `:5801` | Subscribe; start/stop | confirmed |
| V158 | WS event | 6 backtrack events | `vertical-canvas.cpp:6126`, `:6467`, `:5510`, `:5817`, `:6457`, `:6477` | Subscribe; start/save/stop | confirmed |
| V159 | WS event | 4 virtual camera events | `vertical-canvas.cpp:5437`, `:5295`, `:5463`, `:5304` | Subscribe; start/stop | confirmed |
| V160 | WS event | All vendor events carry width/height | `vertical-canvas.cpp:8546-8559` | Subscribe to any; verify payload | confirmed |
| V161 | Proc handler | `aitum_vertical_get_video` | `vertical-canvas.cpp:653`, `:229-241` | Call; verify pointer | confirmed |
| V162 | Proc handler | get/set stream settings | `vertical-canvas.cpp:654-657`, `:243-275` | Round-trip; verify unchanged | confirmed |
| V163 | Proc handler | get/start/stop stream output by name | `vertical-canvas.cpp:658-663`, `:277-320` | Call each; verify state | confirmed |
| V164 | Proc handler | `aitum_vertical_add_chapter` | `vertical-canvas.cpp:664-665`, `:322-345` | Call while recording | confirmed |
| V165 | Proc handler | get/switch scene | `vertical-canvas.cpp:666-668`, `:347-373` | Call; verify active scene | confirmed |
| V166 | Integration | Downstream keyer add/remove canvas with transition callback | `vertical-canvas.cpp:5261-5268`, `:1780-1784`, `:8972-8981` | With keyer plugin; start vcam | confirmed |
| V167 | Integration | Frontend event bridge main outputs → vertical backtrack/ match-main, 200–250 ms retries | `vertical-canvas.cpp:178-226`, `:8438-8488` | Toggle main outputs; verify | confirmed |
| V168 | Integration | Main transition_start signal → MainSceneChanged | `vertical-canvas.cpp:124-129`, `:146-164` | Switch main scene; verify link | confirmed |
| V169 | Display helper | `OBSQTDisplay` native surface lifecycle, color-space updates | `qt-display.cpp:26-63`, `:79-115`, `:171-243` | Move projector between monitors | confirmed |
| V170 | Misc | Modal dialogs, 200×100 min, 170-char names, trimming | `name-dialog.cpp:7-25`, `:40-53` | Open rename dialogs; verify constraints | confirmed |

## Known gaps to verify before release

- V44: group/ungroup helpers exist but no UI wiring was found; verify on a live
  build before treating as missing upstream functionality.
- Several helpers are defined but apparently unused (`SetIconsVisible`,
  `MultipleBaseSelected`, `ShowScenes`, `HelpSupport`, `Canvas`,
  `VirtualCam` locale strings, empty Appearance/Audio/Video icons). These are
  upstream traits, not regressions; record them as confirmed-or-N/A.

## Performance hypothesis seeds

The source study found candidate waste sites: per-frame vertex-buffer
allocation for guide/selection lines (`vertical-canvas.cpp:2230-2248`,
`:2655-2896`), private text-source updates for pixel labels (`:2285-2587`),
an extra texrender pass per canvas in multi-canvas mode
(`multi-canvas-source.c:58-126`), vestigial `texrender`/`stagesurface` members
(`vertical-canvas.hpp:152-153`), a 1 s polling timer (`:1418-1447`), many
`QTimer::singleShot(200-500 ms)` workarounds, and a startup libcurl thread
(`file-updater.c:101-144`). These are recorded in
[HYPOTHESES_BACKLOG.md](HYPOTHESES_BACKLOG.md) and must be profiled before any
code change.
