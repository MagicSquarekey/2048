# -*- coding: utf-8 -*-
# @Function: 登录页面 - 云端同步预留

import pygame
from typing import Optional, Any

from src.views.pages.base_page import Page
from src.views.ui_components import Button, Label, Panel
from src.views.sound_manager import get_sound_manager
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_TEXT, COLOR_TEXT_LIGHT,
    COLOR_BTN_PRIMARY, COLOR_BTN_PRIMARY_HOVER,
    COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
)
from src.utils import draw_rounded_rect, draw_text_centered, get_font_manager


class LoginPage(Page):
    """登录页面 - 云端同步预留"""

    def __init__(self) -> None:
        super().__init__("login")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI"""
        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2
        btn_w, btn_h = 220, 50

        # 标题
        self.title = Label(
            cx, cy - 120, "用户登录",
            font_size=48, color=COLOR_TEXT, bold=True, centered=True,
        )

        # 说明文字
        self.desc = Label(
            cx, cy - 55, "登录后可云端同步游戏进度",
            font_size=20, color=(150, 140, 130), centered=True,
        )

        # 用户名输入框（占位）
        box_w, box_h = 260, 45
        box_x = cx - box_w // 2
        self.username_box = pygame.Rect(box_x, cy - 20, box_w, box_h)
        self.username = ""
        self.username_active = False

        # 密码输入框（占位）
        self.password_box = pygame.Rect(box_x, cy + 40, box_w, box_h)
        self.password = ""
        self.password_active = False

        # 登录按钮
        self.btn_login = Button(
            cx - btn_w // 2, cy + 100, btn_w, btn_h, "登录",
            color=COLOR_BTN_PRIMARY, hover_color=COLOR_BTN_PRIMARY_HOVER,
            callback=self._on_login,
        )

        # 返回按钮
        self.btn_back = Button(
            cx - btn_w // 2, cy + 165, btn_w, btn_h, "返回",
            color=COLOR_BTN_SECONDARY, hover_color=COLOR_BTN_SECONDARY_HOVER,
            callback=lambda: self._set_result("menu"),
        )

        self._result: Optional[str] = None
        self._message = ""

    def _on_login(self) -> None:
        """登录按钮回调（占位）"""
        if not self.username or not self.password:
            self._message = "请输入用户名和密码"
            return
        # 云端登录预留，当前仅提示
        self._message = "云端同步功能开发中..."
        get_sound_manager().play("click")

    def _set_result(self, result: str) -> None:
        """设置操作结果"""
        self._result = result
        get_sound_manager().play("click")

    def on_enter(self, **kwargs: Any) -> None:
        """进入页面"""
        super().on_enter(**kwargs)
        self._result = None
        self._message = ""
        self.username = ""
        self.password = ""
        self.username_active = False
        self.password_active = False

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """处理事件"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 点击输入框激活
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
        """绘制输入框"""
        # 背景
        bg_color = (255, 255, 255) if is_active else (240, 238, 230)
        draw_rounded_rect(surface, bg_color, rect, 8)

        # 边框
        border_color = COLOR_BTN_PRIMARY if is_active else (200, 190, 180)
        pygame.draw.rect(surface, border_color, rect, 2, border_radius=8)

        # 文字
        font = get_font_manager().get_medium()
        display_text = "*" * len(text) if is_password else text
        if display_text:
            text_surf = font.render(display_text, True, COLOR_TEXT)
        else:
            text_surf = font.render(placeholder, True, (180, 170, 160))

        # 垂直居中
        text_y = rect.y + (rect.height - text_surf.get_height()) // 2
        # 左侧 padding
        clip_rect = pygame.Rect(rect.x + 12, rect.y, rect.width - 24, rect.height)
        surface.set_clip(clip_rect)
        surface.blit(text_surf, (rect.x + 12, text_y))
        surface.set_clip(None)

    def draw(self, surface: pygame.Surface) -> None:
        """绘制登录页面"""
        # 半透明遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((250, 248, 239, 240))
        surface.blit(overlay, (0, 0))

        # 绘制面板
        panel_w, panel_h = 400, 380
        panel_x = (WINDOW_WIDTH - panel_w) // 2
        panel_y = (WINDOW_HEIGHT - panel_h) // 2
        draw_rounded_rect(surface, (255, 255, 255), (panel_x, panel_y, panel_w, panel_h), 16)

        # 绘制元素
        self.title.draw(surface)
        self.desc.draw(surface)

        # 输入框
        self._draw_input_box(
            surface, self.username_box, self.username,
            "用户名", False, self.username_active,
        )
        self._draw_input_box(
            surface, self.password_box, self.password,
            "密码", True, self.password_active,
        )

        # 提示信息
        if self._message:
            msg_surf = get_font_manager().get_small().render(self._message, True, (200, 80, 80))
            msg_x = WINDOW_WIDTH // 2 - msg_surf.get_width() // 2
            surface.blit(msg_surf, (msg_x, WINDOW_HEIGHT // 2 + 90))

        self.btn_login.draw(surface)
        self.btn_back.draw(surface)
