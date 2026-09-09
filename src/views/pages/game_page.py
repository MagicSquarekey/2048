# -*- coding: utf-8 -*-
# @Function: 游戏页面 - 计分、棋盘、道具栏、交互 / Game page - scoring, board, powerups, interaction

import pygame
from typing import Optional, Any, Tuple

from src.views.pages.base_page import Page
from src.views.ui_components import Button, ScoreBox
from src.views.board_view import BoardView, TileRenderer
from src.models.game_state import GameState
from src.models.data_manager import DataManager
from src.models.achievements import check_achievements
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_TEXT, COLOR_TEXT_SECONDARY,
    COLOR_TEXT_TERTIARY, ACCENT_BLUE, ACCENT_ORANGE, ACCENT_GREEN, ACCENT_GOLD,
    CARD_BG, CARD_BORDER, SWIPE_THRESHOLD,
    INPUT_QUEUE_MAX, INPUT_APPLY_PROGRESS,
    FONT_SIZE_SUBHEAD, FONT_SIZE_BODY, FONT_SIZE_FOOTNOTE, FONT_SIZE_LARGE_TITLE,
)
from src.utils import (
    blit_background, blit_overlay, draw_card, draw_text_centered, get_font_manager, format_time,
)
from src.i18n import t
from src.views.sound_manager import get_sound_manager

# 漂浮分数存活时长（秒）
_FLOAT_LIFE = 0.7


class _ScoreFloater:
    """合并得分漂浮文字 / Floating '+N' score text on merge"""

    def __init__(self, text: str, center: Tuple[int, int]) -> None:
        self.text = text
        self.x, self.y = center
        self.life = _FLOAT_LIFE

    @property
    def dead(self) -> bool:
        return self.life <= 0

    def update(self, dt: float) -> None:
        self.life -= dt
        self.y -= 34 * dt

    def draw(self, surface: pygame.Surface) -> None:
        alpha = max(0, min(255, int(255 * (self.life / _FLOAT_LIFE))))
        font = get_font_manager().get_font(20, bold=True)
        text = font.render(self.text, True, ACCENT_GOLD)
        text.set_alpha(alpha)
        surface.blit(text, text.get_rect(center=(self.x, self.y)))


class GamePage(Page):
    """游戏页面 / Game page"""

    def __init__(self) -> None:
        super().__init__("game")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化 UI / Initialize UI"""
        cx = WINDOW_WIDTH // 2

        # 返回按钮（玻璃胶囊）
        self.btn_back = Button(
            20, 20, 88, 40, "← 返回", font_size=15,
            color=CARD_BG, hover_color=(66, 70, 116),
            text_color=COLOR_TEXT_SECONDARY, style="ghost", shadow=False,
            callback=self._on_back,
        )

        # 分数卡片（当前分蓝 / 最高分橙）
        box_w, box_h = 132, 60
        gap = 16
        total_w = box_w * 2 + gap
        start_x = cx - total_w // 2

        self.score_box = ScoreBox(start_x, 14, box_w, box_h, t("current_score"), 0,
                                  title_color=COLOR_TEXT_TERTIARY, value_color=ACCENT_BLUE)
        self.best_box = ScoreBox(start_x + box_w + gap, 14, box_w, box_h, t("best_score"), 0,
                                 title_color=COLOR_TEXT_TERTIARY, value_color=ACCENT_ORANGE)

        # 模式信息胶囊（y=84，棋盘 118 之前）
        self._chip_rect = pygame.Rect(0, 82, 240, 26)
        self._chip_rect.centerx = cx
        self._chip_text = ""

        # 棋盘视图
        self.board_view = BoardView()

        # 道具栏（玻璃按钮，复活为主按钮样式）
        props_y = 552
        btn_w, btn_h = 110, 40
        btn_gap = 14
        props_start_x = cx - (btn_w * 3 + btn_gap * 2) // 2

        self.btn_undo = Button(
            props_start_x, props_y, btn_w, btn_h,
            f"{t('undo')} ×2", font_size=FONT_SIZE_BODY,
            color=CARD_BG, hover_color=(66, 70, 116),
            text_color=COLOR_TEXT, style="ghost", shadow=False,
            callback=self._on_undo,
        )

        self.btn_clean = Button(
            props_start_x + btn_w + btn_gap, props_y, btn_w, btn_h,
            f"{t('clean')} ×0", font_size=FONT_SIZE_BODY,
            color=CARD_BG, hover_color=(66, 70, 116),
            text_color=COLOR_TEXT, style="ghost", shadow=False,
            callback=self._on_clean,
        )

        self.btn_revive = Button(
            props_start_x + (btn_w + btn_gap) * 2, props_y, btn_w, btn_h,
            t("revive"), font_size=FONT_SIZE_BODY,
            color=ACCENT_GREEN, hover_color=(96, 236, 190),
            style="primary", shadow=True,
            callback=self._on_revive,
        )

        self.buttons = [self.btn_back, self.btn_undo, self.btn_clean, self.btn_revive]

        # 触摸滑动状态
        self._swipe_start: Optional[Tuple[int, int]] = None
        self._game_state: Optional[GameState] = None
        self._target_page = None
        self._game_result = None

        # 操作流畅度：输入队列 + 结束过渡
        self._input_queue = []
        self._floaters = []
        self._ending = False
        self._end_timer = 0.0

    def _on_back(self) -> None:
        """返回按钮 / Back button"""
        if self._game_state and self._game_state.state == GameState.STATE_PLAYING:
            self._game_state.pause()
        self._target_page = "menu"

    def _on_undo(self) -> None:
        """撤销道具 / Undo powerup"""
        if self._ending:
            return
        if self._game_state:
            if self._game_state.undo():
                self._update_props_ui()
                self.score_box.set_value(self._game_state.board.score)
                get_sound_manager().play_sfx("prop")

    def _on_clean(self) -> None:
        """清理道具 / Clean powerup"""
        if self._ending:
            return
        if self._game_state:
            if self._game_state.use_clean():
                self._update_props_ui()
                get_sound_manager().play_sfx("prop")

    def _on_revive(self) -> None:
        """复活（广告） / Revive via ad"""
        gs = self._game_state
        if not gs or not gs.board:
            return
        if gs.state not in (GameState.STATE_GAME_OVER, GameState.STATE_WIN):
            return
        dm = DataManager()
        if not dm.can_watch_ad():
            return
        dm.record_ad_watch()
        gs.is_ad_reward_used = True
        if gs.state == GameState.STATE_WIN:
            # 胜利后复活 = 继续，保留 is_win 结果
            gs.board.continue_after_win()
        else:
            # 失败后复活 = 移除两个最小方块腾出空间
            gs.board.clean_min_tile()
            gs.board.clean_min_tile()
            gs.board.is_game_over = False
        gs.state = GameState.STATE_PLAYING
        self._ending = False
        get_sound_manager().play_sfx("prop")

    def _update_props_ui(self) -> None:
        """更新道具 UI 显示（次数并入按钮文字）/ Update powerup UI display"""
        if self._game_state:
            self.btn_undo.text = f"{t('undo')} ×{self._game_state.undo_count}"
            self.btn_clean.text = f"{t('clean')} ×{self._game_state.clean_count}"

    def on_enter(self, **kwargs: Any) -> None:
        """进入游戏页面 / Enter game page"""
        super().on_enter(**kwargs)
        self._target_page = None
        self._game_result = None
        self._input_queue = []
        self._floaters = []
        self._ending = False
        self._end_timer = 0.0

        mode = kwargs.get("mode", "classic")
        self._game_state = GameState()
        self._game_state.start_game(mode=mode)

        dm = DataManager()
        self.best_box.set_value(dm.get("high_score", 0))
        self.score_box.set_value(0)
        self._update_props_ui()

    def _update_mode_chip(self) -> None:
        """更新模式信息胶囊文字 / Update mode chip text"""
        gs = self._game_state
        if not gs:
            self._chip_text = ""
            return
        if gs.mode == "timed":
            self._chip_text = f"限时模式 · 剩余 {format_time(int(gs.time_remaining))}"
        elif gs.mode == "challenge":
            remain = max(0, gs.move_limit - (gs.board.move_count if gs.board else 0))
            self._chip_text = f"挑战模式 · 剩余 {remain} 步"
        else:
            self._chip_text = "经典模式"

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """处理事件 / Handle event"""
        for btn in self.buttons:
            btn.handle_event(event)

        if not self._game_state or not self._game_state.board:
            return None

        if event.type == pygame.KEYDOWN:
            direction_map = {
                pygame.K_UP: "up", pygame.K_DOWN: "down",
                pygame.K_LEFT: "left", pygame.K_RIGHT: "right",
                pygame.K_w: "up", pygame.K_s: "down",
                pygame.K_a: "left", pygame.K_d: "right",
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
        """
        请求移动（输入队列入口）/ Request a move (input queue entry)

        动画进行中且进度未过阈值时缓存输入，动画临近结束时立即连击，
        保证快速连续操作不丢步、视觉不跳变。
        """
        if not self._game_state or self._game_state.state != GameState.STATE_PLAYING:
            return
        if self._ending:
            return

        bv = self.board_view
        if bv.is_animating and bv.animation_progress() < INPUT_APPLY_PROGRESS:
            if len(self._input_queue) < INPUT_QUEUE_MAX and \
               (not self._input_queue or self._input_queue[-1] != direction):
                self._input_queue.append(direction)
            return

        self._execute_move(direction)

    def _begin_ending(self) -> None:
        """进入结束过渡：停留展示盘面后再跳结算 / Begin game-over transition"""
        get_sound_manager().play_sfx("game_over")
        self._ending = True
        self._end_timer = 1.0
        self._input_queue = []

    def _execute_move(self, direction: str) -> None:
        """立即执行移动 / Execute the move immediately"""
        gs = self._game_state
        if not gs or gs.state != GameState.STATE_PLAYING:
            return
        # 若上一轮动画仍在收尾，直接定格，避免视觉回跳
        self.board_view.finish()
        gs.save_for_undo()
        moved = gs.board.move(direction)
        if not moved:
            return

        self.board_view.start_move_animation(gs.board)
        self.score_box.set_value(gs.board.score)
        self._update_props_ui()
        get_sound_manager().play_sfx("move")

        # 合并位置生成 "+N" 漂浮分数
        for tile in gs.board.get_all_tiles():
            if tile.merged_from:
                cell = TileRenderer.get_tile_rect(tile.row, tile.col)
                self._floaters.append(
                    _ScoreFloater(f"+{tile.value}", (cell.centerx, cell.y + 22))
                )

        dm = DataManager()
        new_ach = check_achievements(
            gs.board.max_tile,
            dm.get("total_games", 0),
            gs.board.score,
        )

        gs.update()
        if gs.state in (GameState.STATE_GAME_OVER, GameState.STATE_WIN):
            self._begin_ending()

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

        # 漂浮分数
        for f in self._floaters:
            f.update(dt)
        self._floaters = [f for f in self._floaters if not f.dead]

        # 输入队列：动画临近结束时应用下一条输入（连击不丢步）
        bv = self.board_view
        if self._input_queue and (not bv.is_animating or
                                  bv.animation_progress() >= INPUT_APPLY_PROGRESS):
            direction = self._input_queue.pop(0)
            self._execute_move(direction)

        # 非移动路径触发的结束（限时超时/挑战步数用尽等）同样走过渡
        gs = self._game_state
        if gs and gs.state in (GameState.STATE_GAME_OVER, GameState.STATE_WIN) \
                and not self._ending and self._game_result is None:
            self._begin_ending()

        # 结束过渡：停留片刻让玩家看清盘面，再进入结算
        if self._ending:
            self._end_timer -= dt
            if self._end_timer <= 0:
                self._ending = False
                self._save_game_result()

        self._update_mode_chip()

        if self._target_page:
            target = self._target_page
            self._target_page = None
            return target
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """绘制游戏页面 / Draw game page"""
        blit_background(surface)

        # 顶栏
        self.btn_back.draw(surface)
        self.score_box.draw(surface)
        self.best_box.draw(surface)

        # 模式信息胶囊
        if self._chip_text:
            font = get_font_manager().get_font(FONT_SIZE_FOOTNOTE)
            text_w = font.size(self._chip_text)[0]
            chip = self._chip_rect.copy()
            chip.width = max(chip.width, text_w + 28)
            chip.centerx = self._chip_rect.centerx
            draw_card(surface, chip, chip.height // 2, bg=CARD_BG)
            draw_text_centered(surface, self._chip_text, font,
                               COLOR_TEXT_SECONDARY, chip.center)

        # 棋盘
        if self._game_state and self._game_state.board:
            self.board_view.draw(surface, self._game_state.board)

        # 漂浮分数（画在棋盘之上、遮罩之下）
        for f in self._floaters:
            f.draw(surface)

        # 道具栏
        for btn in (self.btn_undo, self.btn_clean, self.btn_revive):
            btn.draw(surface)

        # 结束过渡遮罩（停留展示盘面与结果）
        gs = self._game_state
        if gs and (self._ending or gs.state == GameState.STATE_GAME_OVER):
            is_win = gs.state == GameState.STATE_WIN
            blit_overlay(surface, 120)

            title = "你赢了！" if is_win else t("game_over")
            font_big = get_font_manager().get_font(FONT_SIZE_LARGE_TITLE, bold=True)
            draw_text_centered(surface, title, font_big, COLOR_TEXT,
                             (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 24))
            font_sm = get_font_manager().get_font(FONT_SIZE_SUBHEAD)
            draw_text_centered(surface, f"最终得分 {gs.board.score}", font_sm,
                             ACCENT_GOLD if is_win else COLOR_TEXT_SECONDARY,
                             (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 24))

    def get_game_result(self) -> Optional[dict]:
        """获取游戏结果（供结算页面使用）/ Get game result (for result page)"""
        return self._game_result
