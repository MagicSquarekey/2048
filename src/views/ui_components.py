# -*- coding: utf-8 -*-
# @Function: UI 基础组件 - 深空霓虹主题 / Deep-space neon theme components

import pygame
from typing import Tuple, Optional, Callable

from src.config import (
    COLOR_BTN_PRIMARY, COLOR_BTN_PRIMARY_HOVER,
    COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
    COLOR_BTN_DANGER, COLOR_BTN_DANGER_HOVER,
    COLOR_TEXT, COLOR_TEXT_SECONDARY, COLOR_OVERLAY,
    ACCENT_BLUE, ACCENT_GREEN, CARD_BG, CARD_BORDER,
    RADIUS_MD, RADIUS_LG,
)
from src.utils import (
    draw_rounded_rect, draw_text_centered, get_font_manager, point_in_rect,
    draw_card, draw_glow, draw_gradient_rounded_rect, lighten,
)


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
    """霓虹渐变按钮组件（主按钮带渐变 + 辉光）/ Neon gradient button"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font_size: int = 17,
        color: Tuple[int, int, int] = COLOR_BTN_PRIMARY,
        hover_color: Tuple[int, int, int] = COLOR_BTN_PRIMARY_HOVER,
        text_color: Tuple[int, int, int] = (255, 255, 255),
        callback: Optional[Callable] = None,
        radius: int = RADIUS_MD,
        shadow: bool = True,           # 主按钮辉光（次要按钮自动降级为微光）
        style: str = "primary",        # primary=渐变辉光 / ghost=玻璃卡片
    ) -> None:
        super().__init__(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.callback = callback
        self.radius = radius
        self.shadow = shadow
        self.style = style
        self.is_hovered = False
        self.is_pressed = False

        # 动画参数
        self._press_scale = 1.0
        self._target_scale = 1.0
        self._animation_speed = 14.0
        self._bounce_scale = 1.0
        self._bounce_velocity = 0.0

        # 弹簧参数（iOS UIKit 风格）
        self._spring_stiffness = 0.5
        self._spring_damping = 0.75
        self._spring_velocity_threshold = 0.001
        self._spring_displacement_threshold = 0.001

    def _base_color(self) -> Tuple[int, int, int]:
        if not self.enabled:
            return (70, 72, 104)
        if self.is_hovered:
            return self.hover_color
        return self.color

    def update(self, dt: float) -> None:
        """更新动画 - 精确弹簧物理模拟"""
        if abs(self._press_scale - self._target_scale) > 0.001:
            diff = self._target_scale - self._press_scale
            self._press_scale += diff * min(1.0, self._animation_speed * dt)
        else:
            self._press_scale = self._target_scale

        if self._target_scale == 1.0:
            displacement = self._bounce_scale - 1.0
            if abs(displacement) > self._spring_displacement_threshold or \
               abs(self._bounce_velocity) > self._spring_velocity_threshold:
                spring_force = -self._spring_stiffness * displacement
                damping_force = -self._spring_damping * self._bounce_velocity
                acceleration = spring_force + damping_force
                self._bounce_velocity += acceleration * dt
                self._bounce_scale += self._bounce_velocity * dt
            else:
                self._bounce_scale = 1.0
                self._bounce_velocity = 0.0

    def draw(self, surface: pygame.Surface) -> None:
        """绘制霓虹按钮"""
        if not self.visible:
            return

        scale = self._press_scale * self._bounce_scale
        w = int(self.rect.width * scale)
        h = int(self.rect.height * scale)
        draw_rect = pygame.Rect(
            self.rect.x + (self.rect.width - w) // 2,
            self.rect.y + (self.rect.height - h) // 2,
            w, h
        )

        base = self._base_color()
        if self.style == "primary":
            # 主按钮：彩色辉光 + 垂直渐变
            if self.shadow:
                draw_glow(surface, draw_rect, base,
                          alpha=40 if not self.is_pressed else 18,
                          blur=12 if not self.is_pressed else 6,
                          radius=self.radius)
            draw_gradient_rounded_rect(
                surface, draw_rect, lighten(base, 1.22), base, self.radius,
            )
        else:
            # ghost 按钮：玻璃卡片，悬停提亮
            bg = base if self.is_hovered else CARD_BG
            draw_card(surface, draw_rect, self.radius, bg=bg)

        text_color = self.text_color if self.enabled else (140, 142, 165)
        font = get_font_manager().get_font(self.font_size, bold=True)
        draw_text_centered(surface, self.text, font, text_color, draw_rect.center)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible or not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = point_in_rect(event.pos, self.rect)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True
                self._target_scale = 0.96
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed:
                self.is_pressed = False
                self._target_scale = 1.0
                self._bounce_scale = 0.98
                self._bounce_velocity = 0.1
                if self.is_hovered and self.callback:
                    self.callback()
                    return True
        return False


class Label(UIComponent):
    """标签组件"""

    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        font_size: int = 17,
        color: Tuple[int, int, int] = COLOR_TEXT,
        bold: bool = False,
        centered: bool = False,
    ) -> None:
        self.text = text
        self.font_size = font_size
        self.color = color
        self.bold = bold
        self.centered = centered
        font = get_font_manager().get_font(font_size, bold)
        text_surface = font.render(text, True, color)
        w, h = text_surface.get_size()
        if centered:
            super().__init__(x - w // 2, y - h // 2, w, h)
        else:
            super().__init__(x, y, w, h)

    def draw(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        font = get_font_manager().get_font(self.font_size, self.bold)
        if self.centered:
            draw_text_centered(surface, self.text, font, self.color, self.rect.center)
        else:
            surface.blit(font.render(self.text, True, self.color), self.rect.topleft)

    def set_text(self, text: str) -> None:
        self.text = text
        font = get_font_manager().get_font(self.font_size, self.bold)
        text_surface = font.render(text, True, self.color)
        w, h = text_surface.get_size()
        self.rect.width = w
        self.rect.height = h


class Panel(UIComponent):
    """玻璃卡片面板组件"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Tuple[int, int, int] = CARD_BG,
        radius: int = RADIUS_LG,
        border_width: int = 1,
        border_color: Optional[Tuple[int, int, int]] = CARD_BORDER,
        alpha: int = 255,
        shadow: bool = False,
    ) -> None:
        super().__init__(x, y, width, height)
        self.color = color
        self.radius = radius
        self.border_width = border_width
        self.border_color = border_color
        self.alpha = alpha
        self.shadow = shadow

    def draw(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        draw_card(surface, self.rect, self.radius, bg=self.color,
                  border=self.border_color or self.color,
                  draw_border=self.border_width > 0 and self.border_color is not None)


class ScoreBox(UIComponent):
    """分数显示卡片（深色玻璃 + 彩色数值）"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        title: str,
        value: int = 0,
        bg_color: Tuple[int, int, int] = CARD_BG,
        title_color: Tuple[int, int, int] = COLOR_TEXT_SECONDARY,
        value_color: Tuple[int, int, int] = ACCENT_BLUE,
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
        self._target_value = value
        if value > self.value:
            # 增加时滚动动画
            self._animating = True
            self._anim_speed = max(1, (value - self.value) // 20)
        else:
            # 减少（撤销等）时立即同步，避免显示残留
            self.value = value
            self._animating = False

    def update(self, dt: float) -> None:
        if self._animating:
            if self.value < self._target_value:
                self.value = min(self._target_value, self.value + self._anim_speed)
            else:
                self._animating = False

    def draw(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        # 数值同色微辉光 + 玻璃卡片
        draw_glow(surface, self.rect, self.value_color, alpha=22, blur=8, radius=RADIUS_MD)
        draw_card(surface, self.rect, RADIUS_MD, bg=self.bg_color)
        # 标题
        font_sm = get_font_manager().get_small()
        draw_text_centered(surface, self.title, font_sm, self.title_color,
                          (self.rect.centerx, self.rect.y + 16))
        # 数值
        font_lg = get_font_manager().get_large(bold=True)
        draw_text_centered(surface, str(self.value), font_lg, self.value_color,
                          (self.rect.centerx, self.rect.y + 41))


class iOSAlert(UIComponent):
    """通用弹窗组件（深色主题）"""

    def __init__(
        self,
        title: str,
        message: str,
        confirm_text: str = "确认",
        cancel_text: str = "取消",
        on_confirm: Optional[Callable] = None,
        on_cancel: Optional[Callable] = None,
        title_color: Tuple[int, int, int] = COLOR_TEXT,
        message_color: Tuple[int, int, int] = COLOR_TEXT_SECONDARY,
        confirm_color: Tuple[int, int, int] = COLOR_BTN_DANGER,
        cancel_color: Tuple[int, int, int] = (110, 114, 150),
    ) -> None:
        from src.config import WINDOW_WIDTH, WINDOW_HEIGHT
        dlg_w, dlg_h = 320, 190
        dlg_x = (WINDOW_WIDTH - dlg_w) // 2
        dlg_y = (WINDOW_HEIGHT - dlg_h) // 2
        super().__init__(dlg_x, dlg_y, dlg_w, dlg_h)

        self.title = title
        self.message = message
        self.confirm_text = confirm_text
        self.cancel_text = cancel_text
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.title_color = title_color
        self.message_color = message_color
        self.confirm_color = confirm_color
        self.cancel_color = cancel_color

        btn_w, btn_h = 120, 40
        btn_y = dlg_y + dlg_h - 62
        self.btn_confirm = Button(
            dlg_x + 24, btn_y, btn_w, btn_h,
            confirm_text, font_size=15,
            color=confirm_color, hover_color=COLOR_BTN_DANGER_HOVER,
            callback=self._on_confirm,
        )
        self.btn_cancel = Button(
            dlg_x + dlg_w - btn_w - 24, btn_y, btn_w, btn_h,
            cancel_text, font_size=15,
            color=cancel_color, hover_color=(140, 144, 184),
            style="ghost", text_color=(220, 222, 240), shadow=False,
            callback=self._on_cancel,
        )
        self.is_visible = False

    def show(self) -> None:
        """显示弹窗"""
        self.is_visible = True

    def hide(self) -> None:
        """隐藏弹窗"""
        self.is_visible = False

    def _on_confirm(self) -> None:
        """确认按钮回调"""
        self.is_visible = False
        if self.on_confirm:
            self.on_confirm()

    def _on_cancel(self) -> None:
        """取消按钮回调"""
        self.is_visible = False
        if self.on_cancel:
            self.on_cancel()

    def draw(self, surface: pygame.Surface) -> None:
        """绘制弹窗"""
        if not self.is_visible:
            return

        from src.utils import blit_overlay
        blit_overlay(surface, COLOR_OVERLAY[3])

        draw_glow(surface, self.rect, ACCENT_BLUE, alpha=26, blur=14, radius=RADIUS_LG)
        draw_card(surface, self.rect, RADIUS_LG)

        font_title = get_font_manager().get_medium(bold=True)
        draw_text_centered(surface, self.title, font_title, self.title_color,
                          (self.rect.centerx, self.rect.y + 44))

        font_msg = get_font_manager().get_small()
        draw_text_centered(surface, self.message, font_msg, self.message_color,
                          (self.rect.centerx, self.rect.y + 86))

        self.btn_confirm.draw(surface)
        self.btn_cancel.draw(surface)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """处理事件"""
        if not self.is_visible:
            return False

        if self.btn_confirm.handle_event(event):
            return True
        if self.btn_cancel.handle_event(event):
            return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.rect.collidepoint(event.pos):
                self.is_visible = False
                if self.on_cancel:
                    self.on_cancel()
                return True

        return False


class iOSSwitch(UIComponent):
    """胶囊开关组件"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int = 51,
        height: int = 31,
        is_on: bool = False,
        on_color: Tuple[int, int, int] = ACCENT_GREEN,
        off_color: Tuple[int, int, int] = (96, 100, 142),
        thumb_color: Tuple[int, int, int] = (255, 255, 255),
        callback: Optional[Callable] = None,
    ) -> None:
        super().__init__(x, y, width, height)
        self.is_on = is_on
        self.on_color = on_color
        self.off_color = off_color
        self.thumb_color = thumb_color
        self.callback = callback

        self._thumb_x = x + 2 if not is_on else x + width - 29
        self._target_x = self._thumb_x
        self._animation_speed = 15.0

    def toggle(self):
        """切换开关状态"""
        self.is_on = not self.is_on
        self._target_x = self.rect.x + 2 if not self.is_on else self.rect.x + self.rect.width - 29

        if self.callback:
            self.callback(self.is_on)

    def update(self, dt: float):
        """更新动画"""
        if abs(self._thumb_x - self._target_x) > 0.5:
            diff = self._target_x - self._thumb_x
            self._thumb_x += diff * min(1.0, self._animation_speed * dt)
        else:
            self._thumb_x = self._target_x

    def draw(self, surface: pygame.Surface):
        """绘制开关"""
        if not self.visible:
            return

        track_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        track_color = self.on_color if self.is_on else self.off_color
        if self.is_on:
            draw_glow(surface, track_rect, self.on_color, alpha=36, blur=8, radius=self.rect.height // 2)
        draw_rounded_rect(surface, track_color, track_rect, self.rect.height // 2)

        thumb_size = 27
        thumb_rect = pygame.Rect(
            int(self._thumb_x),
            self.rect.y + 2,
            thumb_size,
            thumb_size
        )
        draw_rounded_rect(surface, self.thumb_color, thumb_rect, thumb_size // 2)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """处理事件"""
        if not self.visible or not self.enabled:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.toggle()
                return True

        return False


class iOSInput(UIComponent):
    """输入框组件（深色主题）"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int = 44,
        placeholder: str = "",
        font_size: int = 17,
        text_color: Tuple[int, int, int] = (245, 246, 252),
        placeholder_color: Tuple[int, int, int] = (120, 124, 160),
        bg_color: Tuple[int, int, int] = (30, 32, 58),
        border_color: Tuple[int, int, int] = CARD_BORDER,
        focus_border_color: Tuple[int, int, int] = ACCENT_BLUE,
        radius: int = 10,
    ) -> None:
        super().__init__(x, y, width, height)
        self.placeholder = placeholder
        self.font_size = font_size
        self.text_color = text_color
        self.placeholder_color = placeholder_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.focus_border_color = focus_border_color
        self.radius = radius

        self.text = ""
        self.is_focused = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_speed = 0.5

    def update(self, dt: float):
        """更新光标闪烁"""
        if self.is_focused:
            self.cursor_timer += dt
            if self.cursor_timer >= self.cursor_blink_speed:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

    def draw(self, surface: pygame.Surface):
        """绘制输入框"""
        if not self.visible:
            return

        draw_rounded_rect(surface, self.bg_color, self.rect, self.radius)

        border_color = self.focus_border_color if self.is_focused else self.border_color
        border_width = 2 if self.is_focused else 1
        pygame.draw.rect(
            surface,
            border_color,
            self.rect,
            width=border_width,
            border_radius=self.radius
        )

        font = get_font_manager().get_font(self.font_size)
        if self.text:
            text_surface = font.render(self.text, True, self.text_color)
            text_x = self.rect.x + 12
            text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
            surface.blit(text_surface, (text_x, text_y))
        elif self.placeholder:
            placeholder_surface = font.render(self.placeholder, True, self.placeholder_color)
            placeholder_x = self.rect.x + 12
            placeholder_y = self.rect.y + (self.rect.height - placeholder_surface.get_height()) // 2
            surface.blit(placeholder_surface, (placeholder_x, placeholder_y))

        if self.is_focused and self.cursor_visible:
            cursor_x = self.rect.x + 12
            if self.text:
                text_surface = font.render(self.text, True, self.text_color)
                cursor_x += text_surface.get_width()
            cursor_y = self.rect.y + 8
            cursor_height = self.rect.height - 16
            pygame.draw.line(
                surface,
                self.text_color,
                (cursor_x, cursor_y),
                (cursor_x, cursor_y + cursor_height),
                width=2
            )

    def handle_event(self, event: pygame.event.Event) -> bool:
        """处理事件"""
        if not self.visible or not self.enabled:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.is_focused = self.rect.collidepoint(event.pos)
                return self.is_focused

        if event.type == pygame.KEYDOWN and self.is_focused:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.is_focused = False
            elif event.unicode and event.unicode.isprintable():
                self.text += event.unicode
            return True

        return False
