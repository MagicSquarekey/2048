# -*- coding: utf-8 -*-
# @Function: 成就页面 / Achievements page

import pygame
from typing import Optional, Any

from src.views.pages.base_page import Page
from src.views.ui_components import Button, Label, Panel
from src.models.achievements import ACHIEVEMENTS, get_all_achievements
from src.models.data_manager import DataManager
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_TEXT,
    COLOR_TEXT_SECONDARY, COLOR_TEXT_TERTIARY,
    COLOR_TILE_EMPTY, COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
    FONT_SIZE_TITLE1, FONT_SIZE_BODY, FONT_SIZE_FOOTNOTE,
)
from src.utils import draw_rounded_rect, draw_text_centered, get_font_manager


class AchievementsPage(Page):
    """成就页面 / Achievements page"""

    def __init__(self) -> None:
        super().__init__("achievements")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI / Initialize UI"""
        cx = WINDOW_WIDTH // 2

        # 标题 (iOS Title 1: 28pt)
        self.title_label = Label(cx, 40, "成就", font_size=FONT_SIZE_TITLE1, color=COLOR_TEXT,
                                bold=True, centered=True)

        # 成就面板
        panel_w, panel_h = 440, 420
        panel_x = cx - panel_w // 2
        panel_y = 100
        self.panel = Panel(panel_x, panel_y, panel_w, panel_h, (255, 255, 255), radius=16)

        # 返回按钮 (iOS Body: 17pt)
        self.btn_back = Button(
            cx - 80, panel_y + panel_h + 16, 160, 44,  # 8pt网格: 8×2=16
            "返回主菜单", font_size=FONT_SIZE_BODY,
            color=COLOR_BTN_SECONDARY, hover_color=COLOR_BTN_SECONDARY_HOVER,
            callback=self._on_back,
        )

        self.buttons = [self.btn_back]
        self._target_page = None
        self._achievements = []

    def _on_back(self) -> None:
        """返回 / Go back"""
        self._target_page = "menu"

    def on_enter(self, **kwargs: Any) -> None:
        """进入页面 / Enter page"""
        super().on_enter(**kwargs)
        self._target_page = None
        self._achievements = get_all_achievements()

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """处理事件 / Handle event"""
        for btn in self.buttons:
            btn.handle_event(event)
        return None

    def update(self, dt: float) -> Optional[str]:
        """更新 / Update"""
        for btn in self.buttons:
            btn.update(dt)
        if self._target_page:
            target = self._target_page
            self._target_page = None
            return target
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """绘制成就页面 / Draw achievements page"""
        surface.fill(COLOR_BG)

        # 标题
        self.title_label.draw(surface)

        # 面板
        self.panel.draw(surface)

        # 成就列表
        cx = WINDOW_WIDTH // 2
        start_y = self.panel.rect.y + 20
        item_h = 56  # 8pt网格: 8×7=56
        font = get_font_manager().get_small()
        font_name = get_font_manager().get_tiny()

        for i, ach in enumerate(self._achievements):
            y = start_y + i * item_h
            if y + item_h > self.panel.rect.bottom - 10:
                break

            # 成就项背景 (iOS 系统色)
            item_rect = pygame.Rect(cx - 190, y, 380, 44)
            bg_color = COLOR_TILE_EMPTY if ach["unlocked"] else (245, 245, 245)
            draw_rounded_rect(surface, bg_color, item_rect, 8)

            # 图标
            icon = ach["icon"] if ach["unlocked"] else "🔒"
            icon_color = COLOR_TEXT if ach["unlocked"] else (180, 180, 180)
            # 使用文字代替 emoji（避免渲染问题）
            draw_text_centered(surface, ach["id"][:4], font_name, icon_color,
                             (item_rect.x + 25, item_rect.centery))

            # 名称
            name_color = COLOR_TEXT if ach["unlocked"] else (180, 180, 180)
            draw_text_centered(surface, ach["name"], font, name_color,
                             (item_rect.x + 100, item_rect.centery - 8))

            # 描述
            desc_color = COLOR_TEXT_TERTIARY if ach["unlocked"] else (200, 200, 200)
            draw_text_centered(surface, ach["description"], font_name, desc_color,
                             (item_rect.x + 100, item_rect.centery + 10))

            # 状态
            status_text = "✓ 已达成" if ach["unlocked"] else "未达成"
            from src.config import COLOR_GREEN
            status_color = COLOR_GREEN if ach["unlocked"] else (180, 180, 180)
            draw_text_centered(surface, status_text, font_name, status_color,
                             (item_rect.right - 50, item_rect.centery))

        # 按钮
        self.btn_back.draw(surface)
