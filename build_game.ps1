# 2048 Game Build Script
# Usage: .\build_game.ps1

param(
    [switch]$SkipClean
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  2048 Game Build Tool" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check environment
Write-Host "[1/4] Checking environment..." -ForegroundColor Yellow

try {
    $pythonVersion = python --version 2>&1
    Write-Host "  OK Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Python not found" -ForegroundColor Red
    exit 1
}

# Step 2: Clean old files
Write-Host "[2/4] Cleaning old files..." -ForegroundColor Yellow

if (-not $SkipClean) {
    @("build", "dist") | ForEach-Object {
        $path = Join-Path $ProjectRoot $_
        if (Test-Path $path) {
            Remove-Item -Recurse -Force $path
            Write-Host "  Deleted $_" -ForegroundColor Gray
        }
    }
    Write-Host "  Done" -ForegroundColor Green
}

# Step 3: Build
Write-Host "[3/4] Building..." -ForegroundColor Yellow

Push-Location $ProjectRoot
try {
    & pyinstaller --onefile --windowed --name 2048 --clean --noconfirm --exclude-module matplotlib --exclude-module pandas --exclude-module scipy src\main.py
    if ($LASTEXITCODE -ne 0) { throw "Build failed" }
} finally {
    Pop-Location
}

# Step 4: Create shortcut
Write-Host "[4/4] Creating shortcut..." -ForegroundColor Yellow

$ExePath = Join-Path $ProjectRoot "dist\2048.exe"
if (Test-Path $ExePath) {
    $WScriptShell = New-Object -ComObject WScript.Shell
    $DesktopPath = [Environment]::GetFolderPath("Desktop")
    $Shortcut = $WScriptShell.CreateShortcut("$DesktopPath\2048_Game.lnk")
    $Shortcut.TargetPath = $ExePath
    $Shortcut.WorkingDirectory = $ProjectRoot
    $Shortcut.Save()
    Write-Host "  OK Shortcut created" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  BUILD SUCCESSFUL" -ForegroundColor Green
Write-Host "  Output: dist\2048.exe" -ForegroundColor Green
Write-Host "  Shortcut: 2048_Game.lnk" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
