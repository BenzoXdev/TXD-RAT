# TXD - by benzoXdev
# Disables SmartScreen to allow .exe execution

# Check if running as administrator
If (-Not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script must be run with administrator privileges." -ForegroundColor Red
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    Exit
}

# SmartScreen registry path
$regPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer"

If (Test-Path $regPath) {
    Set-ItemProperty -Path $regPath -Name "SmartScreenEnabled" -Value "Off"
    Write-Host "SmartScreen disabled successfully." -ForegroundColor Green
} Else {
    Write-Host "SmartScreen registry key not found." -ForegroundColor Yellow
}
