# Dismiss the OBS crash-recovery dialog by choosing "Run in Normal Mode".
# Copyright (C) 2026 Wormhole-vertical contributors
# SPDX-License-Identifier: GPL-2.0-or-later
Add-Type -AssemblyName UIAutomationClient
$root = [System.Windows.Automation.AutomationElement]::RootElement
$cond = New-Object System.Windows.Automation.PropertyCondition(
    [System.Windows.Automation.AutomationElement]::NameProperty, 'OBS Studio Crash Detected')
$dlg = $root.FindFirst([System.Windows.Automation.TreeScope]::Children, $cond)
if ($dlg) {
    $btn = $dlg.FindFirst([System.Windows.Automation.TreeScope]::Descendants,
        (New-Object System.Windows.Automation.PropertyCondition(
            [System.Windows.Automation.AutomationElement]::NameProperty, 'Run in Normal Mode')))
    if ($btn) {
        $btn.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
        Write-Output 'dismissed'
    }
}
