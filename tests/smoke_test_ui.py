# -*- coding: utf-8 -*-
# @Function: 冒烟测试 - 真实时钟主循环模拟（输入队列/连发/页面切换）

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pygame

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((800, 600), pygame.HIDDEN)
pygame.key.set_repeat(220, 110)  # 与 main.py 一致

from src.config import FPS, KEY_REPEAT_DELAY_MS, KEY_REPEAT_INTERVAL_MS
from src.views.pages import PageManager, MenuPage, GamePage, ResultPage, SettingsPage, AchievementsPage, PausePage, LoginPage
from src.utils import blit_background

pm = PageManager()
for p in (MenuPage(), GamePage(), ResultPage(), SettingsPage(), AchievementsPage(), PausePage(), LoginPage()):
    pm.register_page(p)

def handle(target):
    if target == "classic" or target == "game":
        pm.switch_to("game", mode="classic")
    elif target == "pause":
        pm.push_page("pause")
    elif target == "resume":
        pm.pop_page()
    elif target:
        pm.switch_to(target)

pm.switch_to("menu")
clock = pygame.time.Clock()
errors = []

def pump(frames=30, label=""):
    for _ in range(frames):
        dt = clock.tick(FPS) / 1000.0
        for ev in pygame.event.get():
            # 复刻 main.py 的全局 ESC 逻辑
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                name = pm.current_page.name
                if name == "game":
                    handle("pause")
                    continue
                elif name == "pause":
                    handle("resume")
                    continue
            t = pm.current_page.handle_event(ev)
            if t: handle(t)
        t = pm.current_page.update(dt)
        if t: handle(t)
        screen.fill((0, 0, 0))
        pm.current_page.draw(screen)
    print(f"[ok] {label} -> page={pm.current_page.name}")

# 1. 菜单 -> 点击经典模式卡片（模拟鼠标点击卡片中心）
card = pm.current_page.mode_cards[0]
pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION, pos=card.rect.center))
pump(2, "hover")
pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=card.rect.center, button=1))
pump(1, "press")
pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=card.rect.center, button=1))
pump(2, "release")
assert pm.current_page.name == "game", f"expected game, got {pm.current_page.name}"
print("[ok] 进入游戏页")

# 2. 单次按键移动
before = pm.current_page._game_state.board.move_count
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
pump(30, "single move")  # 0.5s 真实时间，动画完成
after = pm.current_page._game_state.board.move_count
assert after == before + 1, f"move_count {before} -> {after}"
print(f"[ok] 单步移动成功 move_count={after}")

# 3. 按住连发（按真实 set_repeat 间隔 110ms ≈ 7 帧发 KEYDOWN）
#    上下交替保证每步棋盘都有变化（同方向连按在贴边后本就是无效操作）
before = pm.current_page._game_state.board.move_count
for i in range(8):
    key = pygame.K_DOWN if i % 2 == 0 else pygame.K_UP
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key))
    pump(7, f"repeat {i}")  # 7 帧 ≈ 116ms，接近真实连发间隔
pump(40, "flush queue")
after = pm.current_page._game_state.board.move_count
applied = after - before
# 节奏上限：每次移动最快约 132ms（0.6*220ms），8 次按键窗口内至少应应用 6 步，
# 松键后队列必须排空，不滞留输入
print(f"[ok] 连发 8 次 KEYDOWN(110ms) -> 实际应用 {applied} 步 (节奏上限 6-8)")
assert applied >= 6, f"低于节奏上限! 应用 {applied}/8"
assert pm.current_page._input_queue == [], "队列未排空"

# 3b. 动画中快速交替方向：不同方向的输入必须全部保留应用
before = pm.current_page._game_state.board.move_count
for d in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT):
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=d))
    pump(2, "alt")  # 33ms 间隔快速交替，前几步会进队列
pump(60, "flush alt")
applied = pm.current_page._game_state.board.move_count - before
print(f"[ok] 快速交替 4 次方向 -> 实际应用 {applied} 步 (期望 4)")
assert applied == 4, f"方向输入丢失! 应用 {applied}/4"

# 4. 鼠标滑动
start = (400, 300)
pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=start, button=1))
pump(1, "swipe down")
pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(400, 380), button=1))
pump(30, "swipe applied")
print(f"[ok] 滑动后 move_count={pm.current_page._game_state.board.move_count}")

# 5. ESC 暂停 -> 继续
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
pump(2, "pause")
assert pm.current_page.name == "pause", f"expected pause, got {pm.current_page.name}"
print("[ok] ESC 暂停")
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
pump(2, "resume")
assert pm.current_page.name == "game", f"expected game, got {pm.current_page.name}"
print("[ok] ESC 继续")

# 6. 性能抽样：游戏页 update+draw 纯耗时（不含 clock.tick 限流睡眠）
import time
times = []
for _ in range(120):
    dt = clock.tick(FPS) / 1000.0
    t0 = time.perf_counter()
    pm.current_page.update(dt)
    blit_background(screen)
    pm.current_page.draw(screen)
    times.append((time.perf_counter() - t0) * 1000)
times.sort()
print(f"[perf] update+draw 耗时 p50={times[60]:.2f}ms p95={times[114]:.2f}ms p99={times[119]:.2f}ms (16.7ms 预算)")
assert times[114] < 16.7, "p95 超出 60FPS 预算!"

print("\nALL SMOKE TESTS PASSED")
pygame.quit()
