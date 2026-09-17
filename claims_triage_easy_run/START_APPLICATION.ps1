$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$host.UI.RawUI.WindowTitle = "AI Claims Triage Prototype"
Write-Host "AI-DRIVEN CLAIMS TRIAGE PROTOTYPE" -ForegroundColor Cyan
Write-Host ""
$python = $null
if (Get-Command py -ErrorAction SilentlyContinue) { $python = "py" }
elseif (Get-Command python -ErrorAction SilentlyContinue) { $python = "python" }
if (-not $python) {
    Write-Host "Python was not found." -ForegroundColor Red
    Write-Host "Install Python 3 and select 'Add Python to PATH'."
    Write-Host "https://www.python.org/downloads/"
    Read-Host "Press Enter to close"
    exit 1
}
Write-Host "Python detected: $python" -ForegroundColor Green
Start-Job -ScriptBlock { Start-Sleep -Seconds 2; Start-Process "http://localhost:8000" } | Out-Null
& $python -u -m app.server
Read-Host "Application stopped. Press Enter to close"
