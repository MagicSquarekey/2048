# -*- coding: utf-8 -*-
# @Function: BoardView - 棋盘视图、方块渲染、动画

import pygame
import time
from typing import List, Tuple, Optional

from src.config import (
    BOARD_SIZE, TILE_SIZE, TILE_GAP, BOARD_PADDING,
    BOARD_X, BOARD_Y, COLOR_BOARD_BG, COLOR_TILE_EMPTY,
    TILE_COLORS, TILE_FONT_SIZES,
    ANIMATION_MOVE_DURATION, ANIMATION_MERGE_DURATION, ANIMATION_SPAWN_DURATION,
)
from src.models.board import GameBoard
from src.models.tile import Tile
from src.utils import (
    draw_rounded_rect, draw_text_centered, get_font_manager,
    ease_out_cubic, ease_out_back, lerp, get_tile_color,
)


class TileRenderer:
    """方块渲染器"""

    @staticmethod
    def get_tile_rect(row: int, col: int) -> pygame.Rect:
        """获取方块在屏幕上的矩形区域"""
        x = BOARD_X + col * (TILE_SIZE + TILE_GAP) + BOARD_PADDING
        y = BOARD_Y + row * (TILE_SIZE + TILE_GAP) + BOARD_PADDING
        return pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    @staticmethod
    def draw_tile(
        surface: pygame.Surface,
        tile: Tile,
        progress: float = 1.0,
        scale: float = 1.0,
    ) -> None:
        """
        绘制单个方块
        
        Args:
            surface: 绘制目标
            tile: 方块数据
            progress: 动画进度 (0-1)
            scale: 缩放比例（用于生成动画）
        """
        # 计算位置（支持动画插值）
        if tile.prev_row is not None and tile.prev_col is not None and progress < 1.0:
            # 移动动画
            row = lerp(tile.prev_row, tile.row, ease_out_cubic(progress))
            col = lerp(tile.prev_col, tile.col, ease_out_cubic(progress))
        else:
            row = float(tile.row)
            col = float(tile.col)

        # 计算屏幕坐标
        x = BOARD_X + col * (TILE_SIZE + TILE_GAP) + BOARD_PADDING
        y = BOARD_Y + row * (TILE_SIZE + TILE_GAP) + BOARD_PADDING

        # 应用缩放（生成动画）
        if scale != 1.0:
            center_x = x + TILE_SIZE / 2
            center_y = y + TILE_SIZE / 2
            size = int(TILE_SIZE * scale)
            x = center_x - size / 2
            y = center_y - size / 2
            rect = pygame.Rect(int(x), int(y), size, size)
        else:
            rect = pygame.Rect(int(x), int(y), TILE_SIZE, TILE_SIZE)

        # 获取颜色
        bg_color, text_color = get_tile_color(tile.value)

        # 绘制背景
        draw_rounded_rect(surface, bg_color, rect, 8)

        # 绘制数字
        font_size = TILE_FONT_SIZES.get(tile.value, 28)
        if scale != 1.0:
            font_size = int(font_size * scale)
        font = get_font_manager().get_font(font_size, bold=True)
        draw_text_centered(surface, str(tile.value), font, text_color, rect.center)


class BoardView:
    """棋盘视图 - 负责整个棋盘的渲染和动画"""

    def __init__(self) -> None:
        self.animations: List[dict] = []
        self.is_animating: bool = False
        self._anim_start: float = 0
        self.board_rect = pygame.Rect(
            BOARD_X, BOARD_Y,
            TILE_SIZE * BOARD_SIZE + TILE_GAP * (BOARD_SIZE - 1) + BOARD_PADDING * 2,
            TILE_SIZE * BOARD_SIZE + TILE_GAP * (BOARD_SIZE - 1) + BOARD_PADDING * 2,
        )

    def start_move_animation(self, board: GameBoard) -> None:
        """开始移动动画"""
        self.animations = []
        self.is_animating = True
        self._anim_start = time.time()

        # 为每个方块创建动画数据
        for tile in board.get_all_tiles():
            anim_data = {
                "tile": tile,
                "type": "merge" if tile.merged_from else "move" if tile.prev_row is not None else "spawn",
                "start_time": self._anim_start,
            }
            if anim_data["type"] == "merge":
                anim_data["duration"] = ANIMATION_MERGE_DURATION / 1000.0
            elif anim_data["type"] == "spawn":
                anim_data["duration"] = ANIMATION_SPAWN_DURATION / 1000.0
                anim_data["start_time"] = self._anim_start + ANIMATION_MOVE_DURATION / 1000.0
            else:
                anim_data["duration"] = ANIMATION_MOVE_DURATION / 1000.0
            self.animations.append(anim_data)

    def update(self, dt: float) -> None:
        """更新动画"""
        if not self.is_animating:
            return
        # 检查所有动画是否完成
        now = time.time()
        all_done = True
        for anim in self.animations:
            elapsed = now - anim["start_time"]
            if elapsed < anim["duration"]:
                all_done = False
                break
        if all_done:
            self.is_animating = False
            # 重置所有方块的动画状态
            for anim in self.animations:
                anim["tile"].reset_animation()

    def draw(self, surface: pygame.Surface, board: GameBoard) -> None:
        """绘制棋盘"""
        # 绘制棋盘背景
        draw_rounded_rect(surface, COLOR_BOARD_BG, self.board_rect, 12)

        # 绘制空方块背景
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = TileRenderer.get_tile_rect(row, col)
                draw_rounded_rect(surface, COLOR_TILE_EMPTY, rect, 8)

        # 绘制方块
        now = time.time()
        for tile in board.get_all_tiles():
            # 查找对应动画
            anim = self._find_animation(tile)
            if anim and self.is_animating:
                elapsed = now - anim["start_time"]
                progress = min(1.0, elapsed / anim["duration"]) if anim["duration"] > 0 else 1.0
                if anim["type"] == "merge":
                    # 合并动画：弹跳效果
                    scale = ease_out_back(progress)
                    TileRenderer.draw_tile(surface, tile, 1.0, scale)
                elif anim["type"] == "spawn":
                    # 生成动画：缩放效果
                    if progress < 0:
                        continue  # 还没开始
                    scale = ease_out_back(progress)
                    TileRenderer.draw_tile(surface, tile, 1.0, scale)
                else:
                    # 移动动画
                    TileRenderer.draw_tile(surface, tile, progress, 1.0)
            else:
                TileRenderer.draw_tile(surface, tile, 1.0, 1.0)

    def _find_animation(self, tile: Tile) -> Optional[dict]:
        """查找方块对应的动画"""
        for anim in self.animations:
            if anim["tile"] is tile:
                return anim
        return None

    def get_cell_from_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """根据屏幕坐标获取棋盘格子位置"""
        x, y = pos
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = TileRenderer.get_tile_rect(row, col)
                if rect.collidepoint(x, y):
                    return (row, col)
        return None
