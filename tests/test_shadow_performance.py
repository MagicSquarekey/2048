# -*- coding: utf-8 -*-
# @Function: 阴影缓存性能测试

import sys
import os
import time
import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import WINDOW_WIDTH, WINDOW_HEIGHT
from src.utils import draw_shadow, draw_shadow_optimized, ShadowCache

def test_shadow_performance():
    """测试阴影缓存性能提升"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # 测试参数
    test_rect = pygame.Rect(100, 100, 200, 100)
    iterations = 100
    
    # 测试原始draw_shadow性能
    start_time = time.time()
    for _ in range(iterations):
        draw_shadow(screen, test_rect)
    original_time = time.time() - start_time
    
    # 测试优化后的draw_shadow_optimized性能（首次调用，会建立缓存）
    start_time = time.time()
    for _ in range(iterations):
        draw_shadow_optimized(screen, test_rect)
    optimized_first_time = time.time() - start_time
    
    # 测试优化后的draw_shadow_optimized性能（有缓存）
    start_time = time.time()
    for _ in range(iterations):
        draw_shadow_optimized(screen, test_rect)
    optimized_cached_time = time.time() - start_time
    
    pygame.quit()
    
    # 输出结果
    print("=" * 60)
    print("阴影缓存性能测试结果")
    print("=" * 60)
    print(f"测试次数: {iterations} 次")
    print(f"测试矩形: {test_rect}")
    print("-" * 60)
    print(f"原始 draw_shadow: {original_time*1000:.2f} ms")
    print(f"优化 draw_shadow_optimized (首次): {optimized_first_time*1000:.2f} ms")
    print(f"优化 draw_shadow_optimized (缓存): {optimized_cached_time*1000:.2f} ms")
    print("-" * 60)
    
    if original_time > 0:
        speedup_first = original_time / optimized_first_time if optimized_first_time > 0 else 0
        speedup_cached = original_time / optimized_cached_time if optimized_cached_time > 0 else 0
        print(f"首次调用加速比: {speedup_first:.2f}x")
        print(f"缓存调用加速比: {speedup_cached:.2f}x")
    
    print("=" * 60)
    
    return {
        "original": original_time,
        "optimized_first": optimized_first_time,
        "optimized_cached": optimized_cached_time
    }

if __name__ == "__main__":
    test_shadow_performance()
