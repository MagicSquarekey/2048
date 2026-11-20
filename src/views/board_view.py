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
    TILE_FONT_SIZES, UI_SUPERSAMPLE,
    ANIMATION_MOVE_DURATION, ANIMATION_MERGE_DURATION, ANIMATION_SPAWN_DURATION,
)
from src.models.board import GameBoard
from src.models.tile import Tile
from src.utils import (
    get_font_manager,
    ease_out_cubic, ease_out_back, lerp, get_tile_color,
    lighten, draw_card, draw_glow,
)
from src.views.effects import ScreenShake

# 高级方块（>=128）预渲染外发光的边距（px）
_TILE_GLOW_PAD = 10
_TILE_RADIUS = 14
# 静态图形超采样倍数（至少 1）/ Static-graphics supersampling factor (>=1)
_SS = max(1, int(UI_SUPERSAMPLE))


class TileSurfaceCache:
    """
    方块 Surface 预渲染缓存 / Pre-rendered tile surface cache

    将 (辉光 + 渐变底 + 轮辋光 + 顶部光泽 + 数字投影) 一次成型并按值缓存，
    静止方块每帧只需一次 blit。>=128 的方块自带同色霓虹辉光。
    缓存值为 (surface, pad)，pad 为辉光外边距，blit 时向左上偏移。

    绘制在 TILE_SIZE*_SS 的高分辨率画布上，最后 smoothscale 回原尺寸；
    内部直接按 _SS 放大绘制，不调用已超采样的 draw_glow / draw_gradient_rounded_rect，
    避免二次超采样（4x 内存与耗时）。
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
            ss = _SS
            tile_ss = TILE_SIZE * ss
            pad_ss = pad * ss
            radius_ss = _TILE_RADIUS * ss
            surface_hi = pygame.Surface((size * ss, size * ss), pygame.SRCALPHA)
            # smoothscale 不预乘 alpha：透明底先用方块底色填充，避免边缘发暗
            surface_hi.fill((*bg_color, 0))
            inner = pygame.Rect(pad_ss, pad_ss, tile_ss, tile_ss)

            if glow:
                # 与 draw_glow 等效的同心圆角矩形循环（blur 层已按 ss 放大）
                for i in range(pad_ss, 0, -1):
                    layer_alpha = int(110 * (1 - i / (pad_ss + 1)) ** 1.5)
                    layer_rect = inner.inflate(i * 2, i * 2)
                    pygame.draw.rect(
                        surface_hi, (*bg_color, layer_alpha), layer_rect,
                        border_radius=radius_ss + i,
                    )

            # 渐变底：在 tile_ss 临时 Surface 上逐行绘制，再用圆角蒙版裁切
            grad = pygame.Surface((tile_ss, tile_ss), pygame.SRCALPHA)
            grad.fill((*bg_color, 0))
            top_color = lighten(bg_color, 1.28)
            for y in range(tile_ss):
                t = y / max(1, tile_ss - 1)
                color = (
                    int(top_color[0] + (bg_color[0] - top_color[0]) * t),
                    int(top_color[1] + (bg_color[1] - top_color[1]) * t),
                    int(top_color[2] + (bg_color[2] - top_color[2]) * t),
                )
                pygame.draw.line(grad, color, (0, y), (tile_ss, y))
            # 蒙版透明区保持白色 RGB，用 MULT 只改 alpha、保留渐变 RGB，
            # 避免缩小时圆角被透明黑压暗
            mask = pygame.Surface((tile_ss, tile_ss), pygame.SRCALPHA)
            mask.fill((255, 255, 255, 0))
            pygame.draw.rect(
                mask, (255, 255, 255, 255), (0, 0, tile_ss, tile_ss),
                border_radius=radius_ss,
            )
            grad.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            surface_hi.blit(grad, inner.topleft)

            # 轮辋光：整圈描边，塑造体积感（宽度按 ss 放大保持观感）
            pygame.draw.rect(
                surface_hi, lighten(bg_color, 1.55), inner,
                width=max(1, 2 * ss), border_radius=radius_ss,
            )
            # 顶部光泽：上半部白色低透明圆角，经典玻璃高光
            gloss_h = int(TILE_SIZE * 0.42)
            gloss = pygame.Surface((tile_ss, gloss_h * ss), pygame.SRCALPHA)
            # 透明底用方块底色填充，避免光泽圆角处混入透明黑
            gloss.fill((*bg_color, 0))
            pygame.draw.rect(
                gloss, (255, 255, 255, 30), (0, 0, tile_ss, gloss_h * ss),
                border_radius=radius_ss,
            )
            surface_hi.blit(gloss, (pad_ss, pad_ss))

            font_size = TILE_FONT_SIZES.get(value, 28) * ss
            font = get_font_manager().get_font(font_size, bold=True)
            center = inner.center
            # 数字投影（向下 2*ss px 半透明深色），增强立体感
            shadow = font.render(str(value), True, (0, 0, 0))
            shadow.set_alpha(80)
            surface_hi.blit(shadow, shadow.get_rect(center=(center[0], center[1] + 2 * ss)))
            text = font.render(str(value), True, text_color)
            surface_hi.blit(text, text.get_rect(center=center))

            if ss > 1:
                surface = pygame.transform.smoothscale(surface_hi, (size, size))
            else:
                surface = surface_hi
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
        offset: Tuple[int, int] = (0, 0),
    ) -> None:
        """
        绘制单个方块（使用预渲染缓存）

        Args:
            surface: 绘制目标
            tile: 方块数据
            pos: 浮点 (row, col) 格子坐标；None 表示使用 tile 当前逻辑位置
            scale: 缩放比例（生成/合并动画），1.0 时零缩放直出
            offset: 震屏像素偏移
        """
        if pos is None:
            pos = (float(tile.row), float(tile.col))
        x, y = TileRenderer.tile_origin(pos[0], pos[1])
        x += offset[0]
        y += offset[1]
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
        self.shake = ScreenShake()     # 大合并震屏
        self._empty_cache: dict = {}   # 空格子内凹贴图缓存
        self.board_rect = pygame.Rect(
            BOARD_X, BOARD_Y,
            TILE_SIZE * BOARD_SIZE + TILE_GAP * (BOARD_SIZE - 1) + BOARD_PADDING * 2,
            TILE_SIZE * BOARD_SIZE + TILE_GAP * (BOARD_SIZE - 1) + BOARD_PADDING * 2,
        )

    def _get_empty_cell(self) -> pygame.Surface:
        """空格内凹贴图（底色 + 内侧暗边一次成型）/ Inset empty-cell surface"""
        size = (TILE_SIZE, TILE_SIZE, COLOR_TILE_EMPTY)
        surf = self._empty_cache.get(size)
        if surf is None:
            ss = _SS
            w_ss = TILE_SIZE * ss
            hi = pygame.Surface((w_ss, w_ss), pygame.SRCALPHA)
            # smoothscale 不预乘 alpha：透明底先用空格底色填充，避免边缘发暗
            hi.fill((*COLOR_TILE_EMPTY, 0))
            pygame.draw.rect(hi, COLOR_TILE_EMPTY, (0, 0, w_ss, w_ss),
                             border_radius=10 * ss)
            # 内凹感：顶部 1px 暗边 + 底部 1px 亮边（坐标与线宽按 ss 放大）
            line_w = max(1, ss)
            pygame.draw.line(hi, lighten(COLOR_TILE_EMPTY, 0.72), (8 * ss, ss),
                             (w_ss - 8 * ss, ss), line_w)
            pygame.draw.line(hi, lighten(COLOR_TILE_EMPTY, 1.22),
                             (8 * ss, (TILE_SIZE - 2) * ss),
                             (w_ss - 8 * ss, (TILE_SIZE - 2) * ss), line_w)
            if ss > 1:
                surf = pygame.transform.smoothscale(hi, (TILE_SIZE, TILE_SIZE))
            else:
                surf = hi
            self._empty_cache[size] = surf
        return surf

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
        self.shake.update(dt)
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
        ox, oy = self.shake.offset
        # 棋盘卡片：靛蓝辉光 + 玻璃卡片（随震屏偏移）
        shaken = self.board_rect.move(ox, oy)
        draw_glow(surface, shaken, (110, 96, 255), alpha=34, blur=16, radius=20)
        draw_card(surface, shaken, 20, bg=COLOR_BOARD_BG)

        # 空格子背景（内凹质感，缓存 blit）
        empty = self._get_empty_cell()
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = TileRenderer.get_tile_rect(row, col)
                surface.blit(empty, (rect.x + ox, rect.y + oy))

        elapsed = self._anim_elapsed
        animating = self.is_animating
        for tile in board.get_all_tiles():
            anim = self._find_animation(tile) if animating else None

            if anim is None or anim["type"] == "static" or anim["duration"] <= 0:
                TileRenderer.draw_tile(surface, tile, offset=(ox, oy))
                continue

            if elapsed - anim["start_time"] <= 0:
                continue  # 动画尚未开始（如 spawn 等待移动完成）
            progress = min(1.0, (elapsed - anim["start_time"]) / anim["duration"])
            p = ease_out_cubic(progress)

            if anim["type"] == "move":
                # 移动动画：prev -> target 平滑减速插值
                row_f = lerp(tile.prev_row, tile.row, p)
                col_f = lerp(tile.prev_col, tile.col, p)
                TileRenderer.draw_tile(surface, tile, pos=(row_f, col_f), offset=(ox, oy))
            elif anim["type"] == "merge":
                # 合并动画：轻微膨胀后回落（脉冲式，不越界闪烁）
                scale = 1.0 + 0.14 * math.sin(progress * math.pi)
                TileRenderer.draw_tile(surface, tile, scale=scale, offset=(ox, oy))
            else:  # spawn
                # 生成动画：从小弹出（轻微过冲，spring 观感）
                scale = 0.3 + 0.7 * ease_out_back(progress)
                TileRenderer.draw_tile(surface, tile, scale=scale, offset=(ox, oy))

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
