# HARNESS — benchmark and OBS control

The harness makes both plugins observable and reproducible without a human.
It drives OBS through **OBS-MCP** (`E:\__PROJECTS__\OBS-MCP`, MIT, external
tool, used as-is) and stores raw results under `benchmarks/`. Python tooling
uses `@dataclass` configs only — never `argparse`.

## Layout (planned)

```
harness/
  config/*.toml              typed configs for OBS-MCP and benchmark runs
  bench_config.py            @dataclass config objects with defaults
  run_benchmark.py           scenario runner -> benchmarks/*.csv|json
  setup_benchmark_obs.ps1    install matching scenes/profiles into portable OBS
  compare.py                 median/min/max and noise-margin analysis
benchmarks/
  fixtures/                  scene collection + profile for deterministic runs
  raw/                       git-ignored CSV/JSON/ETL/PresentMon output
exp_NNN/HYPOTHESIS.md        written before the experiment
exp_NNN/FINDINGS.md          written after, including negative results
```

## OBS-MCP usage

OBS-MCP speaks JSON-RPC 2.0 over stdio, one request per line. Start it with:

```bat
E:\__PROJECTS__\OBS-MCP\build\obs-mcp.exe --config harness\config\obs-mcp.toml
```

Tools used here: `obs_list_instances`, `obs_launch`, `obs_terminate`,
`obs_cpu_stats`, `obs_ws_call`, `obs_log_tail`, `wait_ms`. Example request:

```json
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"obs_ws_call","arguments":{"name":"wormhole","request":"{\"op\":6,\"d\":{\"requestType\":\"GetStats\",\"requestId\":1}}"}}}
```

Every run starts from a fresh portable OBS copy, checks `obs_log_tail` for
plugin errors, and discards runs that show a crash dialog or missing module.

## Deterministic fixtures

- Both plugin canvases receive **matching multi-scene sets** created through
  `obs_ws_call` (`CreateScene`, `CreateInput`, `SetSceneItemTransform`).
- Sources: colour/image sources, a fixed media-file loop, and one fixed
  browser source. No network-dependent live content.
- Warm-up 10 s, measure 60 s, 5 runs; median with min/max; outliers recorded.

## Metrics per scenario

See [PERFORMANCE_TARGETS.md](PERFORMANCE_TARGETS.md). In short: process CPU
(total and per-thread), OBS render time, GPU engine utilization (3D, Copy,
Video Encode, Video Decode), VRAM, system RAM, encoder lag, dropped/skipped/
missed frames, and OBS WebSocket stats via OBS-MCP. Windows collectors: PDH
counters / PowerShell process sampling, ETW/WPA where a detailed trace is
needed, PresentMon for present timing, OBS's own stats/profiler, NVIDIA tooling
for GPU counters.

## Evidence rules

- Raw machine-readable results are git-ignored; a small structured summary is
  promoted into `exp_NNN/FINDINGS.md`.
- `exp_000` measures the noise margin first. No delta smaller than that margin
  is ever claimed as a finding.
- Every claim links to a committed result or a findings file.
