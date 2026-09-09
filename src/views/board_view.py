# -*- coding: utf-8 -*-
# @Function: BoardView - 棋盘视图、方块渲染、动画
# 性能设计：方块整块预渲染缓存（辉光+渐变+数字一次成型），每帧仅 blit；
#          渐变/卡片/辉光走全局缓存；移动动画用 ease_out_cubic 平滑减速。

import math
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
    get_font_manager,
    ease_out_cubic, ease_out_back, lerp, get_tile_color,
    lighten, draw_card, draw_glow, draw_gradient_rounded_rect, draw_rounded_rect,
)

# 高级方块（>=128）预渲染外发光的边距（px）
_TILE_GLOW_PAD = 10
_TILE_RADIUS = 14


class TileSurfaceCache:
    """
    方块 Surface 预渲染缓存 / Pre-rendered tile surface cache

    将 (辉光 + 渐变底 + 数字投影) 一次性渲染成 Surface 按方块值缓存，
    静止方块每帧只需一次 blit。>=128 的方块自带同色霓虹辉光。
    缓存值为 (surface, pad)，pad 为辉光外边距，blit 时向左上偏移。
    """

    _cache: dict = {}

    @classmethod
    def get(cls, value: int) -> Tuple[pygame.Surface, int]:
        entry = cls._cache.get(value)
        if entry is None:
            bg_color, text_color = get_tile_color(value)
            glow = value >= 128
            pad = _TILE_GLOW_PAD if glow else 0
            size = TILE_SIZE + pad * 2
            surface = pygame.Surface((size, size), pygame.SRCALPHA)

            inner = pygame.Rect(pad, pad, TILE_SIZE, TILE_SIZE)
            if glow:
                draw_glow(surface, inner, bg_color, alpha=110, blur=pad, radius=_TILE_RADIUS)
            draw_gradient_rounded_rect(
                surface, inner, lighten(bg_color, 1.28), bg_color, _TILE_RADIUS,
            )

            font_size = TILE_FONT_SIZES.get(value, 28)
            font = get_font_manager().get_font(font_size, bold=True)
            center = inner.center
            # 数字投影（向下 2px 半透明深色），增强立体感
            shadow = font.render(str(value), True, (0, 0, 0))
            shadow.set_alpha(80)
            surface.blit(shadow, shadow.get_rect(center=(center[0], center[1] + 2)))
            text = font.render(str(value), True, text_color)
            surface.blit(text, text.get_rect(center=center))

            entry = (surface, pad)
            cls._cache[value] = entry
        return entry


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
        cached, pad = TileSurfaceCache.get(tile.value)

        if scale >= 0.999:
            surface.blit(cached, (x - pad, y - pad))
            return

        # 缩放路径（生成/合并动画），以方块中心为基准
        full = TILE_SIZE + pad * 2
        size = max(1, int(full * scale))
        scaled = pygame.transform.smoothscale(cached, (size, size))
        cx = x + TILE_SIZE / 2
        cy = y + TILE_SIZE / 2
        surface.blit(scaled, (int(cx - size / 2), int(cy - size / 2)))


class BoardView:
    """棋盘视图 - 负责整个棋盘的渲染和动画 / Board view - manages board rendering and animation"""

    def __init__(self) -> None:
        self.animations: List[dict] = []
        self.is_animating: bool = False
        self._anim_elapsed: float = 0  # 累计动画时长（秒），由 update(dt) 驱动，帧率无关
        self._anim_total: float = 0    # 整轮动画总时长（秒），供输入队列查询进度
        self.board_rect = pygame.Rect(
            BOARD_X, BOARD_Y,
            TILE_SIZE * BOARD_SIZE + TILE_GAP * (BOARD_SIZE - 1) + BOARD_PADDING * 2,
            TILE_SIZE * BOARD_SIZE + TILE_GAP * (BOARD_SIZE - 1) + BOARD_PADDING * 2,
        )

    def start_move_animation(self, board: GameBoard) -> None:
        """开始移动动画 / Start move animation"""
        self.animations = []
        self.is_animating = True
        self._anim_elapsed = 0.0

        move_s = ANIMATION_MOVE_DURATION / 1000.0
        merge_s = ANIMATION_MERGE_DURATION / 1000.0
        spawn_s = ANIMATION_SPAWN_DURATION / 1000.0

        start = 0.0
        end_time = 0.0
        for tile in board.get_all_tiles():
            if tile.merged_from:
                anim_type, duration, anim_start = "merge", merge_s, start
            elif tile.is_new:
                anim_type, duration, anim_start = "spawn", spawn_s, move_s * 0.5
            elif tile.prev_row is not None:
                anim_type, duration, anim_start = "move", move_s, start
            else:
                anim_type, duration, anim_start = "static", 0.0, start
            end_time = max(end_time, anim_start + duration)
            self.animations.append({
                "tile": tile, "type": anim_type,
                "duration": duration, "start_time": anim_start,
            })
        self._anim_total = max(0.0001, end_time)

    def animation_progress(self) -> float:
        """整轮动画完成比例 (0~1)，未在动画时返回 1 / Overall animation progress"""
        if not self.is_animating:
            return 1.0
        return min(1.0, self._anim_elapsed / self._anim_total)

    def finish(self) -> None:
        """立即定格当前动画（连击时避免视觉回跳）/ Snap ongoing animation to end"""
        if self.is_animating:
            for anim in self.animations:
                anim["tile"].reset_animation()
            self.animations = []
            self.is_animating = False

    def update(self, dt: float) -> None:
        """更新动画 / Update animations"""
        if not self.is_animating:
            return
        self._anim_elapsed += dt
        for anim in self.animations:
            if anim["duration"] > 0 and self._anim_elapsed - anim["start_time"] < anim["duration"]:
                return
        # 全部动画结束，重置方块动画状态
        self.is_animating = False
        for anim in self.animations:
            anim["tile"].reset_animation()
        self.animations = []

    def draw(self, surface: pygame.Surface, board: GameBoard) -> None:
        """绘制棋盘 / Draw board"""
        # 棋盘卡片：靛蓝辉光 + 玻璃卡片
        draw_glow(surface, self.board_rect, (110, 96, 255), alpha=34, blur=16, radius=20)
        draw_card(surface, self.board_rect, 20, bg=COLOR_BOARD_BG)

        # 空格子背景（缓存 blit）
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = TileRenderer.get_tile_rect(row, col)
                draw_rounded_rect(surface, COLOR_TILE_EMPTY, rect, 10)

        elapsed = self._anim_elapsed
        animating = self.is_animating
        for tile in board.get_all_tiles():
            anim = self._find_animation(tile) if animating else None

            if anim is None or anim["type"] == "static" or anim["duration"] <= 0:
                TileRenderer.draw_tile(surface, tile)
                continue

            if elapsed - anim["start_time"] <= 0:
                continue  # 动画尚未开始（如 spawn 等待移动完成）
            progress = min(1.0, (elapsed - anim["start_time"]) / anim["duration"])
            p = ease_out_cubic(progress)

            if anim["type"] == "move":
                # 移动动画：prev -> target 平滑减速插值
                row_f = lerp(tile.prev_row, tile.row, p)
                col_f = lerp(tile.prev_col, tile.col, p)
                TileRenderer.draw_tile(surface, tile, pos=(row_f, col_f))
            elif anim["type"] == "merge":
                # 合并动画：轻微膨胀后回落（脉冲式，不越界闪烁）
                scale = 1.0 + 0.14 * math.sin(progress * math.pi)
                TileRenderer.draw_tile(surface, tile, scale=scale)
            else:  # spawn
                # 生成动画：从小弹出（轻微过冲，spring 观感）
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
