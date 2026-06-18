# -*- coding: utf-8 -*-
# @Function: 游戏页面 - 计分、棋盘、道具栏、交互 / Game page - scoring, board, powerups, interaction

import pygame
import time
from typing import Optional, Any, Tuple

from src.views.pages.base_page import Page
from src.views.ui_components import Button, Label, ScoreBox
from src.views.board_view import BoardView
from src.models.game_state import GameState
from src.models.data_manager import DataManager
from src.models.achievements import check_achievements
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_TEXT,
    COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER,
    COLOR_BOARD_BG, SWIPE_THRESHOLD,
)
from src.utils import draw_rounded_rect, draw_text_centered, get_font_manager, format_time
from src.i18n import t
from src.views.sound_manager import get_sound_manager


class GamePage(Page):
    """游戏页面 / Game page"""

    def __init__(self) -> None:
        super().__init__("game")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI / Initialize UI"""
        cx = WINDOW_WIDTH // 2

        # 返回按钮
        self.btn_back = Button(
            20, 15, 80, 36, t("back"), font_size=16,
            color=COLOR_BTN_SECONDARY, hover_color=COLOR_BTN_SECONDARY_HOVER,
            callback=self._on_back,
        )

        # 分数框
        box_w, box_h = 130, 65
        gap = 15
        total_w = box_w * 2 + gap
        start_x = cx - total_w // 2

        self.score_box = ScoreBox(start_x, 12, box_w, box_h, t("current_score"), 0)
        self.best_box = ScoreBox(start_x + box_w + gap, 12, box_w, box_h, t("best_score"), 0)

        # 模式/时间/步数提示
        self.mode_label = Label(cx, 95, "", font_size=18, color=(120, 110, 100), centered=True)

        # 棋盘视图
        self.board_view = BoardView()

        # 道具栏 - 适配 600px 窗口高度
        props_y = 550
        btn_w, btn_h = 100, 40
        props_cx = cx
        props_start_x = props_cx - (btn_w * 3 + 15 * 2) // 2

        self.btn_undo = Button(
            props_start_x, props_y, btn_w, btn_h,
            t("undo"), font_size=18,
            color=COLOR_BTN_SECONDARY, hover_color=COLOR_BTN_SECONDARY_HOVER,
            callback=self._on_undo,
        )

        self.btn_clean = Button(
            props_start_x + btn_w + 15, props_y, btn_w, btn_h,
            t("clean"), font_size=18,
            color=COLOR_BTN_SECONDARY, hover_color=COLOR_BTN_SECONDARY_HOVER,
            callback=self._on_clean,
        )

        self.btn_revive = Button(
            props_start_x + (btn_w + 15) * 2, props_y, btn_w, btn_h,
            t("revive"), font_size=18,
            color=COLOR_BTN_SECONDARY, hover_color=COLOR_BTN_SECONDARY_HOVER,
            callback=self._on_revive,
        )

        # 道具次数标签
        self.undo_label = Label(props_start_x + btn_w // 2, props_y + 45, "x2", font_size=14,
                               color=(150, 140, 130), centered=True)
        self.clean_label = Label(props_start_x + btn_w + 15 + btn_w // 2, props_y + 45, "x0",
                                font_size=14, color=(150, 140, 130), centered=True)
        self.revive_label = Label(props_start_x + (btn_w + 15) * 2 + btn_w // 2, props_y + 45,
                                 "广告", font_size=14, color=(150, 140, 130), centered=True)

        self.buttons = [self.btn_back, self.btn_undo, self.btn_clean, self.btn_revive]

        # 触摸滑动状态
        self._swipe_start: Optional[Tuple[int, int]] = None
        self._game_state: Optional[GameState] = None
        self._target_page = None
        self._game_result = None

    def _on_back(self) -> None:
        """返回按钮 / Back button"""
        if self._game_state and self._game_state.state == GameState.STATE_PLAYING:
            self._game_state.pause()
        self._target_page = "menu"

    def _on_undo(self) -> None:
        """撤销道具 / Undo powerup"""
        if self._game_state:
            if self._game_state.undo():
                self._update_props_ui()
                get_sound_manager().play_sfx("undo")

    def _on_clean(self) -> None:
        """清理道具 / Clean powerup"""
        if self._game_state:
            if self._game_state.use_clean():
                self._update_props_ui()
                get_sound_manager().play_sfx("clean")

    def _on_revive(self) -> None:
        """复活（广告） / Revive via ad"""
        if not self._game_state or not self._game_state.board:
            return
        dm = DataManager()
        if not dm.can_watch_ad_watch():
            return
        # 模拟广告观看
        dm.record_ad_watch()
        self._game_state.is_ad_reward_used = True
        # 移除两个最小方块，让游戏继续
        self._game_state.board.clean_min_tile()
        self._game_state.board.clean_min_tile()
        self._game_state.board.is_game_over = False
        get_sound_manager().play_sfx("revive")

    def _update_props_ui(self) -> None:
        """更新道具 UI 显示 / Update powerup UI display"""
        if self._game_state:
            self.undo_label.set_text(f"x{self._game_state.undo_count}")
            self.clean_label.set_text(f"x{self._game_state.clean_count}")

    def on_enter(self, **kwargs: Any) -> None:
        """进入游戏页面 / Enter game page"""
        super().on_enter(**kwargs)
        self._target_page = None
        self._game_result = None

        # 创建游戏状态
        mode = kwargs.get("mode", "classic")
        self._game_state = GameState()
        self._game_state.start_game(mode=mode)

        # 更新 UI
        dm = DataManager()
        self.best_box.set_value(dm.get("high_score", 0))
        self.score_box.set_value(0)

        # 更新模式提示
        if mode == "timed":
            self.mode_label.set_text("限时模式 - 60秒内达到目标分数")
        elif mode == "challenge":
            self.mode_label.set_text("挑战模式 - 有限步数达到目标")
        else:
            self.mode_label.set_text("经典模式")

        self._update_props_ui()

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """处理事件 / Handle event"""
        # 按钮事件
        for btn in self.buttons:
            btn.handle_event(event)

        if not self._game_state or not self._game_state.board:
            return None

        # 键盘事件
        if event.type == pygame.KEYDOWN:
            direction_map = {
                pygame.K_UP: "up",
                pygame.K_DOWN: "down",
                pygame.K_LEFT: "left",
                pygame.K_RIGHT: "right",
                pygame.K_w: "up",
                pygame.K_s: "down",
                pygame.K_a: "left",
                pygame.K_d: "right",
            }
            if event.key in direction_map:
                self._do_move(direction_map[event.key])

        # 触摸/鼠标滑动
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._swipe_start = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self._swipe_start:
                self._handle_swipe(event.pos)
                self._swipe_start = None

        return None

    def _handle_swipe(self, end_pos: tuple) -> None:
        """处理滑动手势 / Handle swipe gesture"""
        if not self._swipe_start:
            return
        dx = end_pos[0] - self._swipe_start[0]
        dy = end_pos[1] - self._swipe_start[1]
        if abs(dx) < SWIPE_THRESHOLD and abs(dy) < SWIPE_THRESHOLD:
            return
        if abs(dx) > abs(dy):
            direction = "right" if dx > 0 else "left"
        else:
            direction = "down" if dy > 0 else "up"
        self._do_move(direction)

    def _do_move(self, direction: str) -> None:
        """执行移动 / Execute move"""
        if not self._game_state or self._game_state.state != GameState.STATE_PLAYING:
            return
        self._game_state.save_for_undo()
        moved = self._game_state.board.move(direction)
        if moved:
            self.board_view.start_move_animation(self._game_state.board)
            self.score_box.set_value(self._game_state.board.score)
            self._update_props_ui()
            # Play move sound effect
            sound_mgr = get_sound_manager()
            sound_mgr.play_sfx("move")
            # Check achievements
            dm = DataManager()
            new_ach = check_achievements(
                self._game_state.board.max_tile,
                dm.get("total_games", 0),
                self._game_state.board.score,
            )
            # Update game state
            self._game_state.update()
            # Check if game is over
            if self._game_state.state in (GameState.STATE_GAME_OVER, GameState.STATE_WIN):
                sound_mgr.play_sfx("game_over")
                self._save_game_result()

    def _save_game_result(self) -> None:
        """保存游戏结果 / Save game result"""
        if not self._game_state:
            return
        result = self._game_state.get_result()
        dm = DataManager()
        dm.increment_games()
        dm.update_high_score(result["score"])
        dm.update_max_tile(result["max_tile"])
        dm.update_mode_stats(result["mode"], result["score"])
        self._game_result = result
        # 延迟跳转到结算页面
        self._target_page = "result"

    def update(self, dt: float) -> Optional[str]:
        """更新 / Update"""
        if self._game_state:
            self._game_state.update()
        self.board_view.update(dt)
        self.score_box.update(dt)
        self.best_box.update(dt)

        for btn in self.buttons:
            btn.update(dt)

        if self._target_page:
            target = self._target_page
            self._target_page = None
            return target
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """绘制游戏页面 / Draw game page"""
        surface.fill(COLOR_BG)

        # 顶栏
        self.btn_back.draw(surface)
        self.score_box.draw(surface)
        self.best_box.draw(surface)

        # 模式提示
        self.mode_label.draw(surface)

        # 限时模式时间显示
        if self._game_state and self._game_state.mode == "timed":
            time_text = format_time(int(self._game_state.time_remaining))
            font = get_font_manager().get_small()
            draw_text_centered(surface, f"剩余时间: {time_text}", font,
                             (200, 80, 60), (WINDOW_WIDTH // 2, 510))

        # 棋盘
        if self._game_state and self._game_state.board:
            self.board_view.draw(surface, self._game_state.board)

        # 游戏结束覆盖层
        if self._game_state and self._game_state.state == GameState.STATE_GAME_OVER:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            surface.blit(overlay, (0, 0))
            font = get_font_manager().get_large(bold=True)
            draw_text_centered(surface, t("game_over"), font, (255, 255, 255),
                             (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            font_sm = get_font_manager().get_small()
            draw_text_centered(surface, "点击任意按钮继续", font_sm, (200, 200, 200),
                             (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))

        # 道具栏
        self.btn_undo.draw(surface)
        self.btn_clean.draw(surface)
        self.btn_revive.draw(surface)
        self.undo_label.draw(surface)
        self.clean_label.draw(surface)
        self.revive_label.draw(surface)

    def get_game_result(self) -> Optional[dict]:
        """获取游戏结果（供结算页面使用）/ Get game result (for result page)"""
        return self._game_result
