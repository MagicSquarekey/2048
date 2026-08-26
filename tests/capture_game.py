# -*- coding: utf-8 -*-
# @Function: 游戏页面截图捕获

import sys
import os
import pygame

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, COLOR_BG
from src.views.pages.game_page import GamePage

# 截图目录
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def main():
    """捕获游戏页面截图"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2048 - Game")
    clock = pygame.time.Clock()
    
    game = GamePage()
    game.on_enter(mode="classic")
    
    # 绘制几帧让初始动画完成
    for _ in range(20):
        dt = clock.tick(FPS) / 1000.0
        screen.fill(COLOR_BG)
        game.update(dt)
        game.draw(screen)
        pygame.display.flip()
    
    # 保存初始状态截图
    screenshot_path = os.path.join(SCREENSHOT_DIR, 'game_initial.png')
    pygame.image.save(screen, screenshot_path)
    print(f"游戏初始状态截图已保存: {screenshot_path}")
    
    # 模拟向左移动
    from src.models.board import GameBoard
    game.board.move_left()
    
    # 绘制动画帧
    for _ in range(20):
        dt = clock.tick(FPS) / 1000.0
        screen.fill(COLOR_BG)
        game.update(dt)
        game.draw(screen)
        pygame.display.flip()
    
    # 保存移动后截图
    screenshot_path2 = os.path.join(SCREENSHOT_DIR, 'game_after_move.png')
    pygame.image.save(screen, screenshot_path2)
    print(f"移动后游戏截图已保存: {screenshot_path2}")
    
    pygame.quit()
    return screenshot_path, screenshot_path2

if __name__ == "__main__":
    try:
        paths = main()
        print(f"截图成功: {paths}")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
