# -*- coding: utf-8 -*-
# @Function: 窗口自由缩放与等比展示 / Window resizing with aspect-fit presentation

from typing import Tuple

import pygame

from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT,
)


class DisplayManager:
    """管理逻辑画布、缩放视口与窗口展示 / Manage logical canvas, viewport and presentation.

    逻辑分辨率固定为 800x600，所有页面绘制到 ``canvas``；``present()`` 时按
    aspect-fit 等比缩放到窗口并居中，窗口留边区域用画面边缘延展填充，
    避免出现突兀的黑边。

    Logical resolution stays at 800x600 and all pages draw onto ``canvas``.
    ``present()`` scales it to the window with aspect-fit letterboxing and
    extends the canvas edges into the letterbox so no harsh black bars appear.
    """

    def __init__(self) -> None:
        self.logical_size: Tuple[int, int] = (WINDOW_WIDTH, WINDOW_HEIGHT)
        # 先创建普通 Surface，init() 在视频模式建立后再 convert()
        # Create a plain surface first; init() converts it after a video mode exists.
        self.canvas: pygame.Surface = pygame.Surface(self.logical_size)
        self.screen: pygame.Surface = None  # type: ignore[assignment]
        self.viewport: pygame.Rect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        self._flags: int = 0
        self._scaled: pygame.Surface = None  # type: ignore[assignment]

    # ========== 初始化 / Initialization ==========

    def init(self, flags: int = pygame.RESIZABLE) -> None:
        """初始化显示窗口 / Initialize the display window."""
        self.screen = pygame.display.set_mode(self.logical_size, flags)
        self._flags = flags
        self.canvas = self.canvas.convert()
        self._recompute_viewport()

    # ========== 窗口尺寸 / Window size ==========

    def resize(self, width: int, height: int) -> None:
        """调整窗口尺寸并重算视口 / Resize the window and recompute the viewport.

        Args:
            width: 目标窗口宽 / Target window width
            height: 目标窗口高 / Target window height
        """
        width = max(MIN_WINDOW_WIDTH, int(width))
        height = max(MIN_WINDOW_HEIGHT, int(height))

        if self.screen is None:
            self.init(self._flags or pygame.RESIZABLE)

        if self.screen.get_size() != (width, height):
            self.screen = pygame.display.set_mode((width, height), self._flags)

        self._recompute_viewport()

    def _recompute_viewport(self) -> None:
        """按 aspect-fit 计算居中视口与缩放缓冲 / Recompute centered aspect-fit viewport."""
        win_w, win_h = self.screen.get_size()
        scale = min(win_w / self.logical_size[0], win_h / self.logical_size[1])

        vw = max(1, int(self.logical_size[0] * scale))
        vh = max(1, int(self.logical_size[1] * scale))
        self.viewport = pygame.Rect((win_w - vw) // 2, (win_h - vh) // 2, vw, vh)

        # 缩放缓冲尺寸不变时复用，避免窗口缩放过程中反复分配
        # Reuse the scaled buffer when its size is unchanged.
        if self._scaled is None or self._scaled.get_size() != (vw, vh):
            self._scaled = pygame.Surface((vw, vh)).convert()

    # ========== 坐标与事件 / Coordinates and events ==========

    def is_inside_viewport(self, pos: Tuple[int, int]) -> bool:
        """判断窗口坐标是否落在有效画面区域内 / Whether a window point is inside the viewport."""
        return self.viewport.collidepoint(pos)

    def map_pos(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """窗口坐标 -> 逻辑坐标（并 clamp 到画布内）/ Window position to logical position.

        留边区域内的点也会被夹取到最近的逻辑坐标，避免页面收到画布外坐标。
        Points in the letterbox are clamped to the nearest logical coordinate.
        """
        x, y = pos
        vp = self.viewport
        lx = (x - vp.x) * self.logical_size[0] / vp.width
        ly = (y - vp.y) * self.logical_size[1] / vp.height
        lx = max(0, min(self.logical_size[0] - 1, int(lx)))
        ly = max(0, min(self.logical_size[1] - 1, int(ly)))
        return lx, ly

    def translate_event(self, event: pygame.event.Event) -> pygame.event.Event:
        """把窗口鼠标事件转换为逻辑坐标 / Translate mouse event to logical coordinates.

        保持事件对象本身不变并返回它，调用方可直接继续分发。
        The same event object is modified and returned for immediate dispatch.
        """
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            event.pos = self.map_pos(event.pos)
            if event.type == pygame.MOUSEMOTION:
                rel_x, rel_y = event.rel
                event.rel = (
                    int(round(rel_x * self.logical_size[0] / self.viewport.width)),
                    int(round(rel_y * self.logical_size[1] / self.viewport.height)),
                )
        return event

    # ========== 展示 / Presentation ==========

    def present(self) -> None:
        """把逻辑画布等比缩放后展示到窗口 / Present the canvas with aspect-fit scaling."""
        if self.screen is None:
            raise RuntimeError("DisplayManager.init() must be called before present()")

        win_w, win_h = self.screen.get_size()
        vp = self.viewport

        # 先缩放内容，再从缩放后的边缘生成留边条，保证边界颜色与画面完全一致
        # Scale first, then sample the scaled edges so letterbox colors match exactly.
        if vp.size == self.logical_size:
            # 窗口比例恰好一致，无需重采样 / Exact match: no resampling needed.
            content = self.canvas
        else:
            pygame.transform.smoothscale(self.canvas, vp.size, self._scaled)
            content = self._scaled

        if vp.size != (win_w, win_h):
            self._draw_letterbox_edges(win_w, win_h, content)

        self.screen.blit(content, vp.topleft)
        pygame.display.flip()

    def _draw_letterbox_edges(
        self,
        win_w: int,
        win_h: int,
        content: pygame.Surface,
    ) -> None:
        """用缩放后内容四边 1px 实时生成留边条 / Draw letterbox strips from scaled content edges.

        只生成实际需要的窄条并直接 blit 到窗口，不创建整屏 Surface。
        Only the needed strips are created and blitted directly onto the screen.
        """
        vp = self.viewport
        content_w, content_h = content.get_size()

        # 左右条：整列拉伸到窗口高度（同时覆盖四个角落）
        # Left/right strips: stretch a column to full window height (covers corners).
        if vp.x > 0:
            left = pygame.transform.scale(
                content.subsurface((0, 0, 1, content_h)),
                (vp.x, win_h),
            )
            self.screen.blit(left, (0, 0))
        right_w = win_w - vp.right
        if right_w > 0:
            right = pygame.transform.scale(
                content.subsurface((content_w - 1, 0, 1, content_h)),
                (right_w, win_h),
            )
            self.screen.blit(right, (vp.right, 0))

        # 上下条：整行拉伸到视口宽度的留边区域
        # Top/bottom strips: stretch a row across the viewport-width letterbox.
        if vp.y > 0:
            top = pygame.transform.scale(
                content.subsurface((0, 0, content_w, 1)),
                (vp.width, vp.y),
            )
            self.screen.blit(top, (vp.x, 0))
        bottom_h = win_h - vp.bottom
        if bottom_h > 0:
            bottom = pygame.transform.scale(
                content.subsurface((0, content_h - 1, content_w, 1)),
                (vp.width, bottom_h),
            )
            self.screen.blit(bottom, (vp.x, vp.bottom))
