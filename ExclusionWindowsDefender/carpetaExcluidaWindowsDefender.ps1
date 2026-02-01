# TXD - by benzoXdev
# Creates a folder excluded from Windows Defender to store the .exe

$currentDir = Get-Location

# Folder name to create
$folderName = "Excluded"  # Change this if you want a different name

$exclusionPath = Join-Path -Path $currentDir -ChildPath $folderName

# Create folder if it doesn't exist
If (-Not (Test-Path -Path $exclusionPath)) {
    New-Item -Path $exclusionPath -ItemType Directory -Force
    Write-Host "Folder '$exclusionPath' created." -ForegroundColor Green
} Else {
    Write-Host "Folder '$exclusionPath' already exists." -ForegroundColor Yellow
}

# Add folder to Windows Defender exclusions
Add-MpPreference -ExclusionPath $exclusionPath
Write-Host "Folder '$exclusionPath' added to Windows Defender exclusions." -ForegroundColor Green
