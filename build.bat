@echo off
title 2048 Game Builder
color 0A

echo ============================================================
echo        2048 Game Build Tool
echo ============================================================
echo.

echo [1/3] Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo Done.
echo.

echo [2/3] Building with PyInstaller...
pyinstaller --onefile --windowed --name 2048 --clean --noconfirm --exclude-module matplotlib --exclude-module pandas --exclude-module scipy src\main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo [3/3] Creating desktop shortcut...
cscript //nologo "%~dp0create_shortcut.vbs"

echo.
echo ============================================================
echo        BUILD SUCCESSFUL!
echo.
echo        Output: dist\2048.exe
echo        Desktop shortcut: 2048 Game.lnk
echo ============================================================
echo.
pause
