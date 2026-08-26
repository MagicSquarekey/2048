# -*- coding: utf-8 -*-
# @Function: 捕获所有页面截图用于iOS风格验收

import sys
import os
import pygame

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, COLOR_BG
from src.views.pages.menu_page import MenuPage
from src.views.pages.game_page import GamePage
from src.views.pages.settings_page import SettingsPage
from src.views.pages.result_page import ResultPage
from src.views.pages.pause_page import PausePage

# 截图目录
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def capture_page(page_class, page_name, **kwargs):
    """捕获单个页面截图"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(f"2048 - {page_name}")
    clock = pygame.time.Clock()
    
    page = page_class()
    page.on_enter(**kwargs)
    
    # 绘制几帧确保渲染完成
    for _ in range(5):
        dt = clock.tick(FPS) / 1000.0
        screen.fill(COLOR_BG)
        page.update(dt)
        page.draw(screen)
        pygame.display.flip()
    
    # 保存截图
    screenshot_path = os.path.join(SCREENSHOT_DIR, f'{page_name}.png')
    pygame.image.save(screen, screenshot_path)
    print(f"{page_name} 页面截图已保存: {screenshot_path}")
    
    pygame.quit()
    return screenshot_path

def main():
    """捕获所有页面截图"""
    print("开始捕获2048游戏各页面截图...")
    print("=" * 50)
    
    try:
        # 捕获主菜单页面
        menu_path = capture_page(MenuPage, "menu_page")
        
        # 捕获游戏页面
        game_path = capture_page(GamePage, "game_page", mode="classic")
        
        # 捕获设置页面
        settings_path = capture_page(SettingsPage, "settings_page")
        
        # 捕获结果页面
        result_path = capture_page(ResultPage, "result_page", 
                                   score=12345, is_win=True, 
                                   mode="classic", moves=150, time_played=180)
        
        print("=" * 50)
        print("所有页面截图捕获完成！")
        print(f"截图保存目录: {SCREENSHOT_DIR}")
        
        return {
            "menu": menu_path,
            "game": game_path,
            "settings": settings_path,
            "result": result_path
        }
        
    except Exception as e:
        print(f"截图捕获出错: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    paths = main()
    if paths:
        print("\n截图文件列表:")
        for name, path in paths.items():
            print(f"  - {name}: {path}")
