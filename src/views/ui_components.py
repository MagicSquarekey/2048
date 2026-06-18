# -*- coding: utf-8 -*-
# @Function: UI 基础组件 - Button、Label、Panel / UI base components - Button, Label, Panel

import pygame
from typing import Tuple, Optional, Callable

from src.config import (
    COLOR_BTN_PRIMARY, COLOR_BTN_PRIMARY_HOVER,
    COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
    COLOR_BTN_DANGER, COLOR_BTN_DANGER_HOVER,
    COLOR_TEXT, COLOR_TEXT_LIGHT,
)
from src.utils import draw_rounded_rect, draw_text_centered, get_font_manager, point_in_rect


class UIComponent:
    """UI 组件基类 / UI component base class"""

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.visible: bool = True
        self.enabled: bool = True

    def draw(self, surface: pygame.Surface) -> None:
        """绘制组件 / Draw component"""
        pass

    def handle_event(self, event: pygame.event.Event) -> bool:
        """处理事件 / Handle event"""
        return False

    def update(self, dt: float) -> None:
        """更新组件状态 / Update component state"""
        pass

    def set_position(self, x: int, y: int) -> None:
        """设置位置 / Set position"""
        self.rect.x = x
        self.rect.y = y


class Button(UIComponent):
    """按钮组件 / Button component"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font_size: int = 24,
        color: Tuple[int, int, int] = COLOR_BTN_PRIMARY,
        hover_color: Tuple[int, int, int] = COLOR_BTN_PRIMARY_HOVER,
        text_color: Tuple[int, int, int] = COLOR_TEXT_LIGHT,
        callback: Optional[Callable] = None,
        radius: int = 8,
    ) -> None:
        super().__init__(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.callback = callback
        self.radius = radius
        self.is_hovered = False
        self.is_pressed = False

    def draw(self, surface: pygame.Surface) -> None:
        """绘制按钮 / Draw button"""
        if not self.visible:
            return
        # 选择颜色
        if not self.enabled:
            bg_color = self.color
        elif self.is_pressed:
            bg_color = tuple(max(0, c - 30) for c in self.color)
        elif self.is_hovered:
            bg_color = self.hover_color
        else:
            bg_color = self.color

        # 绘制背景
        draw_rounded_rect(surface, bg_color, self.rect, self.radius)

        # 绘制文字
        font = get_font_manager().get_font(self.font_size, bold=True)
        text_color = self.text_color if self.enabled else (180, 180, 180)
        draw_text_centered(surface, self.text, font, text_color, self.rect.center)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """处理事件 / Handle event"""
        if not self.visible or not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = point_in_rect(event.pos, self.rect)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed:
                self.is_pressed = False
                if self.is_hovered and self.callback:
                    self.callback()
                    return True
        return False


class Label(UIComponent):
    """标签组件 / Label component"""

    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        font_size: int = 24,
        color: Tuple[int, int, int] = COLOR_TEXT,
        bold: bool = False,
        centered: bool = False,
    ) -> None:
        self.text = text
        self.font_size = font_size
        self.color = color
        self.bold = bold
        self.centered = centered
        # 计算大小
        font = get_font_manager().get_font(font_size, bold)
        text_surface = font.render(text, True, color)
        w, h = text_surface.get_size()
        if centered:
            # centered=True 时，(x, y) 表示文本中心点
            super().__init__(x - w // 2, y - h // 2, w, h)
        else:
            super().__init__(x, y, w, h)

    def draw(self, surface: pygame.Surface) -> None:
        """绘制标签 / Draw label"""
        if not self.visible:
            return
        font = get_font_manager().get_font(self.font_size, self.bold)
        if self.centered:
            draw_text_centered(surface, self.text, font, self.color, self.rect.center)
        else:
            surface.blit(font.render(self.text, True, self.color), self.rect.topleft)

    def set_text(self, text: str) -> None:
        """更新文字 / Update text"""
        self.text = text
        font = get_font_manager().get_font(self.font_size, self.bold)
        text_surface = font.render(text, True, self.color)
        w, h = text_surface.get_size()
        self.rect.width = w
        self.rect.height = h


class Panel(UIComponent):
    """面板组件 / Panel component"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Tuple[int, int, int] = (255, 255, 255),
        radius: int = 12,
        border_width: int = 0,
        border_color: Optional[Tuple[int, int, int]] = None,
        alpha: int = 255,
    ) -> None:
        super().__init__(x, y, width, height)
        self.color = color
        self.radius = radius
        self.border_width = border_width
        self.border_color = border_color
        self.alpha = alpha

    def draw(self, surface: pygame.Surface) -> None:
        """绘制面板 / Draw panel"""
        if not self.visible:
            return
        draw_rounded_rect(
            surface, self.color, self.rect, self.radius,
            self.border_width, self.border_color,
        )


class ScoreBox(UIComponent):
    """分数显示框 / Score display box"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        title: str,
        value: int = 0,
        bg_color: Tuple[int, int, int] = (187, 173, 160),
        title_color: Tuple[int, int, int] = (238, 228, 218),
        value_color: Tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        super().__init__(x, y, width, height)
        self.title = title
        self.value = value
        self.bg_color = bg_color
        self.title_color = title_color
        self.value_color = value_color
        self._target_value = 0
        self._animating = False
        self._anim_speed = 0

    def set_value(self, value: int) -> None:
        """设置分数值（带动画）/ Set score value (with animation)"""
        self._target_value = value
        if value > self.value:
            self._animating = True
            self._anim_speed = max(1, (value - self.value) // 20)

    def update(self, dt: float) -> None:
        """更新动画 / Update animation"""
        if self._animating:
            if self.value < self._target_value:
                self.value = min(self._target_value, self.value + self._anim_speed)
            else:
                self._animating = False

    def draw(self, surface: pygame.Surface) -> None:
        """绘制分数框 / Draw score box"""
        if not self.visible:
            return
        # 标题
        font_sm = get_font_manager().get_small()
        draw_text_centered(surface, self.title, font_sm, self.title_color,
                          (self.rect.centerx, self.rect.y + 18))
        # 分数值
        font_lg = get_font_manager().get_medium(bold=True)
        draw_text_centered(surface, str(self.value), font_lg, self.value_color,
                          (self.rect.centerx, self.rect.y + 48))
