# Create matching, deterministic multi-scene sets in both vertical canvases.
# Copyright (C) 2026 Wormhole-vertical contributors
# SPDX-License-Identifier: GPL-2.0-or-later
[CmdletBinding()]
param([string] $Config = 'harness/config/obs-mcp.toml')

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$colors = @('0x4C403CFF', '0x3C4C40FF', '0x403C4CFF')
$canvases = @(
    @{ Canvas = 'Wormhole Vertical'; Prefix = 'WH Bench' },
    @{ Canvas = 'Aitum Vertical'; Prefix = 'AV Bench' }
)

$calls = [System.Collections.Generic.List[string]]::new()
foreach ($c in $canvases) {
    for ($i = 1; $i -le 3; $i++) {
        $scene = "$($c.Prefix) $i"
        $req = @{ op = 6; d = @{ requestType = 'CreateScene'; requestId = ($i * 10); requestData = @{ sceneName = $scene; canvasName = $c.Canvas } } } | ConvertTo-Json -Compress -Depth 8
        $calls.Add((@{ name = 'obs_ws_call'; arguments = @{ name = 'wormhole'; request = $req } } | ConvertTo-Json -Compress -Depth 8))
        $settings = @{ color = $colors[$i - 1]; width = 1080; height = 1920 }
        $req2 = @{ op = 6; d = @{ requestType = 'CreateInput'; requestId = ($i * 10 + 1); requestData = @{ sceneName = $scene; inputName = "$scene Color"; inputKind = 'color_source_v3'; inputSettings = $settings; sceneItemEnabled = $true; canvasName = $c.Canvas } } } | ConvertTo-Json -Compress -Depth 10
        $calls.Add((@{ name = 'obs_ws_call'; arguments = @{ name = 'wormhole'; request = $req2 } } | ConvertTo-Json -Compress -Depth 8))
    }
}

& (Join-Path $root 'scripts\obs_mcp_call.ps1') -ToolCall $calls -Config $Config
