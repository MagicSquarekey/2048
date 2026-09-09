# -*- coding: utf-8 -*-
# @Function: 结算页面 / Result page - 游戏结束/获胜展示（深空霓虹主题）

import pygame
from typing import Optional, Any

from src.views.pages.base_page import Page
from src.views.ui_components import Button, Label
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_TEXT, COLOR_TEXT_SECONDARY,
    COLOR_TEXT_TERTIARY, ACCENT_BLUE, ACCENT_GOLD, CARD_BG, CARD_BORDER,
    FONT_SIZE_TITLE1, FONT_SIZE_LARGE_TITLE, FONT_SIZE_SUBHEAD, FONT_SIZE_BODY,
)
from src.utils import (
    blit_background, draw_card, draw_glow, draw_text_centered, get_font_manager,
)
from src.i18n import t


class ResultPage(Page):
    """结算页面 / Result page"""

    def __init__(self) -> None:
        super().__init__("result")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI / Initialize UI"""
        cx = WINDOW_WIDTH // 2

        # 结果卡片
        panel_w, panel_h = 400, 400
        panel_x = cx - panel_w // 2
        panel_y = 80
        self.panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

        # 标题
        self.title_label = Label(cx, panel_y + 46, "", font_size=FONT_SIZE_TITLE1,
                                 color=COLOR_TEXT, bold=True, centered=True)

        # 分数标签 + 大分数
        self.score_title = Label(cx, panel_y + 96, t("final_score"),
                                 font_size=FONT_SIZE_SUBHEAD, color=COLOR_TEXT_TERTIARY,
                                 centered=True)
        self.score_label = Label(cx, panel_y + 136, "0", font_size=44,
                                 color=ACCENT_GOLD, bold=True, centered=True)

        # 统计信息（2×2 网格小卡片）
        self.stats_y = panel_y + 186
        self.stat_labels = []

        # 按钮
        btn_w, btn_h = 160, 48
        btn_y = panel_y + panel_h - 66
        btn_gap = 16

        self.btn_retry = Button(
            cx - btn_w - btn_gap // 2, btn_y, btn_w, btn_h,
            t("play_again"), font_size=FONT_SIZE_BODY,
            callback=self._on_retry,
        )

        self.btn_menu = Button(
            cx + btn_gap // 2, btn_y, btn_w, btn_h,
            t("back_to_menu"), font_size=FONT_SIZE_BODY,
            color=CARD_BG, hover_color=(66, 70, 116),
            text_color=COLOR_TEXT_SECONDARY, style="ghost", shadow=False,
            callback=self._on_menu,
        )

        self.buttons = [self.btn_retry, self.btn_menu]
        self._target_page = None
        self._result_data = {}
        self._is_win = False

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

        is_win = data.get("is_win", False)
        self._is_win = is_win
        self.title_label.set_text(t("you_win") if is_win else t("game_over"))

        score = data.get("score", 0)
        self.score_label.set_text(str(score))

        # 统计信息（2×2 网格）
        mode_names = {"classic": t("mode_classic"), "timed": t("mode_timed"),
                      "challenge": t("mode_challenge")}
        mode = mode_names.get(data.get("mode", "classic"), t("mode_classic"))
        max_tile = data.get("max_tile", 0)
        move_count = data.get("move_count", 0)
        elapsed = data.get("elapsed_time", 0)
        minutes = int(elapsed) // 60
        seconds = int(elapsed) % 60

        stats = [
            (t("max_tile"), str(max_tile)),
            (t("move_count"), str(move_count)),
            (t("mode_label"), mode),
            (t("elapsed_time"), f"{minutes:02d}:{seconds:02d}"),
        ]
        self.stat_labels = stats

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
        blit_background(surface)

        rect = self.panel_rect
        cx = WINDOW_WIDTH // 2

        # 卡片（胜利金色辉光 / 失败蓝色辉光）
        draw_glow(surface, rect, ACCENT_GOLD if self._is_win else ACCENT_BLUE,
                  alpha=34, blur=18, radius=20)
        draw_card(surface, rect, 20)

        self.title_label.draw(surface)

        # 分数区
        self.score_title.draw(surface)
        self.score_label.draw(surface)

        # 2×2 统计网格
        grid_w, grid_h = 172, 52
        grid_gap = 12
        start_x = cx - (grid_w * 2 + grid_gap) // 2
        for i, (title, value) in enumerate(self.stat_labels):
            row, col = divmod(i, 2)
            cell = pygame.Rect(start_x + col * (grid_w + grid_gap),
                               self.stats_y + row * (grid_h + grid_gap),
                               grid_w, grid_h)
            draw_card(surface, cell, 12, bg=(32, 34, 62))
            font_t = get_font_manager().get_tiny()
            font_v = get_font_manager().get_font(17, bold=True)
            draw_text_centered(surface, title, font_t, COLOR_TEXT_TERTIARY,
                               (cell.centerx, cell.y + 13))
            draw_text_centered(surface, value, font_v, COLOR_TEXT_SECONDARY,
                               (cell.centerx, cell.y + 35))

        # 按钮
        for btn in self.buttons:
            btn.draw(surface)
