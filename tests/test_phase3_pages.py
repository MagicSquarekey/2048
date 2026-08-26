# -*- coding: utf-8 -*-
# @Function: Phase 3 - 页面适配层验证测试

import unittest
import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 初始化 pygame（页面实例化需要字体系统）
import pygame
pygame.init()


class TestPageImports(unittest.TestCase):
    """页面模块导入验证"""

    def test_all_pages_import(self):
        """验证所有页面模块可正常导入"""
        from src.views.pages.menu_page import MenuPage
        from src.views.pages.game_page import GamePage
        from src.views.pages.result_page import ResultPage
        from src.views.pages.achievements_page import AchievementsPage
        from src.views.pages.settings_page import SettingsPage
        from src.views.pages.pause_page import PausePage
        from src.views.pages.login_page import LoginPage
        self.assertTrue(True)  # 导入成功即通过

    def test_pages_package_import(self):
        """验证 pages 包级导入"""
        from src.views.pages import (
            MenuPage, GamePage, ResultPage,
            AchievementsPage, SettingsPage,
            PausePage, LoginPage,
        )
        self.assertTrue(True)


class TestMenuPage(unittest.TestCase):
    """菜单页面 iOS 适配验证"""

    def test_menu_page_exists(self):
        """菜单页面类存在"""
        from src.views.pages.menu_page import MenuPage
        self.assertTrue(callable(MenuPage))

    def test_menu_page_instantiation(self):
        """菜单页面可实例化"""
        from src.views.pages.menu_page import MenuPage
        page = MenuPage()
        self.assertIsNotNone(page)

    def test_menu_page_has_draw(self):
        """菜单页面有 draw 方法"""
        from src.views.pages.menu_page import MenuPage
        page = MenuPage()
        self.assertTrue(hasattr(page, 'draw'))
        self.assertTrue(callable(page.draw))

    def test_menu_page_has_handle_event(self):
        """菜单页面有 handle_event 方法"""
        from src.views.pages.menu_page import MenuPage
        page = MenuPage()
        self.assertTrue(hasattr(page, 'handle_event'))
        self.assertTrue(callable(page.handle_event))


class TestGamePage(unittest.TestCase):
    """游戏页面 iOS 适配验证"""

    def test_game_page_exists(self):
        """游戏页面类存在"""
        from src.views.pages.game_page import GamePage
        self.assertTrue(callable(GamePage))

    def test_game_page_instantiation(self):
        """游戏页面可实例化"""
        from src.views.pages.game_page import GamePage
        page = GamePage()
        self.assertIsNotNone(page)

    def test_game_page_has_draw(self):
        """游戏页面有 draw 方法"""
        from src.views.pages.game_page import GamePage
        page = GamePage()
        self.assertTrue(hasattr(page, 'draw'))
        self.assertTrue(callable(page.draw))

    def test_game_page_has_handle_event(self):
        """游戏页面有 handle_event 方法"""
        from src.views.pages.game_page import GamePage
        page = GamePage()
        self.assertTrue(hasattr(page, 'handle_event'))
        self.assertTrue(callable(page.handle_event))


class TestResultPage(unittest.TestCase):
    """结果页面 iOS 适配验证"""

    def test_result_page_exists(self):
        """结果页面类存在"""
        from src.views.pages.result_page import ResultPage
        self.assertTrue(callable(ResultPage))

    def test_result_page_instantiation(self):
        """结果页面可实例化"""
        from src.views.pages.result_page import ResultPage
        page = ResultPage()
        self.assertIsNotNone(page)


class TestAchievementsPage(unittest.TestCase):
    """成就页面 iOS 适配验证"""

    def test_achievements_page_exists(self):
        """成就页面类存在"""
        from src.views.pages.achievements_page import AchievementsPage
        self.assertTrue(callable(AchievementsPage))

    def test_achievements_page_instantiation(self):
        """成就页面可实例化"""
        from src.views.pages.achievements_page import AchievementsPage
        page = AchievementsPage()
        self.assertIsNotNone(page)


class TestSettingsPage(unittest.TestCase):
    """设置页面 iOS 适配验证"""

    def test_settings_page_exists(self):
        """设置页面类存在"""
        from src.views.pages.settings_page import SettingsPage
        self.assertTrue(callable(SettingsPage))

    def test_settings_page_instantiation(self):
        """设置页面可实例化"""
        from src.views.pages.settings_page import SettingsPage
        page = SettingsPage()
        self.assertIsNotNone(page)


class TestPausePage(unittest.TestCase):
    """暂停页面 iOS 适配验证"""

    def test_pause_page_exists(self):
        """暂停页面类存在"""
        from src.views.pages.pause_page import PausePage
        self.assertTrue(callable(PausePage))

    def test_pause_page_instantiation(self):
        """暂停页面可实例化"""
        from src.views.pages.pause_page import PausePage
        page = PausePage()
        self.assertIsNotNone(page)


class TestLoginPage(unittest.TestCase):
    """登录页面 iOS 适配验证"""

    def test_login_page_exists(self):
        """登录页面类存在"""
        from src.views.pages.login_page import LoginPage
        self.assertTrue(callable(LoginPage))

    def test_login_page_instantiation(self):
        """登录页面可实例化"""
        from src.views.pages.login_page import LoginPage
        page = LoginPage()
        self.assertIsNotNone(page)


class TestPageNavigation(unittest.TestCase):
    """页面导航验证"""

    def test_page_registry(self):
        """页面注册表完整性"""
        from src.views.pages import (
            MenuPage, GamePage, ResultPage,
            AchievementsPage, SettingsPage,
            PausePage, LoginPage,
        )
        pages = {
            'menu': MenuPage,
            'game': GamePage,
            'result': ResultPage,
            'achievements': AchievementsPage,
            'settings': SettingsPage,
            'pause': PausePage,
            'login': LoginPage,
        }
        self.assertEqual(len(pages), 7)
        for name, cls in pages.items():
            self.assertTrue(callable(cls), f"Page '{name}' is not callable")

    def test_page_enum_completeness(self):
        """页面枚举完整性"""
        from src.config import (
            PAGE_SPLASH, PAGE_MENU, PAGE_GAME, PAGE_RESULT,
            PAGE_SETTINGS, PAGE_MODES,
        )
        self.assertEqual(PAGE_SPLASH, "splash")
        self.assertEqual(PAGE_MENU, "menu")
        self.assertEqual(PAGE_GAME, "game")
        self.assertEqual(PAGE_RESULT, "result")
        self.assertEqual(PAGE_SETTINGS, "settings")
        self.assertEqual(PAGE_MODES, "modes")


class TestiOSComponents(unittest.TestCase):
    """iOS 组件集成验证"""

    def test_button_import(self):
        """Button 组件导入"""
        from src.views.ui_components import Button
        self.assertTrue(callable(Button))

    def test_label_import(self):
        """Label 组件导入"""
        from src.views.ui_components import Label
        self.assertTrue(callable(Label))

    def test_panel_import(self):
        """Panel 组件导入"""
        from src.views.ui_components import Panel
        self.assertTrue(callable(Panel))

    def test_scorebox_import(self):
        """ScoreBox 组件导入"""
        from src.views.ui_components import ScoreBox
        self.assertTrue(callable(ScoreBox))

    def test_ios_radius_in_config(self):
        """iOS 圆角令牌在配置中"""
        from src.config import RADIUS_SM, RADIUS_MD, RADIUS_LG, RADIUS_XL
        self.assertGreater(RADIUS_SM, 0)
        self.assertGreater(RADIUS_MD, 0)
        self.assertGreater(RADIUS_LG, 0)
        self.assertGreater(RADIUS_XL, 0)
        self.assertLess(RADIUS_SM, RADIUS_MD)
        self.assertLess(RADIUS_MD, RADIUS_LG)
        self.assertLess(RADIUS_LG, RADIUS_XL)

    def test_ios_colors_in_config(self):
        """iOS 颜色在配置中"""
        from src.config import (
            COLOR_BG, COLOR_BOARD_BG, COLOR_TILE_EMPTY,
            COLOR_BTN_PRIMARY, COLOR_BTN_DANGER,
        )
        # 验证所有颜色为 RGB 元组
        for color in [COLOR_BG, COLOR_BOARD_BG, COLOR_TILE_EMPTY,
                      COLOR_BTN_PRIMARY, COLOR_BTN_DANGER]:
            self.assertIsInstance(color, tuple)
            self.assertEqual(len(color), 3)


class TestFullFlow(unittest.TestCase):
    """完整流程验证"""

    def test_full_game_flow(self):
        """完整游戏流程：启动→游戏→得分→结束"""
        from src.models.game_state import GameState
        from src.models.board import GameBoard

        state = GameState()
        state.start_game("classic")
        self.assertEqual(state.state, GameState.STATE_PLAYING)

        # 模拟几步操作
        board = state.board
        initial_score = board.score

        # 执行移动
        moved = board.move("left")
        self.assertIsInstance(moved, bool)

        state = GameState()
        state.start_game("classic")
        self.assertIsNotNone(state.board)
        self.assertEqual(state.mode, "classic")

    def test_three_game_modes(self):
        """三种游戏模式可启动"""
        from src.models.game_state import GameState

        for mode in ["classic", "timed", "challenge"]:
            state = GameState()
            state.start_game(mode)
            self.assertEqual(state.state, GameState.STATE_PLAYING)
            self.assertEqual(state.mode, mode)

    def test_undo_functionality(self):
        """撤销功能完整"""
        from src.models.game_state import GameState

        state = GameState()
        state.start_game("classic")
        board = state.board
        board.move("left")
        state.undo()
        self.assertIsNotNone(state.board)

    def test_data_persistence_import(self):
        """数据持久化模块导入正常"""
        from src.models.data_manager import DataManager
        self.assertTrue(callable(DataManager))

    def test_i18n_import(self):
        """国际化模块导入正常"""
        from src.i18n import t, get_current_lang
        self.assertTrue(callable(t))
        self.assertTrue(callable(get_current_lang))
        self.assertEqual(get_current_lang(), "zh")


class TestPerformance(unittest.TestCase):
    """性能验证"""

    def test_page_instantiation_time(self):
        """页面实例化性能"""
        from src.views.pages.menu_page import MenuPage
        from src.views.pages.game_page import GamePage
        from src.views.pages.result_page import ResultPage
        from src.views.pages.settings_page import SettingsPage
        from src.views.pages.pause_page import PausePage
        from src.views.pages.login_page import LoginPage
        from src.views.pages.achievements_page import AchievementsPage

        pages = [MenuPage, GamePage, ResultPage, SettingsPage,
                 PausePage, LoginPage, AchievementsPage]

        start = time.time()
        for _ in range(10):
            for page_cls in pages:
                page_cls()
        elapsed = time.time() - start

        # 70次实例化（7页面 x 10次）应在2秒内完成
        self.assertLess(elapsed, 2.0,
                        f"Page instantiation too slow: {elapsed:.2f}s for 70 ops")

    def test_config_import_time(self):
        """配置模块导入性能"""
        start = time.time()
        for _ in range(100):
            import importlib
            import src.config
            importlib.reload(src.config)
        elapsed = time.time() - start

        # 100次重载应在5秒内完成
        self.assertLess(elapsed, 5.0,
                        f"Config import too slow: {elapsed:.2f}s for 100 reloads")


if __name__ == "__main__":
    unittest.main()