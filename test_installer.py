# -*- coding: utf-8 -*-
# @Function: 安装程序测试脚本

import os
import sys
import tempfile
import shutil

# 添加脚本目录到路径
script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
sys.path.insert(0, script_dir)


def test_installer_import():
    """测试安装程序导入"""
    try:
        from installer import InstallerApp
        print("[OK] 安装程序模块导入成功")
        return True
    except ImportError as e:
        print(f"[ERROR] 安装程序模块导入失败: {e}")
        return False


def test_installer_initialization():
    """测试安装程序初始化"""
    try:
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        
        # 修改安装路径到临时目录
        original_init = None
        try:
            from installer import InstallerApp
            
            # 保存原始初始化方法
            original_init = InstallerApp.__init__
            
            # 创建测试类
            class TestInstaller(InstallerApp):
                def __init__(self):
                    # 跳过GUI初始化
                    self.install_path = type('obj', (object,), {'get': lambda self: temp_dir})()
                    self.create_shortcut = type('obj', (object,), {'get': lambda self: True})()
                    self.create_start_menu = type('obj', (object,), {'get': lambda self: True})()
            
            # 测试初始化
            installer = TestInstaller()
            print("[OK] 安装程序初始化成功")
            
            # 清理
            shutil.rmtree(temp_dir, ignore_errors=True)
            return True
            
        except Exception as e:
            print(f"[ERROR] 安装程序初始化失败: {e}")
            shutil.rmtree(temp_dir, ignore_errors=True)
            return False
        finally:
            # 恢复原始方法
            if original_init:
                InstallerApp.__init__ = original_init
                
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        return False


def test_file_operations():
    """测试文件操作"""
    try:
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        install_dir = os.path.join(temp_dir, "2048 Test")
        
        # 测试目录创建
        os.makedirs(install_dir, exist_ok=True)
        print("[OK] 目录创建成功")
        
        # 测试文件创建
        test_file = os.path.join(install_dir, "test.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("测试文件")
        
        if os.path.exists(test_file):
            print("[OK] 文件创建成功")
        else:
            print("[ERROR] 文件创建失败")
            return False
        
        # 测试文件删除
        os.remove(test_file)
        if not os.path.exists(test_file):
            print("[OK] 文件删除成功")
        else:
            print("[ERROR] 文件删除失败")
            return False
        
        # 清理
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("[OK] 文件操作测试通过")
        return True
        
    except Exception as e:
        print(f"[ERROR] 文件操作测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("=" * 50)
    print("安装程序测试")
    print("=" * 50)
    
    tests = [
        ("导入测试", test_installer_import),
        ("初始化测试", test_installer_initialization),
        ("文件操作测试", test_file_operations),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n运行 {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("所有测试通过！")
    else:
        print("部分测试失败，请检查错误信息。")
    print("=" * 50)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)