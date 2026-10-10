<#
.SYNOPSIS
Register the unattended-run watchdog as a Windows Scheduled Task.

.DESCRIPTION
Creates a task that runs scripts/watchdog.py every -IntervalMinutes for
-DurationHours. A healthy run makes every firing a no-op; a stalled one gets
restarted from its run log.

The task runs whether or not the user is logged on, and only on AC power.
It does NOT wake the machine: a sleeping or hibernating computer runs nothing,
so this script reports the current sleep settings and the command to change
them rather than changing power policy behind your back. The 2026-08-30 run
this exists because of had HIBERNATEIDLE set to 90 minutes while its own
preconditions claimed otherwise — check the value, do not trust the claim.

.EXAMPLE
./install-watchdog-windows.ps1 -Project C:\src\photo-culling -DryRun

.EXAMPLE
./install-watchdog-windows.ps1 -Project C:\src\photo-culling -IntervalMinutes 20 -DurationHours 12
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Project,
    [int]$IntervalMinutes = 20,
    [int]$DurationHours = 12,
    [int]$StaleAfterSeconds = 1200,
    [string]$TaskName,
    [string]$Python = "python",
    [string]$NotifyCmd,
    [double]$MaxBudgetUsd,
    [switch]$DryRun,
    [switch]$Uninstall
)

$ErrorActionPreference = "Stop"

$projectPath = (Resolve-Path $Project).Path
$watchdog = Join-Path $PSScriptRoot "watchdog.py"
if (-not (Test-Path $watchdog)) { throw "watchdog.py not found beside this script at $watchdog" }

if (-not $TaskName) {
    $TaskName = "agent-crew watchdog - " + (Split-Path $projectPath -Leaf)
}

if ($Uninstall) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "removed scheduled task: $TaskName"
    return
}

$argList = @(
    "`"$watchdog`""
    "--project"; "`"$projectPath`""
    "--stale-after"; $StaleAfterSeconds
)
if ($NotifyCmd)    { $argList += @("--notify-cmd", "`"$NotifyCmd`"") }
if ($MaxBudgetUsd) { $argList += @("--max-budget-usd", $MaxBudgetUsd) }
$arguments = $argList -join " "

Write-Host "task name : $TaskName"
Write-Host "command   : $Python $arguments"
Write-Host "cadence   : every $IntervalMinutes minutes for $DurationHours hours"
Write-Host ""

# Report sleep policy rather than changing it. A watchdog cannot fire on a
# machine that has gone to sleep, and this is the setting that silently ends
# long unattended runs.
Write-Host "current AC sleep settings (both must read 0x00000000 for an overnight run):"
foreach ($setting in @("STANDBYIDLE", "HIBERNATEIDLE")) {
    $line = (powercfg -q SCHEME_CURRENT SUB_SLEEP $setting |
             Select-String "Current AC Power Setting Index").ToString().Trim()
    Write-Host "  $setting  $line"
}
Write-Host "  fix, from an elevated console:"
Write-Host "    powercfg /setacvalueindex SCHEME_CURRENT SUB_SLEEP STANDBYIDLE 0"
Write-Host "    powercfg /setacvalueindex SCHEME_CURRENT SUB_SLEEP HIBERNATEIDLE 0"
Write-Host "    powercfg /setactive SCHEME_CURRENT"
Write-Host ""

if ($DryRun) {
    Write-Host "dry run - nothing registered."
    return
}

$action = New-ScheduledTaskAction -Execute $Python -Argument $arguments -WorkingDirectory $projectPath
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
    -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes) `
    -RepetitionDuration (New-TimeSpan -Hours $DurationHours)
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries:$false `
    -StopIfGoingOnBatteries `
    -WakeToRun:$false `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2)

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
    -Settings $settings -Description "Restarts a stalled agent-crew unattended run in $projectPath" `
    -Force | Out-Null

Write-Host "registered: $TaskName"
Write-Host ""
Write-Host "Fire it once before relying on it — an untested trigger is indistinguishable"
Write-Host "from a working one until the night it matters:"
Write-Host "    Start-ScheduledTask -TaskName `"$TaskName`""
Write-Host "    Get-ScheduledTaskInfo -TaskName `"$TaskName`""
Write-Host ""
Write-Host "Remove it when the run is done:"
Write-Host "    ./install-watchdog-windows.ps1 -Project `"$projectPath`" -Uninstall"
