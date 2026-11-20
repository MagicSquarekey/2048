# -*- coding: utf-8 -*-
# @Function: Button / ModeCard 过期 hover 交互回归测试
# Regression tests for stale hover on Button and ModeCard

import os
import sys
import unittest
from unittest.mock import patch

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

# 添加项目根目录到 Python 路径 / Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame  # noqa: E402

from src.views.ui_components import Button  # noqa: E402
from src.views.pages.menu_page import ModeCard  # noqa: E402
from src.views.pages.game_page import GamePage  # noqa: E402


def _mouse_event(event_type: int, pos: tuple, button: int = 1) -> pygame.event.Event:
    """构造鼠标事件 / Build a mouse event"""
    attrs = {"pos": pos}
    if event_type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
        attrs["button"] = button
    elif event_type == pygame.MOUSEMOTION:
        attrs.update({"rel": (0, 0), "buttons": (0, 0, 0)})
    return pygame.event.Event(event_type, attrs)


class _DisplayTestCase(unittest.TestCase):
    """提供隐藏窗口的测试基类 / Base test case with a hidden display"""

    def setUp(self) -> None:
        if not pygame.get_init():
            pygame.init()
        pygame.display.set_mode((800, 600), pygame.HIDDEN)


class TestButtonInteraction(_DisplayTestCase):
    """Button 过期 hover 不应触发点击 / Stale hover must not fire Button callbacks"""

    def setUp(self) -> None:
        super().setUp()
        self.calls = []
        self.button = Button(
            100, 100, 200, 50, "Test",
            callback=lambda: self.calls.append(1),
        )

    def test_stale_hover_does_not_trigger_outside_click(self) -> None:
        """hover 缓存仍在，但窗口外按下/抬起不触发 / Outside click does not fire"""
        self.button.handle_event(_mouse_event(pygame.MOUSEMOTION, (150, 125)))
        self.assertTrue(self.button.is_hovered)

        self.button.handle_event(_mouse_event(pygame.MOUSEBUTTONDOWN, (10, 10)))
        self.assertFalse(self.button.is_pressed)
        self.button.handle_event(_mouse_event(pygame.MOUSEBUTTONUP, (10, 10)))

        self.assertEqual(self.calls, [])
        self.assertFalse(self.button.is_pressed)

    def test_inside_click_triggers_callback_once(self) -> None:
        """按钮内正常点击只触发一次 / Inside click fires exactly once"""
        self.button.handle_event(_mouse_event(pygame.MOUSEMOTION, (150, 125)))
        self.button.handle_event(_mouse_event(pygame.MOUSEBUTTONDOWN, (150, 125)))
        self.assertTrue(self.button.is_pressed)

        self.button.handle_event(_mouse_event(pygame.MOUSEBUTTONUP, (150, 125)))
        self.assertEqual(self.calls, [1])
        self.assertFalse(self.button.is_pressed)


class TestModeCardInteraction(_DisplayTestCase):
    """ModeCard 过期 hover 不应触发回调 / Stale hover must not fire ModeCard callbacks"""

    def setUp(self) -> None:
        super().setUp()
        self.calls = []
        self.card = ModeCard(
            0, 0, 440, 64, "classic",
            lambda: self.calls.append(1),
        )

    def test_stale_hover_does_not_trigger_outside_click(self) -> None:
        """hover 缓存仍在，但卡片外按下/抬起不触发 / Outside click does not fire"""
        self.card.handle_event(_mouse_event(pygame.MOUSEMOTION, (200, 30)))
        self.assertTrue(self.card.is_hovered)

        self.card.handle_event(_mouse_event(pygame.MOUSEBUTTONDOWN, (200, 100)))
        self.assertFalse(self.card.is_pressed)
        self.card.handle_event(_mouse_event(pygame.MOUSEBUTTONUP, (200, 100)))

        self.assertEqual(self.calls, [])
        self.assertFalse(self.card.is_pressed)

    def test_inside_click_triggers_callback_once(self) -> None:
        """卡片内正常点击只触发一次 / Inside click fires exactly once"""
        self.card.handle_event(_mouse_event(pygame.MOUSEMOTION, (200, 30)))
        self.card.handle_event(_mouse_event(pygame.MOUSEBUTTONDOWN, (200, 30)))
        self.assertTrue(self.card.is_pressed)

        self.card.handle_event(_mouse_event(pygame.MOUSEBUTTONUP, (200, 30)))
        self.assertEqual(self.calls, [1])
        self.assertFalse(self.card.is_pressed)


class TestGamePageLetterboxSwipe(_DisplayTestCase):
    """GamePage 留边抬起只清手势 / Letterbox release clears the swipe gesture"""

    def setUp(self) -> None:
        super().setUp()
        self.game = GamePage()
        self.game.on_enter(mode="classic")

    def test_outside_up_clears_swipe_without_move(self) -> None:
        """留边抬起清空 `_swipe_start` 且不触发移动 / Outside release never moves"""
        self.game._swipe_start = (600, 300)
        event = _mouse_event(pygame.MOUSEBUTTONUP, (0, 300))
        event.outside_viewport = True

        with patch.object(self.game, "_do_move") as do_move:
            self.game.handle_event(event)
            do_move.assert_not_called()

        self.assertIsNone(self.game._swipe_start)

    def test_inside_up_moves(self) -> None:
        """视口内抬起按滑动方向移动一次 / Inside release performs one move"""
        self.game._swipe_start = (600, 300)
        event = _mouse_event(pygame.MOUSEBUTTONUP, (200, 300))
        event.outside_viewport = False

        with patch.object(self.game, "_do_move") as do_move:
            self.game.handle_event(event)
            do_move.assert_called_once()

        self.assertIsNone(self.game._swipe_start)


if __name__ == "__main__":
    unittest.main()
