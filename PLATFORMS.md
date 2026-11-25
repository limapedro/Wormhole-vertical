# PLATFORMS — Wormhole-vertical

## Test machine (authoritative for all performance numbers)

See [PERFORMANCE_TARGETS.md](PERFORMANCE_TARGETS.md) for the full table.
Summary: i5-12400F, GTX 1660 SUPER 6 GB, 32 GB RAM, Windows 10 Pro
`26300.10075`, driver `32.0.16.2101`. The portable OBS used for all benchmarks
was updated to **33.0.3** on 2026-11-25; the system install remains 33.0.0
because the session has no administrator rights. **All performance numbers
come from this machine.**

## Windows

- Primary development and test platform. Required CI job.
- Configure: `cmake --preset windows-x64 -G "Visual Studio 18 2026"` (the
  upstream preset names VS 17 2022, which is not installed here; the generator
  override is a command-line choice, not a source change).
- Build: `cmake --build build_x64 --config RelWithDebInfo --parallel`.
- Stage: `cmake --install build_x64 --config RelWithDebInfo --prefix staging`.
- Test target: disposable portable OBS under `obs-portable/`, launched with
  `--portable`, driven by OBS-MCP over stdio JSON-RPC and OBS WebSocket v5.
- Release artifact: a zip whose root contains `obs-plugins/64bit/*.dll` and
  `data/obs-plugins/*`, so unzipping into the OBS folder installs it.

## Linux

- Build via `cmake --preset ubuntu-x86_64` in CI (`ubuntu-latest`). Upstream
  CI installs Qt6 and OBS dependencies with apt; keep those steps.
- Functional/parity checks run headlessly where practical; performance numbers
  from CI are never compared to the Windows machine without normalization.
- Anything unverifiable on real hardware is mirrored into
  [RISKS.md](RISKS.md).

## macOS

- Build via `cmake --preset macos` (Xcode, universal) in CI. Codesigning and
  notarization secrets belong to CI only, never to this repo.
- No real-hardware performance numbers; build/functional only.

## OBS version policy

- Latest stable OBS is the runtime target. Record **exact** runtime version,
  driver and Windows build in every benchmark result.
- The buildspec pins OBS 31.1.0 SDK headers; that is a build dependency, not
  the runtime target. Upstream 1.6.8 was verified to load on OBS 33.0.0.
