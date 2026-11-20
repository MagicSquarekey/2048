# -*- coding: utf-8 -*-
# @Function: 渲染质量测试 - 验证 2x 超采样缓存的尺寸、抗锯齿与边缘颜色
# 说明：所有缓存的输出尺寸/坐标必须与超采样前完全一致；半透明边缘像素的 RGB
#       必须保持在图形本色附近，而不是被 smoothscale 的透明黑压暗。

import os

# 无头模式（若其他测试模块已设置驱动则沿用）
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

if not pygame.display.get_init():
    pygame.display.init()
if pygame.display.get_surface() is None:
    pygame.display.set_mode((1, 1), pygame.HIDDEN)
if not pygame.font.get_init():
    pygame.font.init()

from src.config import (
    CARD_BG, CARD_BORDER, TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT,
)
from src.utils import (
    RoundedRectCache, BorderedRectCache, CardCache,
    BackgroundCache, GradientRectCache,
)
from src.views.board_view import TileSurfaceCache
from src.views.effects import _SoftCircleCache
from src.views.ui_components import _GlossCache


def _semitransparent_pixels(surface: pygame.Surface) -> list:
    """收集所有半透明像素 (x, y, (r, g, b, a)) / Collect semi-transparent pixels"""
    width, height = surface.get_size()
    pixels = []
    for y in range(height):
        for x in range(width):
            color = surface.get_at((x, y))
            if 0 < color.a < 255:
                pixels.append((x, y, (color.r, color.g, color.b, color.a)))
    return pixels


def _find_rgb_close(surface: pygame.Surface, expected, tolerance: int):
    """查找第一个 RGB 接近期望值的半透明像素 / Find semi pixel with matching RGB"""
    for x, y, color in _semitransparent_pixels(surface):
        if all(abs(color[i] - expected[i]) <= tolerance for i in range(3)):
            return (x, y, color)
    return None


def test_rounded_rect_cache_antialiased_edges():
    """圆角矩形：尺寸不变、圆角外透明、边缘半透明像素 RGB 保持本色（不压暗）"""
    surface = RoundedRectCache.get_surface(120, 80, (100, 100, 140), 20)

    assert surface.get_size() == (120, 80)
    assert surface.get_flags() & pygame.SRCALPHA
    assert surface.get_at((0, 0)).a == 0

    pixels = _semitransparent_pixels(surface)
    assert pixels, "圆角边缘应存在半透明抗锯齿像素"
    # 修复前透明区域是 (0,0,0,0)，下采样后边缘约为 (50,50,70)；修复后应接近本色
    assert _find_rgb_close(surface, (100, 100, 140), 3) is not None, pixels[:8]


def test_card_cache_antialiased_edges():
    """卡片缓存：尺寸不变、边缘半透明像素 RGB 接近边框色"""
    surface = CardCache.get_surface(200, 100, CARD_BG, CARD_BORDER, 16)

    assert surface.get_size() == (200, 100)
    assert surface.get_flags() & pygame.SRCALPHA
    assert surface.get_at((0, 0)).a == 0

    pixels = _semitransparent_pixels(surface)
    assert pixels
    assert _find_rgb_close(surface, CARD_BORDER, 4) is not None, pixels[:8]


def test_bordered_rect_cache_antialiased_edges():
    """带边框缓存：尺寸不变、边缘半透明像素 RGB 接近边框色"""
    surface = BorderedRectCache.get_surface(
        120, 44, (30, 32, 58), (92, 96, 150), 2, 10,
    )

    assert surface.get_size() == (120, 44)
    assert surface.get_flags() & pygame.SRCALPHA
    assert surface.get_at((0, 0)).a == 0

    pixels = _semitransparent_pixels(surface)
    assert pixels
    assert _find_rgb_close(surface, (92, 96, 150), 4) is not None, pixels[:8]


def test_tile_surface_cache_sizes_and_edge_rgb():
    """方块缓存：尺寸/alpha 不变；圆角边缘不再出现透明黑导致的暗圈"""
    glow_surface, glow_pad = TileSurfaceCache.get(128)
    assert glow_pad == 10
    assert glow_surface.get_size() == (TILE_SIZE + 20, TILE_SIZE + 20)
    assert glow_surface.get_flags() & pygame.SRCALPHA
    assert glow_surface.get_at(glow_surface.get_rect().center).a == 255

    plain_surface, plain_pad = TileSurfaceCache.get(2)
    assert plain_pad == 0
    assert plain_surface.get_size() == (TILE_SIZE, TILE_SIZE)
    assert plain_surface.get_flags() & pygame.SRCALPHA
    assert plain_surface.get_at(plain_surface.get_rect().center).a == 255

    # 修复前透明底为黑色，圆角处约 (39,41,55)；修复后应为底色的混合，
    # 任何通道都不应低于方块底色（轮辋光会让边缘略亮于底色）。
    base = (94, 98, 140)
    pixels = _semitransparent_pixels(plain_surface)
    assert pixels, "方块圆角应有半透明抗锯齿像素"
    darkest = min(pixels, key=lambda p: sum(p[2][:3]))
    assert all(darkest[2][i] >= base[i] - 4 for i in range(3)), darkest
    assert not any(
        all(abs(p[2][i] - (39, 41, 55)[i]) <= 4 for i in range(3))
        for p in pixels
    ), "不应再出现透明黑导致的暗边"


def test_soft_circle_cache_antialiased_edges():
    """粒子柔边圆：输出尺寸不变、边缘半透明像素 RGB 保持粒子色"""
    surface = _SoftCircleCache.get((255, 100, 100), 6)

    assert surface.get_size() == (12, 12)
    assert surface.get_flags() & pygame.SRCALPHA
    pixels = _semitransparent_pixels(surface)
    assert pixels
    assert _find_rgb_close(surface, (255, 100, 100), 3) is not None, pixels[:8]


def test_gloss_cache_size_and_edges():
    """按钮顶部光泽缓存：输出尺寸不变、边缘半透明且保持白色"""
    surface = _GlossCache.get(200, 40, 16, alpha=30)

    assert surface.get_size() == (200, 40)
    assert surface.get_flags() & pygame.SRCALPHA
    pixels = _semitransparent_pixels(surface)
    assert pixels
    assert _find_rgb_close(surface, (255, 255, 255), 3) is not None, pixels[:8]
    # 再次获取应命中缓存并返回同一 Surface
    assert _GlossCache.get(200, 40, 16, alpha=30) is surface


def test_background_cache_size():
    """整窗背景缓存：输出仍为 800x600"""
    surface = BackgroundCache.get_surface()

    assert surface.get_size() == (WINDOW_WIDTH, WINDOW_HEIGHT)


def test_gradient_rect_cache_corners_and_center():
    """渐变圆角矩形：尺寸不变、四角透明且保留渐变 RGB、中心不透明"""
    surface = GradientRectCache.get_surface(
        160, 48, (100, 160, 255), (40, 80, 200), 12,
    )

    assert surface.get_size() == (160, 48)
    assert surface.get_flags() & pygame.SRCALPHA
    assert surface.get_at((0, 0)).a == 0
    assert surface.get_at((159, 0)).a == 0
    assert surface.get_at((0, 47)).a == 0
    assert surface.get_at((159, 47)).a == 0
    assert surface.get_at((80, 24)).a == 255

    # 透明区域应保留渐变 RGB（蓝色分量高），而不是透明黑 (0,0,0,0)
    pixels = _semitransparent_pixels(surface)
    assert pixels
    assert any(p[2][2] > 150 for p in pixels), pixels[:8]
