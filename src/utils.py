# -*- coding: utf-8 -*-
# @Function: 工具函数 - 绘图辅助、字体管理、通用工具

import pygame
import math
from typing import Tuple, Optional

from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FONT_PATH,
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL, FONT_SIZE_TINY,
    COLOR_OVERLAY,
)


class FontManager:
    """字体管理器 - 全局字体缓存"""

    _instance: Optional["FontManager"] = None
    _cache: dict = {}

    def __new__(cls) -> "FontManager":
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._cache = {}
        return cls._instance

    def get_font(self, size: int, bold: bool = False) -> pygame.font.Font:
        """获取指定大小的字体"""
        key = (size, bold)
        if key not in self._cache:
            font = pygame.font.Font(FONT_PATH, size)
            font.bold = bold
            self._cache[key] = font
        return self._cache[key]

    def get_large(self, bold: bool = False) -> pygame.font.Font:
        """获取大号字体"""
        return self.get_font(FONT_SIZE_LARGE, bold)

    def get_medium(self, bold: bool = False) -> pygame.font.Font:
        """获取中号字体"""
        return self.get_font(FONT_SIZE_MEDIUM, bold)

    def get_small(self, bold: bool = False) -> pygame.font.Font:
        """获取小号字体"""
        return self.get_font(FONT_SIZE_SMALL, bold)

    def get_tiny(self, bold: bool = False) -> pygame.font.Font:
        """获取微小字体"""
        return self.get_font(FONT_SIZE_TINY, bold)


def get_font_manager() -> FontManager:
    """获取字体管理器实例"""
    return FontManager()


def draw_rounded_rect(
    surface: pygame.Surface,
    color: Tuple[int, int, int],
    rect: pygame.Rect,
    radius: int = 8,
    border_width: int = 0,
    border_color: Optional[Tuple[int, int, int]] = None,
) -> None:
    """绘制圆角矩形"""
    shape_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(
        shape_surface,
        color,
        (0, 0, rect.width, rect.height),
        border_radius=radius,
    )
    if border_width > 0 and border_color:
        pygame.draw.rect(
            shape_surface,
            border_color,
            (0, 0, rect.width, rect.height),
            width=border_width,
            border_radius=radius,
        )
    surface.blit(shape_surface, rect.topleft)


def draw_text_centered(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: Tuple[int, int, int],
    center: Tuple[int, int],
    antialias: bool = True,
) -> pygame.Rect:
    """在指定位置居中绘制文字"""
    text_surface = font.render(text, antialias, color)
    text_rect = text_surface.get_rect(center=center)
    surface.blit(text_surface, text_rect)
    return text_rect


def draw_text_at(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: Tuple[int, int, int],
    pos: Tuple[int, int],
    antialias: bool = True,
) -> pygame.Rect:
    """在指定位置绘制文字（左上角对齐）"""
    text_surface = font.render(text, antialias, color)
    text_rect = text_surface.get_rect(topleft=pos)
    surface.blit(text_surface, text_rect)
    return text_rect


def draw_overlay(surface: pygame.Surface, alpha: int = 150) -> None:
    """绘制半透明遮罩"""
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, alpha))
    surface.blit(overlay, (0, 0))


def ease_out_cubic(t: float) -> float:
    """缓出动画曲线 - 三次方"""
    return 1 - (1 - t) ** 3


def ease_in_out_cubic(t: float) -> float:
    """缓入缓出动画曲线 - 三次方"""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2


def ease_out_back(t: float) -> float:
    """弹性缓出动画曲线"""
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def lerp(start: float, end: float, t: float) -> float:
    """线性插值"""
    return start + (end - start) * t


def clamp(value: float, min_val: float, max_val: float) -> float:
    """限制数值范围"""
    return max(min_val, min(max_val, value))


def point_in_rect(point: Tuple[int, int], rect: pygame.Rect) -> bool:
    """判断点是否在矩形内"""
    return rect.collidepoint(point)


def format_score(score: int) -> str:
    """格式化分数显示"""
    if score >= 1000000:
        return f"{score / 1000000:.1f}M"
    elif score >= 1000:
        return f"{score / 1000:.1f}K"
    return str(score)


def format_time(seconds: int) -> str:
    """格式化时间显示"""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def get_tile_color(value: int):
    """获取方块颜色方案"""
    from src.config import TILE_COLORS
    if value in TILE_COLORS:
        return TILE_COLORS[value]
    # 超过 2048 的方块使用金色
    return ((237, 194, 46), (249, 246, 242))
