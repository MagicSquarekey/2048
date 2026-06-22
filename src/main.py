# -*- coding: utf-8 -*-
# @Function: 2048 游戏主入口 / 2048 Game main entry point

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 隐藏控制台窗口（Windows平台）
def hide_console_window():
    """隐藏控制台窗口 / Hide console window on Windows"""
    if sys.platform == 'win32':
        try:
            import ctypes
            console_window = ctypes.windll.kernel32.GetConsoleWindow()
            if console_window:
                # SW_HIDE = 0
                ctypes.windll.user32.ShowWindow(console_window, 0)
        except Exception:
            # 如果获取控制台窗口失败，静默处理
            pass

# 在程序启动时立即隐藏控制台
hide_console_window()

import pygame
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, COLOR_BG
from src.views.pages import (
    PageManager, MenuPage, GamePage, ResultPage,
    SettingsPage, AchievementsPage, PausePage, LoginPage,
)


def init_pygame() -> pygame.Surface:
    """初始化 Pygame / Initialize Pygame"""
    pygame.init()
    pygame.display.set_caption("2048 - 休闲游戏")
    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    return surface


def register_pages() -> PageManager:
    """注册所有页面 / Register all pages"""
    pm = PageManager()
    pm.register_page(MenuPage())
    pm.register_page(GamePage())
    pm.register_page(ResultPage())
    pm.register_page(SettingsPage())
    pm.register_page(AchievementsPage())
    pm.register_page(PausePage())
    pm.register_page(LoginPage())
    return pm


def main() -> None:
    """主函数 / Main entry point"""
    surface = init_pygame()
    clock = pygame.time.Clock()
    pm = register_pages()

    # 设置页面路由
    def handle_page_switch(page_name: str) -> None:
        """处理页面切换 / Handle page switch"""
        if page_name == "game" or page_name == "classic":
            game_page = pm.get_page("game")
            if game_page:
                pm.switch_to("game", mode="classic")
        elif page_name == "timed":
            pm.switch_to("game", mode="timed")
        elif page_name == "challenge":
            pm.switch_to("game", mode="challenge")
        elif page_name == "result":
            game_page = pm.get_page("game")
            result = game_page.get_game_result() if game_page else None
            pm.switch_to("result", result=result or {})
        elif page_name == "pause":
            pm.push_page("pause")
        elif page_name == "resume":
            # 从暂停恢复，pop 暂停页
            pm.pop_page()
        elif page_name in ("menu", "settings", "achievements", "login"):
            pm.switch_to(page_name)
        else:
            pm.switch_to(page_name)

    # 启动时进入主菜单
    pm.switch_to("menu")

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # 转换为秒

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            # 全局快捷键
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current = pm.current_page
                    if current and current.name == "game":
                        # 游戏中按 ESC -> 暂停
                        handle_page_switch("pause")
                        continue
                    elif current and current.name == "pause":
                        # 暂停中按 ESC -> 继续
                        handle_page_switch("resume")
                        continue
                    elif current and current.name != "menu":
                        # 其他非菜单页面返回菜单
                        pm.switch_to("menu")
                        continue
                    else:
                        # 菜单页面退出游戏
                        running = False
                        break

            # 分发到当前页面
            if pm.current_page:
                target = pm.current_page.handle_event(event)
                if target:
                    handle_page_switch(target)

        # 更新
        if pm.current_page:
            target = pm.current_page.update(dt)
            if target:
                handle_page_switch(target)

        # 绘制
        surface.fill(COLOR_BG)
        pm.draw(surface)
        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
