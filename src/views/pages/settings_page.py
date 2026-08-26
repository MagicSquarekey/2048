# -*- coding: utf-8 -*-
# @Function: 设置页面 / Settings page

import pygame
from typing import Optional, Any

from src.views.pages.base_page import Page
from src.views.ui_components import Button, Label, Panel, iOSAlert, iOSSwitch
from src.models.data_manager import DataManager
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_TEXT,
    COLOR_TEXT_SECONDARY, COLOR_TEXT_TERTIARY,
    COLOR_BTN_PRIMARY, COLOR_BTN_PRIMARY_HOVER,
    COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
    COLOR_BTN_DANGER, COLOR_BTN_DANGER_HOVER,
    COLOR_GREEN, COLOR_OVERLAY, COLOR_BOARD_BG,
    FONT_SIZE_TITLE1, FONT_SIZE_BODY, FONT_SIZE_FOOTNOTE,
)
from src.utils import draw_rounded_rect, draw_text_centered, get_font_manager
from src.i18n import t, set_language, get_language


class SettingsPage(Page):
    """设置页面 / Settings page"""

    def __init__(self) -> None:
        super().__init__("settings")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI - iOS表单列表样式"""
        cx = WINDOW_WIDTH // 2

        # 标题 (iOS Title 1: 28pt)
        self.title_label = Label(cx, 40, t("settings"), font_size=FONT_SIZE_TITLE1, color=COLOR_TEXT,
                                bold=True, centered=True)

        # 设置面板 - iOS表单列表样式
        panel_w, panel_h = 400, 400
        panel_x = cx - panel_w // 2
        panel_y = 90
        self.panel = Panel(panel_x, panel_y, panel_w, panel_h, COLOR_BOARD_BG, radius=16)

        # iOS表单列表布局参数
        row_height = 44  # iOS标准行高
        padding_left = 20
        padding_right = 20
        separator_y = panel_y + row_height  # 分隔线位置

        # === 第一组：音效和音乐开关 ===
        group1_y = panel_y

        # 音效 - 左文字+右控件
        self.sound_label = Label(
            panel_x + padding_left, group1_y + 13,
            t("sound"), font_size=FONT_SIZE_BODY, color=COLOR_TEXT
        )
        self.btn_sound = iOSSwitch(
            panel_x + panel_w - padding_right - 51, group1_y + 7,
            51, 31, is_on=True, callback=self._on_toggle_sound,
        )

        # 分隔线1
        self.separator1_y = group1_y + row_height

        # 音乐 - 左文字+右控件
        self.music_label = Label(
            panel_x + padding_left, group1_y + row_height + 13,
            t("music"), font_size=FONT_SIZE_BODY, color=COLOR_TEXT
        )
        self.btn_music = iOSSwitch(
            panel_x + panel_w - padding_right - 51, group1_y + row_height + 7,
            51, 31, is_on=True, callback=self._on_toggle_music,
        )

        # 分隔线2
        self.separator2_y = group1_y + row_height * 2

        # === 第二组：语言切换 ===
        group2_y = group1_y + row_height * 2
        lang = get_language()
        self.lang_label = Label(
            panel_x + padding_left, group2_y + 13,
            t("language"), font_size=FONT_SIZE_BODY, color=COLOR_TEXT
        )
        self.lang_value = Label(
            panel_x + panel_w - padding_right - 60, group2_y + 13,
            lang.upper(), font_size=FONT_SIZE_BODY, color=COLOR_TEXT_SECONDARY
        )

        # 分隔线3
        self.separator3_y = group2_y + row_height

        # === 第三组：重置数据 ===
        group3_y = group2_y + row_height
        self.btn_reset = Button(
            panel_x + padding_left, group3_y + 4,
            panel_w - padding_left * 2, 36,
            t("reset_data"), font_size=FONT_SIZE_BODY,
            color=COLOR_BTN_DANGER, hover_color=COLOR_BTN_DANGER_HOVER,
            callback=self._on_reset,
        )

        # 分隔线4
        self.separator4_y = group3_y + row_height

        # === 第四组：返回按钮 ===
        group4_y = group3_y + row_height
        self.btn_back = Button(
            panel_x + padding_left, group4_y + 4,
            panel_w - padding_left * 2, 36,
            t("back_to_menu"), font_size=FONT_SIZE_BODY,
            color=COLOR_BTN_PRIMARY, hover_color=COLOR_BTN_PRIMARY_HOVER,
            text_color=(255, 255, 255),  # 白色文字，确保对比度
            callback=self._on_back,
        )

        # 组件列表
        self.buttons = [self.btn_reset, self.btn_back]
        self.switches = [self.btn_sound, self.btn_music]
        self.labels = [self.sound_label, self.music_label, self.lang_label, self.lang_value]
        self._target_page = None

        # iOS Alert 弹窗
        self.alert = iOSAlert(
            title="确认重置",
            message="确认要重置所有数据吗？",
            confirm_text="确认重置",
            cancel_text=t("cancel"),
            on_confirm=self._on_confirm_reset,
            on_cancel=self._on_cancel_reset,
        )

    def _on_toggle_sound(self, is_on: bool) -> None:
        """切换音效 / Toggle sound"""
        dm = DataManager()
        dm.update_setting("sound_enabled", is_on)

    def _on_toggle_music(self, is_on: bool) -> None:
        """切换音乐 / Toggle music"""
        dm = DataManager()
        dm.update_setting("music_enabled", is_on)

    def _on_toggle_lang(self) -> None:
        """切换语言 / Toggle language"""
        current = get_language()
        new_lang = "en" if current == "zh" else "zh"
        set_language(new_lang)
        # 更新语言显示
        self.lang_value.text = new_lang.upper()
        # 刷新标签文本
        self.sound_label.text = t("sound")
        self.music_label.text = t("music")
        # 刷新标题
        self.title_label.text = t("settings")

    def _on_reset(self) -> None:
        """重置数据 / Reset data"""
        self.alert.show()

    def _on_confirm_reset(self) -> None:
        """确认重置 / Confirm reset"""
        dm = DataManager()
        dm.reset_data()
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
        
        # 更新开关状态
        sound_enabled = settings.get("sound_enabled", True)
        music_enabled = settings.get("music_enabled", True)
        
        self.btn_sound.is_on = sound_enabled
        self.btn_sound._target_x = self.btn_sound.rect.x + 2 if not sound_enabled else self.btn_sound.rect.x + self.btn_sound.rect.width - 29
        self.btn_sound._thumb_x = self.btn_sound._target_x
        
        self.btn_music.is_on = music_enabled
        self.btn_music._target_x = self.btn_music.rect.x + 2 if not music_enabled else self.btn_music.rect.x + self.btn_music.rect.width - 29
        self.btn_music._thumb_x = self.btn_music._target_x
        
        # 更新语言显示
        lang = get_language()
        self.lang_value.text = lang.upper()

    def on_enter(self, **kwargs: Any) -> None:
        """进入页面 / Enter page"""
        super().on_enter(**kwargs)
        self._target_page = None
        self._load_settings()

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """处理事件 / Handle event"""
        # 处理 Alert 事件
        if self.alert.handle_event(event):
            return None

        # 处理按钮事件
        for btn in self.buttons:
            btn.handle_event(event)
        
        # 处理开关事件
        for switch in self.switches:
            switch.handle_event(event)
        
        return None

    def update(self, dt: float) -> Optional[str]:
        """更新 / Update"""
        # 更新按钮
        for btn in self.buttons:
            btn.update(dt)
        
        # 更新开关
        for switch in self.switches:
            switch.update(dt)
        
        if self._target_page:
            target = self._target_page
            self._target_page = None
            return target
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """绘制设置页面 - iOS表单列表样式"""
        surface.fill(COLOR_BG)

        # 标题
        self.title_label.draw(surface)

        # 面板
        self.panel.draw(surface)

        # 绘制iOS风格分隔线（浅灰色，左对齐）
        separator_color = (209, 209, 214)  # iOS Gray
        panel_x = self.panel.rect.x
        panel_w = self.panel.rect.width
        
        for sep_y in [self.separator1_y, self.separator2_y, self.separator3_y]:
            pygame.draw.line(
                surface, separator_color,
                (panel_x + 20, sep_y),
                (panel_x + panel_w - 20, sep_y),
                width=1
            )

        # 标签
        for label in self.labels:
            label.draw(surface)

        # 开关
        for switch in self.switches:
            switch.draw(surface)

        # 按钮
        for btn in self.buttons:
            btn.draw(surface)

        # iOS Alert 弹窗
        self.alert.draw(surface)
