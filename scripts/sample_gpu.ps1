# Sample Windows GPU engine utilization and local adapter memory for OBS.
# Copyright (C) 2026 Wormhole-vertical contributors
# SPDX-License-Identifier: GPL-2.0-or-later
[CmdletBinding()]
param(
    [int] $Samples = 3,
    [int] $IntervalMs = 1000
)

$ErrorActionPreference = 'Stop'
$engine = Get-Counter '\GPU Engine(*)\Utilization Percentage' -ErrorAction SilentlyContinue
$memory = Get-Counter '\GPU Local Adapter Memory(*)\Local Usage' -ErrorAction SilentlyContinue
$obs = Get-Process obs64 -ErrorAction SilentlyContinue

$result = [ordered]@{
    timestamp_utc = [DateTime]::UtcNow.ToString('o')
    obs_pid       = if ($obs) { $obs.Id } else { 0 }
    engine_3d     = 0.0
    engine_copy   = 0.0
    engine_encode = 0.0
    engine_decode = 0.0
    vram_bytes    = 0
}
if ($engine) {
    foreach ($set in $engine.CounterSamples) {
        $path = $set.Path
        $value = [double]$set.CookedValue
        if ($path -match 'engtype_3D') { $result.engine_3d += $value }
        elseif ($path -match 'engtype_Copy') { $result.engine_copy += $value }
        elseif ($path -match 'engtype_VideoEncode') { $result.engine_encode += $value }
        elseif ($path -match 'engtype_VideoDecode') { $result.engine_decode += $value }
    }
}
if ($memory) {
    foreach ($set in $memory.CounterSamples) {
        $result.vram_bytes += [int64]$set.CookedValue
    }
}
$result | ConvertTo-Json -Compress
