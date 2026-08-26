# -*- coding: utf-8 -*-
# @Function: 结算页面 / Result page - 游戏结束/获胜展示

import pygame
from typing import Optional, Any

from src.views.pages.base_page import Page
from src.views.ui_components import Button, Label, Panel
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_TEXT,
    COLOR_TEXT_SECONDARY, COLOR_TEXT_TERTIARY,
    COLOR_BTN_PRIMARY, COLOR_BTN_PRIMARY_HOVER,
    COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
    FONT_SIZE_TITLE1, FONT_SIZE_LARGE_TITLE, FONT_SIZE_SUBHEAD, FONT_SIZE_BODY,
)
from src.utils import draw_rounded_rect, draw_text_centered, get_font_manager
from src.i18n import t

# 优化后的结算页面颜色
COLOR_SCORE_TITLE = (100, 100, 108)      # "最终得分" 标题 - 中灰色
COLOR_SCORE_VALUE = (0, 0, 0)            # 得分数字 - 纯黑色，确保清晰可读
COLOR_STAT_TEXT = (60, 60, 67)           # 统计信息 - 深灰色


class ResultPage(Page):
    """结算页面 / Result page"""

    def __init__(self) -> None:
        super().__init__("result")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI / Initialize UI"""
        cx = WINDOW_WIDTH // 2

        # 结果面板 - 增加高度以容纳更好的布局
        panel_w, panel_h = 380, 380
        panel_x = cx - panel_w // 2
        panel_y = 80
        self.panel = Panel(panel_x, panel_y, panel_w, panel_h, (255, 255, 255), radius=16)

        # 标题 (iOS Title 1: 28pt) - 增加与顶部的间距
        self.title_label = Label(cx, panel_y + 48, "", font_size=FONT_SIZE_TITLE1, color=COLOR_TEXT,
                                bold=True, centered=True)

        # 分隔线 - 视觉分隔标题和分数区域
        self.separator_y = panel_y + 72

        # 分数标签 "最终得分" (使用较浅的灰色)
        self.score_title = Label(cx, panel_y + 96, t("final_score"), font_size=FONT_SIZE_SUBHEAD,
                                color=COLOR_SCORE_TITLE, centered=True)

        # 分数数字 (iOS Large Title: 34pt) - 使用纯黑色确保清晰可读
        self.score_label = Label(cx, panel_y + 132, "0", font_size=FONT_SIZE_LARGE_TITLE,
                                color=COLOR_SCORE_VALUE, bold=True, centered=True)

        # 统计信息 - 增加与分数的间距
        self.stats_y = panel_y + 192
        self.stat_labels = []

        # 按钮 - 优化间距和位置
        btn_w, btn_h = 160, 48
        btn_y = panel_y + panel_h - 76
        btn_gap = 16  # 增加按钮间距

        self.btn_retry = Button(
            cx - btn_w - btn_gap // 2, btn_y, btn_w, btn_h,
            t("play_again"), font_size=FONT_SIZE_BODY,
            color=COLOR_BTN_PRIMARY, hover_color=COLOR_BTN_PRIMARY_HOVER,
            callback=self._on_retry,
        )

        self.btn_menu = Button(
            cx + btn_gap // 2, btn_y, btn_w, btn_h,
            t("back_to_menu"), font_size=FONT_SIZE_BODY,
            color=COLOR_BTN_SECONDARY, hover_color=COLOR_BTN_SECONDARY_HOVER,
            callback=self._on_menu,
        )

        self.buttons = [self.btn_retry, self.btn_menu]
        self._target_page = None
        self._result_data = {}

    def _on_retry(self) -> None:
        """点击重试 / Click retry"""
        self._target_page = "game"

    def _on_menu(self) -> None:
        """点击菜单 / Click menu"""
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

        # 统计信息 - 优化间距和对齐
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
        for i, stat in enumerate(stats):
            self.stat_labels.append((stat, cx, self.stats_y + i * 28))  # 增加行间距到28px

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

        # 分隔线 - 轻薄的灰色分隔线，增加视觉层次
        sep_rect = pygame.Rect(self.panel.rect.x + 40, self.separator_y,
                              self.panel.rect.width - 80, 1)
        pygame.draw.rect(surface, (230, 230, 235), sep_rect)

        # 分数
        self.score_title.draw(surface)
        self.score_label.draw(surface)

        # 统计信息 - 使用优化后的颜色
        font = get_font_manager().get_small()
        for text, x, y in self.stat_labels:
            draw_text_centered(surface, text, font, COLOR_STAT_TEXT, (x, y))

        # 按钮
        for btn in self.buttons:
            btn.draw(surface)
