# -*- coding: utf-8 -*-
# @Function: DataManager - 本地数据持久化（JSON 存储）

import json
import os
import shutil
import time
from typing import Dict, Any, Optional

from src.config import DATA_FILE, UNDO_LIMIT_DEFAULT, CLEAN_LIMIT_DEFAULT


class DataManager:
    """本地数据管理器 - JSON 持久化存储"""

    _instance: Optional["DataManager"] = None

    def __new__(cls) -> "DataManager":
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data = cls._instance._load_default()
            cls._instance._load()
        return cls._instance

    def _load_default(self) -> Dict[str, Any]:
        """获取默认数据结构"""
        return {
            "high_score": 0,
            "total_games": 0,
            "max_tile": 0,
            "undo_count": UNDO_LIMIT_DEFAULT,
            "clean_count": CLEAN_LIMIT_DEFAULT,
            "achievements": [],
            "settings": {
                "sound_enabled": True,
                "music_enabled": True,
                "sound_volume": 0.7,
                "music_volume": 0.5,
                "window_size": "medium",
            },
            "ad_stats": {
                "daily_ad_count": 0,
                "last_ad_date": "",
                "last_ad_time": 0,
            },
            "mode_stats": {
                "classic": {"played": 0, "best_score": 0},
                "timed": {"played": 0, "best_score": 0},
                "challenge": {"played": 0, "best_score": 0},
            },
        }

    def _load(self) -> None:
        """从文件加载数据"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                # 合并数据（保留新增字段的默认值）
                self._merge_data(saved)
            except (json.JSONDecodeError, IOError):
                # 数据文件损坏，尝试从备份恢复
                self._recover_from_backup()

    def _merge_data(self, saved: Dict[str, Any]) -> None:
        """合并保存的数据与默认数据"""
        default = self._load_default()
        for key in default:
            if key in saved:
                if isinstance(default[key], dict) and isinstance(saved[key], dict):
                    # 深度合并字典
                    merged = {**default[key], **saved[key]}
                    self._data[key] = merged
                else:
                    self._data[key] = saved[key]

    def _recover_from_backup(self) -> bool:
        """
        尝试从备份文件恢复数据
        
        Returns:
            是否恢复成功
        """
        backup_file = DATA_FILE + ".bak"
        if not os.path.exists(backup_file):
            return False
        try:
            with open(backup_file, "r", encoding="utf-8") as f:
                backup_data = json.load(f)
            if not isinstance(backup_data, dict):
                return False
            required_keys = {"high_score", "total_games", "max_tile"}
            if not required_keys.issubset(backup_data.keys()):
                return False
            self._data = self._load_default()
            self._merge_data(backup_data)
            self.save()
            return True
        except Exception:
            return False

    def get_recovery_status(self) -> str:
        """
        获取数据恢复状态信息
        
        Returns:
            状态描述字符串
        """
        backup_file = DATA_FILE + ".bak"
        if not os.path.exists(backup_file):
            return "no_backup"
        if not os.path.exists(DATA_FILE):
            return "backup_available"
        return "ok"

    def save(self) -> None:
        """保存数据到文件（自动创建备份）"""
        try:
            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
            # 先备份旧文件
            if os.path.exists(DATA_FILE):
                backup_file = DATA_FILE + ".bak"
                try:
                    shutil.copy2(DATA_FILE, backup_file)
                except Exception:
                    pass
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        """获取数据"""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """设置数据"""
        self._data[key] = value

    def update_high_score(self, score: int) -> bool:
        """
        更新最高分
        
        Returns:
            是否创造了新纪录
        """
        if score > self._data["high_score"]:
            self._data["high_score"] = score
            self.save()
            return True
        return False

    def update_max_tile(self, tile: int) -> bool:
        """
        更新最大方块
        
        Returns:
            是否创造了新纪录
        """
        if tile > self._data["max_tile"]:
            self._data["max_tile"] = tile
            self.save()
            return True
        return False

    def increment_games(self) -> None:
        """增加游戏局数"""
        self._data["total_games"] += 1
        self.save()

    def update_mode_stats(self, mode: str, score: int) -> None:
        """更新模式统计"""
        stats = self._data["mode_stats"].get(mode, {"played": 0, "best_score": 0})
        stats["played"] += 1
        if score > stats["best_score"]:
            stats["best_score"] = score
        self._data["mode_stats"][mode] = stats
        self.save()

    def add_achievement(self, achievement_id: str) -> bool:
        """
        添加成就
        
        Returns:
            是否是新成就
        """
        if achievement_id not in self._data["achievements"]:
            self._data["achievements"].append(achievement_id)
            self.save()
            return True
        return False

    def has_achievement(self, achievement_id: str) -> bool:
        """检查是否已获得成就"""
        return achievement_id in self._data["achievements"]

    def get_undo_count(self) -> int:
        """获取剩余撤销次数"""
        return self._data.get("undo_count", UNDO_LIMIT_DEFAULT)

    def set_undo_count(self, count: int) -> None:
        """设置撤销次数"""
        self._data["undo_count"] = count
        self.save()

    def get_clean_count(self) -> int:
        """获取剩余清理次数"""
        return self._data.get("clean_count", CLEAN_LIMIT_DEFAULT)

    def set_clean_count(self, count: int) -> None:
        """设置清理次数"""
        self._data["clean_count"] = count
        self.save()

    def can_watch_ad(self) -> bool:
        """检查是否可以观看广告"""
        ad_stats = self._data.get("ad_stats", {})
        today = time.strftime("%Y-%m-%d")
        if ad_stats.get("last_ad_date") != today:
            return True
        return ad_stats.get("daily_ad_count", 0) < 5

    def record_ad_watch(self) -> None:
        """记录广告观看"""
        today = time.strftime("%Y-%m-%d")
        ad_stats = self._data.get("ad_stats", {})
        if ad_stats.get("last_ad_date") != today:
            ad_stats["daily_ad_count"] = 0
        ad_stats["daily_ad_count"] = ad_stats.get("daily_ad_count", 0) + 1
        ad_stats["last_ad_date"] = today
        ad_stats["last_ad_time"] = time.time()
        self._data["ad_stats"] = ad_stats
        self.save()

    def get_settings(self) -> Dict[str, Any]:
        """获取设置"""
        return self._data.get("settings", {})

    def update_setting(self, key: str, value: Any) -> None:
        """更新设置"""
        if "settings" not in self._data:
            self._data["settings"] = {}
        self._data["settings"][key] = value
        self.save()

    def reset_data(self) -> None:
        """重置所有数据"""
        self._data = self._load_default()
        self.save()
