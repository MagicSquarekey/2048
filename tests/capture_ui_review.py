# -*- coding: utf-8 -*-
# @Function: 捕获全部页面截图（UI 评审用）- 一次性SDL渲染，无需真实窗口

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pygame

pygame.init()
pygame.display.init()
# 使用隐藏 flag，避免弹窗干扰（离屏渲染）
screen = pygame.display.set_mode((800, 600), pygame.HIDDEN)

from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG
from src.views.pages.menu_page import MenuPage
from src.views.pages.game_page import GamePage
from src.views.pages.settings_page import SettingsPage
from src.views.pages.result_page import ResultPage
from src.views.pages.pause_page import PausePage
from src.views.pages.achievements_page import AchievementsPage
from src.views.pages.login_page import LoginPage

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def snap(page, name, **kwargs):
    page.on_enter(**kwargs)
    # 跑几帧让动画/数据就位
    for _ in range(8):
        page.update(1 / 60)
    screen.fill(COLOR_BG)
    page.draw(screen)
    # 游戏页模拟几步棋，看方块渲染效果
    path = os.path.join(SCREENSHOT_DIR, f'{name}.png')
    pygame.image.save(screen, path)
    print(f'saved: {path}')


menu = MenuPage()
snap(menu, 'ui_menu')

game = GamePage()
snap(game, 'ui_game_new')
# 模拟走几步棋
import pygame as pg
for direction in ('left', 'down', 'right', 'up', 'left', 'down', 'right', 'down'):
    game._do_move(direction)
    for _ in range(10):
        game.update(1 / 60)
screen.fill(COLOR_BG)
game.draw(screen)
pygame.image.save(screen, os.path.join(SCREENSHOT_DIR, 'ui_game_mid.png'))
print('saved: ui_game_mid.png')

snap(SettingsPage(), 'ui_settings')
snap(AchievementsPage(), 'ui_achievements')
snap(LoginPage(), 'ui_login')

result = ResultPage()
result.on_enter(result={
    'score': 12345, 'is_win': False, 'mode': 'classic',
    'max_tile': 512, 'move_count': 150, 'elapsed_time': 183,
})
for _ in range(5):
    result.update(1 / 60)
screen.fill(COLOR_BG)
result.draw(screen)
pygame.image.save(screen, os.path.join(SCREENSHOT_DIR, 'ui_result.png'))
print('saved: ui_result.png')

pause = PausePage()
pause.on_enter(result={'score': 4520})
for _ in range(5):
    pause.update(1 / 60)
screen.fill(COLOR_BG)
pause.draw(screen)
pygame.image.save(screen, os.path.join(SCREENSHOT_DIR, 'ui_pause.png'))
print('saved: ui_pause.png')

pygame.quit()
print('all done')
