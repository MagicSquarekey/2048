# -*- coding: utf-8 -*-
# @Function: 截图捕获脚本 - 用于UX评估

import sys
import os
import time
import pygame

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, COLOR_BG
from src.views.pages.menu_page import MenuPage
from src.views.pages.game_page import GamePage
from src.views.pages.settings_page import SettingsPage
from src.views.pages.result_page import ResultPage
from src.views.pages.pause_page import PausePage
from src.models.board import GameBoard

# 截图目录
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def capture_menu_page():
    """捕获主菜单页面截图"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2048 - Menu")
    clock = pygame.time.Clock()
    
    menu = MenuPage()
    menu.on_enter()
    
    # 绘制2帧确保渲染完成
    for _ in range(2):
        screen.fill(COLOR_BG)
        menu.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    
    # 保存截图
    screenshot_path = os.path.join(SCREENSHOT_DIR, '01_menu_page.png')
    pygame.image.save(screen, screenshot_path)
    print(f"菜单页面截图已保存: {screenshot_path}")
    
    pygame.quit()
    return screenshot_path

def capture_game_page():
    """捕获游戏页面截图"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2048 - Game")
    clock = pygame.time.Clock()
    
    game = GamePage()
    game.on_enter(mode="classic")
    
    # 绘制几帧让动画完成
    for _ in range(10):
        dt = clock.tick(FPS) / 1000.0
        screen.fill(COLOR_BG)
        game.update(dt)
        game.draw(screen)
        pygame.display.flip()
    
    # 保存截图
    screenshot_path = os.path.join(SCREENSHOT_DIR, '02_game_page.png')
    pygame.image.save(screen, screenshot_path)
    print(f"游戏页面截图已保存: {screenshot_path}")
    
    # 模拟一次移动
    game.board.move_left()
    for _ in range(15):
        dt = clock.tick(FPS) / 1000.0
        screen.fill(COLOR_BG)
        game.update(dt)
        game.draw(screen)
        pygame.display.flip()
    
    # 保存移动后的截图
    screenshot_path2 = os.path.join(SCREENSHOT_DIR, '03_game_after_move.png')
    pygame.image.save(screen, screenshot_path2)
    print(f"移动后游戏截图已保存: {screenshot_path2}")
    
    pygame.quit()
    return screenshot_path, screenshot_path2

def capture_settings_page():
    """捕获设置页面截图"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2048 - Settings")
    clock = pygame.time.Clock()
    
    settings = SettingsPage()
    settings.on_enter()
    
    # 绘制2帧确保渲染完成
    for _ in range(2):
        screen.fill(COLOR_BG)
        settings.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    
    # 保存截图
    screenshot_path = os.path.join(SCREENSHOT_DIR, '04_settings_page.png')
    pygame.image.save(screen, screenshot_path)
    print(f"设置页面截图已保存: {screenshot_path}")
    
    pygame.quit()
    return screenshot_path

def capture_result_page():
    """捕获结果页面截图"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2048 - Result")
    clock = pygame.time.Clock()
    
    result = ResultPage()
    result.on_enter(score=12345, is_win=True, mode="classic", moves=150, time_played=180)
    
    # 绘制2帧确保渲染完成
    for _ in range(2):
        screen.fill(COLOR_BG)
        result.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    
    # 保存截图
    screenshot_path = os.path.join(SCREENSHOT_DIR, '05_result_page.png')
    pygame.image.save(screen, screenshot_path)
    print(f"结果页面截图已保存: {screenshot_path}")
    
    pygame.quit()
    return screenshot_path

if __name__ == "__main__":
    print("开始捕获2048游戏截图...")
    print("=" * 50)
    
    try:
        # 捕获各页面截图
        menu_path = capture_menu_page()
        game_paths = capture_game_page()
        settings_path = capture_settings_page()
        result_path = capture_result_page()
        
        print("=" * 50)
        print("所有截图捕获完成！")
        print(f"截图保存目录: {SCREENSHOT_DIR}")
        
    except Exception as e:
        print(f"截图捕获出错: {e}")
        import traceback
        traceback.print_exc()
