# Verify that aitum-vertical and wormhole-vertical load together with no
# identifier collisions and with two distinct canvases.
# Copyright (C) 2026 Wormhole-vertical contributors
# SPDX-License-Identifier: GPL-2.0-or-later
[CmdletBinding()]
param(
    [string] $Portable = 'obs-portable',
    [int] $SettleSeconds = 18
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$portable = Join-Path $root $Portable
$logDir = Join-Path $portable 'config\obs-studio\logs'

$running = Get-Process obs64 -ErrorAction SilentlyContinue
if ($running) { Stop-Process -Id $running.Id -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2 }
Get-ChildItem $logDir -Filter '*.txt' -ErrorAction SilentlyContinue | Remove-Item -Force

$proc = Start-Process -FilePath (Join-Path $portable 'bin\64bit\obs64.exe') `
    -WorkingDirectory (Join-Path $portable 'bin\64bit') -ArgumentList '--portable' -PassThru
Start-Sleep -Seconds 8

Add-Type -AssemblyName UIAutomationClient
$rootUi = [System.Windows.Automation.AutomationElement]::RootElement
$cond = New-Object System.Windows.Automation.PropertyCondition(
    [System.Windows.Automation.AutomationElement]::NameProperty, 'OBS Studio Crash Detected')
$dlg = $rootUi.FindFirst([System.Windows.Automation.TreeScope]::Children, $cond)
if ($dlg) {
    $btn = $dlg.FindFirst([System.Windows.Automation.TreeScope]::Descendants,
        (New-Object System.Windows.Automation.PropertyCondition(
            [System.Windows.Automation.AutomationElement]::NameProperty, 'Run in Normal Mode')))
    if ($btn) { $btn.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke() }
}
Start-Sleep -Seconds $SettleSeconds

$log = Get-ChildItem $logDir -Filter '*.txt' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $log) { throw 'No OBS log produced' }
$text = Get-Content $log.FullName -Raw

$loaded = ([regex]::Matches($text, 'loaded version 1\.6\.8')).Count
$collisions = ([regex]::Matches($text, 'already exists')).Count
$whCanvas = $text -match "Canvas 'Wormhole Vertical' scenes:"
$avCanvas = $text -match "Canvas 'Aitum Vertical' scenes:"
$errors = ([regex]::Matches($text, 'Plugin Errors|Failed to initialize module .*vertical')).Count

Write-Output "log=$($log.Name) loaded=$loaded collisions=$collisions wormhole_canvas=$whCanvas aitum_canvas=$avCanvas errors=$errors"

$running = Get-Process obs64 -ErrorAction SilentlyContinue
if ($running) { $running.CloseMainWindow() | Out-Null; Start-Sleep -Seconds 5 }
$running = Get-Process obs64 -ErrorAction SilentlyContinue
if ($running) { Stop-Process -Id $running.Id -Force -ErrorAction SilentlyContinue }

if ($loaded -lt 2 -or $collisions -ne 0 -or -not $whCanvas -or -not $avCanvas -or $errors -ne 0) {
    throw 'Side-by-side verification FAILED'
}
Write-Output 'Side-by-side verification PASSED'
