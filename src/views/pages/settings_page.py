# -*- coding: utf-8 -*-
# @Function: 设置页面 / Settings page - 深空霓虹主题

import pygame
from typing import Optional, Any

from src.views.pages.base_page import Page
from src.views.ui_components import Button, Label, iOSAlert, iOSSwitch
from src.models.data_manager import DataManager
from src.config import (
    WINDOW_WIDTH, COLOR_TEXT, COLOR_TEXT_SECONDARY, COLOR_TEXT_TERTIARY,
    COLOR_BTN_DANGER, CARD_BG, CARD_BORDER,
    FONT_SIZE_TITLE1, FONT_SIZE_BODY,
)
from src.utils import (
    blit_background, draw_card, draw_text_centered, get_font_manager, point_in_rect,
)
from src.i18n import t, set_language, get_language

ROW_HEIGHT = 52


class SettingsPage(Page):
    """设置页面 / Settings page"""

    def __init__(self) -> None:
        super().__init__("settings")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI - 表单卡片布局"""
        cx = WINDOW_WIDTH // 2

        self.title_label = Label(cx, 44, t("settings"), font_size=FONT_SIZE_TITLE1,
                                 color=COLOR_TEXT, bold=True, centered=True)

        # 设置卡片：3 行 + 2 按钮，高度贴合内容
        panel_w = 420
        panel_h = 20 + ROW_HEIGHT * 3 + 18 + 46 + 12 + 46 + 22
        panel_x = cx - panel_w // 2
        panel_y = 104
        self.panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

        padding = 22
        row1_y = panel_y + 8
        row2_y = row1_y + ROW_HEIGHT
        row3_y = row2_y + ROW_HEIGHT

        # 音效
        self.sound_label = Label(panel_x + padding, row1_y + 14,
                                 t("sound"), font_size=FONT_SIZE_BODY, color=COLOR_TEXT)
        self.btn_sound = iOSSwitch(
            panel_x + panel_w - padding - 51, row1_y + 10,
            51, 31, is_on=True, callback=self._on_toggle_sound,
        )

        # 音乐
        self.music_label = Label(panel_x + padding, row2_y + 14,
                                 t("music"), font_size=FONT_SIZE_BODY, color=COLOR_TEXT)
        self.btn_music = iOSSwitch(
            panel_x + panel_w - padding - 51, row2_y + 10,
            51, 31, is_on=True, callback=self._on_toggle_music,
        )

        # 语言（整行可点击切换）
        self.lang_label = Label(panel_x + padding, row3_y + 14,
                                t("language"), font_size=FONT_SIZE_BODY, color=COLOR_TEXT)
        self.lang_value = Label(0, 0, get_language().upper(), font_size=FONT_SIZE_BODY,
                                color=COLOR_TEXT_SECONDARY)
        self.lang_row_rect = pygame.Rect(panel_x, row3_y, panel_w, ROW_HEIGHT)
        self._update_lang_value_pos()

        # 操作按钮
        btn_y = row3_y + ROW_HEIGHT + 18
        self.btn_reset = Button(
            panel_x + padding, btn_y, panel_w - padding * 2, 46,
            t("reset_data"), font_size=FONT_SIZE_BODY,
            color=COLOR_BTN_DANGER, hover_color=(255, 112, 122),
            callback=self._on_reset,
        )
        self.btn_back = Button(
            panel_x + padding, btn_y + 58, panel_w - padding * 2, 46,
            t("back_to_menu"), font_size=FONT_SIZE_BODY,
            color=CARD_BG, hover_color=(66, 70, 116),
            text_color=COLOR_TEXT_SECONDARY, style="ghost", shadow=False,
            callback=self._on_back,
        )

        # 行分隔线位置（卡片内）
        self._separator_ys = [row1_y + ROW_HEIGHT, row2_y + ROW_HEIGHT]

        self.buttons = [self.btn_reset, self.btn_back]
        self.switches = [self.btn_sound, self.btn_music]
        self.labels = [self.sound_label, self.music_label, self.lang_label, self.lang_value]
        self._target_page = None

        # 重置确认弹窗
        self.alert = iOSAlert(
            title="确认重置",
            message=t("confirm_reset"),
            confirm_text=t("reset_data"),
            cancel_text=t("cancel"),
            on_confirm=self._on_confirm_reset,
            on_cancel=self._on_cancel_reset,
        )

    def _update_lang_value_pos(self) -> None:
        """语言值靠右对齐 / Align language value to the right"""
        rect = self.lang_row_rect
        self.lang_value.set_position(
            rect.right - 22 - self.lang_value.rect.width,
            rect.y + (rect.height - self.lang_value.rect.height) // 2,
        )

    def _on_toggle_sound(self, is_on: bool) -> None:
        """切换音效 / Toggle sound"""
        DataManager().update_setting("sound_enabled", is_on)

    def _on_toggle_music(self, is_on: bool) -> None:
        """切换音乐 / Toggle music"""
        DataManager().update_setting("music_enabled", is_on)

    def _on_toggle_lang(self) -> None:
        """切换语言 / Toggle language"""
        current = get_language()
        new_lang = "en" if current == "zh" else "zh"
        set_language(new_lang)
        self.lang_value.text = new_lang.upper()
        self.sound_label.text = t("sound")
        self.music_label.text = t("music")
        self.lang_label.text = t("language")
        self.title_label.text = t("settings")
        self._update_lang_value_pos()

    def _on_reset(self) -> None:
        """重置数据 / Reset data"""
        self.alert.show()

    def _on_confirm_reset(self) -> None:
        """确认重置 / Confirm reset"""
        DataManager().reset_data()
        self._load_settings()

    def _on_cancel_reset(self) -> None:
        """取消重置 / Cancel reset"""
        pass  # Alert 已自动隐藏

    def _on_back(self) -> None:
        """返回 / Go back"""
        self._target_page = "menu"

    def _load_settings(self) -> None:
        """加载设置 / Load settings"""
        dm = DataManager()
        settings = dm.get_settings()

        sound_enabled = settings.get("sound_enabled", True)
        music_enabled = settings.get("music_enabled", True)

        for switch, enabled in ((self.btn_sound, sound_enabled), (self.btn_music, music_enabled)):
            switch.is_on = enabled
            switch._target_x = switch.rect.x + 2 if not enabled else \
                switch.rect.x + switch.rect.width - 29
            switch._thumb_x = switch._target_x

        self.lang_value.text = get_language().upper()
        self._update_lang_value_pos()

    def on_enter(self, **kwargs: Any) -> None:
        """进入页面 / Enter page"""
        super().on_enter(**kwargs)
        self._target_page = None
        self._load_settings()

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """处理事件 / Handle event"""
        if self.alert.handle_event(event):
            return None

        # 语言行点击切换
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if point_in_rect(event.pos, self.lang_row_rect):
                self._on_toggle_lang()
                return None

        for btn in self.buttons:
            btn.handle_event(event)
        for switch in self.switches:
            switch.handle_event(event)

        return None

    def update(self, dt: float) -> Optional[str]:
        """更新 / Update"""
        for btn in self.buttons:
            btn.update(dt)
        for switch in self.switches:
            switch.update(dt)

        if self._target_page:
            target = self._target_page
            self._target_page = None
            return target
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """绘制设置页面 / Draw settings page"""
        blit_background(surface)

        self.title_label.draw(surface)
        draw_card(surface, self.panel_rect, 20)

        # 分隔线
        for sep_y in self._separator_ys:
            pygame.draw.line(surface, CARD_BORDER,
                             (self.panel_rect.x + 22, sep_y),
                             (self.panel_rect.right - 22, sep_y), width=1)

        # 语言行右侧提示可点击
        font_hint = get_font_manager().get_tiny()
        draw_text_centered(surface, "点击切换", font_hint, COLOR_TEXT_TERTIARY,
                           (self.panel_rect.right - 88, self.lang_row_rect.centery))

        for label in self.labels:
            label.draw(surface)
        for switch in self.switches:
            switch.draw(surface)
        for btn in self.buttons:
            btn.draw(surface)

        self.alert.draw(surface)
