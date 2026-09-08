# -*- coding: utf-8 -*-
# @Function: BoardView - 棋盘视图、方块渲染、动画
# 性能设计：方块整块预渲染缓存（背景+数字一次成型），每帧仅 blit；
#          圆角矩形走全局缓存；移动动画用 ease_out_cubic 平滑减速。

import math
import time
from typing import List, Tuple, Optional

import pygame

from src.config import (
    BOARD_SIZE, TILE_SIZE, TILE_GAP, BOARD_PADDING,
    BOARD_X, BOARD_Y, COLOR_BOARD_BG, COLOR_TILE_EMPTY,
    TILE_FONT_SIZES,
    ANIMATION_MOVE_DURATION, ANIMATION_MERGE_DURATION, ANIMATION_SPAWN_DURATION,
)
from src.models.board import GameBoard
from src.models.tile import Tile
from src.utils import (
    draw_rounded_rect, get_font_manager,
    ease_out_cubic, ease_out_back, lerp, get_tile_color,
    draw_shadow_optimized,
)


class TileSurfaceCache:
    """
    方块 Surface 预渲染缓存 / Pre-rendered tile surface cache

    将 (背景圆角矩形 + 数字) 一次性渲染成 Surface 并按方块值缓存，
    静止方块每帧只需一次 blit —— 彻底消除每帧的
    Surface 创建、圆角绘制与字体渲染开销。
    """

    _cache: dict = {}

    @classmethod
    def get_surface(cls, value: int) -> pygame.Surface:
        surface = cls._cache.get(value)
        if surface is None:
            bg_color, text_color = get_tile_color(value)
            surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(surface, bg_color, (0, 0, TILE_SIZE, TILE_SIZE), border_radius=12)
            font_size = TILE_FONT_SIZES.get(value, 28)
            font = get_font_manager().get_font(font_size, bold=True)
            text = font.render(str(value), True, text_color)
            surface.blit(text, text.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2)))
            cls._cache[value] = surface
        return surface


class TileRenderer:
    """方块渲染器 / Tile renderer"""

    @staticmethod
    def get_tile_rect(row: int, col: int) -> pygame.Rect:
        """获取方块在屏幕上的矩形区域 / Get tile screen rectangle"""
        x = BOARD_X + col * (TILE_SIZE + TILE_GAP) + BOARD_PADDING
        y = BOARD_Y + row * (TILE_SIZE + TILE_GAP) + BOARD_PADDING
        return pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    @staticmethod
    def tile_origin(row_f: float, col_f: float) -> Tuple[int, int]:
        """由浮点行列坐标计算方块左上角屏幕坐标 / Screen origin from float row/col"""
        x = BOARD_X + col_f * (TILE_SIZE + TILE_GAP) + BOARD_PADDING
        y = BOARD_Y + row_f * (TILE_SIZE + TILE_GAP) + BOARD_PADDING
        return (int(x), int(y))

    @staticmethod
    def draw_tile(
        surface: pygame.Surface,
        tile: Tile,
        pos: Optional[Tuple[float, float]] = None,
        scale: float = 1.0,
    ) -> None:
        """
        绘制单个方块（使用预渲染缓存）

        Args:
            surface: 绘制目标
            tile: 方块数据
            pos: 浮点 (row, col) 位置；None 表示使用 tile 当前逻辑位置
            scale: 缩放比例（生成/合并动画），1.0 时零缩放直出
        """
        if pos is None:
            pos = (float(tile.row), float(tile.col))
        x, y = TileRenderer.tile_origin(pos[0], pos[1])
        cached = TileSurfaceCache.get_surface(tile.value)

        if scale >= 0.999:
            surface.blit(cached, (x, y))
            return

        # 缩放路径（生成/合并动画），以方块中心为基准
        size = max(1, int(TILE_SIZE * scale))
        scaled = pygame.transform.smoothscale(cached, (size, size))
        cx = x + TILE_SIZE / 2
        cy = y + TILE_SIZE / 2
        surface.blit(scaled, (int(cx - size / 2), int(cy - size / 2)))


class BoardView:
    """棋盘视图 - 负责整个棋盘的渲染和动画 / Board view - manages board rendering and animation"""

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
        """开始移动动画 / Start move animation"""
        self.animations = []
        self.is_animating = True
        self._anim_start = time.perf_counter()

        move_s = ANIMATION_MOVE_DURATION / 1000.0
        merge_s = ANIMATION_MERGE_DURATION / 1000.0
        spawn_s = ANIMATION_SPAWN_DURATION / 1000.0

        for tile in board.get_all_tiles():
            if tile.merged_from:
                anim_type, duration, start = "merge", merge_s, self._anim_start
            elif tile.is_new:
                anim_type, duration, start = "spawn", spawn_s, self._anim_start + move_s * 0.6
            elif tile.prev_row is not None:
                anim_type, duration, start = "move", move_s, self._anim_start
            else:
                anim_type, duration, start = "static", 0.0, self._anim_start
            self.animations.append({
                "tile": tile, "type": anim_type,
                "duration": duration, "start_time": start,
            })

    def update(self, dt: float) -> None:
        """更新动画 / Update animations"""
        if not self.is_animating:
            return
        now = time.perf_counter()
        for anim in self.animations:
            if anim["duration"] > 0 and now - anim["start_time"] < anim["duration"]:
                return
        # 全部动画结束，重置方块动画状态
        self.is_animating = False
        for anim in self.animations:
            anim["tile"].reset_animation()
        self.animations = []

    def draw(self, surface: pygame.Surface, board: GameBoard) -> None:
        """绘制棋盘 / Draw board"""
        # 棋盘卡片阴影（iOS 风格：无边界 + 柔和投影）
        draw_shadow_optimized(surface, self.board_rect, alpha=10, blur=10)
        # 棋盘背景（缓存 blit）
        draw_rounded_rect(surface, COLOR_BOARD_BG, self.board_rect, 20)

        # 空格子背景（缓存 blit）
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = TileRenderer.get_tile_rect(row, col)
                draw_rounded_rect(surface, COLOR_TILE_EMPTY, rect, 10)

        now = time.perf_counter()
        animating = self.is_animating
        for tile in board.get_all_tiles():
            anim = self._find_animation(tile) if animating else None

            if anim is None or anim["type"] == "static" or anim["duration"] <= 0:
                TileRenderer.draw_tile(surface, tile)
                continue

            elapsed = now - anim["start_time"]
            if elapsed <= 0:
                continue  # 动画尚未开始（如 spawn 等待移动完成）
            progress = min(1.0, elapsed / anim["duration"])
            p = ease_out_cubic(progress)

            if anim["type"] == "move":
                # 移动动画：prev -> target 平滑减速插值
                row_f = lerp(tile.prev_row, tile.row, p)
                col_f = lerp(tile.prev_col, tile.col, p)
                TileRenderer.draw_tile(surface, tile, pos=(row_f, col_f))
            elif anim["type"] == "merge":
                # 合并动画：轻微膨胀后回落（脉冲式，不越界闪烁）
                scale = 1.0 + 0.12 * math.sin(progress * math.pi)
                TileRenderer.draw_tile(surface, tile, scale=scale)
            else:  # spawn
                # 生成动画：从小弹出（轻微过冲，iOS spring 观感）
                scale = 0.3 + 0.7 * ease_out_back(progress)
                TileRenderer.draw_tile(surface, tile, scale=scale)

    def _find_animation(self, tile: Tile) -> Optional[dict]:
        """查找方块对应的动画 / Find animation for tile"""
        for anim in self.animations:
            if anim["tile"] is tile:
                return anim
        return None

    def get_cell_from_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """根据屏幕坐标获取棋盘格子位置 / Get board cell from screen coordinates"""
        x, y = pos
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = TileRenderer.get_tile_rect(row, col)
                if rect.collidepoint(x, y):
                    return (row, col)
        return None
