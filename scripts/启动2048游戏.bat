@echo off
chcp 65001 >nul
title 2048 游戏

echo ==============================
echo        2048 游戏启动器
echo ==============================
echo.
echo 正在检查游戏文件...

REM 检查可执行文件是否存在
if not exist "dist\2048\2048.exe" (
    echo.
    echo 错误: 找不到可执行文件
    echo 路径: dist\2048\2048.exe
    echo.
    echo 请确保:
    echo 1. 游戏文件夹完整
    echo 2. 2048.exe 在 dist\2048\ 目录下
    echo.
    pause
    exit /b 1
)

echo.
echo 游戏文件检查通过!
echo 正在启动游戏...
echo.

REM 启动游戏
start "" "dist\2048\2048.exe"

echo 游戏已启动!
echo 如果游戏没有自动打开，请检查任务管理器
echo.
timeout /t 3 >nul