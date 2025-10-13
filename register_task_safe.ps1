# Register a Scheduled Task 'IssuePing' that repeats every 10 minutes for 7 days (safe)
$taskName = 'IssuePing'
$scriptPath = 'E:\IssuePing\run_issueping.ps1'

Write-Host "Registering scheduled task '$taskName' to run $scriptPath every 10 minutes (7 day repetition)"

$action = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File \"$scriptPath\""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 10) -RepetitionDuration (New-TimeSpan -Days 7)

try {
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -RunLevel Highest -Force
    Write-Host "Scheduled task '$taskName' registered."
    Get-ScheduledTask -TaskName $taskName | Select-Object TaskName, State, LastRunTime, NextRunTime
} catch {
    Write-Error "Failed to register task: $_"
}
