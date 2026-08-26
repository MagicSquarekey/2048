# -*- coding: utf-8 -*-
# @Function: iOS风格改造验收测试用例
# @Description: 全面验证iOS风格改造的功能正确性、UI一致性和用户体验

import unittest
import sys
import os
import time
import pygame

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import (
    # 颜色系统
    COLOR_BG, COLOR_BOARD_BG, COLOR_TILE_EMPTY,
    COLOR_TEXT, COLOR_TEXT_SECONDARY, COLOR_TEXT_TERTIARY, COLOR_TEXT_QUATERNARY,
    COLOR_BTN_PRIMARY, COLOR_BTN_PRIMARY_HOVER,
    COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
    COLOR_BTN_DANGER, COLOR_BTN_DANGER_HOVER,
    COLOR_GREEN, COLOR_ORANGE, COLOR_TEAL, COLOR_INDIGO, COLOR_PINK,
    COLOR_YELLOW, COLOR_RED,
    COLOR_SCORE_BG, COLOR_OVERLAY,
    TILE_COLORS,
    # 字体系统
    FONT_SIZE_CAPTION2, FONT_SIZE_CAPTION1, FONT_SIZE_FOOTNOTE,
    FONT_SIZE_SUBHEAD, FONT_SIZE_BODY, FONT_SIZE_TITLE3,
    FONT_SIZE_TITLE2, FONT_SIZE_TITLE1, FONT_SIZE_LARGE_TITLE,
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL, FONT_SIZE_TINY,
    TILE_FONT_SIZES,
    # 圆角配置
    RADIUS_SM, RADIUS_MD, RADIUS_LG, RADIUS_XL,
    # 动画配置
    ANIMATION_MOVE_DURATION, ANIMATION_MERGE_DURATION,
    ANIMATION_SPAWN_DURATION, ANIMATION_FADE_DURATION,
    SPRING_DAMPING, SPRING_FREQUENCY,
    # 间距系统
    IOS_SPACING_BASE, IOS_SPACING_XXS, IOS_SPACING_XS, IOS_SPACING_SM,
    IOS_SPACING_MD, IOS_SPACING_LG, IOS_SPACING_XL, IOS_SPACING_XXL, IOS_SPACING_XXXL,
    SPACING_TINY, SPACING_SMALL, SPACING_MEDIUM, SPACING_LARGE, SPACING_HUGE,
    # 棋盘配置
    WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_SIZE, TILE_SIZE, TILE_GAP, BOARD_PADDING, BOARD_X, BOARD_Y,
    # 游戏参数
    INITIAL_TILES, WIN_TILE, UNDO_LIMIT_DEFAULT, CLEAN_LIMIT_DEFAULT,
    MODE_CONFIG,
)


class TestIOSColorSystemAcceptance(unittest.TestCase):
    """iOS颜色系统验收测试"""

    def test_background_colors(self):
        """测试背景颜色配置"""
        # 验证颜色格式
        self.assertIsInstance(COLOR_BG, tuple)
        self.assertEqual(len(COLOR_BG), 3)
        self.assertIsInstance(COLOR_BOARD_BG, tuple)
        self.assertEqual(len(COLOR_BOARD_BG), 3)
        self.assertIsInstance(COLOR_TILE_EMPTY, tuple)
        self.assertEqual(len(COLOR_TILE_EMPTY), 3)

        # 验证颜色值范围
        for color in [COLOR_BG, COLOR_BOARD_BG, COLOR_TILE_EMPTY]:
            for value in color:
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, 255)

        # 验证iOS系统颜色值
        self.assertEqual(COLOR_BG, (242, 242, 247))  # iOS Gray 6
        self.assertEqual(COLOR_BOARD_BG, (255, 255, 255))  # 纯白
        self.assertEqual(COLOR_TILE_EMPTY, (230, 230, 235))  # iOS Gray 5

    def test_text_colors(self):
        """测试文字颜色配置"""
        # 验证主要文字颜色
        self.assertEqual(COLOR_TEXT, (0, 0, 0))  # 纯黑

        # 验证次要文字颜色（优化后对比度≥4.5:1）
        self.assertEqual(COLOR_TEXT_SECONDARY, (48, 48, 54))  # iOS Gray（优化后）

        # 验证第三级文字颜色（优化后对比度5.2:1）
        self.assertEqual(COLOR_TEXT_TERTIARY, (100, 100, 108))

        # 验证第四级文字颜色
        self.assertEqual(COLOR_TEXT_QUATERNARY, (142, 142, 147))

        # 验证对比度优化
        # COLOR_TEXT_TERTIARY (100,100,108) vs 背景 (242,242,247)
        # 对比度应 >= 4.5:1 (WCAG AA标准)
        bg_luminance = self._relative_luminance(COLOR_BG)
        text_luminance = self._relative_luminance(COLOR_TEXT_TERTIARY)
        contrast = self._contrast_ratio(bg_luminance, text_luminance)
        self.assertGreaterEqual(contrast, 4.5, f"文字对比度不足: {contrast:.2f}:1")

    def _relative_luminance(self, color):
        """计算相对亮度"""
        r, g, b = [x / 255.0 for x in color]
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def _contrast_ratio(self, l1, l2):
        """计算对比度"""
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)

    def test_button_colors(self):
        """测试按钮颜色配置"""
        # 验证主要按钮颜色（iOS Blue）
        self.assertEqual(COLOR_BTN_PRIMARY, (0, 122, 255))
        self.assertEqual(COLOR_BTN_PRIMARY_HOVER, (10, 132, 255))

        # 验证次要按钮颜色
        self.assertEqual(COLOR_BTN_SECONDARY, (242, 242, 247))
        self.assertEqual(COLOR_BTN_SECONDARY_HOVER, (230, 230, 235))

        # 验证危险按钮颜色（iOS Red）
        self.assertEqual(COLOR_BTN_DANGER, (255, 59, 48))
        self.assertEqual(COLOR_BTN_DANGER_HOVER, (255, 69, 58))

    def test_system_colors(self):
        """测试iOS系统颜色"""
        # 验证iOS系统颜色值
        self.assertEqual(COLOR_GREEN, (52, 199, 89))  # iOS Green
        self.assertEqual(COLOR_ORANGE, (255, 149, 0))  # iOS Orange
        self.assertEqual(COLOR_TEAL, (90, 200, 250))  # iOS Teal
        self.assertEqual(COLOR_INDIGO, (88, 86, 214))  # iOS Indigo
        self.assertEqual(COLOR_PINK, (255, 45, 85))  # iOS Pink
        self.assertEqual(COLOR_YELLOW, (255, 204, 0))  # iOS Yellow
        self.assertEqual(COLOR_RED, (255, 59, 48))  # iOS Red

    def test_tile_colors(self):
        """测试方块颜色配置"""
        # 验证所有必需的方块值都有对应的颜色
        required_values = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
        for value in required_values:
            self.assertIn(value, TILE_COLORS, f"方块值 {value} 缺少颜色配置")
            bg_color, text_color = TILE_COLORS[value]
            self.assertEqual(len(bg_color), 3, f"方块 {value} 背景颜色格式错误")
            self.assertEqual(len(text_color), 3, f"方块 {value} 文字颜色格式错误")

            # 验证颜色值范围
            for c in bg_color + text_color:
                self.assertGreaterEqual(c, 0)
                self.assertLessEqual(c, 255)

    def test_overlay_color(self):
        """测试遮罩颜色"""
        # 验证遮罩颜色格式（RGBA）
        self.assertEqual(len(COLOR_OVERLAY), 4)
        self.assertEqual(COLOR_OVERLAY, (0, 0, 0, 40))  # iOS 更浅的遮罩


class TestIOSFontSystemAcceptance(unittest.TestCase):
    """iOS字号系统验收测试"""

    def test_ios_font_sizes(self):
        """测试iOS标准字号"""
        # 验证字号类型
        font_sizes = [
            FONT_SIZE_CAPTION2, FONT_SIZE_CAPTION1, FONT_SIZE_FOOTNOTE,
            FONT_SIZE_SUBHEAD, FONT_SIZE_BODY, FONT_SIZE_TITLE3,
            FONT_SIZE_TITLE2, FONT_SIZE_TITLE1, FONT_SIZE_LARGE_TITLE
        ]

        for size in font_sizes:
            self.assertIsInstance(size, int)
            self.assertGreater(size, 0)

        # 验证字号递增关系
        self.assertLess(FONT_SIZE_CAPTION2, FONT_SIZE_CAPTION1)
        self.assertLess(FONT_SIZE_CAPTION1, FONT_SIZE_FOOTNOTE)
        self.assertLess(FONT_SIZE_FOOTNOTE, FONT_SIZE_SUBHEAD)
        self.assertLess(FONT_SIZE_SUBHEAD, FONT_SIZE_BODY)
        self.assertLess(FONT_SIZE_BODY, FONT_SIZE_TITLE3)
        self.assertLess(FONT_SIZE_TITLE3, FONT_SIZE_TITLE2)
        self.assertLess(FONT_SIZE_TITLE2, FONT_SIZE_TITLE1)
        self.assertLess(FONT_SIZE_TITLE1, FONT_SIZE_LARGE_TITLE)

        # 验证iOS 8pt网格值
        self.assertEqual(FONT_SIZE_CAPTION2, 11)
        self.assertEqual(FONT_SIZE_CAPTION1, 12)
        self.assertEqual(FONT_SIZE_FOOTNOTE, 13)
        self.assertEqual(FONT_SIZE_SUBHEAD, 15)
        self.assertEqual(FONT_SIZE_BODY, 17)
        self.assertEqual(FONT_SIZE_TITLE3, 20)
        self.assertEqual(FONT_SIZE_TITLE2, 22)
        self.assertEqual(FONT_SIZE_TITLE1, 28)
        self.assertEqual(FONT_SIZE_LARGE_TITLE, 34)

    def test_legacy_font_compatibility(self):
        """测试旧接口兼容性"""
        # 验证兼容性映射
        self.assertEqual(FONT_SIZE_LARGE, FONT_SIZE_LARGE_TITLE)
        self.assertEqual(FONT_SIZE_MEDIUM, FONT_SIZE_BODY)
        self.assertEqual(FONT_SIZE_SMALL, FONT_SIZE_FOOTNOTE)
        self.assertEqual(FONT_SIZE_TINY, FONT_SIZE_CAPTION1)

    def test_tile_font_sizes(self):
        """测试方块数字字号映射"""
        required_values = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
        for value in required_values:
            self.assertIn(value, TILE_FONT_SIZES, f"方块值 {value} 缺少字号配置")
            self.assertIsInstance(TILE_FONT_SIZES[value], int)
            self.assertGreater(TILE_FONT_SIZES[value], 0)

        # 验证字号递减关系（数字位数越多，字号越小）
        self.assertGreater(TILE_FONT_SIZES[2], TILE_FONT_SIZES[16])
        self.assertGreater(TILE_FONT_SIZES[16], TILE_FONT_SIZES[128])
        self.assertGreater(TILE_FONT_SIZES[128], TILE_FONT_SIZES[1024])


class TestIOSRadiusConfigAcceptance(unittest.TestCase):
    """iOS圆角配置验收测试"""

    def test_radius_tokens(self):
        """测试圆角令牌"""
        # 验证圆角值类型和范围
        radii = [RADIUS_SM, RADIUS_MD, RADIUS_LG, RADIUS_XL]
        for radius in radii:
            self.assertIsInstance(radius, int)
            self.assertGreater(radius, 0)
            self.assertLessEqual(radius, 50)  # 合理范围

        # 验证递增关系
        self.assertLess(RADIUS_SM, RADIUS_MD)
        self.assertLess(RADIUS_MD, RADIUS_LG)
        self.assertLess(RADIUS_LG, RADIUS_XL)

        # 验证iOS圆角值
        self.assertEqual(RADIUS_SM, 8)
        self.assertEqual(RADIUS_MD, 12)
        self.assertEqual(RADIUS_LG, 16)
        self.assertEqual(RADIUS_XL, 20)


class TestIOSAnimationConfigAcceptance(unittest.TestCase):
    """iOS动画配置验收测试"""

    def test_animation_durations(self):
        """测试动画时长配置"""
        durations = [
            ANIMATION_MOVE_DURATION, ANIMATION_MERGE_DURATION,
            ANIMATION_SPAWN_DURATION, ANIMATION_FADE_DURATION
        ]

        for duration in durations:
            self.assertIsInstance(duration, int)
            self.assertGreater(duration, 0)
            self.assertLessEqual(duration, 1000)  # 合理范围（毫秒）

        # 验证动画时长值
        self.assertEqual(ANIMATION_MOVE_DURATION, 250)
        self.assertEqual(ANIMATION_MERGE_DURATION, 280)
        self.assertEqual(ANIMATION_SPAWN_DURATION, 200)
        self.assertEqual(ANIMATION_FADE_DURATION, 350)

    def test_spring_animation_params(self):
        """测试弹簧动画参数"""
        # 验证阻尼系数
        self.assertIsInstance(SPRING_DAMPING, (int, float))
        self.assertGreater(SPRING_DAMPING, 0)
        self.assertLessEqual(SPRING_DAMPING, 1.0)

        # 验证频率
        self.assertIsInstance(SPRING_FREQUENCY, (int, float))
        self.assertGreater(SPRING_FREQUENCY, 0)
        self.assertLessEqual(SPRING_FREQUENCY, 10.0)  # 合理范围

        # 验证弹簧参数值
        self.assertEqual(SPRING_DAMPING, 0.75)
        self.assertEqual(SPRING_FREQUENCY, 2.5)

    def test_spring_animation_function(self):
        """测试弹簧动画函数"""
        from src.utils import ease_out_spring

        # 测试边界值
        self.assertAlmostEqual(ease_out_spring(0), 0, places=3)
        self.assertAlmostEqual(ease_out_spring(1), 1, places=1)  # 允许回弹

        # 测试中间值（应该有弹簧效果）
        mid_result = ease_out_spring(0.5)
        self.assertGreater(mid_result, 0)  # 应该大于0
        self.assertLess(mid_result, 1.5)  # 不应过大


class TestIOSBoardConfigAcceptance(unittest.TestCase):
    """iOS棋盘配置验收测试"""

    def test_board_dimensions(self):
        """测试棋盘尺寸配置"""
        # 验证棋盘大小
        self.assertEqual(BOARD_SIZE, 4)  # 2048标准4x4棋盘

        # 验证尺寸类型和范围
        self.assertIsInstance(TILE_SIZE, int)
        self.assertGreater(TILE_SIZE, 50)
        self.assertLess(TILE_SIZE, 150)

        self.assertIsInstance(TILE_GAP, int)
        self.assertGreater(TILE_GAP, 5)
        self.assertLess(TILE_GAP, 30)

        self.assertIsInstance(BOARD_PADDING, int)
        self.assertGreater(BOARD_PADDING, 0)

        # 验证iOS优化值
        self.assertEqual(TILE_SIZE, 90)
        self.assertEqual(TILE_GAP, 12)
        self.assertEqual(BOARD_PADDING, 16)  # 优化为8pt网格对齐

    def test_board_position(self):
        """测试棋盘位置计算"""
        # 验证棋盘居中计算
        expected_x = (WINDOW_WIDTH - (TILE_SIZE * BOARD_SIZE + TILE_GAP * (BOARD_SIZE - 1))) // 2
        self.assertEqual(BOARD_X, expected_x)


class TestIOSSpacingConfigAcceptance(unittest.TestCase):
    """iOS间距配置验收测试"""

    def test_spacing_tokens(self):
        """测试间距令牌"""
        # 验证基础间距单位
        self.assertEqual(IOS_SPACING_BASE, 8)

        # 验证间距值
        self.assertEqual(IOS_SPACING_XXS, 2)
        self.assertEqual(IOS_SPACING_XS, 4)
        self.assertEqual(IOS_SPACING_SM, 8)
        self.assertEqual(IOS_SPACING_MD, 16)
        self.assertEqual(IOS_SPACING_LG, 24)
        self.assertEqual(IOS_SPACING_XL, 32)
        self.assertEqual(IOS_SPACING_XXL, 40)
        self.assertEqual(IOS_SPACING_XXXL, 48)

        # 验证递增关系
        self.assertLess(IOS_SPACING_XXS, IOS_SPACING_XS)
        self.assertLess(IOS_SPACING_XS, IOS_SPACING_SM)
        self.assertLess(IOS_SPACING_SM, IOS_SPACING_MD)
        self.assertLess(IOS_SPACING_MD, IOS_SPACING_LG)
        self.assertLess(IOS_SPACING_LG, IOS_SPACING_XL)
        self.assertLess(IOS_SPACING_XL, IOS_SPACING_XXL)
        self.assertLess(IOS_SPACING_XXL, IOS_SPACING_XXXL)

    def test_legacy_spacing_compatibility(self):
        """测试旧接口兼容性"""
        self.assertEqual(SPACING_TINY, IOS_SPACING_XS)
        self.assertEqual(SPACING_SMALL, IOS_SPACING_SM)
        self.assertEqual(SPACING_MEDIUM, IOS_SPACING_MD)
        self.assertEqual(SPACING_LARGE, IOS_SPACING_LG)
        self.assertEqual(SPACING_HUGE, IOS_SPACING_XL)


class TestIOSGameConfigAcceptance(unittest.TestCase):
    """iOS游戏配置验收测试"""

    def test_game_parameters(self):
        """测试游戏参数"""
        self.assertEqual(INITIAL_TILES, 2)
        self.assertEqual(WIN_TILE, 2048)
        self.assertGreater(UNDO_LIMIT_DEFAULT, 0)
        self.assertGreater(CLEAN_LIMIT_DEFAULT, 0)

    def test_mode_config(self):
        """测试游戏模式配置"""
        required_modes = ["classic", "timed", "challenge"]
        for mode in required_modes:
            self.assertIn(mode, MODE_CONFIG, f"缺少游戏模式: {mode}")
            config = MODE_CONFIG[mode]
            self.assertIn("name", config, f"模式 {mode} 缺少名称")
            self.assertIn("description", config, f"模式 {mode} 缺少描述")
            self.assertIn("icon", config, f"模式 {mode} 缺少图标")


class TestIOSUIComponentsAcceptance(unittest.TestCase):
    """iOS UI组件验收测试"""

    def test_button_component_import(self):
        """测试Button组件导入"""
        from src.views.ui_components import Button
        self.assertTrue(hasattr(Button, '__init__'))
        self.assertTrue(hasattr(Button, 'draw'))
        self.assertTrue(hasattr(Button, 'handle_event'))

    def test_panel_component_import(self):
        """测试Panel组件导入"""
        from src.views.ui_components import Panel
        self.assertTrue(hasattr(Panel, '__init__'))
        self.assertTrue(hasattr(Panel, 'draw'))

    def test_scorebox_component_import(self):
        """测试ScoreBox组件导入"""
        from src.views.ui_components import ScoreBox
        self.assertTrue(hasattr(ScoreBox, '__init__'))
        self.assertTrue(hasattr(ScoreBox, 'draw'))
        self.assertTrue(hasattr(ScoreBox, 'set_value'))

    def test_ios_alert_component_import(self):
        """测试iOSAlert组件导入"""
        from src.views.ui_components import iOSAlert
        self.assertTrue(hasattr(iOSAlert, '__init__'))
        self.assertTrue(hasattr(iOSAlert, 'show'))
        self.assertTrue(hasattr(iOSAlert, 'hide'))


class TestIOSUtilsAcceptance(unittest.TestCase):
    """iOS工具函数验收测试"""

    def test_draw_shadow_function(self):
        """测试阴影绘制函数"""
        from src.utils import draw_shadow
        self.assertTrue(callable(draw_shadow))

    def test_ease_out_spring_function(self):
        """测试弹簧动画函数"""
        from src.utils import ease_out_spring
        self.assertTrue(callable(ease_out_spring))

    def test_draw_rounded_rect_function(self):
        """测试圆角矩形绘制函数"""
        from src.utils import draw_rounded_rect
        self.assertTrue(callable(draw_rounded_rect))

    def test_font_manager(self):
        """测试字体管理器"""
        from src.utils import get_font_manager, FontManager
        fm = get_font_manager()
        self.assertIsInstance(fm, FontManager)
        self.assertTrue(hasattr(fm, 'get_font'))
        self.assertTrue(hasattr(fm, 'get_large'))
        self.assertTrue(hasattr(fm, 'get_medium'))
        self.assertTrue(hasattr(fm, 'get_small'))


class TestIOSVisualRenderingAcceptance(unittest.TestCase):
    """iOS视觉渲染验收测试"""

    def setUp(self):
        """测试初始化"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def tearDown(self):
        """测试清理"""
        pygame.quit()

    def test_background_rendering(self):
        """测试背景渲染"""
        from src.utils import draw_rounded_rect

        # 清屏
        self.screen.fill(COLOR_BG)

        # 绘制棋盘背景
        board_rect = pygame.Rect(BOARD_X, BOARD_Y,
                                 TILE_SIZE * BOARD_SIZE + TILE_GAP * (BOARD_SIZE - 1) + BOARD_PADDING * 2,
                                 TILE_SIZE * BOARD_SIZE + TILE_GAP * (BOARD_SIZE - 1) + BOARD_PADDING * 2)
        draw_rounded_rect(self.screen, COLOR_BOARD_BG, board_rect, RADIUS_MD)

        # 验证渲染成功（无异常）
        pygame.display.flip()

    def test_tile_rendering(self):
        """测试方块渲染"""
        from src.utils import draw_rounded_rect, draw_text_centered, get_font_manager

        # 绘制测试方块
        tile_rect = pygame.Rect(100, 100, TILE_SIZE, TILE_SIZE)
        bg_color, text_color = TILE_COLORS[2]

        draw_rounded_rect(self.screen, bg_color, tile_rect, 10)
        font = get_font_manager().get_font(TILE_FONT_SIZES[2], bold=True)
        draw_text_centered(self.screen, "2", font, text_color, tile_rect.center)

        # 验证渲染成功
        pygame.display.flip()

    def test_button_rendering(self):
        """测试按钮渲染"""
        from src.views.ui_components import Button

        # 创建测试按钮
        btn = Button(100, 100, 200, 50, "测试按钮",
                     color=COLOR_BTN_PRIMARY,
                     hover_color=COLOR_BTN_PRIMARY_HOVER)

        # 绘制按钮
        btn.draw(self.screen)

        # 验证渲染成功
        pygame.display.flip()

    def test_panel_rendering(self):
        """测试面板渲染"""
        from src.views.ui_components import Panel

        # 创建测试面板
        panel = Panel(100, 100, 300, 200,
                      color=(255, 255, 255),
                      radius=RADIUS_LG)

        # 绘制面板
        panel.draw(self.screen)

        # 验证渲染成功
        pygame.display.flip()


if __name__ == "__main__":
    unittest.main()
