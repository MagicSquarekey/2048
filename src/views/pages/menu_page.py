# -*- coding: utf-8 -*-
# @Function: 主菜单页面 / Main menu page - 深空霓虹主题

import pygame
from typing import Optional, Any

from src.views.pages.base_page import Page
from src.views.ui_components import Button, Label, ScoreBox
from src.models.data_manager import DataManager
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_TEXT, COLOR_TEXT_SECONDARY,
    COLOR_TEXT_TERTIARY, ACCENT_BLUE, ACCENT_ORANGE,
    CARD_BG, CARD_BG_LIGHT, CARD_BORDER,
    MODE_CONFIG,
    FONT_SIZE_SUBHEAD, FONT_SIZE_BODY, FONT_SIZE_FOOTNOTE,
)
from src.utils import (
    blit_background, draw_card, draw_glow, draw_gradient_rounded_rect,
    draw_text_centered, get_font_manager, lighten, point_in_rect,
)
from src.i18n import t


class ModeCard:
    """模式选择卡片：图标 + 名称 + 描述 + 箭头，带悬停/按压反馈"""

    def __init__(self, x: int, y: int, w: int, h: int, mode_key: str, callback) -> None:
        cfg = MODE_CONFIG[mode_key]
        self.rect = pygame.Rect(x, y, w, h)
        self.accent = cfg["accent"]
        self.icon = cfg["icon"]
        self.name = cfg["name"]
        self.desc = cfg["description"]
        self.callback = callback
        self.is_hovered = False
        self.is_pressed = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = point_in_rect(event.pos, self.rect)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed:
                self.is_pressed = False
                if self.is_hovered:
                    self.callback()
                    return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        r = self.rect
        bg = CARD_BG_LIGHT if self.is_hovered else CARD_BG
        offset = 1 if self.is_pressed else 0
        draw_rect = r.move(0, offset)
        if self.is_hovered:
            draw_glow(surface, draw_rect, self.accent, alpha=30, blur=10, radius=16)
        draw_card(surface, draw_rect, 16, bg=bg)

        # 图标贴片（模式强调色渐变圆角块）
        icon_rect = pygame.Rect(r.x + 14, r.y + (r.height - 40) // 2 - offset, 40, 40)
        draw_gradient_rounded_rect(surface, icon_rect, lighten(self.accent, 1.2), self.accent, 12)
        font_icon = get_font_manager().get_font(17 if len(self.icon) > 2 else 19, bold=True)
        draw_text_centered(surface, self.icon, font_icon, (255, 255, 255), icon_rect.center)

        # 名称 + 描述（左对齐，避免与图标重叠）
        font_name = get_font_manager().get_font(FONT_SIZE_BODY, bold=True)
        name_surf = font_name.render(self.name, True, COLOR_TEXT)
        surface.blit(name_surf, (r.x + 76, r.y + 12 - offset))
        font_desc = get_font_manager().get_font(FONT_SIZE_FOOTNOTE)
        desc_surf = font_desc.render(self.desc, True, COLOR_TEXT_TERTIARY)
        surface.blit(desc_surf, (r.x + 77, r.y + 36 - offset))

        # 右侧箭头
        font_arrow = get_font_manager().get_font(20, bold=True)
        draw_text_centered(surface, "›", font_arrow,
                           self.accent if self.is_hovered else COLOR_TEXT_TERTIARY,
                           (r.right - 28, r.centery - offset))


class MenuPage(Page):
    """主菜单页面 / Main menu page"""

    def __init__(self) -> None:
        super().__init__("menu")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI 元素 / Initialize UI elements"""
        cx = WINDOW_WIDTH // 2

        # Logo：四枚迷你方块贴片拼出 2048（交替错位，游戏感）
        self._logo_tiles = []
        logo_values = [2, 0, 4, 8]
        logo_colors = {2: (110, 114, 158), 0: ACCENT_ORANGE,
                       4: (140, 145, 196), 8: ACCENT_BLUE}
        tile_s, tile_gap = 48, 8
        total_w = tile_s * 4 + tile_gap * 3
        start_x = cx - total_w // 2
        for i, v in enumerate(logo_values):
            x = start_x + i * (tile_s + tile_gap)
            y = 36 + (6 if i % 2 else 0)
            self._logo_tiles.append((pygame.Rect(x, y, tile_s, tile_s), str(v), logo_colors[v]))

        # 副标题
        self.subtitle_label = Label(
            cx, 116, "挑战你的数字极限",
            font_size=FONT_SIZE_SUBHEAD, color=COLOR_TEXT_SECONDARY, centered=True,
        )

        # 分数显示区
        box_w, box_h = 130, 64
        gap = 20
        total_w = box_w * 3 + gap * 2
        start_x = cx - total_w // 2
        y = 140

        self.score_box = ScoreBox(
            start_x, y, box_w, box_h, t("current_score"), 0,
            title_color=COLOR_TEXT_TERTIARY, value_color=ACCENT_BLUE,
        )
        self.best_box = ScoreBox(
            start_x + box_w + gap, y, box_w, box_h, t("best_score"), 0,
            title_color=COLOR_TEXT_TERTIARY, value_color=ACCENT_ORANGE,
        )
        self.games_box = ScoreBox(
            start_x + (box_w + gap) * 2, y, box_w, box_h, t("total_games"), 0,
            title_color=COLOR_TEXT_TERTIARY, value_color=COLOR_TEXT,
        )

        # 三张模式卡片
        card_w, card_h, card_gap = 440, 64, 14
        card_x = cx - card_w // 2
        card_y0 = 232
        self.mode_cards = [
            ModeCard(card_x, card_y0 + i * (card_h + card_gap), card_w, card_h,
                     key, lambda k=key: self._on_btn_click(k))
            for i, key in enumerate(("classic", "timed", "challenge"))
        ]

        # 次要按钮 - 并排两个玻璃胶囊
        btn_sm_w, btn_sm_h = 160, 46
        btn_sm_gap = 20
        btn_sm_y = card_y0 + (card_h + card_gap) * 3 + 10

        self.btn_settings = Button(
            cx - btn_sm_w - btn_sm_gap // 2, btn_sm_y, btn_sm_w, btn_sm_h,
            t("settings"), font_size=FONT_SIZE_BODY,
            color=CARD_BG, hover_color=CARD_BG_LIGHT,
            text_color=COLOR_TEXT_SECONDARY, style="ghost", shadow=False,
            callback=lambda: self._on_btn_click("settings"),
        )

        self.btn_achievements = Button(
            cx + btn_sm_gap // 2, btn_sm_y, btn_sm_w, btn_sm_h,
            t("achievements"), font_size=FONT_SIZE_BODY,
            color=CARD_BG, hover_color=CARD_BG_LIGHT,
            text_color=COLOR_TEXT_SECONDARY, style="ghost", shadow=False,
            callback=lambda: self._on_btn_click("achievements"),
        )

        self.buttons = [self.btn_settings, self.btn_achievements]
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
        for card in self.mode_cards:
            card.handle_event(event)
        for btn in self.buttons:
            btn.handle_event(event)
        return None

    def update(self, dt: float) -> Optional[str]:
        """更新 / Update"""
        self.best_box.update(dt)
        self.games_box.update(dt)

        if self._target_page:
            target = self._target_page
            self._target_page = None
            return target
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """绘制菜单页面 / Draw menu page"""
        blit_background(surface)

        # Logo 贴片（辉光 + 渐变 + 悬浮数字）
        font_logo = get_font_manager().get_font(24, bold=True)
        for rect, text, color in self._logo_tiles:
            draw_glow(surface, rect, color, alpha=34, blur=8, radius=12)
            draw_gradient_rounded_rect(surface, rect, lighten(color, 1.25), color, 12)
            draw_text_centered(surface, text, font_logo, (255, 255, 255), rect.center)

        self.subtitle_label.draw(surface)

        self.score_box.draw(surface)
        self.best_box.draw(surface)
        self.games_box.draw(surface)

        for card in self.mode_cards:
            card.draw(surface)

        for btn in self.buttons:
            btn.draw(surface)

        # 底部提示
        font = get_font_manager().get_tiny()
        draw_text_centered(
            surface, "方向键 / WASD / 鼠标滑动 操作方块 · ESC 暂停",
            font, COLOR_TEXT_TERTIARY,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20),
        )
