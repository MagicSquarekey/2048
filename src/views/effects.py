# -*- coding: utf-8 -*-
# @Function: 游戏特效 - 粒子系统、震屏 / Game effects - particles, screen shake
# 性能设计：粒子软圆贴图按 (颜色,尺寸) 预渲染缓存，每帧仅 set_alpha + blit；
#          粒子总量受 PARTICLE_MAX 约束，超限丢弃最旧粒子。

import math
import random
from typing import List, Tuple

import pygame

from src.config import PARTICLE_MAX


class _SoftCircleCache:
    """柔边圆贴图缓存 / Soft-edged circle surface cache"""
    _cache: dict = {}
    _max = 64

    @classmethod
    def get(cls, color: Tuple[int, int, int], size: int) -> pygame.Surface:
        key = (color, size)
        surf = cls._cache.get(key)
        if surf is None:
            if len(cls._cache) >= cls._max:
                cls._cache.clear()
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            steps = 4
            for i in range(steps, 0, -1):
                r = max(1, int(size * i / steps))
                alpha = int(255 * (1 - i / (steps + 1)) ** 0.8)
                pygame.draw.circle(surf, (*color, min(255, alpha)), (size, size), r)
            cls._cache[key] = surf
        return surf


class Particle:
    """单个粒子 / Single particle"""

    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "size", "color", "gravity")

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 life: float, size: int, color: Tuple[int, int, int], gravity: float) -> None:
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.life = self.max_life = life
        self.size = size
        self.color = color
        self.gravity = gravity

    @property
    def dead(self) -> bool:
        return self.life <= 0


class ParticleSystem:
    """粒子系统 / Particle system"""

    def __init__(self, max_particles: int = PARTICLE_MAX) -> None:
        self.particles: List[Particle] = []
        self._max = max_particles

    def burst(
        self,
        center: Tuple[float, float],
        color: Tuple[int, int, int],
        count: int = 10,
        speed_range: Tuple[float, float] = (50.0, 190.0),
        size_range: Tuple[int, int] = (3, 6),
        life_range: Tuple[float, float] = (0.28, 0.5),
        gravity: float = 320.0,
        direction_bias: float = None,
    ) -> None:
        """在 center 处爆出一圈粒子 / Spawn a burst of particles"""
        cx, cy = center
        for _ in range(count):
            if len(self.particles) >= self._max:
                self.particles.pop(0)
            angle = random.uniform(0, math.tau)
            speed = random.uniform(*speed_range)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - random.uniform(20, 60)  # 轻微上抛
            self.particles.append(Particle(
                cx + random.uniform(-6, 6), cy + random.uniform(-6, 6),
                vx, vy,
                random.uniform(*life_range),
                random.randint(*size_range),
                color, gravity,
            ))

    def update(self, dt: float) -> None:
        for p in self.particles:
            p.life -= dt
            p.vy += p.gravity * dt
            p.vx *= (1 - 1.6 * dt)   # 空气阻尼
            p.x += p.vx * dt
            p.y += p.vy * dt
        self.particles = [p for p in self.particles if not p.dead]

    def draw(self, surface: pygame.Surface) -> None:
        for p in self.particles:
            alpha = int(255 * (p.life / p.max_life))
            if alpha <= 0:
                continue
            surf = _SoftCircleCache.get(p.color, p.size)
            surf.set_alpha(alpha)
            surface.blit(surf, (int(p.x - p.size), int(p.y - p.size)))

    def clear(self) -> None:
        self.particles.clear()


class ScreenShake:
    """震屏效果：幅度随时间衰减 / Screen shake with decaying amplitude"""

    def __init__(self) -> None:
        self._elapsed: float = 0.0
        self._duration: float = 0.0
        self._amplitude: float = 0.0

    def kick(self, amplitude: float, duration: float) -> None:
        """触发震屏（若当前震屏更强则忽略弱震）/ Trigger shake (stronger wins)"""
        if self.active and self._amplitude >= amplitude:
            return
        self._amplitude = amplitude
        self._duration = duration
        self._elapsed = 0.0

    @property
    def active(self) -> bool:
        return self._elapsed < self._duration

    @property
    def offset(self) -> Tuple[int, int]:
        """当前帧偏移量 / Current frame offset"""
        if not self.active:
            return (0, 0)
        decay = 1 - self._elapsed / self._duration
        amp = self._amplitude * decay * decay
        t = self._elapsed * 72  # 高频抖动
        return (int(amp * math.sin(t)), int(amp * math.cos(t * 1.31)))

    def update(self, dt: float) -> None:
        if self.active:
            self._elapsed += dt
            if self._elapsed >= self._duration:
                self._elapsed = self._duration = 0.0
                self._amplitude = 0.0
