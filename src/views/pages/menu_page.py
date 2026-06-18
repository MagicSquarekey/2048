# -*- coding: utf-8 -*-
# @Function: 主菜单页面 / Main menu page

import pygame
from typing import Optional, Any

from src.views.pages.base_page import Page
from src.views.ui_components import Button, Label, Panel, ScoreBox
from src.views.board_view import BoardView
from src.models.data_manager import DataManager
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_TEXT,
    COLOR_BTN_PRIMARY, COLOR_BTN_PRIMARY_HOVER,
    COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
)
from src.utils import draw_rounded_rect, draw_text_centered, get_font_manager
from src.i18n import t


class MenuPage(Page):
    """主菜单页面 / Main menu page"""

    def __init__(self) -> None:
        super().__init__("menu")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI 元素 / Initialize UI elements"""
        cx = WINDOW_WIDTH // 2

        # 标题 (font_size=96，文本高度约 100px，中心 y=60 → 顶部≈10，底部≈110)
        self.title_label = Label(
            cx, 60, "2048",
            font_size=96, color=(119, 110, 101), bold=True, centered=True,
        )

        # 副标题 (font_size=20，文本高度约 25px，中心 y=130 → 顶部≈118，底部≈142)
        self.subtitle_label = Label(
            cx, 130, "挑战你的数字极限",
            font_size=20, color=(140, 130, 120), bold=False, centered=True,
        )

        # 分数显示区 (y=155, 高 70 → 底部 225)
        box_w, box_h = 140, 70
        gap = 20
        total_w = box_w * 3 + gap * 2
        start_x = cx - total_w // 2
        y = 155

        self.score_box = ScoreBox(
            start_x, y, box_w, box_h, t("current_score"), 0,
            title_color=(119, 110, 101)
        )
        self.best_box = ScoreBox(
            start_x + box_w + gap, y, box_w, box_h, t("best_score"), 0,
            title_color=(119, 110, 101)
        )
        self.games_box = ScoreBox(
            start_x + (box_w + gap) * 2, y, box_w, box_h, t("total_games"), 0,
            title_color=(119, 110, 101)
        )

        # 按钮 (5个按钮, h=52, gap=55: 250→305→360→415→470, 最后底部 522)
        btn_w, btn_h = 220, 52
        btn_y_start = 250
        btn_gap = 55

        self.btn_classic = Button(
            cx - btn_w // 2, btn_y_start, btn_w, btn_h,
            t("start_game"), font_size=24,
            color=COLOR_BTN_PRIMARY, hover_color=COLOR_BTN_PRIMARY_HOVER,
            callback=lambda: self._on_btn_click("classic"),
        )

        self.btn_timed = Button(
            cx - btn_w // 2, btn_y_start + btn_gap, btn_w, btn_h,
            t("time_challenge"), font_size=24,
            color=COLOR_BTN_PRIMARY, hover_color=COLOR_BTN_PRIMARY_HOVER,
            callback=lambda: self._on_btn_click("timed"),
        )

        self.btn_challenge = Button(
            cx - btn_w // 2, btn_y_start + btn_gap * 2, btn_w, btn_h,
            t("challenge_mode"), font_size=24,
            color=COLOR_BTN_PRIMARY, hover_color=COLOR_BTN_PRIMARY_HOVER,
            callback=lambda: self._on_btn_click("challenge"),
        )

        self.btn_settings = Button(
            cx - btn_w // 2, btn_y_start + btn_gap * 3, btn_w, btn_h,
            t("settings"), font_size=24,
            color=COLOR_BTN_SECONDARY, hover_color=COLOR_BTN_SECONDARY_HOVER,
            callback=lambda: self._on_btn_click("settings"),
        )

        self.btn_achievements = Button(
            cx - btn_w // 2, btn_y_start + btn_gap * 4, btn_w, btn_h,
            t("achievements"), font_size=24,
            color=COLOR_BTN_SECONDARY, hover_color=COLOR_BTN_SECONDARY_HOVER,
            callback=lambda: self._on_btn_click("achievements"),
        )

        self.buttons = [
            self.btn_classic, self.btn_timed, self.btn_challenge,
            self.btn_settings, self.btn_achievements,
        ]

        self._target_page = None

    def _on_btn_click(self, action: str) -> None:
        """按钮点击回调 / Button click callback"""
        self._target_page = action

    def on_enter(self, **kwargs: Any) -> None:
        """进入页面时刷新数据 / Refresh data when entering page"""
        super().on_enter(**kwargs)
        self._target_page = None
        dm = DataManager()
        self.best_box.set_value(dm.get("high_score", 0))
        self.games_box.set_value(dm.get("total_games", 0))
        self.score_box.set_value(0)

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """处理事件 / Handle event"""
        for btn in self.buttons:
            btn.handle_event(event)
        return None

    def update(self, dt: float) -> Optional[str]:
        """更新 / Update"""
        for btn in self.buttons:
            btn.update(dt)
        self.best_box.update(dt)
        self.games_box.update(dt)

        if self._target_page:
            target = self._target_page
            self._target_page = None
            return target
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """绘制菜单页面 / Draw menu page"""
        surface.fill(COLOR_BG)

        # 标题
        self.title_label.draw(surface)
        self.subtitle_label.draw(surface)

        # 分数框
        self.score_box.draw(surface)
        self.best_box.draw(surface)
        self.games_box.draw(surface)

        # 按钮
        for btn in self.buttons:
            btn.draw(surface)

        # 底部提示 - 调整颜色和位置避免重叠
        font = get_font_manager().get_tiny()
        draw_text_centered(
            surface, "用方向键或滑动操作方块",
            font, (119, 110, 101),
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 15),
        )
