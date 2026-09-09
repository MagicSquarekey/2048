# -*- coding: utf-8 -*-
# @Function: 暂停页面 / Pause Page - 游戏暂停叠加层（深空霓虹主题）

import pygame
from typing import Optional, Any

from src.views.pages.base_page import Page
from src.views.ui_components import Button, Label
from src.views.sound_manager import get_sound_manager
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_TEXT, COLOR_TEXT_SECONDARY,
    COLOR_OVERLAY, CARD_BG, ACCENT_BLUE,
    FONT_SIZE_TITLE1, FONT_SIZE_BODY,
)
from src.utils import blit_background, blit_overlay, draw_card, draw_glow, get_font_manager


class PausePage(Page):
    """暂停页面 - 覆盖在游戏页面上方 / Pause page - overlay on game page"""

    def __init__(self) -> None:
        super().__init__("pause")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI / Initialize UI"""
        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2
        btn_w, btn_h = 260, 48
        btn_gap = 64

        self.title = Label(
            cx, cy - 104, "游戏暂停",
            font_size=FONT_SIZE_TITLE1, color=COLOR_TEXT, bold=True, centered=True,
        )

        self.btn_resume = Button(
            cx - btn_w // 2, cy - 40, btn_w, btn_h, "继续游戏",
            font_size=FONT_SIZE_BODY,
            color=ACCENT_BLUE, hover_color=(104, 178, 255),
            callback=lambda: self._set_result("resume"),
        )

        self.btn_restart = Button(
            cx - btn_w // 2, cy - 40 + btn_gap, btn_w, btn_h, "重新开始",
            font_size=FONT_SIZE_BODY,
            color=CARD_BG, hover_color=(66, 70, 116),
            text_color=COLOR_TEXT_SECONDARY, style="ghost", shadow=False,
            callback=lambda: self._set_result("restart"),
        )

        self.btn_menu = Button(
            cx - btn_w // 2, cy - 40 + btn_gap * 2, btn_w, btn_h, "返回主菜单",
            font_size=FONT_SIZE_BODY,
            color=CARD_BG, hover_color=(66, 70, 116),
            text_color=COLOR_TEXT_SECONDARY, style="ghost", shadow=False,
            callback=lambda: self._set_result("menu"),
        )

        self._result: Optional[str] = None
        self._panel_rect = pygame.Rect(0, 0, 340, 330)
        self._panel_rect.center = (cx, cy)

    def _set_result(self, result: str) -> None:
        """设置操作结果 / Set operation result"""
        self._result = result
        get_sound_manager().play("click")

    def on_enter(self, **kwargs: Any) -> None:
        """进入暂停页面 / Enter pause page"""
        super().on_enter(**kwargs)
        self._result = None

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """处理事件 / Handle events"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "resume"

        self.btn_resume.handle_event(event)
        self.btn_restart.handle_event(event)
        self.btn_menu.handle_event(event)

        if self._result:
            result = self._result
            self._result = None
            return result
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """绘制暂停页面（半透明叠加层）/ Draw pause page (translucent overlay)"""
        blit_overlay(surface, COLOR_OVERLAY[3])

        draw_glow(surface, self._panel_rect, ACCENT_BLUE, alpha=30, blur=16, radius=20)
        draw_card(surface, self._panel_rect, 20)

        self.title.draw(surface)
        self.btn_resume.draw(surface)
        self.btn_restart.draw(surface)
        self.btn_menu.draw(surface)
