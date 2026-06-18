# -*- coding: utf-8 -*-
# @Function: 完整用户流程验证脚本

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
pygame.init()
screen = pygame.display.set_mode((1, 1))

from src.views.pages.base_page import Page, PageManager
from src.views.pages import (
    MenuPage, GamePage, ResultPage, SettingsPage,
    AchievementsPage, PausePage, LoginPage,
)
from src.models.game_state import GameState
from src.models.board import GameBoard
from src.models.tile import Tile
from src.models.data_manager import DataManager
from src.views.sound_manager import SoundManager
from src.i18n import t, set_language, get_language

passed = 0
failed = 0


def check(name, condition):
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {name}")
    else:
        failed += 1
        print(f"  [FAIL] {name}")


def fill_board(board, pattern):
    board.grid = [[None] * board.size for _ in range(board.size)]
    for r in range(board.size):
        for c in range(board.size):
            if pattern[r][c] != 0:
                board.set_tile(r, c, Tile(pattern[r][c], r, c))


print("=" * 60)
print("  2048 Game - User Flow Validation")
print("=" * 60)

# ========== 1. App startup ==========
print("\n[1] App Startup")
PageManager._instance = None
pm = PageManager()
pm.register_page(MenuPage())
pm.register_page(GamePage())
pm.register_page(ResultPage())
pm.register_page(SettingsPage())
pm.register_page(AchievementsPage())
pm.register_page(PausePage())
pm.register_page(LoginPage())
check("Pages registered (7)", len(pm._pages) == 7)
# current_page is None until we explicitly switch
pm.switch_to("menu")
check("Starts on menu", pm.current_page.name == "menu")

# ========== 2. Page navigation ==========
print("\n[2] Page Navigation")
pm.switch_to("game")
check("Navigate to game", pm.current_page.name == "game")
pm.switch_to("settings")
check("Navigate to settings", pm.current_page.name == "settings")
pm.switch_to("achievements")
check("Navigate to achievements", pm.current_page.name == "achievements")
pm.switch_to("menu")
check("Navigate back to menu", pm.current_page.name == "menu")

# ========== 3. Start classic game ==========
print("\n[3] Start Classic Game")
gs = GameState()
gs.start_game("classic")
check("State is PLAYING", gs.state == GameState.STATE_PLAYING)
check("Mode is classic", gs.mode == "classic")
check("Board created", gs.board is not None)
check("Initial tiles >= 2", len(gs.board.get_all_tiles()) >= 2)
check("Undo count is 2", gs.undo_count == 2)
check("Score is 0", gs.board.score == 0)

# ========== 4. Gameplay - move left ==========
print("\n[4] Gameplay - Move Left")
fill_board(gs.board, [
    [2, 2, 4, 4],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
])
gs.board.score = 0
gs.save_for_undo()
moved = gs.board.move("left")
check("Move succeeded", moved)
check("2+2=4 at [0,0]", gs.board.grid[0][0].value == 4)
check("4+4=8 at [0,1]", gs.board.grid[0][1].value == 8)
check("Score is 12", gs.board.score == 12)

# ========== 5. Undo ==========
print("\n[5] Undo")
result = gs.undo()
check("Undo succeeded", result)
check("Score restored to 0", gs.board.score == 0)
check("Undo count decreased", gs.undo_count == 1)

# ========== 6. Move right ==========
print("\n[6] Move Right")
fill_board(gs.board, [
    [2, 2, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
])
gs.board.score = 0
moved = gs.board.move("right")
check("Move right succeeded", moved)
check("Merged at [0,3]", gs.board.grid[0][3].value == 4)

# ========== 7. Move up ==========
print("\n[7] Move Up")
fill_board(gs.board, [
    [2, 0, 0, 0],
    [2, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
])
moved = gs.board.move("up")
check("Move up succeeded", moved)
check("Merged at [0,0]", gs.board.grid[0][0].value == 4)

# ========== 8. Move down ==========
print("\n[8] Move Down")
fill_board(gs.board, [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [2, 0, 0, 0],
    [2, 0, 0, 0],
])
moved = gs.board.move("down")
check("Move down succeeded", moved)
check("Merged at [3,0]", gs.board.grid[3][0].value == 4)

# ========== 9. No move possible ==========
print("\n[9] No Move Possible")
fill_board(gs.board, [
    [2, 4, 2, 4],
    [4, 2, 4, 2],
    [2, 4, 2, 4],
    [4, 2, 4, 2],
])
moved = gs.board.move("left")
check("No move on alternating pattern", not moved)

# ========== 10. Win detection ==========
print("\n[10] Win Detection")
gs2 = GameState()
gs2.start_game("classic")
fill_board(gs2.board, [
    [1024, 1024, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
])
gs2.board.move("left")
check("Win detected after 1024+1024", gs2.board.is_won)
check("Value is 2048", gs2.board.grid[0][0].value == 2048)

# ========== 11. Continue after win ==========
print("\n[11] Continue After Win")
gs2.board.continue_after_win()
check("is_won reset", not gs2.board.is_won)
check("keep_playing set", gs2.board.keep_playing)

# ========== 12. Game over detection ==========
print("\n[12] Game Over Detection")
gs3 = GameState()
gs3.start_game("classic")
fill_board(gs3.board, [
    [2, 4, 2, 4],
    [4, 2, 4, 2],
    [2, 4, 2, 4],
    [4, 2, 4, 2],
])
gs3.board._check_game_state()
check("Game over detected", gs3.board.is_game_over)

# ========== 13. Clean power-up ==========
print("\n[13] Clean Power-up")
gs4 = GameState()
gs4.start_game("classic")
gs4.clean_count = 1
fill_board(gs4.board, [
    [2, 0, 0, 0],
    [0, 4, 0, 0],
    [0, 0, 8, 0],
    [0, 0, 0, 0],
])
result = gs4.use_clean()
check("Clean succeeded", result)
check("Tile 2 removed", gs4.board.get_tile(0, 0) is None)
check("Tile 4 still there", gs4.board.get_tile(1, 1) is not None)
check("Tile 8 still there", gs4.board.get_tile(2, 2) is not None)

# ========== 14. Timed mode ==========
print("\n[14] Timed Mode")
gs5 = GameState()
gs5.start_game("timed", {"time_limit": 60})
check("Mode is timed", gs5.mode == "timed")
check("Time remaining 60", gs5.time_remaining == 60)

# ========== 15. Challenge mode ==========
print("\n[15] Challenge Mode")
gs6 = GameState()
gs6.start_game("challenge", {"move_limit": 50, "target_tile": 128})
check("Mode is challenge", gs6.mode == "challenge")
check("Move limit 50", gs6.move_limit == 50)
check("Target tile 128", gs6.target_tile == 128)

# ========== 16. Pause / Resume ==========
print("\n[16] Pause / Resume")
gs7 = GameState()
gs7.start_game("classic")
gs7.pause()
check("State is PAUSED", gs7.state == GameState.STATE_PAUSED)
gs7.resume()
check("State is PLAYING again", gs7.state == GameState.STATE_PLAYING)

# ========== 17. Data persistence ==========
print("\n[17] Data Persistence")
DataManager._instance = None
dm = DataManager()
dm.reset_data()
dm.update_high_score(9999)
check("High score saved", dm.get("high_score") == 9999)
dm.update_high_score(1000)
check("Lower score not saved", dm.get("high_score") == 9999)
initial_games = dm.get("total_games")
dm.increment_games()
check("Total games incremented", dm.get("total_games") == initial_games + 1)
dm.add_achievement("first_128")
check("Achievement unlocked", dm.has_achievement("first_128"))
dm.add_achievement("first_128")
check("Achievement not duplicated", dm.get("achievements").count("first_128") == 1)

# ========== 18. i18n ==========
print("\n[18] Internationalization")
check("Default lang is zh", get_language() == "zh")
check("Chinese start_game", t("start_game") == "开始游戏")
set_language("en")
check("English start_game", t("start_game") == "Start Game")
set_language("zh")
check("Language restored to zh", get_language() == "zh")

# ========== 19. Serialization ==========
print("\n[19] Serialization")
board_a = GameBoard()
fill_board(board_a, [
    [2, 0, 0, 0],
    [0, 128, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
])
board_a.score = 500
data = board_a.to_dict()
board_b = GameBoard.from_dict(data)
check("Serialized score", board_b.score == 500)
check("Tile [0,0] = 2", board_b.grid[0][0].value == 2)
check("Tile [1,1] = 128", board_b.grid[1][1].value == 128)

# ========== 20. Chain merge ==========
print("\n[20] Chain Merge (2+2+2+2)")
board_c = GameBoard()
fill_board(board_c, [
    [2, 2, 2, 2],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
])
board_c.move("left")
check("Chain: [0,0]=4", board_c.grid[0][0].value == 4)
check("Chain: [0,1]=4", board_c.grid[0][1].value == 4)
check("Chain score=8", board_c.score == 8)

# ========== Summary ==========
print("\n" + "=" * 60)
total = passed + failed
print(f"  Results: {passed}/{total} passed, {failed} failed")
print("=" * 60)

pygame.quit()
sys.exit(0 if failed == 0 else 1)
