# -*- coding: utf-8 -*-
# @Function: iOS风格改造详细测试用例

import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestIOSColorSystem(unittest.TestCase):
    """iOS颜色系统测试"""

    def test_background_colors(self):
        """测试背景颜色配置"""
        from src.config import COLOR_BG, COLOR_BOARD_BG, COLOR_TILE_EMPTY

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

    def test_tile_colors(self):
        """测试方块颜色配置"""
        from src.config import TILE_COLORS

        # 验证所有必需的方块值都有对应的颜色
        required_values = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
        for value in required_values:
            self.assertIn(value, TILE_COLORS, f"方块值 {value} 缺少颜色配置")
            bg_color, text_color = TILE_COLORS[value]
            self.assertEqual(len(bg_color), 3, f"方块 {value} 背景颜色格式错误")
            self.assertEqual(len(text_color), 3, f"方块 {value} 文字颜色格式错误")

    def test_ui_colors(self):
        """测试UI颜色配置"""
        from src.config import (COLOR_TEXT, COLOR_TEXT_SECONDARY, COLOR_TEXT_TERTIARY,
                               COLOR_BTN_PRIMARY, COLOR_BTN_PRIMARY_HOVER,
                               COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
                               COLOR_BTN_DANGER, COLOR_BTN_DANGER_HOVER)

        ui_colors = [
            COLOR_TEXT, COLOR_TEXT_SECONDARY, COLOR_TEXT_TERTIARY,
            COLOR_BTN_PRIMARY, COLOR_BTN_PRIMARY_HOVER,
            COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
            COLOR_BTN_DANGER, COLOR_BTN_DANGER_HOVER
        ]

        for color in ui_colors:
            self.assertIsInstance(color, tuple)
            self.assertEqual(len(color), 3)
            for value in color:
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, 255)


class TestIOSFontSystem(unittest.TestCase):
    """iOS字号系统测试"""

    def test_ios_font_sizes(self):
        """测试iOS标准字号"""
        from src.config import (FONT_SIZE_CAPTION2, FONT_SIZE_CAPTION1,
                               FONT_SIZE_FOOTNOTE, FONT_SIZE_SUBHEAD,
                               FONT_SIZE_BODY, FONT_SIZE_TITLE3,
                               FONT_SIZE_TITLE2, FONT_SIZE_TITLE1,
                               FONT_SIZE_LARGE_TITLE)

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

    def test_legacy_font_compatibility(self):
        """测试旧接口兼容性"""
        from src.config import (FONT_SIZE_LARGE, FONT_SIZE_MEDIUM,
                               FONT_SIZE_SMALL, FONT_SIZE_TINY)
        from src.config import (FONT_SIZE_LARGE_TITLE, FONT_SIZE_BODY,
                               FONT_SIZE_FOOTNOTE, FONT_SIZE_CAPTION1)

        # 验证兼容性映射
        self.assertEqual(FONT_SIZE_LARGE, FONT_SIZE_LARGE_TITLE)
        self.assertEqual(FONT_SIZE_MEDIUM, FONT_SIZE_BODY)
        self.assertEqual(FONT_SIZE_SMALL, FONT_SIZE_FOOTNOTE)
        self.assertEqual(FONT_SIZE_TINY, FONT_SIZE_CAPTION1)

    def test_tile_font_sizes(self):
        """测试方块数字字号映射"""
        from src.config import TILE_FONT_SIZES

        required_values = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
        for value in required_values:
            self.assertIn(value, TILE_FONT_SIZES, f"方块值 {value} 缺少字号配置")
            self.assertIsInstance(TILE_FONT_SIZES[value], int)
            self.assertGreater(TILE_FONT_SIZES[value], 0)


class TestIOSRadiusConfig(unittest.TestCase):
    """iOS圆角配置测试"""

    def test_radius_tokens(self):
        """测试圆角令牌"""
        from src.config import RADIUS_SM, RADIUS_MD, RADIUS_LG, RADIUS_XL

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


class TestIOSAnimationConfig(unittest.TestCase):
    """iOS动画配置测试"""

    def test_animation_durations(self):
        """测试动画时长配置"""
        from src.config import (ANIMATION_MOVE_DURATION, ANIMATION_MERGE_DURATION,
                               ANIMATION_SPAWN_DURATION, ANIMATION_FADE_DURATION)

        durations = [
            ANIMATION_MOVE_DURATION, ANIMATION_MERGE_DURATION,
            ANIMATION_SPAWN_DURATION, ANIMATION_FADE_DURATION
        ]

        for duration in durations:
            self.assertIsInstance(duration, int)
            self.assertGreater(duration, 0)
            self.assertLessEqual(duration, 1000)  # 合理范围（毫秒）

    def test_spring_animation_params(self):
        """测试弹簧动画参数"""
        from src.config import SPRING_DAMPING, SPRING_FREQUENCY

        # 验证阻尼系数
        self.assertIsInstance(SPRING_DAMPING, (int, float))
        self.assertGreater(SPRING_DAMPING, 0)
        self.assertLessEqual(SPRING_DAMPING, 1.0)

        # 验证频率
        self.assertIsInstance(SPRING_FREQUENCY, (int, float))
        self.assertGreater(SPRING_FREQUENCY, 0)
        self.assertLessEqual(SPRING_FREQUENCY, 10.0)  # 合理范围


class TestIOSBoardConfig(unittest.TestCase):
    """iOS棋盘配置测试"""

    def test_board_dimensions(self):
        """测试棋盘尺寸配置"""
        from src.config import BOARD_SIZE, TILE_SIZE, TILE_GAP, BOARD_PADDING

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

    def test_board_position(self):
        """测试棋盘位置计算"""
        from src.config import WINDOW_WIDTH, BOARD_SIZE, TILE_SIZE, TILE_GAP, BOARD_X

        # 验证棋盘居中计算
        expected_x = (WINDOW_WIDTH - (TILE_SIZE * BOARD_SIZE + TILE_GAP * (BOARD_SIZE - 1))) // 2
        self.assertEqual(BOARD_X, expected_x)


class TestIOSGameConfig(unittest.TestCase):
    """iOS游戏配置测试"""

    def test_game_parameters(self):
        """测试游戏参数"""
        from src.config import INITIAL_TILES, WIN_TILE, UNDO_LIMIT_DEFAULT, CLEAN_LIMIT_DEFAULT

        self.assertEqual(INITIAL_TILES, 2)
        self.assertEqual(WIN_TILE, 2048)
        self.assertGreater(UNDO_LIMIT_DEFAULT, 0)
        self.assertGreater(CLEAN_LIMIT_DEFAULT, 0)

    def test_mode_config(self):
        """测试游戏模式配置"""
        from src.config import MODE_CONFIG

        required_modes = ["classic", "timed", "challenge"]
        for mode in required_modes:
            self.assertIn(mode, MODE_CONFIG, f"缺少游戏模式: {mode}")
            config = MODE_CONFIG[mode]
            self.assertIn("name", config, f"模式 {mode} 缺少名称")
            self.assertIn("description", config, f"模式 {mode} 缺少描述")
            self.assertIn("icon", config, f"模式 {mode} 缺少图标")


class TestIOSDataConfig(unittest.TestCase):
    """iOS数据配置测试"""

    def test_data_paths(self):
        """测试数据存储路径"""
        from src.config import DATA_DIR, DATA_FILE
        import os

        # 验证路径类型
        self.assertIsInstance(DATA_DIR, str)
        self.assertIsInstance(DATA_FILE, str)

        # 验证路径包含AppData
        self.assertIn("AppData", DATA_DIR)
        self.assertIn("2048_Game", DATA_DIR)

        # 验证文件扩展名
        self.assertTrue(DATA_FILE.endswith(".json"))


if __name__ == "__main__":
    unittest.main()