# -*- coding: utf-8 -*-
# @Function: 2048游戏安装程序
# @Function: 2048 Game Installer

import os
import sys
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import winreg
import subprocess
from pathlib import Path
import threading
import time


class InstallerApp:
    """安装程序主类"""
    
    def __init__(self):
        """初始化安装程序"""
        self.root = tk.Tk()
        self.root.title("2048 游戏安装程序")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        
        # 设置图标（如果有）
        try:
            self.root.iconbitmap(default="")
        except:
            pass
        
        # 安装配置
        self.install_path = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "AppData", "Local", "2048 Game"))
        self.create_shortcut = tk.BooleanVar(value=True)
        self.create_start_menu = tk.BooleanVar(value=True)
        
        # 当前步骤
        self.current_step = 0
        self.steps = ["欢迎", "许可协议", "选择路径", "安装中", "完成"]
        
        # 创建界面
        self.create_widgets()
        
        # 显示欢迎页面
        self.show_welcome()
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题标签
        self.title_label = ttk.Label(self.main_frame, text="", font=("微软雅黑", 16, "bold"))
        self.title_label.pack(pady=(0, 20))
        
        # 内容区域
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 按钮框架
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # 上一步按钮
        self.prev_button = ttk.Button(self.button_frame, text="上一步", command=self.prev_step)
        self.prev_button.pack(side=tk.LEFT)
        
        # 下一步按钮
        self.next_button = ttk.Button(self.button_frame, text="下一步", command=self.next_step)
        self.next_button.pack(side=tk.RIGHT)
        
        # 取消按钮
        self.cancel_button = ttk.Button(self.button_frame, text="取消", command=self.cancel_install)
        self.cancel_button.pack(side=tk.RIGHT, padx=(0, 10))
    
    def clear_content(self):
        """清空内容区域"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_welcome(self):
        """显示欢迎页面"""
        self.clear_content()
        self.title_label.config(text="欢迎使用 2048 游戏安装程序")
        
        welcome_text = """
        欢迎安装 2048 休闲游戏！
        
        本安装程序将引导您完成 2048 游戏的安装过程。
        
        2048 是一款经典的数字合成游戏，支持多种游戏模式：
        • 经典模式：无限时间，自由游玩
        • 挑战模式：限定步数内合成目标方块
        • 计时模式：在时间限制内尽可能合成大方块
        
        点击"下一步"继续安装。
        """
        
        label = ttk.Label(self.content_frame, text=welcome_text, justify=tk.LEFT)
        label.pack(pady=20)
        
        self.prev_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)
    
    def show_license(self):
        """显示许可协议页面"""
        self.clear_content()
        self.title_label.config(text="许可协议")
        
        license_text = """
        MIT 许可证
        
        版权所有 (c) 2026 2048 游戏开发团队
        
        特此免费授予任何获得本软件副本和相关文档文件（"软件"）的人不受限制地处理本软件的权利，包括不受限制地使用、复制、修改、合并、发布、分发、再许可和/或出售本软件副本的权利，以及允许本软件的被提供者这样做，但须满足以下条件：
        
        上述版权声明和本许可声明应包含在本软件的所有副本或重要部分中。
        
        本软件按"原样"提供，不提供任何形式的明示或暗示的保证，包括但不限于对适销性、特定用途适用性和非侵权性的保证。
        """
        
        # 许可协议文本框
        text_frame = ttk.Frame(self.content_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.license_text = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.license_text.insert(tk.END, license_text)
        self.license_text.config(state=tk.DISABLED)
        self.license_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.license_text.yview)
        
        # 同意复选框
        self.license_agreed = tk.BooleanVar(value=False)
        agree_check = ttk.Checkbutton(self.content_frame, text="我接受上述许可协议", variable=self.license_agreed)
        agree_check.pack(pady=10)
        
        self.prev_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)
        
        # 当复选框状态改变时更新按钮状态
        def on_agree_change():
            if self.license_agreed.get():
                self.next_button.config(state=tk.NORMAL)
            else:
                self.next_button.config(state=tk.DISABLED)
        
        self.license_agreed.trace_add("write", lambda *args: on_agree_change())
    
    def show_path_selection(self):
        """显示路径选择页面"""
        self.clear_content()
        self.title_label.config(text="选择安装路径")
        
        path_frame = ttk.Frame(self.content_frame)
        path_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # 安装路径
        ttk.Label(path_frame, text="安装路径:").pack(anchor=tk.W)
        
        path_entry_frame = ttk.Frame(path_frame)
        path_entry_frame.pack(fill=tk.X, pady=(5, 20))
        
        self.path_entry = ttk.Entry(path_entry_frame, textvariable=self.install_path, width=50)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_button = ttk.Button(path_entry_frame, text="浏览...", command=self.browse_path)
        browse_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # 选项
        options_frame = ttk.LabelFrame(path_frame, text="安装选项", padding=10)
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Checkbutton(options_frame, text="创建桌面快捷方式", variable=self.create_shortcut).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="创建开始菜单快捷方式", variable=self.create_start_menu).pack(anchor=tk.W)
        
        # 磁盘空间信息
        info_frame = ttk.Frame(path_frame)
        info_frame.pack(fill=tk.X)
        
        # 计算所需空间（估算）
        required_space = "约 50 MB"
        ttk.Label(info_frame, text=f"所需磁盘空间: {required_space}").pack(anchor=tk.W)
        
        # 检查磁盘空间
        try:
            drive = os.path.splitdrive(self.install_path.get())[0]
            if drive:
                free_space = shutil.disk_usage(drive).free
                free_space_mb = free_space // (1024 * 1024)
                ttk.Label(info_frame, text=f"可用磁盘空间: {free_space_mb} MB").pack(anchor=tk.W)
        except:
            pass
        
        self.prev_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)
    
    def browse_path(self):
        """浏览选择安装路径"""
        path = filedialog.askdirectory(title="选择安装路径")
        if path:
            self.install_path.set(os.path.join(path, "2048 Game"))
    
    def show_progress(self):
        """显示安装进度页面"""
        self.clear_content()
        self.title_label.config(text="正在安装...")
        
        # 进度条
        self.progress = ttk.Progressbar(self.content_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=20)
        
        # 状态标签
        self.status_label = ttk.Label(self.content_frame, text="准备安装...")
        self.status_label.pack(pady=10)
        
        # 详细信息
        self.detail_text = tk.Text(self.content_frame, height=10, width=60)
        self.detail_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.prev_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.DISABLED)
        
        # 开始安装
        self.start_installation()
    
    def start_installation(self):
        """开始安装过程"""
        def install_thread():
            try:
                # 步骤1: 创建安装目录
                self.update_status("创建安装目录...", 10)
                install_dir = self.install_path.get()
                os.makedirs(install_dir, exist_ok=True)
                self.log_detail(f"创建目录: {install_dir}")
                time.sleep(0.5)
                
                # 步骤2: 复制游戏文件
                self.update_status("复制游戏文件...", 30)
                self.copy_game_files(install_dir)
                time.sleep(0.5)
                
                # 步骤3: 创建启动脚本
                self.update_status("创建启动脚本...", 60)
                self.create_launcher(install_dir)
                time.sleep(0.5)
                
                # 步骤4: 创建快捷方式
                if self.create_shortcut.get():
                    self.update_status("创建桌面快捷方式...", 80)
                    self.create_desktop_shortcut(install_dir)
                
                if self.create_start_menu.get():
                    self.update_status("创建开始菜单快捷方式...", 90)
                    self.create_start_menu_shortcut(install_dir)
                
                # 步骤5: 完成
                self.update_status("安装完成!", 100)
                self.log_detail("安装完成！")
                time.sleep(1)
                
                # 切换到完成页面
                self.root.after(0, self.show_complete)
                
            except Exception as e:
                self.root.after(0, lambda: self.show_error(str(e)))
        
        # 在新线程中执行安装
        thread = threading.Thread(target=install_thread)
        thread.daemon = True
        thread.start()
    
    def update_status(self, status, progress):
        """更新安装状态"""
        def update():
            self.status_label.config(text=status)
            self.progress['value'] = progress
        self.root.after(0, update)
    
    def log_detail(self, message):
        """记录详细信息"""
        def update():
            self.detail_text.insert(tk.END, message + "\n")
            self.detail_text.see(tk.END)
        self.root.after(0, update)
    
    def copy_game_files(self, install_dir):
        """复制游戏文件"""
        # 获取源文件路径（假设在dist目录中）
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        dist_dir = os.path.join(project_root, "dist", "2048")
        
        if not os.path.exists(dist_dir):
            raise Exception(f"找不到游戏文件目录: {dist_dir}")
        
        self.log_detail(f"复制文件从: {dist_dir}")
        self.log_detail(f"复制文件到: {install_dir}")
        
        # 复制整个目录
        for item in os.listdir(dist_dir):
            src = os.path.join(dist_dir, item)
            dst = os.path.join(install_dir, item)
            
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            
            self.log_detail(f"复制: {item}")
    
    def create_launcher(self, install_dir):
        """创建启动脚本"""
        launcher_content = f'''@echo off
chcp 65001 >nul
title 2048 游戏
echo 正在启动 2048 游戏...
echo.
start "" "{os.path.join(install_dir, "2048.exe")}"
'''
        
        launcher_path = os.path.join(install_dir, "启动游戏.bat")
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        
        self.log_detail(f"创建启动脚本: {launcher_path}")
    
    def create_desktop_shortcut(self, install_dir):
        """创建桌面快捷方式"""
        try:
            # 获取桌面路径
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            
            # 创建快捷方式
            shortcut_path = os.path.join(desktop, "2048 游戏.lnk")
            
            # 使用PowerShell创建快捷方式
            ps_command = f'''
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{os.path.join(install_dir, "2048.exe")}"
$Shortcut.WorkingDirectory = "{install_dir}"
$Shortcut.Description = "2048 休闲游戏"
$Shortcut.Save()
'''
            
            subprocess.run(['powershell', '-Command', ps_command], 
                         capture_output=True, text=True, check=True)
            
            self.log_detail(f"创建桌面快捷方式: {shortcut_path}")
            
        except Exception as e:
            self.log_detail(f"创建桌面快捷方式失败: {e}")
    
    def create_start_menu_shortcut(self, install_dir):
        """创建开始菜单快捷方式"""
        try:
            # 获取开始菜单程序路径
            start_menu = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs")
            program_dir = os.path.join(start_menu, "2048 游戏")
            os.makedirs(program_dir, exist_ok=True)
            
            # 创建快捷方式
            shortcut_path = os.path.join(program_dir, "2048 游戏.lnk")
            
            # 使用PowerShell创建快捷方式
            ps_command = f'''
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{os.path.join(install_dir, "2048.exe")}"
$Shortcut.WorkingDirectory = "{install_dir}"
$Shortcut.Description = "2048 休闲游戏"
$Shortcut.Save()
'''
            
            subprocess.run(['powershell', '-Command', ps_command], 
                         capture_output=True, text=True, check=True)
            
            self.log_detail(f"创建开始菜单快捷方式: {shortcut_path}")
            
        except Exception as e:
            self.log_detail(f"创建开始菜单快捷方式失败: {e}")
    
    def show_complete(self):
        """显示完成页面"""
        self.clear_content()
        self.title_label.config(text="安装完成")
        
        complete_text = f"""
        2048 游戏已成功安装到:
        
        {self.install_path.get()}
        
        安装选项:
        • 创建桌面快捷方式: {"是" if self.create_shortcut.get() else "否"}
        • 创建开始菜单快捷方式: {"是" if self.create_start_menu.get() else "否"}
        
        您现在可以:
        • 双击桌面快捷方式启动游戏
        • 从开始菜单启动游戏
        • 直接运行安装目录中的 2048.exe
        
        感谢您安装 2048 游戏！
        """
        
        label = ttk.Label(self.content_frame, text=complete_text, justify=tk.LEFT)
        label.pack(pady=20)
        
        # 启动游戏选项
        self.launch_game = tk.BooleanVar(value=True)
        launch_check = ttk.Checkbutton(self.content_frame, text="安装完成后立即启动游戏", variable=self.launch_game)
        launch_check.pack(pady=10)
        
        self.prev_button.config(state=tk.DISABLED)
        self.next_button.config(text="完成", command=self.finish_install)
        self.cancel_button.config(state=tk.DISABLED)
    
    def show_error(self, error_message):
        """显示错误页面"""
        self.clear_content()
        self.title_label.config(text="安装失败")
        
        error_text = f"""
        安装过程中发生错误:
        
        {error_message}
        
        请检查:
        1. 是否有足够的磁盘空间
        2. 是否有写入权限
        3. 杀毒软件是否阻止了安装
        
        如果问题持续存在，请联系技术支持。
        """
        
        label = ttk.Label(self.content_frame, text=error_text, justify=tk.LEFT, foreground="red")
        label.pack(pady=20)
        
        self.prev_button.config(state=tk.NORMAL)
        self.next_button.config(text="重试", command=self.retry_install)
        self.cancel_button.config(state=tk.NORMAL)
    
    def next_step(self):
        """下一步"""
        self.current_step += 1
        
        if self.current_step == 1:
            self.show_license()
        elif self.current_step == 2:
            self.show_path_selection()
        elif self.current_step == 3:
            self.show_progress()
    
    def prev_step(self):
        """上一步"""
        self.current_step -= 1
        
        if self.current_step == 0:
            self.show_welcome()
        elif self.current_step == 1:
            self.show_license()
        elif self.current_step == 2:
            self.show_path_selection()
    
    def retry_install(self):
        """重试安装"""
        self.current_step = 2
        self.show_path_selection()
    
    def cancel_install(self):
        """取消安装"""
        if messagebox.askyesno("确认取消", "确定要取消安装吗？"):
            self.root.destroy()
    
    def finish_install(self):
        """完成安装"""
        # 启动游戏（如果选择了）
        if self.launch_game.get():
            try:
                exe_path = os.path.join(self.install_path.get(), "2048.exe")
                subprocess.Popen([exe_path], cwd=self.install_path.get())
            except Exception as e:
                messagebox.showerror("启动失败", f"无法启动游戏: {e}")
        
        self.root.destroy()
    
    def run(self):
        """运行安装程序"""
        self.root.mainloop()


def main():
    """主函数"""
    app = InstallerApp()
    app.run()


if __name__ == "__main__":
    main()