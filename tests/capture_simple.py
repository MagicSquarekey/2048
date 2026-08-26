# -*- coding: utf-8 -*-
# @Function: 简化截图捕获脚本

import sys
import os
import pygame

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, COLOR_BG
from src.views.pages.menu_page import MenuPage

# 截图目录
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def main():
    """捕获主菜单页面截图"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2048 - Menu")
    clock = pygame.time.Clock()
    
    menu = MenuPage()
    menu.on_enter()
    
    # 绘制几帧确保渲染完成
    for _ in range(5):
        screen.fill(COLOR_BG)
        menu.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    
    # 保存截图
    screenshot_path = os.path.join(SCREENSHOT_DIR, 'menu_page.png')
    pygame.image.save(screen, screenshot_path)
    print(f"菜单页面截图已保存: {screenshot_path}")
    
    pygame.quit()
    return screenshot_path

if __name__ == "__main__":
    try:
        path = main()
        print(f"截图成功: {path}")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
