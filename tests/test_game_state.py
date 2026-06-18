# -*- coding: utf-8 -*-
# @Function: GameState 模型单元测试

import unittest
from src.models.game_state import GameState
from src.models.board import GameBoard
from src.models.tile import Tile


def _fill_board(board: GameBoard, pattern: list) -> None:
    """用指定模式填充棋盘"""
    board.grid = [[None] * board.size for _ in range(board.size)]
    for r in range(board.size):
        for c in range(board.size):
            if pattern[r][c] != 0:
                board.set_tile(r, c, Tile(pattern[r][c], r, c))


class TestGameState(unittest.TestCase):
    """GameState 运行时状态测试"""

    def test_initial_state(self):
        """测试初始状态"""
        gs = GameState()
        self.assertEqual(gs.state, GameState.STATE_IDLE)
        self.assertIsNone(gs.board)
        self.assertEqual(gs.mode, "classic")

    def test_start_game_classic(self):
        """测试开始经典模式"""
        gs = GameState()
        gs.start_game("classic")
        self.assertEqual(gs.state, GameState.STATE_PLAYING)
        self.assertEqual(gs.mode, "classic")
        self.assertIsInstance(gs.board, GameBoard)
        self.assertEqual(gs.undo_count, 2)

    def test_start_game_timed(self):
        """测试开始计时模式"""
        gs = GameState()
        gs.start_game("timed", {"time_limit": 60})
        self.assertEqual(gs.state, GameState.STATE_PLAYING)
        self.assertEqual(gs.mode, "timed")
        self.assertEqual(gs.time_remaining, 60)

    def test_pause_resume(self):
        """测试暂停和恢复"""
        gs = GameState()
        gs.start_game("classic")
        self.assertEqual(gs.state, GameState.STATE_PLAYING)

        gs.pause()
        self.assertEqual(gs.state, GameState.STATE_PAUSED)

        gs.resume()
        self.assertEqual(gs.state, GameState.STATE_PLAYING)

    def test_undo(self):
        """测试撤销功能"""
        gs = GameState()
        gs.start_game("classic")

        # 保存初始状态
        initial_undo = gs.undo_count

        # 模拟一步操作
        _fill_board(gs.board, [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        gs.save_for_undo()
        gs.board.score = 100

        # 执行撤销
        result = gs.undo()
        self.assertTrue(result)
        self.assertEqual(gs.undo_count, initial_undo - 1)
        self.assertEqual(gs.board.score, 0)

    def test_undo_no_moves(self):
        """测试无操作时撤销"""
        gs = GameState()
        gs.start_game("classic")
        gs.undo_count = 0

        result = gs.undo()
        self.assertFalse(result)

    def test_clean(self):
        """测试清理功能"""
        gs = GameState()
        gs.start_game("classic")
        gs.clean_count = 1

        _fill_board(gs.board, [
            [2, 0, 0, 0],
            [0, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])

        result = gs.use_clean()
        self.assertTrue(result)
        # 2应被移除
        self.assertIsNone(gs.board.get_tile(0, 0))
        self.assertIsNotNone(gs.board.get_tile(1, 1))

    def test_check_game_over(self):
        """测试游戏结束检测"""
        gs = GameState()
        gs.start_game("classic")

        # 填满棋盘，无合并可能
        _fill_board(gs.board, [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ])
        gs.board._check_game_state()
        self.assertTrue(gs.board.is_game_over)

    def test_check_win(self):
        """测试胜利检测（通过合并触发）"""
        gs = GameState()
        gs.start_game("classic")

        _fill_board(gs.board, [
            [1024, 1024, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        gs.board.move("left")
        self.assertTrue(gs.board.is_won)
        self.assertEqual(gs.board.grid[0][0].value, 2048)

    def test_game_over_state(self):
        """测试游戏结束状态"""
        gs = GameState()
        gs.start_game("classic")

        _fill_board(gs.board, [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ])
        gs.board._check_game_state()
        self.assertTrue(gs.board.is_game_over)


class TestGameBoardExtended(unittest.TestCase):
    """GameBoard 扩展测试"""

    def test_move_left(self):
        """测试左移"""
        board = GameBoard()
        _fill_board(board, [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        moved = board.move("left")
        self.assertTrue(moved)
        self.assertEqual(board.grid[0][0].value, 4)
        # 新方块会随机生成在剩余空格中，验证[0,0]已合并
        self.assertTrue(board.grid[0][0].value == 4)

    def test_move_right(self):
        """测试右移"""
        board = GameBoard()
        _fill_board(board, [
            [0, 0, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        moved = board.move("right")
        self.assertTrue(moved)
        self.assertEqual(board.grid[0][3].value, 4)

    def test_move_up(self):
        """测试上移"""
        board = GameBoard()
        _fill_board(board, [
            [2, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        moved = board.move("up")
        self.assertTrue(moved)
        self.assertEqual(board.grid[0][0].value, 4)

    def test_move_down(self):
        """测试下移"""
        board = GameBoard()
        _fill_board(board, [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 0, 0, 0],
            [2, 0, 0, 0],
        ])
        moved = board.move("down")
        self.assertTrue(moved)
        self.assertEqual(board.grid[3][0].value, 4)

    def test_no_move(self):
        """测试无法移动"""
        board = GameBoard()
        _fill_board(board, [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ])
        moved = board.move("left")
        self.assertFalse(moved)

    def test_get_empty_cells(self):
        """测试获取空格"""
        board = GameBoard()
        _fill_board(board, [
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        empty = board.get_empty_cells()
        self.assertEqual(len(empty), 15)

    def test_get_all_tiles(self):
        """测试获取所有方块"""
        board = GameBoard()
        _fill_board(board, [
            [2, 0, 0, 0],
            [0, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        tiles = board.get_all_tiles()
        self.assertEqual(len(tiles), 2)
        values = [t.value for t in tiles]
        self.assertIn(2, values)
        self.assertIn(4, values)

    def test_serialization_roundtrip(self):
        """测试序列化/反序列化往返"""
        board = GameBoard()
        _fill_board(board, [
            [2, 0, 0, 0],
            [0, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        board.score = 100

        data = board.to_dict()
        board2 = GameBoard.from_dict(data)

        self.assertEqual(board2.score, 100)
        self.assertEqual(board2.grid[0][0].value, 2)
        self.assertEqual(board2.grid[1][1].value, 4)


if __name__ == "__main__":
    unittest.main()
