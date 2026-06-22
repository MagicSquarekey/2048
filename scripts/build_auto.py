# -*- coding: utf-8 -*-
# @Function: 2048游戏自动打包脚本（无需交互）

import os
import sys
import shutil
import subprocess
from pathlib import Path


def main() -> None:
    """自动打包游戏"""
    print("[2048] 2048游戏自动打包")
    print("=" * 40)
    
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    # 清理构建目录
    for dir_name in ['build', 'dist', '__pycache__']:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 运行PyInstaller
    print("开始打包...")
    cmd = [
        sys.executable, '-m', 'PyInstaller', '--clean',
        '--distpath', 'dist',
        '--workpath', 'build',
        '--specpath', 'scripts',
        '--name', '2048',
        'src/main.py'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("[OK] 打包成功!")
            
            # 检查生成的文件
            exe_path = os.path.join("dist", "2048", "2048.exe")
            if os.path.exists(exe_path):
                print(f"[FILE] 可执行文件: {os.path.abspath(exe_path)}")
                
                # 创建便携式启动器
                launcher_content = f'''@echo off
chcp 65001 >nul
title 2048 游戏
echo 正在启动 2048 游戏...
echo.
start "" "{os.path.abspath(exe_path)}"
echo 游戏已启动!
timeout /t 3 >nul
'''
                
                launcher_path = "启动2048游戏.bat"
                with open(launcher_path, 'w', encoding='utf-8') as f:
                    f.write(launcher_content)
                
                print(f"[LAUNCH] 启动器: {os.path.abspath(launcher_path)}")
                
                # 显示使用说明
                print("\n" + "=" * 50)
                print("[DONE] 打包完成!")
                print("=" * 50)
                print("[DISTRIBUTE] 分发方式:")
                print(f"  1. 将整个文件夹复制给用户: {os.path.abspath(os.path.join('dist', '2048'))}")
                print("  2. 用户双击 2048.exe 即可运行")
                print("  3. 无需安装任何依赖")
                print("\n[QUICK START] 快速启动:")
                print("  双击 '启动2048游戏.bat' 即可运行游戏")
                print("=" * 50)
                
            else:
                print("[ERROR] 未找到可执行文件")
                sys.exit(1)
        else:
            print(f"[ERROR] 打包失败:\n{result.stderr}")
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] 执行PyInstaller时出错: {e}")
        print(f"错误输出: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 未知错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()