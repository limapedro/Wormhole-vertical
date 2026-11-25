# Regenerate git-ignored benchmark plugin binaries from pinned sources:
#   - upstream 1.6.8 release zip in .deps/ (downloaded once by setup)
#   - locally built fork DLL in staging/ (from cmake --install)
# Copyright (C) 2026 Wormhole-vertical contributors
# SPDX-License-Identifier: GPL-2.0-or-later
[CmdletBinding()]
param([switch] $Download)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$store = Join-Path $root 'benchmarks\plugins'
$deps = Join-Path $root '.deps'
$zip = Join-Path $deps 'aitum-vertical-1.6.8.zip'
$upstreamDir = Join-Path $deps 'aitum-vertical-1.6.8\vertical-canvas'

if ($Download -and -not (Test-Path $zip)) {
    Invoke-WebRequest -Uri 'https://github.com/Aitum/obs-vertical-canvas/releases/download/1.6.8/vertical-canvas-windows-programdata.zip' -OutFile $zip -UseBasicParsing
}
if (-not (Test-Path $upstreamDir)) {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [IO.Compression.ZipFile]::ExtractToDirectory($zip, (Join-Path $deps 'aitum-vertical-1.6.8'))
}
if (-not (Test-Path $upstreamDir)) { throw "upstream plugin not staged at $upstreamDir" }

New-Item -ItemType Directory -Force $store | Out-Null
Copy-Item (Join-Path $upstreamDir 'bin\64bit\vertical-canvas.dll') (Join-Path $store 'vertical-canvas.dll') -Force
robocopy (Join-Path $upstreamDir 'data') (Join-Path $store 'vertical-canvas') /E /NFL /NDL /NJH /NJS /NP | Out-Null

$ours = Join-Path $root 'staging\wormhole-vertical'
if (-not (Test-Path (Join-Path $ours 'bin\64bit\wormhole-vertical.dll'))) {
    throw "build the fork first: cmake --install build_x64 --config RelWithDebInfo --prefix staging"
}
Copy-Item (Join-Path $ours 'bin\64bit\wormhole-vertical.dll') (Join-Path $store 'wormhole-vertical.dll') -Force
robocopy (Join-Path $ours 'data') (Join-Path $store 'wormhole-vertical') /E /NFL /NDL /NJH /NJS /NP | Out-Null

Get-ChildItem $store -Filter '*.dll' | Select-Object Name,Length | Format-Table -AutoSize
Write-Output "Staged benchmark plugins into $store"
