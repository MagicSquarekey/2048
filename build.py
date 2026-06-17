# -*- coding: utf-8 -*-
# @Function: 打包脚本 - 使用 PyInstaller 生成 EXE

import subprocess
import sys


def build():
    """执行打包"""
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "2048 Game",
        "--clean",
        "src/main.py"
    ]
    print("开始打包...")
    print(" ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print("\n打包成功！")
        print("输出文件: dist/2048 Game.exe")
    else:
        print("\n打包失败，请检查错误信息")
        sys.exit(1)


if __name__ == "__main__":
    build()
