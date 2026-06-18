# -*- coding: utf-8 -*-
# @Function: 结算页面 / Result page - 游戏结束/获胜展示

import pygame
from typing import Optional, Any

from src.views.pages.base_page import Page
from src.views.ui_components import Button, Label, Panel
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_TEXT,
    COLOR_BTN_PRIMARY, COLOR_BTN_PRIMARY_HOVER,
    COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
)
from src.utils import draw_rounded_rect, draw_text_centered, get_font_manager
from src.i18n import t


class ResultPage(Page):
    """结算页面 / Result page"""

    def __init__(self) -> None:
        super().__init__("result")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI / Initialize UI"""
        cx = WINDOW_WIDTH // 2

        # 结果面板
        panel_w, panel_h = 360, 350
        panel_x = cx - panel_w // 2
        panel_y = 100
        self.panel = Panel(panel_x, panel_y, panel_w, panel_h, (255, 255, 255), radius=16)

        # 标题
        self.title_label = Label(cx, panel_y + 40, "", font_size=36, color=(119, 110, 101),
                                bold=True, centered=True)

        # 分数
        self.score_title = Label(cx, panel_y + 90, t("final_score"), font_size=16,
                                color=(150, 140, 130), centered=True)
        self.score_label = Label(cx, panel_y + 120, "0", font_size=48,
                                color=(119, 110, 101), bold=True, centered=True)

        # 统计信息
        self.stats_y = panel_y + 180
        self.stat_labels = []

        # 按钮
        btn_w, btn_h = 160, 48
        btn_y = panel_y + panel_h - 70

        self.btn_retry = Button(
            cx - btn_w - 10, btn_y, btn_w, btn_h,
            t("play_again"), font_size=22,
            color=COLOR_BTN_PRIMARY, hover_color=COLOR_BTN_PRIMARY_HOVER,
            callback=self._on_retry,
        )

        self.btn_menu = Button(
            cx + 10, btn_y, btn_w, btn_h,
            t("back_to_menu"), font_size=22,
            color=COLOR_BTN_SECONDARY, hover_color=COLOR_BTN_SECONDARY_HOVER,
            callback=self._on_menu,
        )

        self.buttons = [self.btn_retry, self.btn_menu]
        self._target_page = None
        self._result_data = {}

    def _on_retry(self) -> None:
        """点击重试 / Click retry"""
        self._target_page = "game"
        self._target_page = "game"

    def _on_menu(self) -> None:
        """点击重试 / Click retry"""
        self._target_page = "menu"
        self._target_page = "menu"

    def on_enter(self, **kwargs: Any) -> None:
        """进入结算页面 / Enter result page"""
        super().on_enter(**kwargs)
        self._target_page = None
        self._result_data = kwargs.get("result", {})
        self._update_display()

    def _update_display(self) -> None:
        """更新显示内容 / Update display content"""
        data = self._result_data
        if not data:
            return

        # 标题
        is_win = data.get("is_win", False)
        self.title_label.set_text(t("you_win") if is_win else t("game_over"))

        # 分数
        score = data.get("score", 0)
        self.score_label.set_text(str(score))

        # 统计信息
        mode_names = {"classic": t("mode_classic"), "timed": t("mode_timed"), "challenge": t("mode_challenge")}
        mode = mode_names.get(data.get("mode", "classic"), t("mode_classic"))
        max_tile = data.get("max_tile", 0)
        move_count = data.get("move_count", 0)
        elapsed = data.get("elapsed_time", 0)
        minutes = int(elapsed) // 60
        seconds = int(elapsed) % 60

        stats = [
            f"{t('mode_label')}: {mode}",
            f"{t('max_tile')}: {max_tile}",
            f"{t('move_count')}: {move_count}",
            f"{t('elapsed_time')}: {minutes:02d}:{seconds:02d}",
        ]

        self.stat_labels = []
        cx = WINDOW_WIDTH // 2
        font = get_font_manager().get_small()
        for i, stat in enumerate(stats):
            self.stat_labels.append((stat, cx, self.stats_y + i * 25))

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
        """绘制结算页面 / Draw result page"""
        surface.fill(COLOR_BG)

        # 面板
        self.panel.draw(surface)

        # 标题
        self.title_label.draw(surface)

        # 分数
        self.score_title.draw(surface)
        self.score_label.draw(surface)

        # 统计信息
        font = get_font_manager().get_small()
        for text, x, y in self.stat_labels:
            draw_text_centered(surface, text, font, (120, 110, 100), (x, y))

        # 按钮
        for btn in self.buttons:
            btn.draw(surface)
