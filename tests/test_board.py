# -*- coding: utf-8 -*-
# @Function: 核心模型单元测试 - GameBoard 滑动合并算法测试

import unittest
from src.models.board import GameBoard
from src.models.tile import Tile


class TestTile(unittest.TestCase):
    """Tile 模型测试"""

    def test_create_tile(self):
        """测试创建方块"""
        tile = Tile(value=2, row=0, col=0)
        self.assertEqual(tile.value, 2)
        self.assertEqual(tile.row, 0)
        self.assertEqual(tile.col, 0)
        self.assertTrue(tile.is_new)

    def test_set_position(self):
        """测试设置位置"""
        tile = Tile(value=4, row=1, col=1)
        tile.set_position(2, 3, save_prev=True)
        self.assertEqual(tile.row, 2)
        self.assertEqual(tile.col, 3)
        self.assertEqual(tile.prev_row, 1)
        self.assertEqual(tile.prev_col, 1)

    def test_to_dict(self):
        """测试序列化"""
        tile = Tile(value=8, row=2, col=3)
        data = tile.to_dict()
        self.assertEqual(data, {"value": 8, "row": 2, "col": 3})

    def test_from_dict(self):
        """测试反序列化"""
        data = {"value": 16, "row": 1, "col": 2}
        tile = Tile.from_dict(data)
        self.assertEqual(tile.value, 16)
        self.assertEqual(tile.row, 1)
        self.assertEqual(tile.col, 2)
        self.assertFalse(tile.is_new)


class TestGameBoard(unittest.TestCase):
    """GameBoard 棋盘核心逻辑测试"""

    def test_initial_state(self):
        """测试初始状态"""
        board = GameBoard()
        board.reset()
        # 应有 2 个初始方块
        tiles = board.get_all_tiles()
        self.assertEqual(len(tiles), 2)
        # 方块值应为 2 或 4
        for tile in tiles:
            self.assertIn(tile.value, [2, 4])
        self.assertEqual(board.score, 0)
        self.assertFalse(board.is_game_over)
        self.assertFalse(board.is_won)

    def test_empty_cells(self):
        """测试空单元格计算"""
        board = GameBoard()
        board.reset()
        empty = board.get_empty_cells()
        self.assertEqual(len(empty), 14)  # 16 - 2 初始方块

    def test_slide_left(self):
        """测试向左滑动"""
        board = GameBoard()
        # 手动设置棋盘状态
        board.grid = [[None] * 4 for _ in range(4)]
        board.grid[0][0] = Tile(value=2, row=0, col=0)
        board.grid[0][2] = Tile(value=2, row=0, col=2)
        # 向左滑动：两个 2 应该合并成 4
        moved = board._slide_left()
        self.assertTrue(moved)
        self.assertIsNotNone(board.grid[0][0])
        self.assertEqual(board.grid[0][0].value, 4)
        self.assertIsNone(board.grid[0][1])
        self.assertIsNone(board.grid[0][2])
        self.assertIsNone(board.grid[0][3])
        self.assertEqual(board.score, 4)

    def test_slide_right(self):
        """测试向右滑动"""
        board = GameBoard()
        board.grid = [[None] * 4 for _ in range(4)]
        board.grid[0][0] = Tile(value=2, row=0, col=0)
        board.grid[0][2] = Tile(value=2, row=0, col=2)
        moved = board._slide_right()
        self.assertTrue(moved)
        self.assertIsNone(board.grid[0][0])
        self.assertIsNone(board.grid[0][1])
        self.assertIsNone(board.grid[0][2])
        self.assertIsNotNone(board.grid[0][3])
        self.assertEqual(board.grid[0][3].value, 4)
        self.assertEqual(board.score, 4)

    def test_slide_up(self):
        """测试向上滑动"""
        board = GameBoard()
        board.grid = [[None] * 4 for _ in range(4)]
        board.grid[0][0] = Tile(value=4, row=0, col=0)
        board.grid[2][0] = Tile(value=4, row=2, col=0)
        moved = board._slide_up()
        self.assertTrue(moved)
        self.assertIsNotNone(board.grid[0][0])
        self.assertEqual(board.grid[0][0].value, 8)
        self.assertIsNone(board.grid[1][0])
        self.assertIsNone(board.grid[2][0])
        self.assertEqual(board.score, 8)

    def test_slide_down(self):
        """测试向下滑动"""
        board = GameBoard()
        board.grid = [[None] * 4 for _ in range(4)]
        board.grid[0][0] = Tile(value=2, row=0, col=0)
        board.grid[2][0] = Tile(value=2, row=2, col=0)
        moved = board._slide_down()
        self.assertTrue(moved)
        self.assertIsNone(board.grid[0][0])
        self.assertIsNone(board.grid[1][0])
        self.assertIsNone(board.grid[2][0])
        self.assertIsNotNone(board.grid[3][0])
        self.assertEqual(board.grid[3][0].value, 4)
        self.assertEqual(board.score, 4)

    def test_merge_multiple(self):
        """测试连续合并"""
        board = GameBoard()
        board.grid = [[None] * 4 for _ in range(4)]
        board.grid[0][0] = Tile(value=2, row=0, col=0)
        board.grid[0][1] = Tile(value=2, row=0, col=1)
        board.grid[0][2] = Tile(value=2, row=0, col=2)
        board.grid[0][3] = Tile(value=2, row=0, col=3)
        moved = board._slide_left()
        self.assertTrue(moved)
        # 应该合并成 [4, 4, None, None]
        self.assertEqual(board.grid[0][0].value, 4)
        self.assertEqual(board.grid[0][1].value, 4)
        self.assertIsNone(board.grid[0][2])
        self.assertIsNone(board.grid[0][3])
        self.assertEqual(board.score, 8)

    def test_no_merge_different_values(self):
        """测试不同值不合并"""
        board = GameBoard()
        board.grid = [[None] * 4 for _ in range(4)]
        board.grid[0][0] = Tile(value=2, row=0, col=0)
        board.grid[0][1] = Tile(value=4, row=0, col=1)
        moved = board._slide_left()
        # 值不同，位置不变，不发生移动
        self.assertFalse(moved)

    def test_win_condition(self):
        """测试获胜条件"""
        board = GameBoard()
        board.grid = [[None] * 4 for _ in range(4)]
        board.grid[0][0] = Tile(value=1024, row=0, col=0)
        board.grid[0][1] = Tile(value=1024, row=0, col=1)
        board._slide_left()
        self.assertTrue(board.is_won)
        self.assertEqual(board.grid[0][0].value, 2048)

    def test_game_over_detection(self):
        """测试游戏结束检测"""
        board = GameBoard()
        # 填满棋盘，没有可合并的方块
        values = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ]
        for r in range(4):
            for c in range(4):
                board.grid[r][c] = Tile(value=values[r][c], row=r, col=c)
        board._check_game_state()
        self.assertTrue(board.is_game_over)

    def test_undo(self):
        """测试撤销"""
        board = GameBoard()
        board.grid = [[None] * 4 for _ in range(4)]
        board.grid[0][0] = Tile(value=2, row=0, col=0)
        board.grid[0][2] = Tile(value=2, row=0, col=2)
        board.score = 0

        # 保存状态
        prev_grid = board._clone_grid()
        prev_score = board.score

        # 移动
        board._slide_left()
        self.assertEqual(board.score, 4)

        # 撤销
        board.undo(prev_grid, prev_score)
        self.assertEqual(board.score, 0)
        self.assertIsNotNone(board.grid[0][0])
        self.assertEqual(board.grid[0][0].value, 2)
        self.assertIsNotNone(board.grid[0][2])
        self.assertEqual(board.grid[0][2].value, 2)

    def test_clean_min_tile(self):
        """测试清理最小方块"""
        board = GameBoard()
        board.grid = [[None] * 4 for _ in range(4)]
        board.grid[0][0] = Tile(value=2, row=0, col=0)
        board.grid[0][1] = Tile(value=4, row=0, col=1)
        board.grid[0][2] = Tile(value=8, row=0, col=2)

        pos = board.clean_min_tile()
        self.assertEqual(pos, (0, 0))
        self.assertIsNone(board.grid[0][0])

    def test_serialization(self):
        """测试序列化/反序列化"""
        board = GameBoard()
        board.grid = [[None] * 4 for _ in range(4)]
        board.grid[0][0] = Tile(value=2, row=0, col=0)
        board.grid[1][1] = Tile(value=4, row=1, col=1)
        board.score = 100

        data = board.to_dict()
        restored = GameBoard.from_dict(data)

        self.assertEqual(restored.score, 100)
        self.assertEqual(restored.size, 4)
        self.assertIsNotNone(restored.grid[0][0])
        self.assertEqual(restored.grid[0][0].value, 2)
        self.assertIsNotNone(restored.grid[1][1])
        self.assertEqual(restored.grid[1][1].value, 4)


if __name__ == "__main__":
    unittest.main()
