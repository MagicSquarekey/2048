# -*- coding: utf-8 -*-
# @Function: 游戏页面 - 计分、棋盘、道具栏、交互 / Game page - scoring, board, powerups, interaction

import math
import pygame
from typing import Optional, Any, Tuple

from src.views.pages.base_page import Page
from src.views.ui_components import Button, ScoreBox
from src.views.board_view import BoardView, TileRenderer
from src.views.effects import ParticleSystem
from src.models.game_state import GameState
from src.models.data_manager import DataManager
from src.models.achievements import check_achievements
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_TEXT, COLOR_TEXT_SECONDARY,
    COLOR_TEXT_TERTIARY, ACCENT_BLUE, ACCENT_ORANGE, ACCENT_GREEN, ACCENT_GOLD,
    ACCENT_PINK, CARD_BG, SWIPE_THRESHOLD,
    INPUT_QUEUE_MAX, INPUT_APPLY_PROGRESS,
    PARTICLE_MERGE_COUNT, SHAKE_MIN_TILE, SHAKE_DURATION, SHAKE_AMPLITUDE,
    GAME_OVER_PAUSE,
    FONT_SIZE_SUBHEAD, FONT_SIZE_BODY, FONT_SIZE_FOOTNOTE, FONT_SIZE_LARGE_TITLE,
)
from src.utils import (
    blit_background, blit_overlay, draw_card, draw_glow, draw_text_centered,
    get_font_manager, format_time,
)
from src.i18n import t
from src.views.sound_manager import get_sound_manager

# 漂浮分数存活时长（秒）
_FLOAT_LIFE = 0.7
# 漂浮分数文字渲染缓存 {文字: (字号, Surface)}
_float_text_cache: dict = {}


class _ScoreFloater:
    """合并得分漂浮文字（先弹出后上浮淡出）/ Floating '+N' score text"""

    def __init__(self, text: str, center: Tuple[int, int]) -> None:
        self.text = text
        self.x, self.y = center
        self.age = 0.0
        self.life = _FLOAT_LIFE

    @property
    def dead(self) -> bool:
        return self.life <= 0

    def update(self, dt: float) -> None:
        self.age += dt
        self.life -= dt
        self.y -= 34 * dt

    def draw(self, surface: pygame.Surface) -> None:
        alpha = max(0, min(255, int(255 * (self.life / _FLOAT_LIFE))))
        # 弹出：前 0.16s 字号从 26 弹到 20（ease-out 观感）
        pop = max(0.0, 1.0 - self.age / 0.16)
        size = 20 + int(6 * pop)
        entry = _float_text_cache.get(self.text)
        if entry is None or entry[0] != size:
            font = get_font_manager().get_font(size, bold=True)
            entry = (size, font.render(self.text, True, ACCENT_GOLD))
            _float_text_cache[self.text] = entry
        text = entry[1].copy()
        text.set_alpha(alpha)
        surface.blit(text, text.get_rect(center=(int(self.x), int(self.y))))


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
            20, 20, 88, 40, t("back"), font_size=15,
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

        # 模式信息胶囊（y=82，棋盘 118 之前）
        self._chip_rect = pygame.Rect(0, 82, 240, 26)
        self._chip_rect.centerx = cx
        self._chip_text = ""

        # 棋盘视图
        self.board_view = BoardView()

        # 特效：粒子系统
        self.particles = ParticleSystem()

        # 道具栏（玻璃按钮，复活为主按钮样式）
        props_y = 552
        btn_w, btn_h = 110, 40
        btn_gap = 14
        props_start_x = cx - (btn_w * 3 + btn_gap * 2) // 2

        self.btn_undo = Button(
            props_start_x, props_y, btn_w, btn_h,
            f"{t('undo')} ×3", font_size=FONT_SIZE_BODY,
            color=CARD_BG, hover_color=(66, 70, 116),
            text_color=COLOR_TEXT, style="ghost", shadow=False,
            callback=self._on_undo,
        )

        self.btn_clean = Button(
            props_start_x + btn_w + btn_gap, props_y, btn_w, btn_h,
            f"{t('clean')} ×1", font_size=FONT_SIZE_BODY,
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
        self._ending_is_win = False

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
        self.particles.clear()
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
        self.particles.clear()

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
            self._chip_text = t("mode_chip_timed", time=format_time(int(gs.time_remaining)))
        elif gs.mode == "challenge":
            remain = max(0, gs.move_limit - (gs.board.move_count if gs.board else 0))
            self._chip_text = t("mode_chip_challenge", moves=remain)
        else:
            self._chip_text = t("mode_chip_classic")

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

        # 合并位置：粒子爆发 + "+N" 漂浮分数；大连环触发震屏
        for tile in gs.board.get_all_tiles():
            if not tile.merged_from:
                continue
            cell = TileRenderer.get_tile_rect(tile.row, tile.col)
            center = (cell.centerx, cell.centery)
            from src.utils import get_tile_color
            tile_color, _ = get_tile_color(tile.value)
            self.particles.burst(center, tile_color, count=PARTICLE_MERGE_COUNT,
                                 size_range=(4, 8), life_range=(0.32, 0.55))
            self._floaters.append(
                _ScoreFloater(f"+{tile.value}", (cell.centerx, cell.y + 22))
            )
            if tile.value >= SHAKE_MIN_TILE:
                self.board_view.shake.kick(
                    SHAKE_AMPLITUDE + min(4, tile.value // 256), SHAKE_DURATION,
                )

        dm = DataManager()
        new_ach = check_achievements(
            gs.board.max_tile,
            dm.get("total_games", 0),
            gs.board.score,
        )

        gs.update()
        if gs.state in (GameState.STATE_GAME_OVER, GameState.STATE_WIN):
            self._begin_ending(is_win=gs.state == GameState.STATE_WIN)

    def _begin_ending(self, is_win: bool) -> None:
        """进入结束过渡：停留展示盘面后再跳结算 / Begin game-over transition"""
        get_sound_manager().play_sfx("game_over")
        self._ending = True
        self._ending_is_win = is_win
        self._end_timer = GAME_OVER_PAUSE
        self._input_queue = []
        if is_win:
            # 胜利：全屏彩色庆祝粒子从上方飘落
            for color in (ACCENT_GOLD, ACCENT_BLUE, ACCENT_PINK, ACCENT_GREEN):
                self.particles.burst(
                    (WINDOW_WIDTH // 2, 120), color,
                    count=14, speed_range=(40, 160), life_range=(0.6, 1.1),
                    gravity=150,
                )

    def _save_game_result(self) -> None:
        """保存游戏结果 / Save game result"""
        if not self._game_state:
            return
        result = self._game_state.get_result()
        dm = DataManager()
        prev_best = dm.get("high_score", 0)
        result["is_new_record"] = result["score"] > prev_best and result["score"] > 0
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
        self.particles.update(dt)

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
            self._begin_ending(is_win=gs.state == GameState.STATE_WIN)

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

    def _draw_ending_overlay(self, surface: pygame.Surface) -> None:
        """结束过渡遮罩：淡入 + 标题弹出 + 卡片承载 / Animated game-over overlay"""
        gs = self._game_state
        if not gs:
            return
        # 进度：0→1（遮罩前 30% 时间淡入，标题前 45% 时间弹出）
        progress = 1.0 - max(0.0, self._end_timer) / GAME_OVER_PAUSE
        fade = min(1.0, progress / 0.30)
        blit_overlay(surface, int(150 * fade))
        if fade <= 0.05:
            return

        # 半透明卡片承载文字
        card_w, card_h = 340, 128
        card = pygame.Rect(0, 0, card_w, card_h)
        card.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        card_alpha = min(255, int(255 * max(0.0, (progress - 0.1) / 0.3)))
        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, (26, 28, 54, card_alpha), (0, 0, card_w, card_h),
                         border_radius=18)
        pygame.draw.rect(card_surf, (110, 114, 170, card_alpha), (0, 0, card_w, card_h),
                         width=1, border_radius=18)
        surface.blit(card_surf, card.topleft)

        # 标题（弹出缩放）
        is_win = self._ending_is_win
        title = t("you_win") if is_win else t("game_over")
        pop = min(1.0, progress / 0.45)
        scale = 0.8 + 0.2 * (1 - (1 - pop) ** 3)  # ease-out-cubic
        font_size = max(12, int(FONT_SIZE_LARGE_TITLE * scale))
        font_big = get_font_manager().get_font(font_size, bold=True)
        title_color = ACCENT_GOLD if is_win else COLOR_TEXT
        title_surf = font_big.render(title, True, title_color)
        title_surf.set_alpha(int(255 * fade))
        surface.blit(title_surf, title_surf.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 22)))

        # 得分 / 新纪录
        font_sm = get_font_manager().get_font(FONT_SIZE_SUBHEAD)
        score_surf = font_sm.render(
            t("final_score_short", score=gs.board.score), True,
            ACCENT_GOLD if is_win else COLOR_TEXT_SECONDARY)
        score_surf.set_alpha(int(255 * fade))
        surface.blit(score_surf, score_surf.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 22)))

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

        # 粒子（棋盘之上、道具之下）
        self.particles.draw(surface)

        # 漂浮分数
        for f in self._floaters:
            f.draw(surface)

        # 道具栏
        for btn in (self.btn_undo, self.btn_clean, self.btn_revive):
            btn.draw(surface)

        # 结束过渡遮罩
        gs = self._game_state
        if gs and (self._ending or gs.state == GameState.STATE_GAME_OVER):
            self._draw_ending_overlay(surface)

    def get_game_result(self) -> Optional[dict]:
        """获取游戏结果（供结算页面使用）/ Get game result (for result page)"""
        return self._game_result
