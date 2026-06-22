# -*- coding: utf-8 -*-
# @Function: 打包安装程序脚本
# @Function: Build installer script

import os
import sys
import subprocess
import shutil
from pathlib import Path


def main():
    """打包安装程序"""
    print("=" * 50)
    print("2048 游戏安装程序打包工具")
    print("=" * 50)
    
    # 获取项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    print(f"项目根目录: {project_root}")
    
    # 检查安装程序脚本是否存在
    installer_script = os.path.join(script_dir, "installer.py")
    if not os.path.exists(installer_script):
        print(f"错误: 找不到安装程序脚本: {installer_script}")
        return False
    
    print(f"安装程序脚本: {installer_script}")
    
    # 清理之前的构建
    print("\n1. 清理构建目录...")
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            print(f"   清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 打包安装程序
    print("\n2. 打包安装程序...")
    
    cmd = [
        sys.executable, '-m', 'PyInstaller', '--clean',
        '--onefile',
        '--windowed',
        '--name', '2048安装程序',
        '--add-data', f'{os.path.join("dist", "2048")};dist/2048',
        installer_script
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("\n3. 打包成功!")
            
            # 检查生成的文件
            installer_path = os.path.join("dist", "2048安装程序.exe")
            if os.path.exists(installer_path):
                print(f"安装程序: {os.path.abspath(installer_path)}")
                
                # 创建说明文件
                create_readme(installer_path)
                
                print("\n" + "=" * 50)
                print("打包完成！")
                print("=" * 50)
                print(f"安装程序位置: {os.path.abspath(installer_path)}")
                print("\n使用说明:")
                print("1. 先运行游戏打包脚本: python scripts/build_auto.py")
                print("2. 然后运行安装程序打包脚本: python scripts/build_installer.py")
                print("3. 分发 2048安装程序.exe 给用户")
                print("4. 用户运行安装程序，选择路径，创建快捷方式")
                
                return True
            else:
                print(f"错误: 找不到生成的安装程序: {installer_path}")
                return False
        else:
            print(f"打包失败:\n{result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"执行PyInstaller时出错: {e}")
        print(f"错误输出: {e.stderr}")
        return False


def create_readme(installer_path):
    """创建说明文件"""
    readme_content = f"""2048 游戏安装程序使用说明
========================

1. 首先确保已运行游戏打包脚本:
   python scripts/build_auto.py

2. 然后运行安装程序打包脚本:
   python scripts/build_installer.py

3. 生成的安装程序位于:
   {os.path.abspath(installer_path)}

4. 分发给用户:
   - 将 2048安装程序.exe 发送给用户
   - 用户双击运行安装程序
   - 选择安装路径（默认: 用户目录\\AppData\\Local\\2048 Game）
   - 选择是否创建桌面和开始菜单快捷方式
   - 点击安装

5. 安装完成后:
   - 用户可以通过桌面快捷方式启动游戏
   - 也可以通过开始菜单启动游戏
   - 或者直接运行安装目录中的 2048.exe

注意事项:
- 安装程序需要管理员权限（如果安装到系统目录）
- 建议安装到用户目录，避免权限问题
- 安装程序会自动检测磁盘空间
"""
    
    readme_path = os.path.join(os.path.dirname(installer_path), "安装程序使用说明.txt")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"说明文件: {readme_path}")


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)