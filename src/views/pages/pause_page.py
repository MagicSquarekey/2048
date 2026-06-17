# -*- coding: utf-8 -*-
# @Function: 暂停页面 - 游戏暂停叠加层

import pygame
from typing import Optional, Any

from src.views.pages.base_page import Page
from src.views.ui_components import Button, Label
from src.views.sound_manager import get_sound_manager
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_TEXT, COLOR_TEXT_LIGHT,
    COLOR_BTN_PRIMARY, COLOR_BTN_PRIMARY_HOVER,
    COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
    COLOR_OVERLAY,
)
from src.utils import draw_rounded_rect, draw_text_centered, get_font_manager


class PausePage(Page):
    """暂停页面 - 覆盖在游戏页面上方"""

    def __init__(self) -> None:
        super().__init__("pause")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI"""
        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2
        btn_w, btn_h = 220, 50

        # 标题
        self.title = Label(
            cx, cy - 100, "游戏暂停",
            font_size=48, color=COLOR_TEXT, bold=True, centered=True,
        )

        # 继续游戏按钮
        self.btn_resume = Button(
            cx - btn_w // 2, cy - 30, btn_w, btn_h, "继续游戏",
            color=COLOR_BTN_PRIMARY, hover_color=COLOR_BTN_PRIMARY_HOVER,
            callback=lambda: self._set_result("resume"),
        )

        # 重新开始按钮
        self.btn_restart = Button(
            cx - btn_w // 2, cy + 35, btn_w, btn_h, "重新开始",
            color=COLOR_BTN_SECONDARY, hover_color=COLOR_BTN_SECONDARY_HOVER,
            callback=lambda: self._set_result("restart"),
        )

        # 返回主菜单按钮
        self.btn_menu = Button(
            cx - btn_w // 2, cy + 100, btn_w, btn_h, "返回主菜单",
            color=COLOR_BTN_SECONDARY, hover_color=COLOR_BTN_SECONDARY_HOVER,
            callback=lambda: self._set_result("menu"),
        )

        self._result: Optional[str] = None

    def _set_result(self, result: str) -> None:
        """设置操作结果"""
        self._result = result
        get_sound_manager().play("click")

    def on_enter(self, **kwargs: Any) -> None:
        """进入暂停页面"""
        super().on_enter(**kwargs)
        self._result = None

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """处理事件"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # ESC 直接恢复
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
        """绘制暂停页面（半透明叠加层）"""
        # 半透明遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        surface.blit(overlay, (0, 0))

        # 绘制暂停面板背景
        panel_w, panel_h = 320, 300
        panel_x = (WINDOW_WIDTH - panel_w) // 2
        panel_y = (WINDOW_HEIGHT - panel_h) // 2
        draw_rounded_rect(surface, (255, 255, 255), (panel_x, panel_y, panel_w, panel_h), 16)

        # 绘制元素
        self.title.draw(surface)
        self.btn_resume.draw(surface)
        self.btn_restart.draw(surface)
        self.btn_menu.draw(surface)
