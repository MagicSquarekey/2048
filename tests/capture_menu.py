# -*- coding: utf-8 -*-
import sys
import os
import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, COLOR_BG
from src.views.pages.menu_page import MenuPage

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    
    menu = MenuPage()
    menu.on_enter()
    
    for _ in range(5):
        dt = clock.tick(FPS) / 1000.0
        screen.fill(COLOR_BG)
        menu.update(dt)
        menu.draw(screen)
        pygame.display.flip()
    
    path = os.path.join(SCREENSHOT_DIR, 'menu_page.png')
    pygame.image.save(screen, path)
    print(f"截图已保存: {path}")
    
    pygame.quit()

if __name__ == "__main__":
    main()
