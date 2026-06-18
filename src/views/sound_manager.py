# -*- coding: utf-8 -*-
# @Function: 音效管理器 - 音效播放、背景音乐管理

import pygame
import numpy as np
from typing import Optional

from src.models.data_manager import DataManager


class SoundManager:
    """音效管理器 - 单例模式 / Sound manager - singleton pattern"""

    _instance: Optional["SoundManager"] = None

    def __new__(cls) -> "SoundManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._sounds: dict = {}
        self._music_playing = False
        self._dm = DataManager()
        self._init_mixer()
        self._generate_sounds()

    def _init_mixer(self) -> None:
        """初始化音频混音器 / Initialize audio mixer"""
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            pygame.mixer.set_num_channels(8)
        except Exception:
            pass

    def _generate_tone(self, freq: float, duration: float, volume: float = 0.3,
                        fade_out: float = 0.05) -> pygame.mixer.Sound:
        """生成简单音调 / Generate simple tone"""
        sample_rate = 44100
        num_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, num_samples, dtype=np.float32)
        # 正弦波 + 衰减
        wave = np.sin(2 * np.pi * freq * t) * volume
        # 淡出
        fade_samples = int(sample_rate * fade_out)
        if fade_samples > 0 and fade_samples < num_samples:
            fade = np.linspace(1.0, 0.0, fade_samples, dtype=np.float32)
            wave[-fade_samples:] *= fade
        # 立体声
        stereo = np.column_stack((wave, wave))
        # 转为 16-bit
        sound_array = (stereo * 32767).astype(np.int16)
        return pygame.mixer.Sound(buffer=sound_array.tobytes())

    def _generate_sounds(self) -> None:
        """生成占位音效 / Generate placeholder sound effects"""
        try:
            # 移动音效 - 短促低音
            self._sounds["move"] = self._generate_tone(220, 0.08, 0.2)
            # 合并音效 - 上升音阶
            self._sounds["merge"] = self._generate_tone(440, 0.15, 0.3)
            # 新方块音效 - 轻柔高音
            self._sounds["new_tile"] = self._generate_tone(660, 0.06, 0.15)
            # 获胜音效 - 欢快音
            self._sounds["win"] = self._generate_tone(523, 0.3, 0.4)
            # 失败音效 - 下降音
            self._sounds["game_over"] = self._generate_tone(200, 0.5, 0.3)
            # 按钮点击
            self._sounds["click"] = self._generate_tone(800, 0.04, 0.15)
            # 道具使用
            self._sounds["prop"] = self._generate_tone(600, 0.12, 0.25)
            # 成就解锁
            self._sounds["achievement"] = self._generate_tone(880, 0.25, 0.35)
        except Exception:
            # 如果 numpy 或 mixer 不可用，使用空声音
            for name in ["move", "merge", "new_tile", "win", "game_over", "click", "prop", "achievement"]:
                self._sounds[name] = None

    def play(self, name: str) -> None:
        """播放音效 / Play sound effect"""
        settings = self._dm.get_settings()
        if not settings.get("sound_enabled", True):
            return
        sound = self._sounds.get(name)
        if sound is not None:
            try:
                volume = settings.get("sound_volume", 0.7)
                sound.set_volume(volume)
                sound.play()
            except Exception:
                pass

    def play_sfx(self, name: str) -> None:
        """播放音效（兼容接口）/ Play sound effect (compatibility interface)"""
        self.play(name)

    def play_music(self, filename: Optional[str] = None) -> None:
        """播放背景音乐（占位实现）/ Play background music (placeholder)"""
        settings = self._dm.get_settings()
        if not settings.get("music_enabled", True):
            return
        # 暂无音乐文件，仅标记状态
        self._music_playing = True

    def stop_music(self) -> None:
        """停止背景音乐 / Stop background music"""
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        self._music_playing = False

    def set_sound_volume(self, volume: float) -> None:
        """设置音效音量 / Set sound volume"""
        self._dm.update_settings(sound_volume=volume)

    def set_music_volume(self, volume: float) -> None:
        """设置音乐音量 / Set music volume"""
        self._dm.update_settings(music_volume=volume)
        try:
            pygame.mixer.music.set_volume(volume)
        except Exception:
            pass

    def pause_music(self) -> None:
        """暂停音乐 / Pause music"""
        try:
            pygame.mixer.music.pause()
        except Exception:
            pass

    def resume_music(self) -> None:
        """恢复音乐 / Resume music"""
        try:
            pygame.mixer.music.unpause()
        except Exception:
            pass


def get_sound_manager() -> SoundManager:
    """获取音效管理器单例 / Get sound manager singleton"""
    return SoundManager()
