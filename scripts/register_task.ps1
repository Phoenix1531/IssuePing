# Registers a Scheduled Task 'IssuePing' that runs every 10 minutes
$taskName = 'IssuePing'
$scriptPath = 'E:\IssuePing\run_issueping.ps1'

$action = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 10) -RepetitionDuration ([TimeSpan]::MaxValue)

# Register the task to run with highest privileges
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -RunLevel Highest -Force

Write-Host "Scheduled task '$taskName' registered."
