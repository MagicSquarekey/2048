# -*- coding: utf-8 -*-
# @Function: AdManager - 广告管理器（本地免费模式）

import time
from typing import Optional

from src.models.data_manager import DataManager
from src.config import FREE_DAILY_LIMIT, AD_REWARD_AMOUNT, AD_COOLDOWN


class AdManager:
    """
    广告管理器 - 本地免费模式
    
    在没有真实广告 SDK 的情况下，提供本地免费模式：
    - 每日免费观看次数限制
    - 观看间隔冷却时间
    - 奖励发放
    """

    _instance: Optional["AdManager"] = None

    def __new__(cls) -> "AdManager":
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """初始化广告管理器"""
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self._data_manager = DataManager()
        self._last_view_time: float = 0
        self._is_viewing: bool = False

    def can_view_ad(self) -> bool:
        """
        检查是否可以观看广告
        
        Returns:
            是否可以观看
        """
        ad_stats = self._data_manager.get("ad_stats", {})
        daily_count = ad_stats.get("daily_ad_count", 0)
        last_date = ad_stats.get("last_ad_date", "")
        last_time = ad_stats.get("last_ad_time", 0)

        # 检查每日限制
        import datetime
        today = datetime.date.today().isoformat()
        if last_date != today:
            # 新的一天，重置计数
            return True

        if daily_count >= FREE_DAILY_LIMIT:
            return False

        # 检查冷却时间
        if last_time > 0:
            elapsed = time.time() - last_time
            if elapsed < AD_COOLDOWN:
                return False

        return True

    def get_remaining_cooldown(self) -> float:
        """
        获取剩余冷却时间（秒）
        
        Returns:
            剩余冷却时间，0 表示无冷却
        """
        ad_stats = self._data_manager.get("ad_stats", {})
        last_time = ad_stats.get("last_ad_time", 0)
        if last_time <= 0:
            return 0.0
        elapsed = time.time() - last_time
        remaining = AD_COOLDOWN - elapsed
        return max(0.0, remaining)

    def get_remaining_views(self) -> int:
        """
        获取今日剩余免费观看次数
        
        Returns:
            剩余次数
        """
        ad_stats = self._data_manager.get("ad_stats", {})
        daily_count = ad_stats.get("daily_ad_count", 0)
        last_date = ad_stats.get("last_ad_date", "")
        
        import datetime
        today = datetime.date.today().isoformat()
        if last_date != today:
            return FREE_DAILY_LIMIT
        
        return max(0, FREE_DAILY_LIMIT - daily_count)

    def view_ad(self, reward_type: str = "undo") -> bool:
        """
        观看广告（本地模拟）
        
        Args:
            reward_type: 奖励类型 ("undo", "clean", "revive")
            
        Returns:
            是否观看成功
        """
        if not self.can_view_ad():
            return False

        self._is_viewing = True
        # 本地模式：立即完成观看
        import datetime
        today = datetime.date.today().isoformat()

        # 更新广告统计
        self._data_manager.update_ad_stats()

        # 发放奖励
        if reward_type == "undo":
            current = self._data_manager.get_prop_count("undo")
            self._data_manager.update_prop_count("undo", current + AD_REWARD_AMOUNT)
        elif reward_type == "clean":
            current = self._data_manager.get_prop_count("clean")
            self._data_manager.update_prop_count("clean", current + AD_REWARD_AMOUNT)

        self._is_viewing = False
        return True

    def is_viewing(self) -> bool:
        """
        是否正在观看广告
        
        Returns:
            是否正在观看
        """
        return self._is_viewing

    def get_ad_info(self) -> dict:
        """
        获取广告信息摘要
        
        Returns:
            广告信息字典
        """
        return {
            "can_view": self.can_view_ad(),
            "remaining_views": self.get_remaining_views(),
            "cooldown": self.get_remaining_cooldown(),
            "reward_amount": AD_REWARD_AMOUNT,
            "daily_limit": FREE_DAILY_LIMIT,
        }


def get_ad_manager() -> AdManager:
    """获取广告管理器单例"""
    return AdManager()
