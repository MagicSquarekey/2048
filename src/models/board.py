# -*- coding: utf-8 -*-
# @Function: GameBoard 数据模型 - 棋盘状态、滑动合并算法、游戏逻辑

import random
import copy
from typing import List, Optional, Tuple

from src.config import BOARD_SIZE, TILE_2_PROBABILITY, INITIAL_TILES, WIN_TILE
from src.models.tile import Tile


class GameBoard:
    """2048 棋盘核心模型"""

    def __init__(self, size: int = BOARD_SIZE) -> None:
        """初始化空棋盘"""
        self.size: int = size
        self.grid: List[List[Optional[Tile]]] = [
            [None for _ in range(size)] for _ in range(size)
        ]
        self.score: int = 0
        self.best_score: int = 0
        self.move_count: int = 0
        self.max_tile: int = 0
        self.is_game_over: bool = False
        self.is_won: bool = False
        self.keep_playing: bool = False       # 获胜后继续游戏
        self.last_move_score: int = 0         # 上一步得分
        self.merged_positions: List[Tuple[int, int]] = []  # 本次合并位置
        self.moved_tiles: List[Tuple[int, int, int, int]] = []  # (from_r, from_c, to_r, to_c)

    def reset(self) -> None:
        """重置棋盘"""
        self.grid = [
            [None for _ in range(self.size)] for _ in range(self.size)
        ]
        self.score = 0
        self.move_count = 0
        self.max_tile = 0
        self.is_game_over = False
        self.is_won = False
        self.keep_playing = False
        self.last_move_score = 0
        self.merged_positions = []
        self.moved_tiles = []
        # 生成初始方块
        for _ in range(INITIAL_TILES):
            self._spawn_tile()

    def get_tile(self, row: int, col: int) -> Optional[Tile]:
        """获取指定位置的方块"""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col]
        return None

    def set_tile(self, row: int, col: int, tile: Optional[Tile]) -> None:
        """设置指定位置的方块"""
        if 0 <= row < self.size and 0 <= col < self.size:
            self.grid[row][col] = tile
            if tile:
                tile.row = row
                tile.col = col

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """获取所有空单元格"""
        cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] is None:
                    cells.append((r, c))
        return cells

    def _spawn_tile(self) -> Optional[Tile]:
        """在空位置随机生成新方块"""
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return None
        row, col = random.choice(empty_cells)
        value = 2 if random.random() < TILE_2_PROBABILITY else 4
        tile = Tile(value=value, row=row, col=col, is_new=True)
        self.grid[row][col] = tile
        # 更新最大方块
        if value > self.max_tile:
            self.max_tile = value
        return tile

    def move(self, direction: str) -> bool:
        """
        执行滑动操作
        
        Args:
            direction: 方向 "up", "down", "left", "right"
            
        Returns:
            是否发生了移动（棋盘状态改变）
        """
        if self.is_game_over:
            return False

        # 保存移动前状态用于撤销
        prev_grid = self._clone_grid()
        prev_score = self.score

        # 重置动画状态
        self.merged_positions = []
        self.moved_tiles = []
        self.last_move_score = 0

        # 根据方向执行滑动
        if direction == "up":
            moved = self._slide_up()
        elif direction == "down":
            moved = self._slide_down()
        elif direction == "left":
            moved = self._slide_left()
        elif direction == "right":
            moved = self._slide_right()
        else:
            return False

        if moved:
            self.move_count += 1
            # 生成新方块
            self._spawn_tile()
            # 检查游戏状态
            self._check_game_state()
            return True

        return False

    def _slide_left(self) -> bool:
        """向左滑动"""
        moved = False
        for row in range(self.size):
            # 提取非空方块
            tiles = [t for t in self.grid[row] if t is not None]
            # 合并相同方块
            merged = self._merge_line(tiles)
            # 填充到一行
            for col in range(self.size):
                old_tile = self.grid[row][col]
                new_tile = merged[col] if col < len(merged) else None
                if old_tile != new_tile:
                    moved = True
                if new_tile:
                    old_pos = (new_tile.row, new_tile.col)
                    new_tile.set_position(row, col, save_prev=True)
                    self.moved_tiles.append((old_pos[0], old_pos[1], row, col))
                self.grid[row][col] = new_tile
        return moved

    def _slide_right(self) -> bool:
        """向右滑动"""
        moved = False
        for row in range(self.size):
            # 提取非空方块（反序）
            tiles = [t for t in reversed(self.grid[row]) if t is not None]
            # 合并相同方块
            merged = self._merge_line(tiles)
            # 填充到一行（反序）
            for col in range(self.size):
                old_tile = self.grid[row][col]
                new_tile = merged[self.size - 1 - col] if (self.size - 1 - col) < len(merged) else None
                if old_tile != new_tile:
                    moved = True
                if new_tile:
                    old_pos = (new_tile.row, new_tile.col)
                    new_tile.set_position(row, col, save_prev=True)
                    self.moved_tiles.append((old_pos[0], old_pos[1], row, col))
                self.grid[row][col] = new_tile
        return moved

    def _slide_up(self) -> bool:
        """向上滑动"""
        moved = False
        for col in range(self.size):
            # 提取列中的非空方块
            tiles = [self.grid[row][col] for row in range(self.size) if self.grid[row][col] is not None]
            # 合并相同方块
            merged = self._merge_line(tiles)
            # 填充到一列
            for row in range(self.size):
                old_tile = self.grid[row][col]
                new_tile = merged[row] if row < len(merged) else None
                if old_tile != new_tile:
                    moved = True
                if new_tile:
                    old_pos = (new_tile.row, new_tile.col)
                    new_tile.set_position(row, col, save_prev=True)
                    self.moved_tiles.append((old_pos[0], old_pos[1], row, col))
                self.grid[row][col] = new_tile
        return moved

    def _slide_down(self) -> bool:
        """向下滑动"""
        moved = False
        for col in range(self.size):
            # 提取列中的非空方块（反序）
            tiles = [self.grid[row][col] for row in range(self.size - 1, -1, -1) if self.grid[row][col] is not None]
            # 合并相同方块
            merged = self._merge_line(tiles)
            # 填充到一列（反序）
            for row in range(self.size):
                old_tile = self.grid[row][col]
                new_tile = merged[self.size - 1 - row] if (self.size - 1 - row) < len(merged) else None
                if old_tile != new_tile:
                    moved = True
                if new_tile:
                    old_pos = (new_tile.row, new_tile.col)
                    new_tile.set_position(row, col, save_prev=True)
                    self.moved_tiles.append((old_pos[0], old_pos[1], row, col))
                self.grid[row][col] = new_tile
        return moved

    def _merge_line(self, tiles: List[Tile]) -> List[Tile]:
        """
        合并一行/列中的相同方块
        
        算法：从左到右扫描，相邻相同则合并为一个更大的方块
        每次移动每个位置最多合并一次
        """
        result = []
        skip = False
        for i, tile in enumerate(tiles):
            if skip:
                skip = False
                continue
            if i + 1 < len(tiles) and tile.value == tiles[i + 1].value:
                # 合并
                new_value = tile.value * 2
                merged_tile = Tile(
                    value=new_value,
                    row=tile.row,
                    col=tile.col,
                    merged_from=(tile.value, tiles[i + 1].value),
                )
                result.append(merged_tile)
                # 更新分数
                self.score += new_value
                self.last_move_score += new_value
                # 更新最大方块
                if new_value > self.max_tile:
                    self.max_tile = new_value
                # 检查是否获胜
                if new_value >= WIN_TILE and not self.keep_playing:
                    self.is_won = True
                skip = True
            else:
                result.append(tile)
        return result

    def _check_game_state(self) -> None:
        """检查游戏是否结束"""
        # 如果棋盘未满，游戏继续
        if len(self.get_empty_cells()) > 0:
            return
        # 检查是否有可合并的相邻方块
        for row in range(self.size):
            for col in range(self.size):
                val = self.grid[row][col].value if self.grid[row][col] else 0
                # 检查右边
                if col + 1 < self.size and self.grid[row][col + 1]:
                    if self.grid[row][col + 1].value == val:
                        return
                # 检查下面
                if row + 1 < self.size and self.grid[row + 1][col]:
                    if self.grid[row + 1][col].value == val:
                        return
        # 没有空位且没有可合并的方块
        self.is_game_over = True

    def can_move(self) -> bool:
        """检查是否还能移动"""
        # 有空位就能移动
        if len(self.get_empty_cells()) > 0:
            return True
        # 检查是否有可合并的相邻方块
        for row in range(self.size):
            for col in range(self.size):
                val = self.grid[row][col].value if self.grid[row][col] else 0
                if col + 1 < self.size and self.grid[row][col + 1]:
                    if self.grid[row][col + 1].value == val:
                        return True
                if row + 1 < self.size and self.grid[row + 1][col]:
                    if self.grid[row + 1][col].value == val:
                        return True
        return False

    def continue_after_win(self) -> None:
        """获胜后继续游戏"""
        self.keep_playing = True
        self.is_won = False

    def _clone_grid(self) -> List[List[Optional[Tile]]]:
        """深拷贝棋盘"""
        return copy.deepcopy(self.grid)

    def undo(self, prev_grid: List[List[Optional[Tile]]], prev_score: int) -> bool:
        """
        撤销上一步操作
        
        Args:
            prev_grid: 移动前的棋盘状态
            prev_score: 移动前的分数
            
        Returns:
            是否撤销成功
        """
        self.grid = prev_grid
        self.score = prev_score
        self.is_game_over = False
        return True

    def clean_min_tile(self) -> Optional[Tuple[int, int]]:
        """
        清理最小的方块
        
        Returns:
            被清理的方块位置，如果没有可清理的方块则返回 None
        """
        min_val = float("inf")
        min_pos = None
        for row in range(self.size):
            for col in range(self.size):
                tile = self.grid[row][col]
                if tile and tile.value < min_val:
                    min_val = tile.value
                    min_pos = (row, col)
        if min_pos:
            self.grid[min_pos[0]][min_pos[1]] = None
        return min_pos

    def get_all_tiles(self) -> List[Tile]:
        """获取所有方块"""
        tiles = []
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col]:
                    tiles.append(self.grid[row][col])
        return tiles

    def to_dict(self) -> dict:
        """序列化棋盘状态"""
        tiles_data = []
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col]:
                    tiles_data.append(self.grid[row][col].to_dict())
        return {
            "size": self.size,
            "tiles": tiles_data,
            "score": self.score,
            "move_count": self.move_count,
            "max_tile": self.max_tile,
            "is_game_over": self.is_game_over,
            "is_won": self.is_won,
            "keep_playing": self.keep_playing,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GameBoard":
        """从字典恢复棋盘"""
        board = cls(size=data.get("size", BOARD_SIZE))
        board.score = data.get("score", 0)
        board.move_count = data.get("move_count", 0)
        board.max_tile = data.get("max_tile", 0)
        board.is_game_over = data.get("is_game_over", False)
        board.is_won = data.get("is_won", False)
        board.keep_playing = data.get("keep_playing", False)
        for tile_data in data.get("tiles", []):
            tile = Tile.from_dict(tile_data)
            board.grid[tile.row][tile.col] = tile
        return board

    def __repr__(self) -> str:
        lines = []
        lines.append(f"GameBoard(score={self.score}, moves={self.move_count})")
        for row in range(self.size):
            row_vals = []
            for col in range(self.size):
                tile = self.grid[row][col]
                row_vals.append(f"{tile.value:4d}" if tile else "   .")
            lines.append(" ".join(row_vals))
        return "\n".join(lines)
