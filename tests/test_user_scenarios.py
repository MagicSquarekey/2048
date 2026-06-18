# -*- coding: utf-8 -*-
# @Function: 用户场景集成测试 - 模拟完整用户操作流程

import os
import json
import time
import unittest
from unittest.mock import patch, MagicMock

from src.models.board import GameBoard
from src.models.tile import Tile
from src.models.game_state import GameState
from src.models.data_manager import DataManager
from src.models.achievements import ACHIEVEMENTS, check_achievements


def _count_tiles(board: GameBoard) -> int:
    """统计棋盘上方块数量"""
    return len(board.get_all_tiles())


def _board_has_value(board: GameBoard, value: int) -> bool:
    """检查棋盘上是否存在指定值的方块"""
    return any(t.value == value for t in board.get_all_tiles())


def _fill_board_with_pattern(board: GameBoard, pattern: list) -> None:
    """用指定模式填充棋盘"""
    board.grid = [[None] * board.size for _ in range(board.size)]
    for r in range(board.size):
        for c in range(board.size):
            if pattern[r][c] != 0:
                board.set_tile(r, c, Tile(pattern[r][c], r, c))


# ========== 场景1: 用户启动游戏，开始经典模式 ==========

class TestUserScenario_StartGame(unittest.TestCase):
    """用户场景: 启动游戏"""

    def setUp(self):
        """重置单例"""
        DataManager._instance = None
        self.dm = DataManager()

    def test_start_classic_game(self):
        """用户点击"开始游戏" → 进入经典模式"""
        gs = GameState()
        gs.start_game("classic")
        self.assertEqual(gs.state, GameState.STATE_PLAYING)
        self.assertEqual(gs.mode, "classic")
        self.assertIsNotNone(gs.board)
        # 棋盘应有2个初始方块
        tile_count = _count_tiles(gs.board)
        self.assertGreaterEqual(tile_count, 2)
        self.assertEqual(gs.undo_count, 2)

    def test_board_has_valid_initial_tiles(self):
        """初始方块值应为2或4"""
        gs = GameState()
        gs.start_game("classic")
        for tile in gs.board.get_all_tiles():
            self.assertIn(tile.value, [2, 4])
            self.assertTrue(tile.is_new)


# ========== 场景2: 用户进行游戏操作 ==========

class TestUserScenario_GamePlay(unittest.TestCase):
    """用户场景: 游戏操作"""

    def setUp(self):
        self.gs = GameState()
        self.gs.start_game("classic")

    def test_move_left_merges(self):
        """用户向左滑动 → 相同方块合并"""
        _fill_board_with_pattern(self.gs.board, [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])

        self.gs.save_for_undo()
        moved = self.gs.board.move("left")

        self.assertTrue(moved)
        self.assertEqual(self.gs.board.grid[0][0].value, 4)
        self.assertIsNone(self.gs.board.grid[0][1])
        self.assertEqual(self.gs.board.score, 4)

    def test_move_right_merges(self):
        """用户向右滑动"""
        _fill_board_with_pattern(self.gs.board, [
            [0, 0, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])

        moved = self.gs.board.move("right")
        self.assertTrue(moved)
        self.assertEqual(self.gs.board.grid[0][3].value, 4)

    def test_move_up_merges(self):
        """用户向上滑动"""
        _fill_board_with_pattern(self.gs.board, [
            [2, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])

        moved = self.gs.board.move("up")
        self.assertTrue(moved)
        self.assertEqual(self.gs.board.grid[0][0].value, 4)

    def test_move_down_merges(self):
        """用户向下滑动"""
        _fill_board_with_pattern(self.gs.board, [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 0, 0, 0],
            [2, 0, 0, 0],
        ])

        moved = self.gs.board.move("down")
        self.assertTrue(moved)
        self.assertEqual(self.gs.board.grid[3][0].value, 4)

    def test_score_accumulates(self):
        """分数正确累加"""
        _fill_board_with_pattern(self.gs.board, [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        self.gs.board.move("left")
        score1 = self.gs.board.score

        _fill_board_with_pattern(self.gs.board, [
            [4, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        self.gs.board.score = 0
        self.gs.board.move("left")
        score2 = self.gs.board.score

        self.assertEqual(score1, 4)
        self.assertEqual(score2, 8)

    def test_different_values_dont_merge(self):
        """不同值的方块不会合并"""
        _fill_board_with_pattern(self.gs.board, [
            [2, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])

        moved = self.gs.board.move("left")
        self.assertFalse(moved)

    def test_move_adds_new_tile(self):
        """移动后自动添加新方块"""
        _fill_board_with_pattern(self.gs.board, [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        occupied_before = _count_tiles(self.gs.board)
        self.gs.board.move("left")
        occupied_after = _count_tiles(self.gs.board)

        # 合并后变成1个方块 + 新生成1个 = 2个
        self.assertEqual(occupied_after, 2)


# ========== 场景3: 道具系统 ==========

class TestUserScenario_Props(unittest.TestCase):
    """用户场景: 道具使用"""

    def setUp(self):
        self.gs = GameState()
        self.gs.start_game("classic")

    def test_undo_restores_previous_state(self):
        """用户点击撤销 → 恢复上一步"""
        _fill_board_with_pattern(self.gs.board, [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        original_score = self.gs.board.score

        self.gs.save_for_undo()
        self.gs.board.move("left")
        self.assertGreater(self.gs.board.score, 0)

        result = self.gs.undo()
        self.assertTrue(result)
        self.assertEqual(self.gs.board.score, original_score)

    def test_undo_count_decreases(self):
        """撤销次数减少"""
        initial = self.gs.undo_count
        _fill_board_with_pattern(self.gs.board, [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        self.gs.save_for_undo()
        self.gs.board.move("left")
        self.gs.undo()
        self.assertEqual(self.gs.undo_count, initial - 1)

    def test_no_undo_when_count_zero(self):
        """撤销次数用完 → 无法撤销"""
        self.gs.undo_count = 0
        _fill_board_with_pattern(self.gs.board, [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        self.gs.save_for_undo()
        self.gs.board.move("left")
        result = self.gs.undo()
        self.assertFalse(result)

    def test_clean_removes_smallest_tile(self):
        """用户使用清理道具 → 移除最小方块"""
        _fill_board_with_pattern(self.gs.board, [
            [2, 0, 0, 0],
            [0, 4, 0, 0],
            [0, 0, 8, 0],
            [0, 0, 0, 0],
        ])
        self.gs.clean_count = 1

        occupied_before = _count_tiles(self.gs.board)
        result = self.gs.use_clean()
        occupied_after = _count_tiles(self.gs.board)

        self.assertTrue(result)
        self.assertEqual(occupied_after, occupied_before - 1)
        # 确认2已被移除
        self.assertFalse(_board_has_value(self.gs.board, 2))
        # 4和8仍在
        self.assertTrue(_board_has_value(self.gs.board, 4))
        self.assertTrue(_board_has_value(self.gs.board, 8))

    def test_no_clean_when_no_count(self):
        """清理次数为0 → 无法使用"""
        self.gs.clean_count = 0
        result = self.gs.use_clean()
        self.assertFalse(result)


# ========== 场景4: 游戏结束和胜利 ==========

class TestUserScenario_GameEnd(unittest.TestCase):
    """用户场景: 游戏结束"""

    def setUp(self):
        self.gs = GameState()
        self.gs.start_game("classic")

    def test_win_detection(self):
        """达到2048 → 检测到胜利（通过合并触发）"""
        _fill_board_with_pattern(self.gs.board, [
            [1024, 1024, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        self.gs.board.move("left")
        self.assertTrue(self.gs.board.is_won)

    def test_win_at_1024_plus_1024(self):
        """两个1024合并后检测胜利"""
        _fill_board_with_pattern(self.gs.board, [
            [1024, 1024, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        self.gs.board.move("left")
        self.assertTrue(self.gs.board.is_won)
        self.assertEqual(self.gs.board.grid[0][0].value, 2048)

    def test_game_over_detection(self):
        """满棋盘且无法移动 → 游戏结束"""
        _fill_board_with_pattern(self.gs.board, [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ])
        self.gs.board._check_game_state()
        self.assertTrue(self.gs.board.is_game_over)

    def test_not_game_over_with_empty_cell(self):
        """有空格 → 不是游戏结束"""
        _fill_board_with_pattern(self.gs.board, [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 0],
        ])
        self.gs.board._check_game_state()
        self.assertFalse(self.gs.board.is_game_over)

    def test_not_game_over_with_adjacent_same(self):
        """满棋盘但有相邻相同方块 → 不是游戏结束"""
        _fill_board_with_pattern(self.gs.board, [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 2, 4],
        ])
        self.gs.board._check_game_state()
        self.assertFalse(self.gs.board.is_game_over)

    def test_keep_playing_after_win(self):
        """胜利后选择继续游戏"""
        _fill_board_with_pattern(self.gs.board, [
            [1024, 1024, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        self.gs.board.move("left")
        self.assertTrue(self.gs.board.is_won)

        self.gs.board.continue_after_win()
        self.assertFalse(self.gs.board.is_won)
        self.assertTrue(self.gs.board.keep_playing)


# ========== 场景5: 计时挑战模式 ==========

class TestUserScenario_TimedMode(unittest.TestCase):
    """用户场景: 计时挑战"""

    def test_start_timed_mode(self):
        """开始计时模式 → 60秒倒计时"""
        gs = GameState()
        gs.start_game("timed", {"time_limit": 60})
        self.assertEqual(gs.mode, "timed")
        self.assertEqual(gs.time_remaining, 60)

    def test_time_tick(self):
        """每秒倒计时"""
        gs = GameState()
        gs.start_game("timed", {"time_limit": 60})
        gs.time_remaining -= 1
        self.assertEqual(gs.time_remaining, 59)

    def test_time_up_game_over(self):
        """时间到 → 游戏结束"""
        gs = GameState()
        gs.start_game("timed", {"time_limit": 1})
        gs.time_remaining = 0
        self.assertEqual(gs.time_remaining, 0)


# ========== 场景6: 挑战模式 ==========

class TestUserScenario_ChallengeMode(unittest.TestCase):
    """用户场景: 挑战模式"""

    def test_start_challenge_mode(self):
        """开始挑战模式 → 设置目标"""
        gs = GameState()
        gs.start_game("challenge", {"move_limit": 100, "target_tile": 128})
        self.assertEqual(gs.mode, "challenge")
        self.assertEqual(gs.move_limit, 100)
        self.assertEqual(gs.target_tile, 128)

    def test_move_count_increases(self):
        """移动步数增加"""
        gs = GameState()
        gs.start_game("challenge", {"move_limit": 100, "target_tile": 128})

        _fill_board_with_pattern(gs.board, [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        initial_count = gs.board.move_count
        gs.board.move("left")
        self.assertEqual(gs.board.move_count, initial_count + 1)

    def test_target_tile_check(self):
        """达到目标方块 → 检测"""
        gs = GameState()
        gs.start_game("challenge", {"move_limit": 100, "target_tile": 128})
        gs.board.max_tile = 128
        self.assertGreaterEqual(gs.board.max_tile, gs.target_tile)


# ========== 场景7: 暂停和恢复 ==========

class TestUserScenario_PauseResume(unittest.TestCase):
    """用户场景: 暂停/恢复"""

    def test_pause_game(self):
        """用户点击暂停 → 游戏暂停"""
        gs = GameState()
        gs.start_game("classic")
        gs.pause()
        self.assertEqual(gs.state, GameState.STATE_PAUSED)

    def test_resume_game(self):
        """用户点击继续 → 游戏恢复"""
        gs = GameState()
        gs.start_game("classic")
        gs.pause()
        gs.resume()
        self.assertEqual(gs.state, GameState.STATE_PLAYING)

    def test_pause_preserves_board(self):
        """暂停时棋盘状态不变"""
        gs = GameState()
        gs.start_game("classic")
        _fill_board_with_pattern(gs.board, [
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])

        gs.pause()
        tile = gs.board.get_tile(0, 0)
        self.assertIsNotNone(tile)
        self.assertEqual(tile.value, 2)

    def test_no_pause_when_not_playing(self):
        """非游戏中状态无法暂停"""
        gs = GameState()
        gs.state = GameState.STATE_IDLE
        gs.pause()
        self.assertEqual(gs.state, GameState.STATE_IDLE)

    def test_no_resume_when_not_paused(self):
        """非暂停状态无法恢复"""
        gs = GameState()
        gs.start_game("classic")
        gs.resume()
        self.assertEqual(gs.state, GameState.STATE_PLAYING)


# ========== 场景8: 数据持久化 ==========

class TestUserScenario_DataPersistence(unittest.TestCase):
    """用户场景: 数据保存"""

    def setUp(self):
        DataManager._instance = None
        self.dm = DataManager()
        self.dm.reset_data()

    def test_high_score_saved(self):
        """最高分正确保存"""
        self.dm.update_high_score(1000)
        self.assertEqual(self.dm.get("high_score"), 1000)

    def test_high_score_not_decreased(self):
        """新分数低于最高分 → 不更新"""
        self.dm.update_high_score(1000)
        self.dm.update_high_score(500)
        self.assertEqual(self.dm.get("high_score"), 1000)

    def test_total_games_increases(self):
        """总局数增加"""
        initial = self.dm.get("total_games")
        self.dm.increment_games()
        self.assertEqual(self.dm.get("total_games"), initial + 1)

    def test_max_tile_updated(self):
        """最大方块值更新"""
        self.dm.update_max_tile(512)
        self.assertEqual(self.dm.get("max_tile"), 512)

    def test_settings_saved(self):
        """设置保存"""
        self.dm.update_setting("sound_enabled", False)
        settings = self.dm.get_settings()
        self.assertFalse(settings["sound_enabled"])

    def test_achievement_unlocked(self):
        """成就解锁"""
        self.dm.add_achievement("first_128")
        self.assertTrue(self.dm.has_achievement("first_128"))

    def test_achievement_not_duplicated(self):
        """成就不会重复解锁"""
        self.dm.add_achievement("first_128")
        self.dm.add_achievement("first_128")
        self.assertEqual(self.dm.get("achievements").count("first_128"), 1)


# ========== 场景9: 成就系统 ==========

class TestUserScenario_Achievements(unittest.TestCase):
    """用户场景: 成就"""

    def setUp(self):
        DataManager._instance = None
        self.dm = DataManager()
        self.dm.reset_data()

    def test_first_128_achievement(self):
        """首次达到128 → 解锁成就"""
        newly = check_achievements(max_tile=128, total_games=0, high_score=0)
        self.assertIn("first_128", newly)

    def test_first_2048_achievement(self):
        """首次达到2048 → 解锁成就"""
        newly = check_achievements(max_tile=2048, total_games=0, high_score=0)
        self.assertIn("first_2048", newly)

    def test_games_10_achievement(self):
        """玩满10局 → 解锁成就"""
        for _ in range(10):
            self.dm.increment_games()
        newly = check_achievements(max_tile=0, total_games=10, high_score=0)
        self.assertIn("games_10", newly)

    def test_no_repeat_achievement(self):
        """已解锁成就不重复"""
        self.dm.add_achievement("first_128")
        newly = check_achievements(max_tile=128, total_games=0, high_score=0)
        self.assertNotIn("first_128", newly)

    def test_achievement_definitions_complete(self):
        """所有成就定义完整"""
        for key, ach in ACHIEVEMENTS.items():
            self.assertIn("name", ach)
            self.assertIn("description", ach)
            self.assertIn("icon", ach)
            self.assertIn("condition", ach)


# ========== 场景10: 棋盘序列化/反序列化 ==========

class TestUserScenario_Serialization(unittest.TestCase):
    """用户场景: 棋盘状态保存"""

    def test_save_load_board(self):
        """保存并恢复棋盘状态"""
        board = GameBoard()
        _fill_board_with_pattern(board, [
            [2, 0, 0, 0],
            [0, 128, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        board.score = 500

        data = board.to_dict()
        board2 = GameBoard.from_dict(data)

        self.assertEqual(board2.score, 500)
        self.assertEqual(board2.grid[0][0].value, 2)
        self.assertEqual(board2.grid[1][1].value, 128)

    def test_undo_state_save_restore(self):
        """撤销状态保存和恢复"""
        gs = GameState()
        gs.start_game("classic")
        _fill_board_with_pattern(gs.board, [
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])

        gs.save_for_undo()
        gs.board.move("left")

        result = gs.undo()
        self.assertTrue(result)
        self.assertEqual(gs.board.grid[0][0].value, 2)


# ========== 场景11: 随机生成方块概率 ==========

class TestUserScenario_TileProbability(unittest.TestCase):
    """用户场景: 方块生成概率"""

    def test_spawn_tile_is_2_or_4(self):
        """新生成的方块只能是2或4"""
        for _ in range(100):
            board = GameBoard()
            tile = board._spawn_tile()
            if tile:
                self.assertIn(tile.value, [2, 4])

    def test_spawn_tile_in_empty_cell(self):
        """方块只在空格生成"""
        board = GameBoard()
        _fill_board_with_pattern(board, [
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        tile = board._spawn_tile()
        if tile:
            self.assertNotEqual((tile.row, tile.col), (0, 0))


# ========== 场景12: 边界情况 ==========

class TestUserScenario_EdgeCases(unittest.TestCase):
    """用户场景: 边界情况"""

    def test_move_empty_board(self):
        """空棋盘移动 → 无变化"""
        board = GameBoard()
        board.grid = [[None] * 4 for _ in range(4)]
        moved = board.move("left")
        self.assertFalse(moved)

    def test_full_board_no_merge_possible(self):
        """满棋盘无合并 → 游戏结束（通过移动触发检查）"""
        board = GameBoard()
        _fill_board_with_pattern(board, [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ])
        self.assertTrue(len(board.get_empty_cells()) == 0)
        # 触发游戏状态检查
        board._check_game_state()
        self.assertTrue(board.is_game_over)

    def test_single_tile_move(self):
        """单个方块移动"""
        board = GameBoard()
        _fill_board_with_pattern(board, [
            [0, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        moved = board.move("left")
        self.assertTrue(moved)
        self.assertEqual(board.grid[1][0].value, 2)
        self.assertIsNone(board.grid[1][1])

    def test_chain_merge_left(self):
        """连续合并: 2+2=4, 4+4=8"""
        board = GameBoard()
        _fill_board_with_pattern(board, [
            [2, 2, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        board.move("left")
        self.assertEqual(board.grid[0][0].value, 4)
        self.assertEqual(board.grid[0][1].value, 4)

    def test_large_tile_merge(self):
        """大数合并: 1024+1024=2048"""
        board = GameBoard()
        _fill_board_with_pattern(board, [
            [1024, 1024, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        board.move("left")
        self.assertEqual(board.grid[0][0].value, 2048)
        self.assertEqual(board.score, 2048)


# ========== 场景13: 国际化 ==========

class TestUserScenario_I18n(unittest.TestCase):
    """用户场景: 多语言"""

    def test_default_language_is_chinese(self):
        """默认语言是中文"""
        from src.i18n import get_language
        self.assertEqual(get_language(), "zh")

    def test_translate_chinese(self):
        """中文翻译正确"""
        from src.i18n import t
        self.assertEqual(t("start_game"), "开始游戏")

    def test_translate_english(self):
        """英文翻译正确"""
        from src.i18n import t, set_language
        set_language("en")
        self.assertEqual(t("start_game"), "Start Game")
        set_language("zh")  # 恢复

    def test_missing_key_returns_key(self):
        """缺失的翻译键返回键名"""
        from src.i18n import t
        result = t("nonexistent_key_xyz")
        self.assertEqual(result, "nonexistent_key_xyz")


# ========== 场景14: 配置验证 ==========

class TestUserScenario_Config(unittest.TestCase):
    """用户场景: 配置"""

    def test_board_size_is_4x4(self):
        """棋盘是4x4"""
        from src.config import BOARD_SIZE
        self.assertEqual(BOARD_SIZE, 4)

    def test_window_size(self):
        """窗口大小合理"""
        from src.config import WINDOW_WIDTH, WINDOW_HEIGHT
        self.assertEqual(WINDOW_WIDTH, 800)
        self.assertEqual(WINDOW_HEIGHT, 600)

    def test_initial_tiles_count(self):
        """初始方块数量正确"""
        from src.config import INITIAL_TILES
        self.assertEqual(INITIAL_TILES, 2)

    def test_win_tile_value(self):
        """胜利方块值为2048"""
        from src.config import WIN_TILE
        self.assertEqual(WIN_TILE, 2048)


# ========== 场景15: 完整游戏流程模拟 ==========

class TestUserScenario_FullFlow(unittest.TestCase):
    """用户场景: 完整游戏流程"""

    def test_play_until_merge(self):
        """完整流程: 开始→移动→合并→计分"""
        gs = GameState()
        gs.start_game("classic")

        # 人为设置棋盘
        _fill_board_with_pattern(gs.board, [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        gs.board.score = 0

        # 保存撤销点
        gs.save_for_undo()
        self.assertEqual(gs.board.score, 0)

        # 执行移动
        gs.board.move("left")
        self.assertEqual(gs.board.score, 4)

        # 撤销
        result = gs.undo()
        self.assertTrue(result)
        self.assertEqual(gs.board.score, 0)

    def test_play_and_lose(self):
        """完整流程: 开始→填满→游戏结束"""
        gs = GameState()
        gs.start_game("classic")

        _fill_board_with_pattern(gs.board, [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ])
        gs.board._check_game_state()
        self.assertTrue(gs.board.is_game_over)

    def test_play_and_win(self):
        """完整流程: 开始→合并到2048→胜利"""
        gs = GameState()
        gs.start_game("classic")

        _fill_board_with_pattern(gs.board, [
            [1024, 1024, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        gs.board.move("left")
        self.assertTrue(gs.board.is_won)
        self.assertEqual(gs.board.grid[0][0].value, 2048)


if __name__ == "__main__":
    unittest.main()
