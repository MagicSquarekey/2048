# -*- coding: utf-8 -*-
# @Function: 登录页面 - 云端同步预留 / Login page - cloud sync placeholder

import pygame
from typing import Optional, Any

from src.views.pages.base_page import Page
from src.views.ui_components import Button, Label
from src.views.sound_manager import get_sound_manager
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_TEXT, COLOR_TEXT_SECONDARY,
    COLOR_TEXT_TERTIARY, COLOR_BTN_DANGER, ACCENT_BLUE, CARD_BG, CARD_BORDER,
    FONT_SIZE_TITLE1, FONT_SIZE_SUBHEAD, FONT_SIZE_BODY,
)
from src.utils import (
    blit_background, draw_card, draw_glow, draw_rounded_rect, get_font_manager,
)


class LoginPage(Page):
    """登录页面 - 云端同步预留 / Login page - cloud sync placeholder"""

    def __init__(self) -> None:
        super().__init__("login")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI / Initialize UI"""
        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2
        btn_w, btn_h = 260, 48

        self._panel_rect = pygame.Rect(0, 0, 400, 400)
        self._panel_rect.center = (cx, cy)

        self.title = Label(
            cx, self._panel_rect.y + 46, "用户登录",
            font_size=FONT_SIZE_TITLE1, color=COLOR_TEXT, bold=True, centered=True,
        )

        self.desc = Label(
            cx, self._panel_rect.y + 86, "登录后可云端同步游戏进度",
            font_size=FONT_SIZE_SUBHEAD, color=COLOR_TEXT_TERTIARY, centered=True,
        )

        # 用户名输入框
        box_w, box_h = 300, 44
        box_x = cx - box_w // 2
        self.username_box = pygame.Rect(box_x, self._panel_rect.y + 126, box_w, box_h)
        self.username = ""
        self.username_active = False

        # 密码输入框
        self.password_box = pygame.Rect(box_x, self._panel_rect.y + 186, box_w, box_h)
        self.password = ""
        self.password_active = False

        self.btn_login = Button(
            cx - btn_w // 2, self._panel_rect.y + 252, btn_w, btn_h, "登录",
            font_size=FONT_SIZE_BODY,
            color=ACCENT_BLUE, hover_color=(104, 178, 255),
            callback=self._on_login,
        )

        self.btn_back = Button(
            cx - btn_w // 2, self._panel_rect.y + 314, btn_w, btn_h, "返回",
            font_size=FONT_SIZE_BODY,
            color=CARD_BG, hover_color=(66, 70, 116),
            text_color=COLOR_TEXT_SECONDARY, style="ghost", shadow=False,
            callback=lambda: self._set_result("menu"),
        )

        self._result: Optional[str] = None
        self._message = ""

    def _on_login(self) -> None:
        """登录按钮回调（占位）/ Login button callback (placeholder)"""
        if not self.username or not self.password:
            self._message = "请输入用户名和密码"
            return
        self._message = "云端同步功能开发中..."
        get_sound_manager().play("click")

    def _set_result(self, result: str) -> None:
        """设置操作结果 / Set operation result"""
        self._result = result
        get_sound_manager().play("click")

    def on_enter(self, **kwargs: Any) -> None:
        """进入页面 / Enter page"""
        super().on_enter(**kwargs)
        self._result = None
        self._message = ""
        self.username = ""
        self.password = ""
        self.username_active = False
        self.password_active = False

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """处理事件 / Handle event"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.username_active = self.username_box.collidepoint(event.pos)
            self.password_active = self.password_box.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN:
            if self.username_active:
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif event.key == pygame.K_TAB:
                    self.username_active = False
                    self.password_active = True
                elif len(self.username) < 20 and event.unicode.isprintable():
                    self.username += event.unicode
            elif self.password_active:
                if event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                elif event.key == pygame.K_TAB:
                    self.password_active = False
                    self.username_active = True
                elif len(self.password) < 20 and event.unicode.isprintable():
                    self.password += event.unicode

        self.btn_login.handle_event(event)
        self.btn_back.handle_event(event)

        if self._result:
            result = self._result
            self._result = None
            return result
        return None

    def _draw_input_box(self, surface: pygame.Surface, rect: pygame.Rect,
                        text: str, placeholder: str, is_password: bool,
                        is_active: bool) -> None:
        """绘制输入框（深色主题）"""
        bg_color = (30, 32, 58) if not is_active else (36, 39, 70)
        draw_rounded_rect(surface, bg_color, rect, 10)

        border_color = ACCENT_BLUE if is_active else CARD_BORDER
        border_width = 2 if is_active else 1
        pygame.draw.rect(surface, border_color, rect, border_width, border_radius=10)

        font = get_font_manager().get_font(FONT_SIZE_BODY)
        display_text = "*" * len(text) if is_password else text
        if display_text:
            text_surf = font.render(display_text, True, COLOR_TEXT)
        else:
            text_surf = font.render(placeholder, True, COLOR_TEXT_TERTIARY)

        text_y = rect.y + (rect.height - text_surf.get_height()) // 2
        clip_rect = pygame.Rect(rect.x + 12, rect.y, rect.width - 24, rect.height)
        surface.set_clip(clip_rect)
        surface.blit(text_surf, (rect.x + 12, text_y))
        surface.set_clip(None)

    def draw(self, surface: pygame.Surface) -> None:
        """绘制登录页面（深色主题）"""
        blit_background(surface)

        draw_glow(surface, self._panel_rect, ACCENT_BLUE, alpha=30, blur=16, radius=20)
        draw_card(surface, self._panel_rect, 20)

        self.title.draw(surface)
        self.desc.draw(surface)

        self._draw_input_box(
            surface, self.username_box, self.username,
            "用户名", False, self.username_active,
        )
        self._draw_input_box(
            surface, self.password_box, self.password,
            "密码", True, self.password_active,
        )

        if self._message:
            font = get_font_manager().get_small()
            draw_msg = font.render(self._message, True, COLOR_BTN_DANGER)
            surface.blit(draw_msg, draw_msg.get_rect(
                center=(WINDOW_WIDTH // 2, self._panel_rect.y + 372)))

        self.btn_login.draw(surface)
        self.btn_back.draw(surface)
