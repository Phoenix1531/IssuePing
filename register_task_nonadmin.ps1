# Registers a Scheduled Task 'IssuePing' for the current user using schtasks (no admin required)
$taskName = 'IssuePing'
$scriptPath = 'Powershell -NoProfile -ExecutionPolicy Bypass -File "E:\IssuePing\run_issueping.ps1"'

Write-Host "Creating task '$taskName' to run every 10 minutes (current user)."

$cmd = "schtasks /Create /SC MINUTE /MO 10 /TN \"$taskName\" /TR \"$scriptPath\" /F"
Write-Host "Running: $cmd"
Invoke-Expression $cmd

Write-Host "Querying task status..."
schtasks /Query /TN $taskName /V /FO LIST
