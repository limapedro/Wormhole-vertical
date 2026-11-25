# Send tool calls to the external OBS-MCP server and print JSON-RPC responses.
# Copyright (C) 2026 Wormhole-vertical contributors
# SPDX-License-Identifier: GPL-2.0-or-later
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string[]] $ToolCall,
    [string] $Config = 'harness/config/obs-mcp.toml',
    [string] $Server = 'E:/__PROJECTS__/OBS-MCP/build/obs-mcp.exe'
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$configPath = Join-Path $root $Config
if (-not (Test-Path $configPath)) { $configPath = $Config }

$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add('{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"wormhole-vertical","version":"1"}}}')
$id = 1
foreach ($raw in $ToolCall) {
    $call = $raw | ConvertFrom-Json
    $payload = @{
        jsonrpc = '2.0'
        id      = $id
        method  = 'tools/call'
        params  = @{ name = $call.name; arguments = $call.arguments }
    } | ConvertTo-Json -Compress -Depth 12
    $lines.Add($payload)
    $id++
}

$lines | & $Server --config $configPath 2>&1
