# -*- coding: utf-8 -*-
# @Function: 完整打包脚本 - 游戏 + 安装程序
# @Function: Complete build script - Game + Installer

import os
import sys
import subprocess
import shutil
from pathlib import Path


def main():
    """完整打包流程"""
    print("=" * 60)
    print("2048 游戏完整打包工具")
    print("=" * 60)
    
    # 获取项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    print(f"项目根目录: {project_root}")
    
    # 步骤1: 打包游戏
    print("\n" + "=" * 60)
    print("步骤 1: 打包游戏")
    print("=" * 60)
    
    if not build_game():
        print("游戏打包失败！")
        return False
    
    # 步骤2: 打包安装程序
    print("\n" + "=" * 60)
    print("步骤 2: 打包安装程序")
    print("=" * 60)
    
    if not build_installer():
        print("安装程序打包失败！")
        return False
    
    # 步骤3: 创建分发包
    print("\n" + "=" * 60)
    print("步骤 3: 创建分发包")
    print("=" * 60)
    
    if not create_distribution():
        print("创建分发包失败！")
        return False
    
    print("\n" + "=" * 60)
    print("打包完成！")
    print("=" * 60)
    print("\n分发文件:")
    print("1. 2048安装程序.exe - 完整安装程序（推荐）")
    print("2. 2048-便携版.zip - 便携版本（无需安装）")
    print("\n分发说明:")
    print("- 安装程序版本: 用户运行安装程序，选择路径，创建快捷方式")
    print("- 便携版本: 用户解压后直接运行 2048.exe")
    print("\n文件位置:")
    print(f"- 安装程序: {os.path.abspath('dist/2048安装程序.exe')}")
    print(f"- 便携版: {os.path.abspath('dist/2048-便携版.zip')}")
    
    return True


def build_game():
    """打包游戏"""
    print("执行游戏打包脚本...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    build_script = os.path.join(script_dir, "build_auto.py")
    
    if not os.path.exists(build_script):
        print(f"错误: 找不到打包脚本: {build_script}")
        return False
    
    try:
        result = subprocess.run([sys.executable, build_script], 
                              capture_output=True, text=True, check=True)
        print("游戏打包成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"游戏打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False


def build_installer():
    """打包安装程序"""
    print("执行安装程序打包脚本...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    build_script = os.path.join(script_dir, "build_installer.py")
    
    if not os.path.exists(build_script):
        print(f"错误: 找不到打包脚本: {build_script}")
        return False
    
    try:
        result = subprocess.run([sys.executable, build_script], 
                              capture_output=True, text=True, check=True)
        print("安装程序打包成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装程序打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False


def create_distribution():
    """创建分发包"""
    print("创建便携版本分发包...")
    
    # 检查游戏文件是否存在
    game_dir = os.path.join("dist", "2048")
    if not os.path.exists(game_dir):
        print(f"错误: 找不到游戏目录: {game_dir}")
        return False
    
    # 创建ZIP文件
    zip_path = os.path.join("dist", "2048-便携版")
    try:
        shutil.make_archive(zip_path, 'zip', "dist", "2048")
        print(f"便携版创建成功: {zip_path}.zip")
        return True
    except Exception as e:
        print(f"创建便携版失败: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)