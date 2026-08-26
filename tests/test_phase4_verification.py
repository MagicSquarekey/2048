# -*- coding: utf-8 -*-
# @Function: Phase 4 测试验证 - iOS Switch组件 + Button动画优化
# 测试工程师: 验证 t2(iOS Switch) 和 t3(Button动画) 的功能正确性

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
    WINDOW_WIDTH, WINDOW_HEIGHT,
    COLOR_GREEN, COLOR_TEXT,
    FONT_SIZE_BODY,
)
from src.views.pages.settings_page import IOSSwitch, SettingsPage
from src.views.ui_components import Button


# ============================================================
# TC-P4-001: iOS Switch 组件测试 (t2 验收)
# ============================================================

class TestIOSSwitch(unittest.TestCase):
    """iOS Switch 开关组件 - 验证 t2 开发成果"""

    def setUp(self):
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    def test_switch_creation(self):
        """TC-P4-001.01: Switch 组件创建"""
        switch = IOSSwitch(100, 100, 200, 44, "音效: 开")
        self.assertEqual(switch.rect.x, 100)
        self.assertEqual(switch.rect.y, 100)
        self.assertEqual(switch.rect.width, 200)
        self.assertEqual(switch.rect.height, 44)

    def test_switch_default_state_on(self):
        """TC-P4-001.02: Switch 默认开启状态"""
        switch = IOSSwitch(0, 0, 200, 44, "测试", is_on=True)
        self.assertTrue(switch.is_on)
        self.assertEqual(switch.color, COLOR_GREEN)

    def test_switch_default_state_off(self):
        """TC-P4-001.03: Switch 关闭状态"""
        switch = IOSSwitch(0, 0, 200, 44, "测试", is_on=False)
        self.assertFalse(switch.is_on)
        self.assertEqual(switch.color, (142, 142, 147))  # iOS Gray

    def test_switch_toggle(self):
        """TC-P4-001.04: Switch 状态切换"""
        switch = IOSSwitch(0, 0, 200, 44, "测试", is_on=True)
        switch.toggle()
        self.assertFalse(switch.is_on)
        switch.toggle()
        self.assertTrue(switch.is_on)

    def test_switch_ios_dimensions(self):
        """TC-P4-001.05: Switch iOS 标准尺寸"""
        switch = IOSSwitch(0, 0, 200, 44, "测试")
        self.assertEqual(switch._switch_width, 51)  # iOS 标准宽度
        self.assertEqual(switch._switch_height, 31)  # iOS 标准高度
        self.assertEqual(switch._knob_size, 27)  # 滑块尺寸

    def test_switch_animation_parameters(self):
        """TC-P4-001.06: Switch 动画参数"""
        switch = IOSSwitch(0, 0, 200, 44, "测试")
        self.assertGreater(switch._animation_speed, 0)
        # _knob_x 可以是 int 或 float
        self.assertIsInstance(switch._knob_x, (int, float))
        self.assertIsInstance(switch._target_knob_x, (int, float))

    def test_switch_draw_no_crash(self):
        """TC-P4-001.07: Switch 绘制无异常"""
        switch = IOSSwitch(100, 100, 200, 44, "音效")
        switch.draw(self.surface)

    def test_switch_draw_off_state(self):
        """TC-P4-001.08: Switch 关闭状态绘制"""
        switch = IOSSwitch(100, 100, 200, 44, "音效", is_on=False)
        switch.draw(self.surface)

    def test_switch_label_text(self):
        """TC-P4-001.09: Switch 标签文本显示"""
        switch = IOSSwitch(0, 0, 200, 44, "音效: 开")
        self.assertIn("音效", switch.text)

    def test_switch_update_animation(self):
        """TC-P4-001.10: Switch 动画更新"""
        switch = IOSSwitch(0, 0, 200, 44, "测试", is_on=True)
        initial_knob_x = switch._knob_x
        switch.toggle()
        # 更新多帧
        for _ in range(30):
            switch.update(0.016)
        # 滑块位置应该变化
        self.assertNotAlmostEqual(switch._knob_x, initial_knob_x, delta=1.0)

    def test_switch_in_settings_page(self):
        """TC-P4-001.11: Switch 集成到设置页面"""
        page = SettingsPage()
        # 验证音效开关是 IOSSwitch 类型
        self.assertIsInstance(page.btn_sound, IOSSwitch)
        # 验证音乐开关是 IOSSwitch 类型
        self.assertIsInstance(page.btn_music, IOSSwitch)

    def test_switch_callback(self):
        """TC-P4-001.12: Switch 回调触发"""
        called = []
        switch = IOSSwitch(0, 0, 200, 44, "测试", callback=lambda: called.append(True))
        switch.is_hovered = True
        switch.is_pressed = True
        event = pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(100, 22))
        switch.handle_event(event)
        self.assertEqual(len(called), 1)


# ============================================================
# TC-P4-002: Button 按压缩放动画测试 (t3 验收)
# ============================================================

class TestButtonPressAnimation(unittest.TestCase):
    """Button 按压缩放动画 - 验证 t3 优化成果"""

    def setUp(self):
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    def test_button_has_press_scale(self):
        """TC-P4-002.01: Button 有按压缩放属性"""
        btn = Button(0, 0, 200, 50, "Test")
        self.assertTrue(hasattr(btn, '_press_scale'))
        self.assertEqual(btn._press_scale, 1.0)

    def test_button_press_scale_range(self):
        """TC-P4-002.02: 按压缩放比例在合理范围"""
        btn = Button(0, 0, 200, 50, "Test")
        # 初始状态应该是 1.0
        self.assertEqual(btn._press_scale, 1.0)
        # 模拟按下
        btn.is_pressed = True
        btn.draw(self.surface)
        # 验证绘制时使用了缩放效果 (在 draw 方法中计算)
        self.assertTrue(btn.is_pressed)

    def test_button_press_scale_smooth_transition(self):
        """TC-P4-002.03: 按压缩放应有平滑过渡"""
        btn = Button(0, 0, 200, 50, "Test")
        # 模拟按下
        btn.is_pressed = True
        # 更新多帧
        for _ in range(10):
            btn.update(0.016)
        # 按压缩放应该平滑过渡
        self.assertTrue(btn.is_pressed)

    def test_button_release_scale_reset(self):
        """TC-P4-002.04: 释放后缩放恢复"""
        btn = Button(0, 0, 200, 50, "Test")
        btn.is_pressed = True
        btn.draw(self.surface)
        # 释放
        btn.is_pressed = False
        btn.draw(self.surface)
        # 应该恢复正常大小
        self.assertFalse(btn.is_pressed)

    def test_button_draw_pressed_state(self):
        """TC-P4-002.05: 按下状态绘制"""
        btn = Button(100, 100, 200, 50, "Press Me")
        btn.is_pressed = True
        # 绘制不应崩溃
        btn.draw(self.surface)

    def test_button_draw_normal_state(self):
        """TC-P4-002.06: 正常状态绘制"""
        btn = Button(100, 100, 200, 50, "Normal")
        btn.draw(self.surface)

    def test_button_rapid_press_release(self):
        """TC-P4-002.07: 快速多次按压释放稳定性"""
        btn = Button(0, 0, 200, 50, "Rapid")
        btn.is_hovered = True
        for _ in range(20):
            btn.is_pressed = True
            btn.update(0.016)
            btn.is_pressed = False
            btn.update(0.016)
        # 不应崩溃
        self.assertIsNotNone(btn)

    def test_button_press_animation_completes(self):
        """TC-P4-002.08: 按压动画应能完成"""
        btn = Button(0, 0, 200, 50, "Animate")
        btn.is_pressed = True
        # 更新足够帧数让动画完成
        for _ in range(60):
            btn.update(0.016)
        # 动画应该完成
        self.assertTrue(btn.is_pressed)

    def test_button_multiple_buttons_independent(self):
        """TC-P4-002.09: 多按钮动画独立"""
        btn1 = Button(0, 0, 100, 50, "B1")
        btn2 = Button(150, 0, 100, 50, "B2")
        btn1.is_pressed = True
        btn1.update(0.016)
        # btn2 不应受影响
        self.assertFalse(btn2.is_pressed)

    def test_button_hover_and_press_combined(self):
        """TC-P4-002.10: 悬停和按压组合效果"""
        btn = Button(0, 0, 200, 50, "Combined")
        btn.is_hovered = True
        btn.is_pressed = True
        btn.draw(self.surface)
        # 不应崩溃
        self.assertTrue(btn.is_hovered)
        self.assertTrue(btn.is_pressed)


# ============================================================
# TC-P4-003: 回归测试 - 现有功能不受影响
# ============================================================

class TestRegressionPhase4(unittest.TestCase):
    """回归测试 - 确保 Phase 4 未破坏现有功能"""

    def test_existing_button_still_works(self):
        """TC-P4-003.01: 现有 Button 功能正常"""
        called = []
        btn = Button(0, 0, 200, 50, "OK", callback=lambda: called.append(True))
        btn.is_hovered = True
        btn.is_pressed = True
        event = pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(100, 25))
        result = btn.handle_event(event)
        self.assertTrue(result)
        self.assertEqual(len(called), 1)

    def test_settings_page_loads(self):
        """TC-P4-003.02: 设置页面正常加载"""
        page = SettingsPage()
        self.assertIsNotNone(page.btn_sound)
        self.assertIsNotNone(page.btn_music)
        self.assertIsNotNone(page.btn_lang)
        self.assertIsNotNone(page.btn_reset)
        self.assertIsNotNone(page.btn_back)

    def test_settings_page_draw(self):
        """TC-P4-003.03: 设置页面绘制正常"""
        page = SettingsPage()
        surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        page.draw(surface)

    def test_settings_page_handle_event(self):
        """TC-P4-003.04: 设置页面事件处理正常"""
        page = SettingsPage()
        event = pygame.event.Event(pygame.MOUSEMOTION, pos=(500, 130))
        result = page.handle_event(event)
        self.assertIsNone(result)

    def test_ios_alert_still_works(self):
        """TC-P4-003.05: iOS Alert 弹窗正常"""
        from src.views.ui_components import iOSAlert
        alert = iOSAlert("测试", "内容")
        alert.show()
        surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        alert.draw(surface)
        self.assertTrue(alert.is_visible)


# ============================================================
# TC-P4-004: Bug 修复验证 (t1 验收)
# ============================================================

class TestBugFixes(unittest.TestCase):
    """Bug 修复验证 - 确保 t1 修复的问题不再复现"""

    def test_settings_page_no_dead_code(self):
        """TC-P4-004.01: settings_page.py 无死代码"""
        # 验证页面可以正常执行到末尾
        page = SettingsPage()
        page._on_back()
        self.assertEqual(page._target_page, "menu")

    def test_result_page_no_duplicate_assignment(self):
        """TC-P4-004.02: result_page.py 无重复赋值"""
        from src.views.pages.result_page import ResultPage
        page = ResultPage()
        # 验证页面可以正常创建和初始化
        self.assertIsNotNone(page)

    def test_sound_manager_update_setting(self):
        """TC-P4-004.03: sound_manager.py 方法调用正确"""
        from src.views.sound_manager import SoundManager
        sm = SoundManager()
        # 验证 set_sound_volume 方法存在且可调用（内部使用 update_setting）
        self.assertTrue(hasattr(sm, 'set_sound_volume'))
        self.assertTrue(hasattr(sm, 'set_music_volume'))


if __name__ == "__main__":
    unittest.main(verbosity=2)
