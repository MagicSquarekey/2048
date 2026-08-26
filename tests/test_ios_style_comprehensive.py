# -*- coding: utf-8 -*-
# @Function: iOS风格改造综合测试 - Step 5 测试验收
# 测试工程师: 覆盖颜色系统、字体系统、动画参数、圆角阴影、UI组件、配置验证

import os
import sys
import math
import time
import unittest

# 设置 pygame 使用 dummy 视频驱动（无头模式）
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
pygame.init()
screen = pygame.display.set_mode((1, 1))

from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS,
    BOARD_SIZE, TILE_SIZE, TILE_GAP, BOARD_PADDING, BOARD_X, BOARD_Y,
    COLOR_BG, COLOR_BOARD_BG, COLOR_TILE_EMPTY, TILE_COLORS,
    COLOR_TEXT, COLOR_TEXT_SECONDARY, COLOR_TEXT_TERTIARY, COLOR_TEXT_LIGHT,
    COLOR_BTN_PRIMARY, COLOR_BTN_PRIMARY_HOVER,
    COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
    COLOR_BTN_DANGER, COLOR_BTN_DANGER_HOVER,
    COLOR_GREEN, COLOR_ORANGE,
    COLOR_SCORE_BG, COLOR_OVERLAY,
    SWIPE_THRESHOLD,
    INITIAL_TILES, WIN_TILE, UNDO_LIMIT_DEFAULT, CLEAN_LIMIT_DEFAULT,
    TILE_2_PROBABILITY,
    SCORE_MULTIPLIERS,
    MODE_CONFIG,
    ANIMATION_MOVE_DURATION, ANIMATION_MERGE_DURATION,
    ANIMATION_SPAWN_DURATION, ANIMATION_FADE_DURATION,
    SPRING_DAMPING, SPRING_FREQUENCY,
    FONT_PATH,
    FONT_SIZE_CAPTION2, FONT_SIZE_CAPTION1, FONT_SIZE_FOOTNOTE,
    FONT_SIZE_SUBHEAD, FONT_SIZE_BODY,
    FONT_SIZE_TITLE3, FONT_SIZE_TITLE2, FONT_SIZE_TITLE1, FONT_SIZE_LARGE_TITLE,
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL, FONT_SIZE_TINY,
    TILE_FONT_SIZES,
    RADIUS_SM, RADIUS_MD, RADIUS_LG, RADIUS_XL,
    FREE_DAILY_LIMIT, AD_REWARD_AMOUNT, AD_COOLDOWN,
    DATA_DIR, DATA_FILE,
)
from src.utils import (
    ease_out_spring, ease_out_cubic, ease_in_out_cubic, ease_out_back,
    lerp, clamp, format_score, format_time, get_tile_color,
    FontManager, draw_rounded_rect, draw_shadow,
)
from src.views.ui_components import Button, Label, Panel, ScoreBox, iOSAlert
from src.views.pages.base_page import Page, PageManager


# ============================================================
# 辅助函数
# ============================================================

def is_valid_rgb(color):
    """验证颜色是否为有效 RGB 元组"""
    if not isinstance(color, tuple):
        return False
    if len(color) not in (3, 4):
        return False
    return all(0 <= c <= 255 for c in color)


def is_light_color(color):
    """判断颜色是否为浅色（亮度 > 128）"""
    return sum(color[:3]) / 3 > 128


def color_distance(c1, c2):
    """计算两个 RGB 颜色的欧几里得距离"""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1[:3], c2[:3])))


# ============================================================
# TC-001: iOS 颜色系统验证
# ============================================================

class TestiOSColorSystem(unittest.TestCase):
    """iOS 颜色系统 - 验证所有颜色常量符合 Apple HIG"""

    def test_bg_color_is_ios_gray6(self):
        """TC-001.01: 背景色应为 iOS System Gray 6 (约 242,242,247)"""
        self.assertTrue(is_valid_rgb(COLOR_BG))
        r, g, b = COLOR_BG
        self.assertGreaterEqual(r, 235, "背景色R值应 ≥ 235 (iOS Gray 6)")
        self.assertGreaterEqual(g, 235, "背景色G值应 ≥ 235 (iOS Gray 6)")
        self.assertGreaterEqual(b, 235, "背景色B值应 ≥ 235 (iOS Gray 6)")

    def test_board_bg_is_white(self):
        """TC-001.02: 棋盘背景应为纯白"""
        self.assertTrue(is_valid_rgb(COLOR_BOARD_BG))
        self.assertEqual(COLOR_BOARD_BG, (255, 255, 255))

    def test_tile_empty_color_exists(self):
        """TC-001.03: 空格颜色存在且有效"""
        self.assertTrue(is_valid_rgb(COLOR_TILE_EMPTY))

    def test_all_tile_colors_defined(self):
        """TC-001.04: 所有 2-2048 方块颜色定义完整"""
        required_values = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
        for value in required_values:
            self.assertIn(value, TILE_COLORS, f"缺少方块 {value} 的颜色定义")
            bg, text = TILE_COLORS[value]
            self.assertTrue(is_valid_rgb(bg), f"方块 {value} 背景色无效")
            self.assertTrue(is_valid_rgb(text), f"方块 {value} 文字色无效")

    def test_tile_colors_contrast(self):
        """TC-001.05: 方块背景色与文字色应有足够对比度"""
        for value, (bg, text) in TILE_COLORS.items():
            dist = color_distance(bg, text)
            self.assertGreater(dist, 80,
                f"方块 {value} 背景色与文字色对比度不足 (距离={dist:.1f})")

    def test_text_colors_valid(self):
        """TC-001.06: 文字颜色系统有效"""
        self.assertTrue(is_valid_rgb(COLOR_TEXT))
        self.assertTrue(is_valid_rgb(COLOR_TEXT_SECONDARY))
        self.assertTrue(is_valid_rgb(COLOR_TEXT_TERTIARY))
        self.assertTrue(is_valid_rgb(COLOR_TEXT_LIGHT))

    def test_button_colors_valid(self):
        """TC-001.07: 按钮颜色系统有效"""
        self.assertTrue(is_valid_rgb(COLOR_BTN_PRIMARY))
        self.assertTrue(is_valid_rgb(COLOR_BTN_PRIMARY_HOVER))
        self.assertTrue(is_valid_rgb(COLOR_BTN_SECONDARY))
        self.assertTrue(is_valid_rgb(COLOR_BTN_SECONDARY_HOVER))
        self.assertTrue(is_valid_rgb(COLOR_BTN_DANGER))
        self.assertTrue(is_valid_rgb(COLOR_BTN_DANGER_HOVER))

    def test_primary_button_is_ios_blue(self):
        """TC-001.08: 主按钮应为 iOS Blue (0,122,255)"""
        self.assertEqual(COLOR_BTN_PRIMARY, (0, 122, 255))

    def test_danger_button_is_ios_red(self):
        """TC-001.09: 危险按钮应为 iOS Red (255,59,48)"""
        self.assertEqual(COLOR_BTN_DANGER, (255, 59, 48))

    def test_green_is_ios_green(self):
        """TC-001.10: 绿色应为 iOS Green (52,199,89)"""
        self.assertEqual(COLOR_GREEN, (52, 199, 89))

    def test_overlay_is_translucent(self):
        """TC-001.11: 遮罩应为半透明"""
        self.assertEqual(len(COLOR_OVERLAY), 4, "遮罩应为 RGBA 格式")
        self.assertLess(COLOR_OVERLAY[3], 100, "遮罩透明度应较低 (半透明)")

    def test_score_bg_color_distinct(self):
        """TC-001.12: 分数背景色应与页面背景区分"""
        dist = color_distance(COLOR_SCORE_BG, COLOR_BG)
        self.assertGreater(dist, 5, "分数背景色应与页面背景区分")


# ============================================================
# TC-002: iOS 字号系统验证（8pt 网格）
# ============================================================

class TestiOSTypographySystem(unittest.TestCase):
    """iOS 字号系统 - 验证 8pt 网格体系"""

    def test_font_size_caption2(self):
        """TC-002.01: Caption2 = 11pt"""
        self.assertEqual(FONT_SIZE_CAPTION2, 11)

    def test_font_size_caption1(self):
        """TC-002.02: Caption1 = 12pt"""
        self.assertEqual(FONT_SIZE_CAPTION1, 12)

    def test_font_size_footnote(self):
        """TC-002.03: Footnote = 13pt"""
        self.assertEqual(FONT_SIZE_FOOTNOTE, 13)

    def test_font_size_subhead(self):
        """TC-002.04: Subhead = 15pt"""
        self.assertEqual(FONT_SIZE_SUBHEAD, 15)

    def test_font_size_body(self):
        """TC-002.05: Body = 17pt"""
        self.assertEqual(FONT_SIZE_BODY, 17)

    def test_font_size_title3(self):
        """TC-002.06: Title 3 = 20pt"""
        self.assertEqual(FONT_SIZE_TITLE3, 20)

    def test_font_size_title2(self):
        """TC-002.07: Title 2 = 22pt"""
        self.assertEqual(FONT_SIZE_TITLE2, 22)

    def test_font_size_title1(self):
        """TC-002.08: Title 1 = 28pt"""
        self.assertEqual(FONT_SIZE_TITLE1, 28)

    def test_font_size_large_title(self):
        """TC-002.09: Large Title = 34pt"""
        self.assertEqual(FONT_SIZE_LARGE_TITLE, 34)

    def test_font_size_hierarchy_ordering(self):
        """TC-002.10: 字号层级有序递增"""
        sizes = [
            FONT_SIZE_CAPTION2, FONT_SIZE_CAPTION1, FONT_SIZE_FOOTNOTE,
            FONT_SIZE_SUBHEAD, FONT_SIZE_BODY,
            FONT_SIZE_TITLE3, FONT_SIZE_TITLE2, FONT_SIZE_TITLE1,
            FONT_SIZE_LARGE_TITLE,
        ]
        for i in range(1, len(sizes)):
            self.assertGreater(sizes[i], sizes[i-1],
                f"字号层级 {i-1} 到 {i} 应递增")

    def test_compatibility_aliases(self):
        """TC-002.11: 兼容旧接口别名正确"""
        self.assertEqual(FONT_SIZE_LARGE, FONT_SIZE_LARGE_TITLE)
        self.assertEqual(FONT_SIZE_MEDIUM, FONT_SIZE_BODY)
        self.assertEqual(FONT_SIZE_SMALL, FONT_SIZE_FOOTNOTE)
        self.assertEqual(FONT_SIZE_TINY, FONT_SIZE_CAPTION1)

    def test_tile_font_sizes_mapping(self):
        """TC-002.12: 方块数字字号映射完整"""
        required = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
        for value in required:
            self.assertIn(value, TILE_FONT_SIZES, f"缺少方块 {value} 的字号映射")
            size = TILE_FONT_SIZES[value]
            self.assertGreater(size, 0, f"方块 {value} 字号应 > 0")
            self.assertLessEqual(size, 40, f"方块 {value} 字号应 ≤ 40")

    def test_tile_font_decreases_for_large_numbers(self):
        """TC-002.13: 大数字方块字号应更小（避免溢出）"""
        self.assertGreater(TILE_FONT_SIZES[2], TILE_FONT_SIZES[2048])

    def test_font_path_exists(self):
        """TC-002.14: 字体文件存在"""
        if FONT_PATH is not None:
            self.assertTrue(os.path.exists(FONT_PATH),
                f"字体文件不存在: {FONT_PATH}")


# ============================================================
# TC-003: iOS 动画参数验证
# ============================================================

class TestiOSAnimationSystem(unittest.TestCase):
    """iOS 动画系统 - 验证弹簧动画参数"""

    def test_move_duration_reasonable(self):
        """TC-003.01: 移动动画时长 150-400ms"""
        self.assertGreaterEqual(ANIMATION_MOVE_DURATION, 150)
        self.assertLessEqual(ANIMATION_MOVE_DURATION, 400)

    def test_merge_duration_reasonable(self):
        """TC-003.02: 合并动画时长 150-400ms"""
        self.assertGreaterEqual(ANIMATION_MERGE_DURATION, 150)
        self.assertLessEqual(ANIMATION_MERGE_DURATION, 400)

    def test_spawn_duration_reasonable(self):
        """TC-003.03: 生成动画时长 100-350ms"""
        self.assertGreaterEqual(ANIMATION_SPAWN_DURATION, 100)
        self.assertLessEqual(ANIMATION_SPAWN_DURATION, 350)

    def test_fade_duration_reasonable(self):
        """TC-003.04: 淡入淡出动画时长 200-500ms"""
        self.assertGreaterEqual(ANIMATION_FADE_DURATION, 200)
        self.assertLessEqual(ANIMATION_FADE_DURATION, 500)

    def test_spring_damping(self):
        """TC-003.05: 弹簧阻尼系数 0.5-0.9 (iOS 标准约 0.7-0.8)"""
        self.assertGreaterEqual(SPRING_DAMPING, 0.5)
        self.assertLessEqual(SPRING_DAMPING, 0.9)

    def test_spring_frequency(self):
        """TC-003.06: 弹簧频率 1.5-3.5"""
        self.assertGreaterEqual(SPRING_FREQUENCY, 1.5)
        self.assertLessEqual(SPRING_FREQUENCY, 3.5)

    def test_spring_animation_at_t0(self):
        """TC-003.07: 弹簧动画 t=0 时应接近 0"""
        val = ease_out_spring(0.0)
        self.assertAlmostEqual(val, 0.0, delta=0.15)

    def test_spring_animation_at_t1(self):
        """TC-003.08: 弹簧动画 t=1 时应接近 1"""
        val = ease_out_spring(1.0)
        self.assertAlmostEqual(val, 1.0, delta=0.15)

    def test_spring_animation_monotonic_region(self):
        """TC-003.09: 弹簧动画在 t=0.3~0.8 区间应持续增长"""
        prev = ease_out_spring(0.3)
        for t_val in [0.4, 0.5, 0.6, 0.7, 0.8]:
            current = ease_out_spring(t_val)
            self.assertGreaterEqual(current, prev - 0.05,
                f"弹簧动画在 t={t_val} 处不应大幅下降")
            prev = current

    def test_ease_out_cubic_at_endpoints(self):
        """TC-003.10: 缓出三次方曲线端点正确"""
        self.assertAlmostEqual(ease_out_cubic(0.0), 0.0, delta=0.01)
        self.assertAlmostEqual(ease_out_cubic(1.0), 1.0, delta=0.01)

    def test_ease_in_out_cubic_at_endpoints(self):
        """TC-003.11: 缓入缓出三次方曲线端点正确"""
        self.assertAlmostEqual(ease_in_out_cubic(0.0), 0.0, delta=0.01)
        self.assertAlmostEqual(ease_in_out_cubic(1.0), 1.0, delta=0.01)

    def test_ease_out_back_overshoot(self):
        """TC-003.12: 弹性缓出应有超调效果"""
        # ease_out_back 在 t=0.7 附近应 > 1.0 (超调)
        max_val = max(ease_out_back(t / 100) for t in range(60, 90))
        self.assertGreater(max_val, 1.0, "弹性缓出应有超调效果")


# ============================================================
# TC-004: iOS 圆角系统验证
# ============================================================

class TestiOSCornerRadiusSystem(unittest.TestCase):
    """iOS 圆角系统 - 验证圆角值配置"""

    def test_radius_sm(self):
        """TC-004.01: 小圆角 = 8"""
        self.assertEqual(RADIUS_SM, 8)

    def test_radius_md(self):
        """TC-004.02: 中圆角 = 12"""
        self.assertEqual(RADIUS_MD, 12)

    def test_radius_lg(self):
        """TC-004.03: 大圆角 = 16"""
        self.assertEqual(RADIUS_LG, 16)

    def test_radius_xl(self):
        """TC-004.04: 棋盘圆角 = 20"""
        self.assertEqual(RADIUS_XL, 20)

    def test_radius_ordering(self):
        """TC-004.05: 圆角值有序递增"""
        self.assertLess(RADIUS_SM, RADIUS_MD)
        self.assertLess(RADIUS_MD, RADIUS_LG)
        self.assertLess(RADIUS_LG, RADIUS_XL)

    def test_radius_positive(self):
        """TC-004.06: 所有圆角值为正数"""
        self.assertGreater(RADIUS_SM, 0)
        self.assertGreater(RADIUS_MD, 0)
        self.assertGreater(RADIUS_LG, 0)
        self.assertGreater(RADIUS_XL, 0)


# ============================================================
# TC-005: 游戏配置验证
# ============================================================

class TestGameConfig(unittest.TestCase):
    """游戏配置 - 验证参数正确性和合理性"""

    def test_window_title(self):
        """TC-005.01: 窗口标题"""
        self.assertEqual(WINDOW_TITLE, "2048")

    def test_window_size(self):
        """TC-005.02: 窗口尺寸合理"""
        self.assertEqual(WINDOW_WIDTH, 800)
        self.assertEqual(WINDOW_HEIGHT, 600)

    def test_fps(self):
        """TC-005.03: 帧率 = 60"""
        self.assertEqual(FPS, 60)

    def test_board_size_4x4(self):
        """TC-005.04: 棋盘为 4x4"""
        self.assertEqual(BOARD_SIZE, 4)

    def test_tile_size_positive(self):
        """TC-005.05: 方块尺寸 > 0"""
        self.assertGreater(TILE_SIZE, 0)

    def test_tile_gap_positive(self):
        """TC-005.06: 方块间距 > 0"""
        self.assertGreater(TILE_GAP, 0)

    def test_board_centered(self):
        """TC-005.07: 棋盘水平居中"""
        expected_x = (WINDOW_WIDTH - (TILE_SIZE * BOARD_SIZE + TILE_GAP * (BOARD_SIZE - 1))) // 2
        self.assertEqual(BOARD_X, expected_x)

    def test_initial_tiles_count(self):
        """TC-005.08: 初始方块 = 2"""
        self.assertEqual(INITIAL_TILES, 2)

    def test_win_tile_value(self):
        """TC-005.09: 胜利方块 = 2048"""
        self.assertEqual(WIN_TILE, 2048)

    def test_undo_limit(self):
        """TC-005.10: 撤销次数限制"""
        self.assertEqual(UNDO_LIMIT_DEFAULT, 3)

    def test_clean_limit(self):
        """TC-005.11: 清理次数限制"""
        self.assertEqual(CLEAN_LIMIT_DEFAULT, 1)

    def test_tile_2_probability(self):
        """TC-005.12: 方块2生成概率 80-95%"""
        self.assertGreaterEqual(TILE_2_PROBABILITY, 0.8)
        self.assertLessEqual(TILE_2_PROBABILITY, 0.95)

    def test_score_multipliers(self):
        """TC-005.13: 分数倍率配置完整"""
        self.assertIn("classic", SCORE_MULTIPLIERS)
        self.assertIn("timed", SCORE_MULTIPLIERS)
        self.assertIn("challenge", SCORE_MULTIPLIERS)
        self.assertGreater(SCORE_MULTIPLIERS["classic"], 0)
        self.assertGreater(SCORE_MULTIPLIERS["timed"], SCORE_MULTIPLIERS["classic"])
        self.assertGreater(SCORE_MULTIPLIERS["challenge"], SCORE_MULTIPLIERS["classic"])

    def test_mode_config_complete(self):
        """TC-005.14: 游戏模式配置完整"""
        for mode in ["classic", "timed", "challenge"]:
            self.assertIn(mode, MODE_CONFIG)
            cfg = MODE_CONFIG[mode]
            self.assertIn("name", cfg)
            self.assertIn("description", cfg)
            self.assertIn("icon", cfg)

    def test_data_dir_created(self):
        """TC-005.15: 数据目录已创建"""
        self.assertTrue(os.path.isdir(DATA_DIR), f"数据目录不存在: {DATA_DIR}")

    def test_swipe_threshold(self):
        """TC-005.16: 滑动阈值合理"""
        self.assertGreater(SWIPE_THRESHOLD, 10)
        self.assertLess(SWIPE_THRESHOLD, 100)

    def test_free_daily_limit(self):
        """TC-005.17: 每日免费次数 > 0"""
        self.assertGreater(FREE_DAILY_LIMIT, 0)

    def test_ad_cooldown(self):
        """TC-005.18: 广告冷却时间 > 0"""
        self.assertGreater(AD_COOLDOWN, 0)


# ============================================================
# TC-006: UI 组件测试
# ============================================================

class TestUIComponents(unittest.TestCase):
    """UI 组件 - 验证 iOS 风格组件正确性"""

    def setUp(self):
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    def test_button_creation(self):
        """TC-006.01: 按钮创建"""
        btn = Button(100, 100, 200, 50, "Test")
        self.assertEqual(btn.rect.x, 100)
        self.assertEqual(btn.rect.y, 100)
        self.assertEqual(btn.rect.width, 200)
        self.assertEqual(btn.rect.height, 50)
        self.assertEqual(btn.text, "Test")

    def test_button_default_style(self):
        """TC-006.02: 按钮默认 iOS 样式"""
        btn = Button(0, 0, 200, 50, "OK")
        self.assertEqual(btn.color, COLOR_BTN_PRIMARY)
        self.assertEqual(btn.hover_color, COLOR_BTN_PRIMARY_HOVER)
        self.assertEqual(btn.font_size, 17)  # iOS Body
        self.assertEqual(btn.radius, RADIUS_MD)  # iOS 中圆角
        self.assertTrue(btn.shadow)

    def test_button_draw_no_crash(self):
        """TC-006.03: 按钮绘制无异常"""
        btn = Button(100, 100, 200, 50, "Play")
        btn.draw(self.surface)
        pygame.display.flip()

    def test_button_disabled_state(self):
        """TC-006.04: 按钮禁用状态"""
        btn = Button(0, 0, 200, 50, "OK")
        btn.enabled = False
        self.assertFalse(btn.enabled)

    def test_button_hidden_state(self):
        """TC-006.05: 按钮隐藏状态"""
        btn = Button(0, 0, 200, 50, "OK")
        btn.visible = False
        self.assertFalse(btn.visible)

    def test_button_hover_state(self):
        """TC-006.06: 按钮悬停状态"""
        btn = Button(0, 0, 200, 50, "OK")
        self.assertFalse(btn.is_hovered)
        btn.is_hovered = True
        self.assertTrue(btn.is_hovered)

    def test_button_press_scale(self):
        """TC-006.07: 按钮按压缩放效果"""
        btn = Button(0, 0, 200, 50, "OK")
        self.assertEqual(btn._press_scale, 1.0)

    def test_button_callback(self):
        """TC-006.08: 按钮回调触发"""
        called = []
        btn = Button(0, 0, 200, 50, "OK", callback=lambda: called.append(True))
        btn.is_hovered = True
        btn.is_pressed = True
        event = pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(100, 25))
        result = btn.handle_event(event)
        self.assertTrue(result)
        self.assertEqual(len(called), 1)

    def test_button_no_event_when_disabled(self):
        """TC-006.09: 禁用按钮不响应事件"""
        called = []
        btn = Button(0, 0, 200, 50, "OK", callback=lambda: called.append(True))
        btn.enabled = False
        event = pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(100, 25))
        result = btn.handle_event(event)
        self.assertFalse(result)
        self.assertEqual(len(called), 0)

    def test_label_creation(self):
        """TC-006.10: 标签创建"""
        label = Label(100, 100, "Score")
        self.assertEqual(label.text, "Score")
        self.assertTrue(label.rect.width > 0)
        self.assertTrue(label.rect.height > 0)

    def test_label_default_style(self):
        """TC-006.11: 标签默认 iOS 样式"""
        label = Label(0, 0, "Score")
        self.assertEqual(label.font_size, 17)  # iOS Body
        self.assertEqual(label.color, COLOR_TEXT)

    def test_label_set_text(self):
        """TC-006.12: 标签更新文本"""
        label = Label(0, 0, "Score: 0")
        old_w = label.rect.width
        label.set_text("Score: 100000")
        new_w = label.rect.width
        self.assertGreater(new_w, old_w)

    def test_label_draw_no_crash(self):
        """TC-006.13: 标签绘制无异常"""
        label = Label(100, 100, "Hello iOS")
        label.draw(self.surface)

    def test_panel_creation(self):
        """TC-006.14: 面板创建"""
        panel = Panel(100, 100, 300, 200)
        self.assertEqual(panel.rect.width, 300)
        self.assertEqual(panel.rect.height, 200)

    def test_panel_default_style(self):
        """TC-006.15: 面板默认 iOS 样式"""
        panel = Panel(0, 0, 300, 200)
        self.assertEqual(panel.color, (255, 255, 255))  # 纯白
        self.assertEqual(panel.radius, RADIUS_LG)  # iOS 大圆角
        self.assertTrue(panel.shadow)

    def test_panel_draw_no_crash(self):
        """TC-006.16: 面板绘制无异常"""
        panel = Panel(100, 100, 300, 200)
        panel.draw(self.surface)

    def test_scorebox_creation(self):
        """TC-006.17: 分数框创建"""
        sb = ScoreBox(100, 100, 120, 60, "SCORE", 42)
        self.assertEqual(sb.title, "SCORE")
        self.assertEqual(sb.value, 42)

    def test_scorebox_set_value(self):
        """TC-006.18: 分数框更新分数"""
        sb = ScoreBox(0, 0, 120, 60, "SCORE", 0)
        sb.set_value(100)
        self.assertEqual(sb._target_value, 100)
        self.assertTrue(sb._animating)

    def test_scorebox_animation_update(self):
        """TC-006.19: 分数框动画更新"""
        sb = ScoreBox(0, 0, 120, 60, "SCORE", 0)
        sb.set_value(100)
        for _ in range(100):
            sb.update(0.016)
        self.assertEqual(sb.value, 100)

    def test_scorebox_draw_no_crash(self):
        """TC-006.20: 分数框绘制无异常"""
        sb = ScoreBox(100, 100, 120, 60, "SCORE", 999)
        sb.draw(self.surface)

    def test_ios_alert_creation(self):
        """TC-006.21: iOS 弹窗创建"""
        alert = iOSAlert("提示", "确认退出？")
        self.assertEqual(alert.title, "提示")
        self.assertEqual(alert.message, "确认退出？")
        self.assertFalse(alert.is_visible)

    def test_ios_alert_show_hide(self):
        """TC-006.22: iOS 弹窗显示/隐藏"""
        alert = iOSAlert("标题", "内容")
        alert.show()
        self.assertTrue(alert.is_visible)
        alert.hide()
        self.assertFalse(alert.is_visible)

    def test_ios_alert_draw_no_crash(self):
        """TC-006.23: iOS 弹窗绘制无异常 (BUG-001 已修复)
        修复: iOSAlert.draw() 顶部添加了 from src.config import WINDOW_WIDTH, WINDOW_HEIGHT
        """
        alert = iOSAlert("提示", "确认退出？")
        alert.show()
        alert.draw(self.surface)  # 修复后不应再抛 NameError

    def test_ios_alert_confirm_callback(self):
        """TC-006.24: iOS 弹窗确认回调"""
        confirmed = []
        alert = iOSAlert("标题", "内容", on_confirm=lambda: confirmed.append(True))
        alert.show()
        alert._on_confirm()
        self.assertFalse(alert.is_visible)
        self.assertEqual(len(confirmed), 1)

    def test_ios_alert_cancel_callback(self):
        """TC-006.25: iOS 弹窗取消回调"""
        cancelled = []
        alert = iOSAlert("标题", "内容", on_cancel=lambda: cancelled.append(True))
        alert.show()
        alert._on_cancel()
        self.assertFalse(alert.is_visible)
        self.assertEqual(len(cancelled), 1)


# ============================================================
# TC-007: 棋盘视图渲染测试
# ============================================================

class TestBoardViewRendering(unittest.TestCase):
    """棋盘视图 - 验证渲染正确性"""

    def setUp(self):
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    def test_rounded_rect_draw(self):
        """TC-007.01: 圆角矩形绘制无异常"""
        rect = pygame.Rect(100, 100, 200, 100)
        draw_rounded_rect(self.surface, (255, 0, 0), rect, RADIUS_MD)
        pygame.display.flip()

    def test_shadow_draw(self):
        """TC-007.02: 阴影绘制无异常"""
        rect = pygame.Rect(100, 100, 200, 100)
        draw_shadow(self.surface, rect)
        pygame.display.flip()

    def test_rounded_rect_with_border(self):
        """TC-007.03: 带边框圆角矩形"""
        rect = pygame.Rect(100, 100, 200, 100)
        draw_rounded_rect(self.surface, (255, 255, 255), rect, RADIUS_MD,
                          border_width=2, border_color=(0, 0, 0))

    def test_font_manager_singleton(self):
        """TC-007.04: 字体管理器单例"""
        fm1 = FontManager()
        fm2 = FontManager()
        self.assertIs(fm1, fm2)

    def test_font_manager_get_font(self):
        """TC-007.05: 字体获取"""
        fm = FontManager()
        font = fm.get_font(17)
        self.assertIsNotNone(font)

    def test_font_manager_cache(self):
        """TC-007.06: 字体缓存生效"""
        fm = FontManager()
        f1 = fm.get_font(17, bold=True)
        f2 = fm.get_font(17, bold=True)
        self.assertIs(f1, f2)

    def test_font_manager_sizes(self):
        """TC-007.07: 各尺寸字体获取"""
        fm = FontManager()
        self.assertIsNotNone(fm.get_large())
        self.assertIsNotNone(fm.get_medium())
        self.assertIsNotNone(fm.get_small())
        self.assertIsNotNone(fm.get_tiny())


# ============================================================
# TC-008: 工具函数测试
# ============================================================

class TestUtilsFunctions(unittest.TestCase):
    """工具函数 - 验证通用工具正确性"""

    def test_lerp(self):
        """TC-008.01: 线性插值"""
        self.assertEqual(lerp(0, 100, 0.0), 0)
        self.assertEqual(lerp(0, 100, 1.0), 100)
        self.assertEqual(lerp(0, 100, 0.5), 50)

    def test_clamp(self):
        """TC-008.02: 范围限制"""
        self.assertEqual(clamp(5, 0, 10), 5)
        self.assertEqual(clamp(-5, 0, 10), 0)
        self.assertEqual(clamp(15, 0, 10), 10)

    def test_format_score_small(self):
        """TC-008.03: 小分数格式"""
        self.assertEqual(format_score(0), "0")
        self.assertEqual(format_score(42), "42")
        self.assertEqual(format_score(999), "999")

    def test_format_score_thousands(self):
        """TC-008.04: 千位分数格式"""
        self.assertEqual(format_score(1000), "1.0K")
        self.assertEqual(format_score(1500), "1.5K")

    def test_format_score_millions(self):
        """TC-008.05: 百万分格式"""
        self.assertEqual(format_score(1000000), "1.0M")

    def test_format_time(self):
        """TC-008.06: 时间格式化"""
        self.assertEqual(format_time(0), "00:00")
        self.assertEqual(format_time(60), "01:00")
        self.assertEqual(format_time(90), "01:30")
        self.assertEqual(format_time(3661), "61:01")

    def test_get_tile_color_known(self):
        """TC-008.07: 已知方块颜色"""
        bg, text = get_tile_color(2)
        self.assertTrue(is_valid_rgb(bg))
        self.assertTrue(is_valid_rgb(text))

    def test_get_tile_color_unknown(self):
        """TC-008.08: 超过 2048 的方块使用金色"""
        bg, text = get_tile_color(4096)
        self.assertTrue(is_valid_rgb(bg))
        self.assertTrue(is_valid_rgb(text))

    def test_ease_out_spring_properties(self):
        """TC-008.09: 弹簧动画函数属性"""
        # t=0 时接近 0
        self.assertAlmostEqual(ease_out_spring(0.0), 0.0, delta=0.2)
        # t=1 时接近 1
        self.assertAlmostEqual(ease_out_spring(1.0), 1.0, delta=0.2)
        # 函数不抛异常
        for t in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
            val = ease_out_spring(t)
            self.assertIsInstance(val, float)


# ============================================================
# TC-009: 页面管理器测试
# ============================================================

class TestPageManager(unittest.TestCase):
    """页面管理器 - 验证页面切换逻辑"""

    def setUp(self):
        PageManager._instance = None
        self.pm = PageManager()

    def test_singleton(self):
        """TC-009.01: 页面管理器单例"""
        pm2 = PageManager()
        self.assertIs(self.pm, pm2)

    def test_register_page(self):
        """TC-009.02: 注册页面"""
        page = Page("test")
        self.pm.register_page(page)
        self.assertIs(self.pm.get_page("test"), page)

    def test_switch_to(self):
        """TC-009.03: 切换页面"""
        p1 = Page("page1")
        p2 = Page("page2")
        self.pm.register_page(p1)
        self.pm.register_page(p2)
        self.pm.switch_to("page1")
        self.assertEqual(self.pm.current_page.name, "page1")
        self.pm.switch_to("page2")
        self.assertEqual(self.pm.current_page.name, "page2")

    def test_switch_triggers_on_exit(self):
        """TC-009.04: 切换页面触发 on_exit"""
        p1 = Page("page1")
        self.pm.register_page(p1)
        self.pm.switch_to("page1")
        self.assertTrue(p1.active)
        p2 = Page("page2")
        self.pm.register_page(p2)
        self.pm.switch_to("page2")
        self.assertFalse(p1.active)

    def test_push_pop_page(self):
        """TC-009.05: 压入/弹出页面"""
        p1 = Page("page1")
        p2 = Page("page2")
        self.pm.register_page(p1)
        self.pm.register_page(p2)
        self.pm.switch_to("page1")
        self.pm.push_page("page2")
        self.assertEqual(self.pm.current_page.name, "page2")
        self.pm.pop_page()
        self.assertEqual(self.pm.current_page.name, "page1")

    def test_pop_empty_stack(self):
        """TC-009.06: 弹出空栈"""
        p1 = Page("page1")
        self.pm.register_page(p1)
        self.pm.switch_to("page1")
        self.pm.pop_page()
        self.assertIsNone(self.pm.current_page)


# ============================================================
# TC-010: 回归测试 - 现有功能不受影响
# ============================================================

class TestRegression(unittest.TestCase):
    """回归测试 - 确保 iOS 改造未破坏核心逻辑"""

    def test_board_core_logic(self):
        """TC-010.01: 棋盘核心逻辑完整"""
        from src.models.board import GameBoard
        from src.models.tile import Tile

        board = GameBoard()
        board.grid = [[None] * 4 for _ in range(4)]
        board.grid[0][0] = Tile(value=2, row=0, col=0)
        board.grid[0][1] = Tile(value=2, row=0, col=1)

        moved = board._slide_left()
        self.assertTrue(moved)
        self.assertEqual(board.grid[0][0].value, 4)
        self.assertEqual(board.score, 4)

    def test_game_state_classic_mode(self):
        """TC-010.02: 经典模式正常"""
        from src.models.game_state import GameState
        gs = GameState()
        gs.start_game("classic")
        self.assertEqual(gs.state, GameState.STATE_PLAYING)
        self.assertEqual(gs.mode, "classic")
        self.assertEqual(gs.undo_count, 2)

    def test_game_state_timed_mode(self):
        """TC-010.03: 计时模式正常"""
        from src.models.game_state import GameState
        gs = GameState()
        gs.start_game("timed", {"time_limit": 60})
        self.assertEqual(gs.mode, "timed")
        self.assertEqual(gs.time_remaining, 60)

    def test_game_state_challenge_mode(self):
        """TC-010.04: 挑战模式正常"""
        from src.models.game_state import GameState
        gs = GameState()
        gs.start_game("challenge", {"move_limit": 50, "target_tile": 128})
        self.assertEqual(gs.mode, "challenge")
        self.assertEqual(gs.move_limit, 50)

    def test_undo_functionality(self):
        """TC-010.05: 撤销功能正常"""
        from src.models.game_state import GameState
        from src.models.board import GameBoard
        from src.models.tile import Tile

        gs = GameState()
        gs.start_game("classic")

        gs.board.grid = [[None] * 4 for _ in range(4)]
        gs.board.grid[0][0] = Tile(value=2, row=0, col=0)
        gs.board.grid[0][1] = Tile(value=2, row=0, col=1)

        gs.save_for_undo()
        gs.board.move("left")
        self.assertEqual(gs.board.score, 4)

        gs.undo()
        self.assertEqual(gs.board.score, 0)

    def test_win_detection(self):
        """TC-010.06: 胜利检测正常"""
        from src.models.board import GameBoard
        from src.models.tile import Tile

        board = GameBoard()
        board.grid = [[None] * 4 for _ in range(4)]
        board.grid[0][0] = Tile(value=1024, row=0, col=0)
        board.grid[0][1] = Tile(value=1024, row=0, col=1)
        board._slide_left()
        self.assertTrue(board.is_won)
        self.assertEqual(board.grid[0][0].value, 2048)

    def test_game_over_detection(self):
        """TC-010.07: 游戏结束检测正常"""
        from src.models.board import GameBoard
        from src.models.tile import Tile

        board = GameBoard()
        values = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ]
        for r in range(4):
            for c in range(4):
                board.grid[r][c] = Tile(value=values[r][c], row=r, col=c)
        board._check_game_state()
        self.assertTrue(board.is_game_over)

    def test_serialization(self):
        """TC-010.08: 序列化/反序列化正常"""
        from src.models.board import GameBoard
        from src.models.tile import Tile

        board = GameBoard()
        board.grid = [[None] * 4 for _ in range(4)]
        board.grid[0][0] = Tile(value=2, row=0, col=0)
        board.score = 500

        data = board.to_dict()
        restored = GameBoard.from_dict(data)
        self.assertEqual(restored.score, 500)
        self.assertEqual(restored.grid[0][0].value, 2)

    def test_data_persistence(self):
        """TC-010.09: 数据持久化正常"""
        from src.models.data_manager import DataManager

        DataManager._instance = None
        dm = DataManager()
        dm.reset_data()
        dm.update_high_score(1000)
        self.assertEqual(dm.get("high_score"), 1000)
        dm.update_high_score(500)
        self.assertEqual(dm.get("high_score"), 1000)  # 不应降低

    def test_i18n(self):
        """TC-010.10: 国际化正常"""
        from src.i18n import t, set_language, get_language

        self.assertEqual(get_language(), "zh")
        self.assertEqual(t("start_game"), "开始游戏")
        set_language("en")
        self.assertEqual(t("start_game"), "Start Game")
        set_language("zh")

    def test_achievements(self):
        """TC-010.11: 成就系统正常"""
        from src.models.achievements import check_achievements, ACHIEVEMENTS

        newly = check_achievements(max_tile=2048, total_games=0, high_score=0)
        self.assertIn("first_2048", newly)
        self.assertGreater(len(ACHIEVEMENTS), 0)


# ============================================================
# TC-011: 边界情况和兼容性
# ============================================================

class TestEdgeCases(unittest.TestCase):
    """边界情况 - 验证健壮性"""

    def test_empty_color_tuple(self):
        """TC-011.01: 空元组不是有效颜色"""
        self.assertFalse(is_valid_rgb(()))
        self.assertFalse(is_valid_rgb(None))

    def test_color_out_of_range(self):
        """TC-011.02: 超范围颜色值"""
        self.assertFalse(is_valid_rgb((256, 0, 0)))
        self.assertFalse(is_valid_rgb((-1, 0, 0)))

    def test_format_score_negative(self):
        """TC-011.03: 负数分数格式化"""
        result = format_score(-100)
        self.assertIsInstance(result, str)

    def test_format_time_zero(self):
        """TC-011.04: 零秒时间格式化"""
        self.assertEqual(format_time(0), "00:00")

    def test_clamp_inverted(self):
        """TC-011.05: 反转范围限制"""
        result = clamp(5, 10, 0)  # min > max
        # 应该返回边界值之一，不应崩溃
        self.assertIsInstance(result, (int, float))

    def test_button_negative_size(self):
        """TC-011.06: 按钮负尺寸不应崩溃"""
        # pygame.Rect 会处理负尺寸
        btn = Button(0, 0, -100, -50, "OK")
        self.assertEqual(btn.rect.width, -100)

    def test_many_components_coexist(self):
        """TC-011.07: 多组件共存"""
        surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        components = []
        for i in range(10):
            btn = Button(i * 80, 0, 70, 40, f"B{i}")
            components.append(btn)
        for comp in components:
            comp.draw(surface)
        self.assertEqual(len(components), 10)

    def test_spring_animation_stress(self):
        """TC-011.08: 弹簧动画压力测试"""
        # 快速调用 1000 次不应崩溃
        for i in range(1000):
            t = i / 1000.0
            val = ease_out_spring(t)
            self.assertIsInstance(val, float)

    def test_large_score_format(self):
        """TC-011.09: 大分数格式化"""
        self.assertEqual(format_score(999999999), "1000.0M")

    def test_font_manager_concurrent(self):
        """TC-011.10: 字体管理器多次获取"""
        fm = FontManager()
        fonts = [fm.get_font(s) for s in range(10, 40, 2)]
        self.assertEqual(len(fonts), 15)
        for f in fonts:
            self.assertIsNotNone(f)


if __name__ == "__main__":
    unittest.main(verbosity=2)
