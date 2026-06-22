@echo off
chcp 65001 >nul
title 2048 游戏打包工具
echo ==============================
echo      2048 游戏打包工具
echo ==============================
echo.
echo 本工具将为您打包游戏和安装程序。
echo.
echo 打包内容:
echo   1. 游戏程序 (2048.exe)
echo   2. 安装程序 (2048安装程序.exe)
echo   3. 便携版本 (2048-便携版.zip)
echo.
echo 注意事项:
echo   - 打包过程可能需要几分钟
echo   - 请确保已安装 Python 和 PyInstaller
echo   - 打包完成后，文件将位于 dist 目录
echo.
echo 开始打包...
echo.

python scripts/build_all.py

echo.
echo ==============================
echo         打包完成！
echo ==============================
echo.
echo 分发文件:
echo   - 2048安装程序.exe (完整安装程序)
echo   - 2048-便携版.zip (便携版本)
echo.
echo 文件位置: dist 目录
echo.
echo 按任意键退出...
pause >nul