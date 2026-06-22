# -*- coding: utf-8 -*-
# @Function: 2048游戏打包脚本

import os
import sys
import shutil
import subprocess
from pathlib import Path


def clean_build_dirs() -> None:
    """清理构建目录"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)


def run_pyinstaller() -> bool:
    """运行PyInstaller打包"""
    print("开始打包...")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    try:
        # 使用PyInstaller打包
        cmd = [
            sys.executable, '-m', 'PyInstaller', '--clean',
            '--distpath', 'dist',
            '--workpath', 'build',
            '--specpath', 'scripts',
            '--name', '2048',
            'src/main.py'
        ]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("打包成功!")
            return True
        else:
            print(f"打包失败:\n{result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"执行PyInstaller时出错: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    except Exception as e:
        print(f"未知错误: {e}")
        return False


def create_desktop_shortcut() -> None:
    """创建桌面快捷方式（仅Windows）"""
    if sys.platform != 'win32':
        print("桌面快捷方式仅支持Windows系统")
        return
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "2048游戏.lnk")
        exe_path = os.path.abspath(os.path.join("dist", "2048", "2048.exe"))
        
        if not os.path.exists(exe_path):
            print(f"可执行文件不存在: {exe_path}")
            return
        
        # 创建快捷方式
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.Description = "2048休闲游戏"
        shortcut.save()
        
        print(f"桌面快捷方式已创建: {shortcut_path}")
        
    except ImportError:
        print("缺少依赖包，跳过创建桌面快捷方式")
        print("请安装: pip install pywin32 winshell")
    except Exception as e:
        print(f"创建桌面快捷方式失败: {e}")


def create_portable_launcher() -> None:
    """创建便携式启动器（推荐方式）"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dist_dir = os.path.join(project_root, "dist", "2048")
    
    if not os.path.exists(dist_dir):
        print("打包目录不存在，请先执行打包")
        return
    
    launcher_content = f'''@echo off
chcp 65001 >nul
title 2048 游戏
echo 正在启动 2048 游戏...
echo.

REM 检查可执行文件是否存在
if not exist "{dist_dir}\\2048.exe" (
    echo 错误: 找不到可执行文件
    echo 请确保已正确打包游戏
    pause
    exit /b 1
)

REM 启动游戏
start "" "{dist_dir}\\2048.exe"

REM 显示提示
echo 游戏已启动!
echo 如果游戏没有自动打开，请检查任务管理器
timeout /t 3 >nul
'''
    
    launcher_path = os.path.join(project_root, "启动2048游戏.bat")
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print(f"便携式启动器已创建: {launcher_path}")
    print("用户双击此文件即可启动游戏")


def show_usage_guide() -> None:
    """显示使用指南"""
    print("\n" + "="*50)
    print("📦 2048游戏打包完成")
    print("="*50)
    print("\n📁 打包结果:")
    print(f"  - 可执行文件目录: {os.path.abspath(os.path.join('dist', '2048'))}")
    print(f"  - 主程序文件: {os.path.abspath(os.path.join('dist', '2048', '2048.exe'))}")
    
    print("\n🚀 使用方式:")
    print("  1. 直接运行: 进入 dist/2048/ 目录，双击 2048.exe")
    print("  2. 便携式启动: 双击项目根目录下的 '启动2048游戏.bat'")
    
    print("\n📋 分发说明:")
    print("  - 将 dist/2048/ 整个文件夹复制给用户")
    print("  - 用户双击 2048.exe 即可运行游戏")
    print("  - 无需安装Python或任何依赖")
    
    print("\n💡 提示:")
    print("  - 如果需要创建桌面快捷方式，需要安装额外依赖:")
    print("    pip install pywin32 winshell")
    print("  - 可以在build.spec中添加游戏图标")
    print("="*50)


def main() -> None:
    """主函数"""
    print("🎮 2048游戏打包工具")
    print("-" * 40)
    
    # 1. 清理旧构建
    clean_build_dirs()
    
    # 2. 运行打包
    if not run_pyinstaller():
        print("打包失败，退出")
        sys.exit(1)
    
    # 3. 创建启动器
    create_portable_launcher()
    
    # 4. 显示结果
    show_usage_guide()
    
    # 5. 可选：创建桌面快捷方式
    print("\n是否创建桌面快捷方式？(y/n): ", end="")
    try:
        choice = input().strip().lower()
        if choice in ['y', 'yes', '是']:
            create_desktop_shortcut()
    except KeyboardInterrupt:
        print("\n跳过创建桌面快捷方式")


if __name__ == "__main__":
    main()