# -*- coding: utf-8 -*-
# @Function: 弹簧动画函数详细测试

import unittest
import math
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestEaseOutSpring(unittest.TestCase):
    """弹簧动画曲线测试"""

    def test_spring_animation_boundaries(self):
        """测试弹簧动画边界值"""
        from src.utils import ease_out_spring

        # 测试边界值
        result_start = ease_out_spring(0)
        result_end = ease_out_spring(1)

        # 验证起始值接近0
        self.assertAlmostEqual(result_start, 0, places=2)

        # 验证结束值接近1
        self.assertAlmostEqual(result_end, 1, places=2)

    def test_spring_animation_parameters(self):
        """测试弹簧动画参数"""
        from src.utils import ease_out_spring

        # 测试不同参数组合
        test_cases = [
            (0.5, 0.75, 2.5),  # 默认参数
            (0.5, 0.5, 2.0),   # 较小阻尼
            (0.5, 0.9, 3.0),   # 较大阻尼
            (0.5, 0.75, 1.5),  # 较低频率
            (0.5, 0.75, 3.5),  # 较高频率
        ]

        for t, damping, frequency in test_cases:
            result = ease_out_spring(t, damping, frequency)
            self.assertIsInstance(result, float)
            # 弹簧动画结果可能超过1.0（弹性回弹）
            self.assertGreater(result, 0)

    def test_spring_animation_overshoot(self):
        """测试弹簧动画的回弹效果"""
        from src.utils import ease_out_spring

        # 测试中间值应该有回弹效果（超过1.0）
        t_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        overshoot_found = False
        for t in t_values:
            result = ease_out_spring(t, 0.75, 2.5)
            # 检查是否有回弹效果（结果大于1.0）
            if result > 1.0:
                overshoot_found = True
                break

        # 应该至少有一个t值产生回弹效果
        self.assertTrue(overshoot_found, "弹簧动画应该有回弹效果")

    def test_spring_animation_performance(self):
        """测试弹簧动画性能"""
        import time
        from src.utils import ease_out_spring

        # 测试大量计算的性能
        start_time = time.time()
        for _ in range(10000):
            ease_out_spring(0.5, 0.75, 2.5)
        end_time = time.time()

        # 应该能在合理时间内完成
        execution_time = end_time - start_time
        self.assertLess(execution_time, 1.0, "弹簧动画计算性能过低")


class TestDrawShadow(unittest.TestCase):
    """阴影绘制函数测试"""

    def test_shadow_function_exists(self):
        """测试阴影函数是否存在"""
        from src.utils import draw_shadow
        self.assertTrue(callable(draw_shadow))

    def test_shadow_function_signature(self):
        """测试阴影函数签名"""
        import inspect
        from src.utils import draw_shadow

        sig = inspect.signature(draw_shadow)
        params = list(sig.parameters.keys())

        # 验证参数存在
        self.assertIn('surface', params)
        self.assertIn('rect', params)
        self.assertIn('color', params)
        self.assertIn('alpha', params)
        self.assertIn('offset', params)
        self.assertIn('blur', params)


class TestIOSAnimationIntegration(unittest.TestCase):
    """iOS动画集成测试"""

    def test_spring_animation_with_config(self):
        """测试弹簧动画与配置集成"""
        from src.utils import ease_out_spring
        from src.config import SPRING_DAMPING, SPRING_FREQUENCY

        # 使用配置中的参数测试
        result = ease_out_spring(0.5, SPRING_DAMPING, SPRING_FREQUENCY)
        self.assertIsInstance(result, float)

    def test_animation_curve_comparison(self):
        """测试动画曲线对比"""
        from src.utils import ease_out_spring, ease_out_cubic

        # 对比弹簧动画和三次方缓动
        t_values = [0.1, 0.3, 0.5, 0.7, 0.9]
        for t in t_values:
            spring_result = ease_out_spring(t, 0.75, 2.5)
            cubic_result = ease_out_cubic(t)

            # 两者都应该在合理范围内
            self.assertGreater(spring_result, 0)
            self.assertGreater(cubic_result, 0)
            self.assertLess(cubic_result, 1.0)  # 三次方缓动不会超过1.0


if __name__ == "__main__":
    unittest.main()