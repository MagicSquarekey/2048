# -*- coding: utf-8 -*-
# @Function: 设置页面

import pygame
from typing import Optional, Any

from src.views.pages.base_page import Page
from src.views.ui_components import Button, Label, Panel
from src.models.data_manager import DataManager
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_TEXT,
    COLOR_BTN_PRIMARY, COLOR_BTN_PRIMARY_HOVER,
    COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
    COLOR_BTN_DANGER, COLOR_BTN_DANGER_HOVER,
)
from src.utils import draw_rounded_rect, draw_text_centered, get_font_manager


class ToggleButton(Button):
    """开关按钮"""

    def __init__(self, x: int, y: int, width: int, height: int,
                 text: str, is_on: bool = True, **kwargs) -> None:
        super().__init__(x, y, width, height, text, **kwargs)
        self.is_on = is_on
        self._update_colors()

    def _update_colors(self) -> None:
        """根据开关状态更新颜色"""
        if self.is_on:
            self.color = (76, 175, 80)
            self.hover_color = (102, 187, 106)
            self.text = self.text.split(":")[0] + ": 开"
        else:
            self.color = (158, 158, 158)
            self.hover_color = (189, 189, 189)
            self.text = self.text.split(":")[0] + ": 关"

    def toggle(self) -> None:
        """切换开关状态"""
        self.is_on = not self.is_on
        self._update_colors()


class SettingsPage(Page):
    """设置页面"""

    def __init__(self) -> None:
        super().__init__("settings")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI"""
        cx = WINDOW_WIDTH // 2

        # 标题
        self.title_label = Label(cx, 40, "设置", font_size=36, color=(119, 110, 101),
                                bold=True, centered=True)

        # 设置面板
        panel_w, panel_h = 400, 400
        panel_x = cx - panel_w // 2
        panel_y = 100
        self.panel = Panel(panel_x, panel_y, panel_w, panel_h, (255, 255, 255), radius=16)

        # 音效开关
        btn_w, btn_h = 200, 44
        row_y = panel_y + 30
        row_gap = 55

        self.btn_sound = ToggleButton(
            cx - btn_w // 2, row_y, btn_w, btn_h,
            "音效: 开", font_size=20,
            color=(76, 175, 80), hover_color=(102, 187, 106),
            callback=self._on_toggle_sound,
        )

        self.btn_music = ToggleButton(
            cx - btn_w // 2, row_y + row_gap, btn_w, btn_h,
            "音乐: 开", font_size=20,
            color=(76, 175, 80), hover_color=(102, 187, 106),
            callback=self._on_toggle_music,
        )

        # 重置数据
        self.btn_reset = Button(
            cx - btn_w // 2, row_y + row_gap * 2, btn_w, btn_h,
            "重置游戏数据", font_size=20,
            color=COLOR_BTN_DANGER, hover_color=COLOR_BTN_DANGER_HOVER,
            callback=self._on_reset,
        )

        # 返回按钮
        self.btn_back = Button(
            cx - btn_w // 2, row_y + row_gap * 3 + 20, btn_w, btn_h,
            "返回主菜单", font_size=20,
            color=COLOR_BTN_SECONDARY, hover_color=COLOR_BTN_SECONDARY_HOVER,
            callback=self._on_back,
        )

        self.buttons = [self.btn_sound, self.btn_music, self.btn_reset, self.btn_back]
        self._target_page = None
        self._show_confirm = False

    def _on_toggle_sound(self) -> None:
        """切换音效"""
        self.btn_sound.toggle()
        dm = DataManager()
        dm.update_setting("sound_enabled", self.btn_sound.is_on)

    def _on_toggle_music(self) -> None:
        """切换音乐"""
        self.btn_music.toggle()
        dm = DataManager()
        dm.update_setting("music_enabled", self.btn_music.is_on)

    def _on_reset(self) -> None:
        """重置数据"""
        self._show_confirm = True

    def _on_confirm_reset(self) -> None:
        """确认重置"""
        dm = DataManager()
        dm.reset_data()
        self._show_confirm = False
        self._load_settings()

    def _on_cancel_reset(self) -> None:
        """取消重置"""
        self._show_confirm = False

    def _on_back(self) -> None:
        """返回"""
        self._target_page = "menu"

    def _load_settings(self) -> None:
        """加载设置"""
        dm = DataManager()
        settings = dm.get_settings()
        self.btn_sound.is_on = settings.get("sound_enabled", True)
        self.btn_sound._update_colors()
        self.btn_music.is_on = settings.get("music_enabled", True)
        self.btn_music._update_colors()

    def on_enter(self, **kwargs: Any) -> None:
        """进入页面"""
        super().on_enter(**kwargs)
        self._target_page = None
        self._show_confirm = False
        self._load_settings()

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """处理事件"""
        if self._show_confirm:
            # 确认对话框中只处理确认/取消按钮
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._show_confirm = False
            return None

        for btn in self.buttons:
            btn.handle_event(event)
        return None

    def update(self, dt: float) -> Optional[str]:
        """更新"""
        for btn in self.buttons:
            btn.update(dt)
        if self._target_page:
            target = self._target_page
            self._target_page = None
            return target
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """绘制设置页面"""
        surface.fill(COLOR_BG)

        # 标题
        self.title_label.draw(surface)

        # 面板
        self.panel.draw(surface)

        # 按钮
        for btn in self.buttons:
            btn.draw(surface)

        # 确认对话框
        if self._show_confirm:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            surface.blit(overlay, (0, 0))

            # 对话框
            dlg_w, dlg_h = 300, 160
            dlg_x = WINDOW_WIDTH // 2 - dlg_w // 2
            dlg_y = WINDOW_HEIGHT // 2 - dlg_h // 2
            draw_rounded_rect(surface, (255, 255, 255),
                            pygame.Rect(dlg_x, dlg_y, dlg_w, dlg_h), 12)

            font = get_font_manager().get_medium(bold=True)
            draw_text_centered(surface, "确认重置所有数据？", font, (200, 50, 50),
                             (WINDOW_WIDTH // 2, dlg_y + 45))

            font_sm = get_font_manager().get_small()
            draw_text_centered(surface, "点击任意位置取消", font_sm, (150, 150, 150),
                             (WINDOW_WIDTH // 2, dlg_y + 80))

            # 确认按钮
            btn_w, btn_h = 100, 36
            btn_y = dlg_y + dlg_h - 55
            confirm_rect = pygame.Rect(WINDOW_WIDTH // 2 - btn_w - 10, btn_y, btn_w, btn_h)
            draw_rounded_rect(surface, (200, 50, 50), confirm_rect, 8)
            draw_text_centered(surface, "确认重置", font_sm, (255, 255, 255),
                             confirm_rect.center)

            cancel_rect = pygame.Rect(WINDOW_WIDTH // 2 + 10, btn_y, btn_w, btn_h)
            draw_rounded_rect(surface, (158, 158, 158), cancel_rect, 8)
            draw_text_centered(surface, "取消", font_sm, (255, 255, 255),
                             cancel_rect.center)

            # 处理确认/取消点击
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0]:
                if confirm_rect.collidepoint(mouse_pos):
                    self._on_confirm_reset()
                elif cancel_rect.collidepoint(mouse_pos):
                    self._on_cancel_reset()
