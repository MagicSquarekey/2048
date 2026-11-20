# -*- coding: utf-8 -*-
# @Function: DisplayManager 窗口缩放与等比展示测试 / DisplayManager resize and aspect-fit tests

import os
import sys
import unittest

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

# 添加项目根目录到 Python 路径 / Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame  # noqa: E402

from src.config import (  # noqa: E402
    MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT,
)
from src.views.display_manager import DisplayManager  # noqa: E402


class TestDisplayManager(unittest.TestCase):
    """DisplayManager 单元测试 / DisplayManager unit tests"""

    def setUp(self) -> None:
        """每个测试创建独立实例 / Create an independent instance per test"""
        if not pygame.get_init():
            pygame.init()
        self.dm = DisplayManager()
        self.dm.init(pygame.HIDDEN | pygame.RESIZABLE)

    # ========== viewport 计算 / viewport calculation ==========

    def test_viewport_matches_800x600(self) -> None:
        """800x600 窗口：viewport 铺满 / 800x600 window fills the viewport"""
        self.dm.resize(800, 600)
        self.assertEqual(self.dm.viewport, pygame.Rect(0, 0, 800, 600))
        self.assertEqual(self.dm._scaled.get_size(), (800, 600))

    def test_viewport_1600x1200(self) -> None:
        """1600x1200 窗口：2 倍等比放大 / 1600x1200 scales by 2x"""
        self.dm.resize(1600, 1200)
        self.assertEqual(self.dm.viewport, pygame.Rect(0, 0, 1600, 1200))
        self.assertEqual(self.dm._scaled.get_size(), (1600, 1200))

    def test_viewport_1200x800_letterbox_left_right(self) -> None:
        """1200x800：左右留边、垂直铺满 / Pillarbox at 1200x800"""
        self.dm.resize(1200, 800)
        self.assertEqual(self.dm.viewport, pygame.Rect(67, 0, 1066, 800))
        self.assertEqual(self.dm._scaled.get_size(), (1066, 800))

    def test_viewport_600x800_letterbox_top_bottom(self) -> None:
        """600x800：上下留边、水平铺满 / Letterbox at 600x800"""
        self.dm.resize(600, 800)
        self.assertEqual(self.dm.viewport, pygame.Rect(0, 175, 600, 450))
        self.assertEqual(self.dm._scaled.get_size(), (600, 450))

    def test_viewport_offsets_when_matching_logical_size(self) -> None:
        """1200x600：视口左右偏移但尺寸仍为 800x600 / Offset viewport at logical size"""
        self.dm.resize(1200, 600)
        self.assertEqual(self.dm.viewport, pygame.Rect(200, 0, 800, 600))

        self.dm.canvas.fill((30, 40, 50))
        pygame.draw.rect(self.dm.canvas, (200, 100, 50), (350, 250, 100, 100))
        self.dm.present()

        # 中心内容直接 blit，不发生重采样 / Center content is copied without resampling
        self.assertEqual(
            tuple(self.dm.screen.get_at((600, 300))[:3]),
            tuple(self.dm.canvas.get_at((400, 300))[:3]),
        )
        self.assertEqual(tuple(self.dm.screen.get_at((600, 300))[:3]), (200, 100, 50))

        # 左右角落为边缘延展色 / Corners are filled from the canvas edges
        for corner in ((0, 0), (1199, 0), (0, 599), (1199, 599)):
            self.assertEqual(
                tuple(self.dm.screen.get_at(corner)[:3]),
                (30, 40, 50),
                f"letterbox not filled at {corner}",
            )

    def test_repeated_resize_reuses_scaled(self) -> None:
        """视口尺寸不变时复用缩放缓冲 / Reuse scaled buffer when viewport size matches"""
        self.dm.resize(1200, 800)
        self.assertEqual(self.dm.viewport, pygame.Rect(67, 0, 1066, 800))
        scaled = self.dm._scaled

        self.dm.resize(1400, 800)
        self.assertEqual(self.dm.viewport, pygame.Rect(167, 0, 1066, 800))
        self.assertIs(self.dm._scaled, scaled)

        self.dm.resize(800, 600)
        self.assertIsNot(self.dm._scaled, scaled)
        self.assertEqual(self.dm._scaled.get_size(), (800, 600))

    # ========== 坐标映射 / position mapping ==========

    def test_map_pos_center(self) -> None:
        """窗口中心映射到逻辑中心 / Window center maps to logical center"""
        self.dm.resize(1200, 800)
        self.assertEqual(self.dm.map_pos((600, 400)), (400, 300))

    def test_map_pos_clamps_letterbox_corners(self) -> None:
        """留边角落被 clamp 到逻辑边界 / Letterbox corners clamp to logical bounds"""
        self.dm.resize(1200, 800)
        self.assertEqual(self.dm.map_pos((0, 0)), (0, 0))
        self.assertEqual(self.dm.map_pos((1199, 799)), (799, 599))
        # 左侧留边内部的点至少被夹到 x=0 / Points inside the left gutter clamp to x=0
        left_x, left_y = self.dm.map_pos((10, 400))
        self.assertEqual(left_x, 0)
        self.assertTrue(0 <= left_y <= 599)

    def test_map_pos_center_with_top_bottom_letterbox(self) -> None:
        """上下留边时中心仍映射到逻辑中心 / Center mapping with top-bottom letterbox"""
        self.dm.resize(600, 800)
        self.assertEqual(self.dm.map_pos((300, 400)), (400, 300))

    def test_is_inside_viewport(self) -> None:
        """留边点不算视口内部 / Letterbox points are outside the viewport"""
        self.dm.resize(1200, 800)
        self.assertTrue(self.dm.is_inside_viewport((600, 400)))
        self.assertFalse(self.dm.is_inside_viewport((10, 400)))
        self.assertFalse(self.dm.is_inside_viewport((1190, 400)))
        self.assertTrue(self.dm.is_inside_viewport((67, 0)))

    # ========== resize clamp ==========

    def test_resize_clamps_to_minimum(self) -> None:
        """过小窗口被 clamp 到最小尺寸 / Tiny windows clamp to minimum size"""
        self.dm.resize(100, 100)
        self.assertEqual(
            self.dm.screen.get_size(),
            (MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT),
        )
        self.assertEqual((MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT), (480, 360))
        self.assertEqual(self.dm.viewport, pygame.Rect(0, 0, 480, 360))

    # ========== 事件换算 / event translation ==========

    def test_translate_mouse_motion(self) -> None:
        """MOUSEMOTION 的 pos 与 rel 都按比例换算 / Both pos and rel are scaled"""
        self.dm.resize(1600, 1200)
        event = pygame.event.Event(
            pygame.MOUSEMOTION,
            {"pos": (800, 600), "rel": (10, 6), "buttons": (0, 0, 0)},
        )
        returned = self.dm.translate_event(event)
        self.assertIs(returned, event)
        self.assertEqual(event.pos, (400, 300))
        self.assertEqual(event.rel, (5, 3))

    def test_translate_mouse_buttons(self) -> None:
        """MOUSEBUTTONDOWN/UP 的 pos 换算为逻辑坐标 / Button positions are scaled"""
        self.dm.resize(1600, 1200)
        down = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {"pos": (400, 300), "button": 1},
        )
        up = pygame.event.Event(
            pygame.MOUSEBUTTONUP,
            {"pos": (1200, 900), "button": 1},
        )
        self.dm.translate_event(down)
        self.dm.translate_event(up)
        self.assertEqual(down.pos, (200, 150))
        self.assertEqual(up.pos, (600, 450))

    # ========== 展示 / presentation ==========

    def test_present_full_window_no_error(self) -> None:
        """800x600 直接展示不抛异常且中心像素一致 / Direct blit keeps center pixel"""
        self.dm.resize(800, 600)
        self.dm.canvas.fill((18, 24, 36))
        pygame.draw.rect(self.dm.canvas, (220, 120, 40), (350, 250, 100, 100))

        self.dm.present()

        self.assertEqual(
            tuple(self.dm.screen.get_at((400, 300))[:3]),
            tuple(self.dm.canvas.get_at((400, 300))[:3]),
        )

    def test_present_1200x800_center_and_backdrop(self) -> None:
        """1200x800：中心内容可见、留边由边缘延展覆盖 / Center visible, letterbox filled"""
        self.dm.resize(1200, 800)
        self.dm.canvas.fill((18, 24, 36))
        pygame.draw.rect(self.dm.canvas, (220, 120, 40), (350, 250, 100, 100))

        self.dm.present()

        # 画面中心与 canvas 中心一致 / Screen center matches canvas center
        self.assertEqual(
            tuple(self.dm.screen.get_at((600, 400))[:3]),
            tuple(self.dm.canvas.get_at((400, 300))[:3]),
        )
        self.assertEqual(tuple(self.dm.screen.get_at((600, 400))[:3]), (220, 120, 40))

        # 四个角落属于留边，应与画面边缘同色 / Corners use edge-extension colors
        for corner in ((0, 0), (1199, 0), (0, 799), (1199, 799)):
            self.assertEqual(
                tuple(self.dm.screen.get_at(corner)[:3]),
                (18, 24, 36),
                f"backdrop not filled at {corner}",
            )

    def test_present_600x800_top_bottom_backdrop(self) -> None:
        """600x800：上下留边与缩放后内容边缘同色 / Top/bottom strips match scaled edges"""
        self.dm.resize(600, 800)
        self.dm.canvas.fill((12, 34, 56))

        self.dm.present()

        # 留边取缩放后内容边缘，允许 smoothscale 整体压暗 / Strips match scaled edges
        self.assertEqual(
            tuple(self.dm.screen.get_at((300, 10))[:3]),
            tuple(self.dm.screen.get_at((300, 175))[:3]),
        )
        self.assertEqual(
            tuple(self.dm.screen.get_at((300, 790))[:3]),
            tuple(self.dm.screen.get_at((300, 624))[:3]),
        )

    def test_letterbox_edge_matches_scaled_content(self) -> None:
        """留边条取自缩放后内容，边界无 1px 色差 / Letterbox matches scaled edge pixels"""
        self.dm.resize(600, 800)
        self.dm.canvas.fill((12, 34, 56))

        self.dm.present()

        self.assertEqual(
            tuple(self.dm.screen.get_at((300, 10))[:3]),
            tuple(self.dm.screen.get_at((300, 175))[:3]),
        )

    def test_letterbox_updates_with_canvas(self) -> None:
        """canvas 变色后留边条实时跟随 / Letterbox strips follow live canvas colors"""
        self.dm.resize(1200, 800)

        self.dm.canvas.fill((255, 0, 0))
        self.dm.present()
        self.assertEqual(tuple(self.dm.screen.get_at((0, 0))[:3]), (255, 0, 0))
        self.assertEqual(tuple(self.dm.screen.get_at((1199, 799))[:3]), (255, 0, 0))

        self.dm.canvas.fill((0, 255, 0))
        self.dm.present()
        self.assertEqual(tuple(self.dm.screen.get_at((0, 0))[:3]), (0, 255, 0))
        self.assertEqual(tuple(self.dm.screen.get_at((1199, 799))[:3]), (0, 255, 0))

    def test_present_before_init_raises(self) -> None:
        """未初始化时 present 给出明确错误 / present without init raises a clear error"""
        dm = DisplayManager()
        with self.assertRaisesRegex(RuntimeError, "init"):
            dm.present()


if __name__ == "__main__":
    unittest.main()
