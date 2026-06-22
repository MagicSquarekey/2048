# -*- coding: utf-8 -*-
# @Function: 测试打包是否成功

import os
import sys


def test_build() -> None:
    """测试打包结果"""
    print("=" * 50)
    print("2048游戏打包测试")
    print("=" * 50)
    
    # 检查打包目录
    dist_dir = os.path.join("dist", "2048")
    exe_path = os.path.join(dist_dir, "2048.exe")
    
    print(f"[1] 检查打包目录: {dist_dir}")
    if os.path.exists(dist_dir):
        print(f"    [OK] 目录存在")
    else:
        print(f"    [ERROR] 目录不存在")
        return
    
    print(f"[2] 检查可执行文件: {exe_path}")
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path)
        print(f"    [OK] 文件存在, 大小: {size / (1024*1024):.2f} MB")
    else:
        print(f"    [ERROR] 文件不存在")
        return
    
    print(f"[3] 检查内部依赖目录")
    internal_dir = os.path.join(dist_dir, "_internal")
    if os.path.exists(internal_dir):
        print(f"    [OK] 内部目录存在")
        
        # 检查关键文件
        key_files = ["python311.dll", "SDL2.dll", "pygame", "src"]
        for file in key_files:
            file_path = os.path.join(internal_dir, file)
            if os.path.exists(file_path):
                print(f"    [OK] 关键文件 {file} 存在")
            else:
                print(f"    [ERROR] 关键文件 {file} 缺失")
    else:
        print(f"    [ERROR] 内部目录缺失")
        return
    
    print(f"[4] 检查启动器")
    launcher_path = "启动2048游戏.bat"
    if os.path.exists(launcher_path):
        print(f"    [OK] 启动器存在: {launcher_path}")
    else:
        print(f"    [ERROR] 启动器不存在")
    
    print("\n" + "=" * 50)
    print("[OK] 打包测试完成!")
    print("=" * 50)
    
    # 使用说明
    print("\n[DISTRIBUTE] 分发说明:")
    print(f"1. 将整个文件夹复制给用户: {os.path.abspath(dist_dir)}")
    print("2. 用户双击 2048.exe 即可运行游戏")
    print("3. 无需安装任何依赖")
    
    print("\n[TEST] 测试运行:")
    print(f"1. 进入目录: {os.path.abspath(dist_dir)}")
    print("2. 双击 2048.exe")
    print("3. 或者在项目根目录双击 '启动2048游戏.bat'")


if __name__ == "__main__":
    test_build()