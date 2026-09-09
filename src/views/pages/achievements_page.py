# -*- coding: utf-8 -*-
# @Function: 成就页面 / Achievements page - 深空霓虹主题

import pygame
from typing import Optional, Any

from src.views.pages.base_page import Page
from src.views.ui_components import Button, Label
from src.models.achievements import get_all_achievements
from src.config import (
    WINDOW_WIDTH, COLOR_TEXT, COLOR_TEXT_SECONDARY, COLOR_TEXT_TERTIARY,
    ACCENT_GOLD, CARD_BG, CARD_BORDER, COLOR_TEXT_QUATERNARY,
    FONT_SIZE_TITLE1, FONT_SIZE_BODY,
)
from src.utils import (
    blit_background, draw_card, draw_text_centered, get_font_manager,
)


class AchievementsPage(Page):
    """成就页面 / Achievements page"""

    def __init__(self) -> None:
        super().__init__("achievements")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI / Initialize UI"""
        cx = WINDOW_WIDTH // 2

        # 标题
        self.title_label = Label(cx, 48, "成就", font_size=FONT_SIZE_TITLE1,
                                 color=COLOR_TEXT, bold=True, centered=True)

        # 成就卡片
        panel_w, panel_h = 480, 424
        panel_x = cx - panel_w // 2
        panel_y = 96
        self.panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

        # 返回按钮
        self.btn_back = Button(
            cx - 90, panel_y + panel_h + 16, 180, 44,
            "返回主菜单", font_size=FONT_SIZE_BODY,
            color=CARD_BG, hover_color=(66, 70, 116),
            text_color=COLOR_TEXT_SECONDARY, style="ghost", shadow=False,
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
        blit_background(surface)

        self.title_label.draw(surface)
        draw_card(surface, self.panel_rect, 20)

        cx = WINDOW_WIDTH // 2
        start_y = self.panel_rect.y + 18
        item_h = 62
        font_name = get_font_manager().get_font(15, bold=True)
        font_desc = get_font_manager().get_tiny()
        font_status = get_font_manager().get_tiny()
        font_icon = get_font_manager().get_font(18, bold=True)

        for i, ach in enumerate(self._achievements):
            y = start_y + i * item_h
            if y + item_h - 8 > self.panel_rect.bottom - 8:
                break

            unlocked = ach["unlocked"]
            item_rect = pygame.Rect(cx - 216, y + 4, 432, 50)
            row_bg = (46, 48, 82) if unlocked else (36, 38, 66)
            draw_card(surface, item_rect, 12, bg=row_bg,
                      border=ACCENT_GOLD if unlocked else CARD_BORDER)

            # 左侧圆形徽标：已达成 ✓（金，线条绘制），未达成 ?（灰）
            icon_rect = pygame.Rect(item_rect.x + 12, item_rect.y + 9, 32, 32)
            pygame.draw.circle(surface, ACCENT_GOLD if unlocked else (70, 73, 108),
                               icon_rect.center, 16)
            if unlocked:
                cx0, cy0 = icon_rect.center
                pygame.draw.line(surface, (40, 34, 10), (cx0 - 6, cy0 + 1),
                                 (cx0 - 1, cy0 + 6), width=3)
                pygame.draw.line(surface, (40, 34, 10), (cx0 - 1, cy0 + 6),
                                 (cx0 + 7, cy0 - 5), width=3)
            else:
                draw_text_centered(surface, "?", font_icon, COLOR_TEXT_QUATERNARY,
                                   icon_rect.center)

            # 名称 + 描述（左对齐，避免与徽标重叠）
            name_surf = font_name.render(ach["name"], True,
                                         COLOR_TEXT if unlocked else COLOR_TEXT_QUATERNARY)
            surface.blit(name_surf, (item_rect.x + 58, item_rect.y + 9))
            desc_surf = font_desc.render(ach["description"], True,
                                         COLOR_TEXT_TERTIARY if unlocked else (96, 99, 130))
            surface.blit(desc_surf, (item_rect.x + 59, item_rect.y + 29))

            # 状态
            status_text = "已达成" if unlocked else "未达成"
            status_color = ACCENT_GOLD if unlocked else COLOR_TEXT_QUATERNARY
            draw_text_centered(surface, status_text, font_status, status_color,
                               (item_rect.right - 42, item_rect.centery))

        self.btn_back.draw(surface)
