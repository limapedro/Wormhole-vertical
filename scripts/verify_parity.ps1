# Automated parity spot-checks for both plugins through OBS-MCP / WebSocket.
# Copyright (C) 2026 Wormhole-vertical contributors
# SPDX-License-Identifier: GPL-2.0-or-later
[CmdletBinding()]
param([string] $Config = 'harness/config/obs-mcp.toml')

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$calls = [System.Collections.Generic.List[string]]::new()
$id = 100

function Add-Ws([string] $requestType, [hashtable] $data = @{}) {
    $script:id++
    $req = @{ op = 6; d = @{ requestType = $requestType; requestId = $script:id; requestData = $data } } | ConvertTo-Json -Compress -Depth 10
    $script:calls.Add((@{ name = 'obs_ws_call'; arguments = @{ name = 'wormhole'; request = $req } } | ConvertTo-Json -Compress -Depth 10))
}

Add-Ws 'GetCanvasList'
Add-Ws 'GetSceneList' @{ canvasName = 'Wormhole Vertical' }
Add-Ws 'GetSceneList' @{ canvasName = 'Aitum Vertical' }
Add-Ws 'GetHotkeyList'
foreach ($vendor in @('wormhole-vertical', 'aitum-vertical-canvas')) {
    $script:id++
    $req = @{ op = 6; d = @{ requestType = 'CallVendorRequest'; requestId = $script:id; requestData = @{ vendorName = $vendor; requestType = 'version'; requestData = @{} } } } | ConvertTo-Json -Compress -Depth 10
    $script:calls.Add((@{ name = 'obs_ws_call'; arguments = @{ name = 'wormhole'; request = $req } } | ConvertTo-Json -Compress -Depth 10))
}

& (Join-Path $root 'scripts\obs_mcp_call.ps1') -ToolCall $calls -Config $Config
