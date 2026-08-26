# -*- coding: utf-8 -*-
# @Function: UI 基础组件 - iOS 风格改造后

import pygame
from typing import Tuple, Optional, Callable

from src.config import (
    COLOR_BTN_PRIMARY, COLOR_BTN_PRIMARY_HOVER,
    COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
    COLOR_BTN_DANGER, COLOR_BTN_DANGER_HOVER,
    COLOR_TEXT, COLOR_TEXT_SECONDARY,
    RADIUS_MD, RADIUS_LG,
)
from src.utils import draw_rounded_rect, draw_text_centered, get_font_manager, point_in_rect, draw_shadow_optimized


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
    """iOS 风格按钮组件"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font_size: int = 17,          # iOS Body 字号
        color: Tuple[int, int, int] = COLOR_BTN_PRIMARY,
        hover_color: Tuple[int, int, int] = COLOR_BTN_PRIMARY_HOVER,
        text_color: Tuple[int, int, int] = (255, 255, 255),
        callback: Optional[Callable] = None,
        radius: int = RADIUS_MD,       # iOS 中圆角
        shadow: bool = True,           # 默认显示阴影
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
        self.is_hovered = False
        self.is_pressed = False

        # 动画参数
        self._press_scale = 1.0        # 当前缩放比例
        self._target_scale = 1.0       # 目标缩放比例
        self._animation_speed = 12.0   # 动画速度 (越快越快到达目标)
        self._bounce_scale = 1.0       # 弹性回弹比例
        self._bounce_velocity = 0.0    # 弹性速度
        
        # 优化弹簧参数（参考iOS UIKit弹簧动画）
        self._spring_stiffness = 0.5      # 弹簧刚度（原0.3 → 0.5，更有力）
        self._spring_damping = 0.75       # 阻尼系数（原0.85 → 0.75，更活泼）
        self._spring_velocity_threshold = 0.001  # 速度阈值
        self._spring_displacement_threshold = 0.001  # 位移阈值

    def update(self, dt: float) -> None:
        """更新动画 - 使用精确弹簧物理模拟"""
        # 平滑缩放动画（按下/释放）
        if abs(self._press_scale - self._target_scale) > 0.001:
            diff = self._target_scale - self._press_scale
            self._press_scale += diff * min(1.0, self._animation_speed * dt)
        else:
            self._press_scale = self._target_scale

        # 弹性回弹效果（释放后）
        if self._target_scale == 1.0:
            displacement = self._bounce_scale - 1.0
            
            if abs(displacement) > self._spring_displacement_threshold or \
               abs(self._bounce_velocity) > self._spring_velocity_threshold:
                # 弹簧力 = -刚度 * 位移
                spring_force = -self._spring_stiffness * displacement
                
                # 阻尼力 = -阻尼 * 速度
                damping_force = -self._spring_damping * self._bounce_velocity
                
                # 加速度 = 合力 / 质量
                acceleration = spring_force + damping_force
                
                # 更新速度和位置
                self._bounce_velocity += acceleration * dt
                self._bounce_scale += self._bounce_velocity * dt
            else:
                # 动画结束，重置状态
                self._bounce_scale = 1.0
                self._bounce_velocity = 0.0

    def draw(self, surface: pygame.Surface) -> None:
        """绘制 iOS 风格按钮"""
        if not self.visible:
            return

        # 计算缩放后的矩形（pressed 效果 + 弹性回弹）
        scale = self._press_scale * self._bounce_scale
        w = int(self.rect.width * scale)
        h = int(self.rect.height * scale)
        draw_rect = pygame.Rect(
            self.rect.x + (self.rect.width - w) // 2,
            self.rect.y + (self.rect.height - h) // 2,
            w, h
        )

        # 绘制阴影（iOS 风格柔和阴影 - 使用优化版）
        if self.shadow and not self.is_pressed:
            draw_shadow_optimized(surface, draw_rect)

        # 选择背景色
        if not self.enabled:
            bg_color = self.color
        elif self.is_hovered:
            bg_color = self.hover_color
        else:
            bg_color = self.color

        # 绘制圆角背景
        draw_rounded_rect(surface, bg_color, draw_rect, self.radius)

        # 绘制文字
        font = get_font_manager().get_font(self.font_size, bold=True)
        text_color = self.text_color if self.enabled else (180, 180, 180)
        draw_text_centered(surface, self.text, font, text_color, draw_rect.center)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible or not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = point_in_rect(event.pos, self.rect)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True
                self._target_scale = 0.96  # 按下时缩小到96%
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed:
                self.is_pressed = False
                self._target_scale = 1.0  # 释放时恢复
                self._bounce_scale = 0.98  # 初始弹性偏移
                self._bounce_velocity = 0.1  # 初始弹性速度
                if self.is_hovered and self.callback:
                    self.callback()
                    return True
        return False


class Label(UIComponent):
    """iOS 风格标签组件"""

    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        font_size: int = 17,          # iOS Body
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
    """iOS 风格面板组件"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Tuple[int, int, int] = (255, 255, 255),  # 默认纯白
        radius: int = RADIUS_LG,       # iOS 大圆角
        border_width: int = 0,
        border_color: Optional[Tuple[int, int, int]] = None,
        alpha: int = 255,
        shadow: bool = True,           # 默认显示阴影
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
        # 绘制阴影（使用优化版）
        if self.shadow:
            draw_shadow_optimized(surface, self.rect)
        # 绘制面板
        draw_rounded_rect(
            surface, self.color, self.rect, self.radius,
            self.border_width, self.border_color,
        )


class ScoreBox(UIComponent):
    """iOS 风格分数显示框"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        title: str,
        value: int = 0,
        bg_color: Tuple[int, int, int] = (255, 255, 255),  # 纯白背景，与页面背景区分
        title_color: Tuple[int, int, int] = (60, 60, 67),   # 深灰色标题
        value_color: Tuple[int, int, int] = (0, 0, 0),      # 纯黑分数
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
            self._animating = True
            self._anim_speed = max(1, (value - self.value) // 20)

    def update(self, dt: float) -> None:
        if self._animating:
            if self.value < self._target_value:
                self.value = min(self._target_value, self.value + self._anim_speed)
            else:
                self._animating = False

    def draw(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        # 绘制阴影（iOS风格柔和阴影）
        draw_shadow_optimized(surface, self.rect)
        # 绘制圆角背景
        draw_rounded_rect(surface, self.bg_color, self.rect, RADIUS_MD)
        # 绘制边框（增加可见性）
        border_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        pygame.draw.rect(surface, (200, 200, 210), border_rect, width=2, border_radius=RADIUS_MD)
        # 标题（使用深灰色）
        font_sm = get_font_manager().get_small()
        draw_text_centered(surface, self.title, font_sm, self.title_color,
                          (self.rect.centerx, self.rect.y + 18))
        # 分数值（使用粗体黑色，确保清晰可读）
        font_lg = get_font_manager().get_large(bold=True)
        draw_text_centered(surface, str(self.value), font_lg, (0, 0, 0),
                          (self.rect.centerx, self.rect.y + 48))


class iOSAlert(UIComponent):
    """iOS 风格通用弹窗组件"""

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
        cancel_color: Tuple[int, int, int] = (142, 142, 147),  # iOS Gray
    ) -> None:
        # 计算弹窗位置（居中）
        from src.config import WINDOW_WIDTH, WINDOW_HEIGHT
        dlg_w, dlg_h = 300, 180
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

        # 创建按钮
        btn_w, btn_h = 100, 36
        btn_y = dlg_y + dlg_h - 60
        self.btn_confirm = Button(
            dlg_x + 20, btn_y, btn_w, btn_h,
            confirm_text, font_size=15,
            color=confirm_color, hover_color=(220, 69, 58),
            callback=self._on_confirm,
        )
        self.btn_cancel = Button(
            dlg_x + dlg_w - btn_w - 20, btn_y, btn_w, btn_h,
            cancel_text, font_size=15,
            color=cancel_color, hover_color=(174, 174, 178),
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
        """绘制 iOS 风格弹窗"""
        if not self.is_visible:
            return

        # 绘制半透明遮罩
        from src.config import COLOR_OVERLAY, WINDOW_WIDTH, WINDOW_HEIGHT
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        surface.blit(overlay, (0, 0))

        # 绘制弹窗背景（使用优化版阴影）
        draw_shadow_optimized(surface, self.rect)
        draw_rounded_rect(surface, (255, 255, 255), self.rect, RADIUS_LG)

        # 绘制标题
        font_title = get_font_manager().get_medium(bold=True)
        draw_text_centered(surface, self.title, font_title, self.title_color,
                          (self.rect.centerx, self.rect.y + 40))

        # 绘制消息
        font_msg = get_font_manager().get_small()
        draw_text_centered(surface, self.message, font_msg, self.message_color,
                          (self.rect.centerx, self.rect.y + 80))

        # 绘制按钮
        self.btn_confirm.draw(surface)
        self.btn_cancel.draw(surface)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """处理事件"""
        if not self.is_visible:
            return False

        # 处理按钮事件
        if self.btn_confirm.handle_event(event):
            return True
        if self.btn_cancel.handle_event(event):
            return True

        # 点击遮罩关闭
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.rect.collidepoint(event.pos):
                self.is_visible = False
                if self.on_cancel:
                    self.on_cancel()
                return True

        return False


class iOSSwitch(UIComponent):
    """iOS标准椭圆形胶囊开关组件"""
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int = 51,      # iOS标准宽度51pt
        height: int = 31,     # iOS标准高度31pt
        is_on: bool = False,
        on_color: Tuple[int, int, int] = (52, 199, 89),   # iOS Green
        off_color: Tuple[int, int, int] = (142, 142, 147), # iOS Gray (标准)
        thumb_color: Tuple[int, int, int] = (255, 255, 255),  # 白色滑块
        callback: Optional[Callable] = None,
    ) -> None:
        super().__init__(x, y, width, height)
        self.is_on = is_on
        self.on_color = on_color
        self.off_color = off_color
        self.thumb_color = thumb_color
        self.callback = callback
        
        # 动画参数
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
        """绘制iOS风格开关"""
        if not self.visible:
            return
        
        # 绘制轨道背景
        track_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        track_color = self.on_color if self.is_on else self.off_color
        draw_rounded_rect(surface, track_color, track_rect, self.rect.height // 2)
        
        # 绘制滑块
        thumb_size = 27
        thumb_rect = pygame.Rect(
            int(self._thumb_x),
            self.rect.y + 2,
            thumb_size,
            thumb_size
        )
        
        # 绘制滑块阴影（使用优化版）
        draw_shadow_optimized(surface, thumb_rect, alpha=6, blur=4)
        
        # 绘制滑块
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
    """iOS风格输入框组件"""
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int = 44,      # iOS标准高度44pt
        placeholder: str = "",
        font_size: int = 17,    # iOS Body字号
        text_color: Tuple[int, int, int] = (0, 0, 0),
        placeholder_color: Tuple[int, int, int] = (142, 142, 147),
        bg_color: Tuple[int, int, int] = (255, 255, 255),
        border_color: Tuple[int, int, int] = (209, 209, 214),
        focus_border_color: Tuple[int, int, int] = (0, 122, 255),
        radius: int = 10,       # iOS标准圆角10pt
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
        self.cursor_blink_speed = 0.5  # 光标闪烁速度
    
    def update(self, dt: float):
        """更新光标闪烁"""
        if self.is_focused:
            self.cursor_timer += dt
            if self.cursor_timer >= self.cursor_blink_speed:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
    
    def draw(self, surface: pygame.Surface):
        """绘制iOS风格输入框"""
        if not self.visible:
            return
        
        # 绘制背景
        draw_rounded_rect(surface, self.bg_color, self.rect, self.radius)
        
        # 绘制边框
        border_color = self.focus_border_color if self.is_focused else self.border_color
        border_width = 2 if self.is_focused else 1
        pygame.draw.rect(
            surface,
            border_color,
            self.rect,
            width=border_width,
            border_radius=self.radius
        )
        
        # 绘制文字或占位符
        font = get_font_manager().get_font(self.font_size)
        if self.text:
            text_surface = font.render(self.text, True, self.text_color)
            text_x = self.rect.x + 12  # 左侧内边距
            text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
            surface.blit(text_surface, (text_x, text_y))
        elif self.placeholder:
            placeholder_surface = font.render(self.placeholder, True, self.placeholder_color)
            placeholder_x = self.rect.x + 12
            placeholder_y = self.rect.y + (self.rect.height - placeholder_surface.get_height()) // 2
            surface.blit(placeholder_surface, (placeholder_x, placeholder_y))
        
        # 绘制光标
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
