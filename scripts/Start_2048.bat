@echo off
chcp 65001 >nul
title 2048 Game

echo ==============================
echo        2048 Game Launcher
echo ==============================
echo.
echo Checking game files...

REM Check if executable exists
if not exist "dist\2048\2048.exe" (
    echo.
    echo Error: Game executable not found
    echo Path: dist\2048\2048.exe
    echo.
    echo Please ensure:
    echo 1. Game folder is complete
    echo 2. 2048.exe is in dist\2048\ directory
    echo.
    pause
    exit /b 1
)

echo.
echo Game files check passed!
echo Starting game...
echo.

REM Start game
start "" "dist\2048\2048.exe"

echo Game started!
echo If game didn't open, check Task Manager
echo.
timeout /t 3 >nul