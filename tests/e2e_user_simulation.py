# -*- coding: utf-8 -*-
# @Function: E2E 真实用户全流程模拟测试
# 模拟真实玩家的完整操作路径：真实时钟、真实事件投递、随机行为序列，
# 覆盖三种模式、全部页面、道具、暂停/重开、弹窗、连点压力与游戏全生命周期。

import sys
import os
import random
import tempfile
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 数据隔离：E2E 全程使用临时存档，绝不触碰玩家真实数据（必须在导入 src 前设置）
os.environ.setdefault(
    "GAME_2048_DATA_DIR",
    os.path.join(tempfile.gettempdir(), "2048_game_e2e_data"),
)

import pygame

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((800, 600), pygame.HIDDEN)
pygame.key.set_repeat(220, 110)

from src.config import FPS, WINDOW_WIDTH, WINDOW_HEIGHT
from src.views.pages import (
    PageManager, MenuPage, GamePage, ResultPage,
    SettingsPage, AchievementsPage, PausePage, LoginPage,
)
from src.models.game_state import GameState
from src.utils import blit_background

SHOTS = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(SHOTS, exist_ok=True)

pm = PageManager()
for p in (MenuPage(), GamePage(), ResultPage(), SettingsPage(),
          AchievementsPage(), PausePage(), LoginPage()):
    pm.register_page(p)

transition_phase = {"active": False}
pending_action = [None]


def request_switch(name, **kwargs):
    """模拟 main.py 的过渡切页"""
    pending_action[0] = (name, kwargs)
    transition_phase["active"] = True


def apply_switch():
    name, kwargs = pending_action[0]
    pending_action[0] = None
    transition_phase["active"] = False
    if name in ("classic", "game"):
        if name == "classic":
            pm.switch_to("game", mode="classic")
        else:
            # 与 main.py 一致：结算页"再来一局"沿用上一局模式
            gp = pm.get_page("game")
            mode = gp._game_state.mode if gp and gp._game_state else "classic"
            pm.switch_to("game", mode=mode)
    elif name in ("timed", "challenge", "restart"):
        gp = pm.get_page("game")
        if name == "restart":
            mode = gp._game_state.mode if gp and gp._game_state else "classic"
            pm.pop_page()
            pm.switch_to("game", mode=mode)
        else:
            pm.switch_to("game", mode=name)
    elif name == "pause":
        gp = pm.get_page("game")
        if gp and gp._game_state:
            gp._game_state.pause()
        pm.push_page("pause")
    elif name == "resume":
        gp = pm.get_page("game")
        if gp and gp._game_state:
            gp._game_state.resume()
        pm.pop_page()
    elif name == "result":
        gp = pm.get_page("game")
        result = gp.get_game_result() if gp else None
        pm.switch_to("result", result=result or {})
    elif name in ("menu", "settings", "achievements", "login"):
        if pm.current_page and pm.current_page.name == "pause":
            pm.pop_page()
        pm.switch_to(name)


def click(center, frames=2, shot=None):
    """模拟一次真实鼠标点击（移动->按下->抬起），并跑帧消化过渡"""
    pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION, pos=center))
    run(frames)
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=center, button=1))
    run(1)
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=center, button=1))
    run(frames)
    if shot:
        take(shot)


def tap_key(key, frames=2):
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key))
    run(frames)


def run(frames=1, dt_scale=1.0):
    """跑主循环 N 帧：事件->更新->绘制，含过渡状态机（与 main.py 一致）"""
    clock = run._clock
    for _ in range(frames):
        dt = clock.tick(FPS) / 1000.0 * dt_scale
        for ev in pygame.event.get():
            if transition_phase["active"]:
                continue
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                name = pm.current_page.name
                if name == "game":
                    request_switch("pause")
                elif name == "pause":
                    request_switch("resume")
                elif name != "menu":
                    request_switch("menu")
                continue
            target = pm.current_page.handle_event(ev)
            if target:
                request_switch(target)
        target = pm.current_page.update(dt)
        if target:
            request_switch(target)
        if transition_phase["active"]:
            # 简化过渡：本帧末应用切页
            apply_switch()
        blit_background(screen)
        pm.current_page.draw(screen)


run._clock = pygame.time.Clock()


def take(name):
    pygame.image.save(screen, os.path.join(SHOTS, f'e2e_{name}.png'))


def check(cond, msg):
    if not cond:
        print(f'[FAIL] {msg}')
        failures.append(msg)
    else:
        print(f'[ok] {msg}')


failures = []
random.seed(20260910)  # 可复现的"用户"

pm.switch_to("menu")

# ========= 场景 1：主菜单浏览 -> 进入经典模式 =========
run(15)
check(pm.current_page.name == "menu", "S1 启动进入主菜单")
click((WINDOW_WIDTH // 2, 264), shot='menu_hover')  # 经典模式卡片
run(5)
check(pm.current_page.name == "game", "S1 点击经典模式卡片进入游戏")
check(pm.current_page._game_state.mode == "classic", "S1 模式为 classic")

# ========= 场景 2：真实玩家随机操作 40 步（含快速连击、停顿、无效方向）=========
page = pm.current_page
moves_before = page._game_state.board.move_count
for i in range(40):
    key = random.choice([pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN])
    tap_key(key, frames=random.choice([2, 2, 3, 5, 8]))  # 真实玩家节奏不一
run(40, dt_scale=1.0)
moves = page._game_state.board.move_count
check(moves > moves_before, f"S2 随机游玩产生移动（{moves_before}->{moves}）")
check(not page._input_queue, "S2 输入队列已排空")
check(len(page.particles.particles) <= 96, "S2 粒子数受控")
take('game_after_40_moves')

# ========= 场景 3：撤销 & 清理道具 =========
page._on_undo()
check(page._game_state.undo_count >= 2, "S3 撤销后剩余次数正确")
page._on_clean()
cleaned = page._game_state.clean_count
check(cleaned in (0, 1), f"S3 清理次数合法（当前 {cleaned}）")

# ========= 场景 4：暂停 -> 继续 -> 暂停 -> 重新开始 =========
tap_key(pygame.K_ESCAPE, frames=3)
check(pm.current_page.name == "pause", "S4 ESC 暂停")
take('pause_page')
click((WINDOW_WIDTH // 2, 300), frames=3)  # 继续游戏按钮（面板中心 y=300 附近）
run(3)
check(pm.current_page.name == "game", "S4 继续游戏回到棋盘")
tap_key(pygame.K_ESCAPE, frames=3)
check(pm.current_page.name == "pause", "S4 再次暂停")
# 找重新开始按钮（面板内第二颗按钮）
btn = pm.current_page.btn_restart
click(btn.rect.center, frames=3)
run(3)
check(pm.current_page.name == "game", "S4 重新开始回到新局")
check(pm.current_page._game_state.board.move_count == 0, "S4 新局步数为 0")

# ========= 场景 5：限时模式完整生命周期（加速到超时）=========
page = pm.current_page
click(page.btn_back.rect.center, frames=3)  # 先回菜单
run(3)
check(pm.current_page.name == "menu", "S5 返回菜单")
click((WINDOW_WIDTH // 2, 342), frames=3)  # 限时模式卡片
run(3)
page = pm.current_page
check(page._game_state.mode == "timed", "S5 进入限时模式")
page._game_state.start_time -= 59  # 模拟已玩 59 秒
for _ in range(200):
    run(1)
    if pm.current_page.name == "result":
        break
run(3)
check(pm.current_page.name == "result", "S5 超时后进入结算页")
result_data = pm.current_page._result_data
check(result_data.get("mode") == "timed", "S5 结算数据模式正确")
take('result_timed')

# ========= 场景 6：结算页 -> 再来一局 / 返回菜单 =========
btn = pm.current_page.btn_retry
click(btn.rect.center, frames=3)
run(3)
check(pm.current_page.name == "game", "S6 再来一局重新开局")
tap_key(pygame.K_ESCAPE, frames=3)   # 暂停
run(2)
tap_key(pygame.K_ESCAPE, frames=3)   # 继续
run(2)
# 用 ESC 返回菜单
tap_key(pygame.K_ESCAPE, frames=3)   # 暂停
run(2)
tap_key(pygame.K_ESCAPE, frames=3)   # 恢复
run(2)
# 直接点击返回按钮
page = pm.current_page
click(page.btn_back.rect.center, frames=3)
run(3)
check(pm.current_page.name == "menu", "S6 返回按钮回到菜单")

# ========= 场景 7：挑战模式速通胜利路径 =========
click((WINDOW_WIDTH // 2, 420), frames=3)  # 挑战模式卡片
run(3)
page = pm.current_page
check(page._game_state.mode == "challenge", "S7 进入挑战模式")
# 直接把最大方块放到目标值，走一步触发胜利判定
page._game_state.board.max_tile = 128
tap_key(pygame.K_LEFT, frames=2)
run(160)  # 等结束过渡（1.1s）
check(pm.current_page.name == "result", "S7 挑战达成进入结算")
check(pm.current_page._result_data.get("is_win") is True, "S7 结算判定为胜利")
take('result_challenge_win')

# ========= 场景 8：经典模式真实玩到游戏结束（快速填盘）=========
click(pm.current_page.btn_retry.rect.center, frames=3)
run(3)
page = pm.current_page
check(page._game_state.mode == "challenge", "S8 再来一局保持挑战模式")
tap_key(pygame.K_ESCAPE, frames=2)
run(2)
# 从暂停返回菜单，重新进经典模式
btn = pm.current_page.btn_menu
click(btn.rect.center, frames=3)
run(3)
check(pm.current_page.name == "menu", "S8 回到菜单")
click((WINDOW_WIDTH // 2, 264), frames=3)
run(3)
page = pm.current_page
# 强制把棋盘填满制造死局（真实玩家终局的等价状态）
from src.models.tile import Tile
board = page._game_state.board
board.grid = [[None] * 4 for _ in range(4)]
vals = [2, 4, 2, 8, 4, 2, 8, 16, 2, 4, 16, 2, 4, 2, 32, 8]
i = 0
for r in range(4):
    for c in range(4):
        tl = Tile(value=vals[i], row=r, col=c)
        tl.is_new = False
        board.grid[r][c] = tl
        i += 1
board._check_game_state()
run(120)
check(page._ending or pm.current_page.name == "result", "S8 死局触发结束过渡")
run(120)
check(pm.current_page.name == "result", "S8 结束过渡后进入结算")
check(pm.current_page._result_data.get("is_game_over") is True, "S8 结算标记游戏结束")
take('result_game_over')

# ========= 场景 9：失败复活 =========
click(pm.current_page.btn_retry.rect.center, frames=3)
run(3)
page = pm.current_page
board = page._game_state.board
board.grid = [[None] * 4 for _ in range(4)]
i = 0
for r in range(4):
    for c in range(4):
        tl = Tile(value=vals[i], row=r, col=c)
        tl.is_new = False
        board.grid[r][c] = tl
        i += 1
board._check_game_state()
page._game_state.update()
run(30)
check(page._game_state.state == GameState.STATE_GAME_OVER, "S9 制造游戏结束")
page._on_revive()
run(5)
check(page._game_state.state == GameState.STATE_PLAYING, "S9 复活恢复对局")
check(not page._ending, "S9 复活取消结束过渡")

# ========= 场景 10：成就 / 设置（开关+语言+弹窗）/ 登录 全页面遍历 =========
tap_key(pygame.K_ESCAPE, frames=2)
run(2)
tap_key(pygame.K_ESCAPE, frames=2)
run(2)
page = pm.current_page
click(page.btn_back.rect.center, frames=3)
run(3)
click((WINDOW_WIDTH // 2 + 90, 497), frames=3)  # 成就按钮（右侧胶囊）
run(3)
check(pm.current_page.name == "achievements", "S10 进入成就页")
take('achievements_page')
click(pm.current_page.btn_back.rect.center, frames=3)
run(3)
check(pm.current_page.name == "menu", "S10 成就页返回菜单")
click((WINDOW_WIDTH // 2 - 90, 497), frames=3)  # 设置按钮（左侧胶囊）
run(3)
check(pm.current_page.name == "settings", "S10 进入设置页")
sw = pm.current_page.btn_sound
click(sw.rect.center, frames=2)
check(pm.current_page.btn_sound.is_on is False, "S10 音效开关切换为关")
click(sw.rect.center, frames=2)
check(pm.current_page.btn_sound.is_on is True, "S10 音效开关切回开")
lang_row = pm.current_page.lang_row_rect
click(lang_row.center, frames=2)
check(pm.current_page.lang_value.text == "EN", "S10 语言切换到 EN")
take('settings_en')
click(lang_row.center, frames=2)
check(pm.current_page.lang_value.text == "ZH", "S10 语言切回 ZH")
# 重置弹窗：打开后取消
click(pm.current_page.btn_reset.rect.center, frames=2)
check(pm.current_page.alert.is_visible, "S10 重置弹窗弹出")
take('reset_alert')
click(pm.current_page.alert.btn_cancel.rect.center, frames=2)
check(not pm.current_page.alert.is_visible, "S10 取消关闭弹窗")
# 返回菜单
click(pm.current_page.btn_back.rect.center, frames=3)
run(3)

# ========= 场景 11：登录页输入 =========
menu = pm.current_page
# 菜单没有登录入口，直接切页验证页面本身
pm.switch_to("login")
run(5)
page = pm.current_page
check(page.name == "login", "S11 进入登录页")
pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=page.username_box.center, button=1))
for ch in "player1":
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a, unicode=ch))
    run(1)
check(page.username == "player1", f"S11 用户名输入（got '{page.username}'）")
click(page.btn_back.rect.center, frames=3)
run(3)
check(pm.current_page.name == "menu", "S11 登录页返回菜单")

# ========= 场景 12：压力测试 - 疯狂连点/连按 3 秒 =========
page = pm.current_page
click((WINDOW_WIDTH // 2, 264), frames=1)  # 进经典模式
run(2)
errors_before = 0
keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
t0 = time.perf_counter()
frames = 0
while time.perf_counter() - t0 < 3.0:
    if random.random() < 0.75:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=random.choice(keys)))
    if random.random() < 0.08:
        pos = (random.randint(100, 700), random.randint(100, 500))
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1))
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=pos, button=1))
    run(1)
    frames += 1
run(60)
check(pm.current_page is not None, "S12 压力测试后游戏状态正常")
take('stress_after')

# ========= 场景 13：性能抽样（游戏页满负载渲染）=========
times = []
page = pm.current_page
for _ in range(120):
    dt = run._clock.tick(FPS) / 1000.0
    t0 = time.perf_counter()
    page.update(dt)
    blit_background(screen)
    page.draw(screen)
    times.append((time.perf_counter() - t0) * 1000)
times.sort()
p95 = times[114]
print(f'[perf] update+draw p50={times[60]:.2f}ms p95={p95:.2f}ms p99={times[119]:.2f}ms')
check(p95 < 16.7, f"S13 帧耗时 p95 达标（{p95:.2f}ms < 16.7ms）")

# ========= 汇总 =========
print("=" * 46)
if failures:
    print(f"E2E FAILED: {len(failures)} 项未通过")
    for f in failures:
        print("  -", f)
    sys.exit(1)
print("E2E ALL PASSED: 13 个场景全部通过")
pygame.quit()
