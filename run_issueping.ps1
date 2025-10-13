Set-Location -Path "E:\IssuePing"

# Activate venv (PowerShell activation script)
if (Test-Path "$PSScriptRoot\.venv\Scripts\Activate.ps1") {
    . "$PSScriptRoot\.venv\Scripts\Activate.ps1"
}

# Run IssuePing
# Ensure logs directory exists
$logDir = Join-Path $PSScriptRoot 'logs'
if (-Not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

$timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
$logFile = Join-Path $logDir 'issueping.log'

# Rotate logs older than LOG_RETENTION_DAYS (default: 7)
$retention = [int]($env:LOG_RETENTION_DAYS -as [int])
if (-not $retention) { $retention = 7 }
$cutoff = (Get-Date).AddDays(-$retention)
Get-ChildItem -Path $logDir -File | Where-Object { $_.LastWriteTime -lt $cutoff } | ForEach-Object { Remove-Item $_.FullName -Force }

# Run and capture output
$proc = Start-Process -FilePath python -ArgumentList '-m issueping' -RedirectStandardOutput "$logFile.tmp" -RedirectStandardError "$logFile.err" -NoNewWindow -PassThru -Wait

# Append to log with timestamp
Add-Content -Path $logFile -Value "----- Run at: $timestamp -----"
if (Test-Path "$logFile.tmp") {
    Get-Content "$logFile.tmp" | Add-Content -Path $logFile
    Remove-Item "$logFile.tmp"
}
if (Test-Path "$logFile.err") {
    "--- STDERR ---" | Add-Content -Path $logFile
    Get-Content "$logFile.err" | Add-Content -Path $logFile
    Remove-Item "$logFile.err"
}

