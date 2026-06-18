# -*- coding: utf-8 -*-
# @Function: GameState - 游戏运行时状态管理

import time
from typing import Optional, Dict, Any

from src.models.board import GameBoard


class GameState:
    """游戏运行时状态 / Runtime game state"""

    # 游戏状态常量
    STATE_IDLE = "idle"             # 未开始
    STATE_PLAYING = "playing"       # 游戏中
    STATE_PAUSED = "paused"         # 暂停
    STATE_WIN = "win"               # 获胜
    STATE_GAME_OVER = "game_over"   # 游戏结束

    def __init__(self) -> None:
        """初始化游戏状态 / Initialize game state"""
        self.state: str = self.STATE_IDLE
        self.mode: str = "classic"           # 游戏模式
        self.board: Optional[GameBoard] = None
        self.start_time: float = 0           # 游戏开始时间
        self.pause_time: float = 0           # 暂停时的时间
        self.total_pause_duration: float = 0  # 总暂停时长
        self.time_remaining: int = 60        # 限时模式剩余时间
        self.move_limit: int = 0             # 挑战模式步数限制
        self.target_score: int = 0           # 目标分数
        self.target_tile: int = 0            # 目标方块
        self.is_ad_reward_used: bool = False  # 本局是否使用过广告复活
        self.undo_count: int = 2             # 剩余撤销次数
        self.clean_count: int = 0            # 剩余清理次数
        self.prev_board_state = None         # 上一步棋盘状态（用于撤销）
        self.prev_score: int = 0             # 上一步分数

    def start_game(self, mode: str = "classic", config: Optional[Dict[str, Any]] = None) -> GameBoard:
        """
        开始新游戏
        
        Args:
            mode: 游戏模式 (classic, timed, challenge)
            config: 模式配置参数
            
        Returns:
            初始化后的棋盘
        """
        self.state = self.STATE_PLAYING
        self.mode = mode
        self.board = GameBoard()
        self.board.reset()
        self.start_time = time.time()
        self.total_pause_duration = 0
        self.is_ad_reward_used = False

        # 初始化模式参数
        config = config or {}
        if mode == "timed":
            self.time_remaining = config.get("time_limit", 60)
            self.target_score = config.get("target_score", 500)
        elif mode == "challenge":
            self.move_limit = config.get("move_limit", 50)
            self.target_tile = config.get("target_tile", 128)

        return self.board

    def pause(self) -> None:
        """暂停游戏 / Pause the game"""
        if self.state == self.STATE_PLAYING:
            self.state = self.STATE_PAUSED
            self.pause_time = time.time()

    def resume(self) -> None:
        """恢复游戏 / Resume the game"""
        if self.state == self.STATE_PAUSED:
            self.state = self.STATE_PLAYING
            self.total_pause_duration += time.time() - self.pause_time

    def update(self) -> None:
        """更新游戏状态（每帧调用） / Update game state (called each frame)"""
        if self.state != self.STATE_PLAYING or not self.board:
            return

        # 检查限时模式
        if self.mode == "timed":
            elapsed = self.get_elapsed_time()
            self.time_remaining = max(0, int(self.board.score > 0 and self.target_score - self.board.score >= 0 and 
                                              self._get_mode_config().get("time_limit", 60) - elapsed or 0))
            if self.time_remaining <= 0:
                self.state = self.STATE_GAME_OVER
                return

        # 检查棋盘状态
        if self.board.is_won and not self.board.keep_playing:
            self.state = self.STATE_WIN
        elif self.board.is_game_over:
            self.state = self.STATE_GAME_OVER

    def get_elapsed_time(self) -> float:
        """获取已用游戏时间（扣除暂停时间）/ Get elapsed game time (excluding pause time)"""
        if self.state == self.STATE_PAUSED:
            return self.pause_time - self.start_time - self.total_pause_duration
        return time.time() - self.start_time - self.total_pause_duration

    def save_for_undo(self) -> None:
        """保存当前状态用于撤销 / Save current state for undo"""
        if self.board:
            self.prev_board_state = self.board._clone_grid()
            self.prev_score = self.board.score

    def undo(self) -> bool:
        """撤销上一步 / Undo the last move"""
        if not self.board or not self.prev_board_state:
            return False
        if self.undo_count <= 0:
            return False
        success = self.board.undo(self.prev_board_state, self.prev_score)
        if success:
            self.undo_count -= 1
            self.prev_board_state = None
            self.prev_score = 0
        return success

    def use_clean(self) -> bool:
        """使用清理道具 / Use clean tile power-up"""
        if not self.board:
            return False
        if self.clean_count <= 0:
            return False
        pos = self.board.clean_min_tile()
        if pos:
            self.clean_count -= 1
            return True
        return False

    def add_undo_count(self, count: int = 1) -> None:
        """增加撤销次数 / Add undo count"""
        self.undo_count += count

    def add_clean_count(self, count: int = 1) -> None:
        """增加清理次数 / Add clean count"""
        self.clean_count += count

    def get_result(self) -> Dict[str, Any]:
        """获取游戏结果 / Get game result"""
        if not self.board:
            return {}
        return {
            "mode": self.mode,
            "score": self.board.score,
            "max_tile": self.board.max_tile,
            "move_count": self.board.move_count,
            "elapsed_time": self.get_elapsed_time(),
            "is_win": self.board.is_won or (self.board.max_tile >= 2048),
            "is_game_over": self.board.is_game_over,
        }

    def _get_mode_config(self) -> Dict[str, Any]:
        """获取当前模式配置 / Get current mode configuration"""
        from src.config import MODE_CONFIG
        return MODE_CONFIG.get(self.mode, {})
