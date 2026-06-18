# -*- coding: utf-8 -*-
# @Function: 成就系统定义与检测 / Achievement system definitions and detection

from typing import Dict, List, Optional
from src.models.data_manager import DataManager


# 成就定义
ACHIEVEMENTS: Dict[str, Dict] = {
    "first_128": {
        "name": "初窥门径",
        "description": "首次合成 128",
        "icon": "🌟",
        "condition": "max_tile >= 128",
    },
    "first_256": {
        "name": "小有成就",
        "description": "首次合成 256",
        "icon": "⭐",
        "condition": "max_tile >= 256",
    },
    "first_512": {
        "name": "登堂入室",
        "description": "首次合成 512",
        "icon": "💫",
        "condition": "max_tile >= 512",
    },
    "first_1024": {
        "name": "炉火纯青",
        "description": "首次合成 1024",
        "icon": "🌠",
        "condition": "max_tile >= 1024",
    },
    "first_2048": {
        "name": "登峰造极",
        "description": "首次合成 2048",
        "icon": "🏆",
        "condition": "max_tile >= 2048",
    },
    "games_10": {
        "name": "休闲玩家",
        "description": "累计游戏 10 局",
        "icon": "🎮",
        "condition": "total_games >= 10",
    },
    "games_50": {
        "name": "忠实玩家",
        "description": "累计游戏 50 局",
        "icon": "🎯",
        "condition": "total_games >= 50",
    },
    "games_100": {
        "name": "核心玩家",
        "description": "累计游戏 100 局",
        "icon": "👑",
        "condition": "total_games >= 100",
    },
    "score_10000": {
        "name": "万分选手",
        "description": "单局得分超过 10000",
        "icon": "💎",
        "condition": "high_score >= 10000",
    },
}


def check_achievements(
    max_tile: int,
    total_games: int,
    high_score: int,
) -> List[str]:
    """
    检查并返回新达成的成就 ID 列表
    Check and return list of newly achieved achievement IDs
    
    Args:
        max_tile: 当前最大方块值 / Current max tile value
        total_games: 累计游戏局数 / Total games played
        high_score: 历史最高分 / Historical high score
        
    Returns:
        新达成的成就 ID 列表 / List of newly achieved achievement IDs
    """
    dm = DataManager()
    new_achievements = []

    # 检查方块合成成就
    tile_milestones = [
        ("first_128", 128),
        ("first_256", 256),
        ("first_512", 512),
        ("first_1024", 1024),
        ("first_2048", 2048),
    ]
    for ach_id, threshold in tile_milestones:
        if max_tile >= threshold and dm.add_achievement(ach_id):
            new_achievements.append(ach_id)

    # 检查游戏局数成就
    game_milestones = [
        ("games_10", 10),
        ("games_50", 50),
        ("games_100", 100),
    ]
    for ach_id, threshold in game_milestones:
        if total_games >= threshold and dm.add_achievement(ach_id):
            new_achievements.append(ach_id)

    # 检查分数成就
    score_milestones = [
        ("score_10000", 10000),
    ]
    for ach_id, threshold in score_milestones:
        if high_score >= threshold and dm.add_achievement(ach_id):
            new_achievements.append(ach_id)

    return new_achievements


def get_achievement_info(achievement_id: str) -> Optional[Dict]:
    """获取成就信息 / Get achievement info"""
    return ACHIEVEMENTS.get(achievement_id)


def get_all_achievements() -> List[Dict]:
    """获取所有成就列表 / Get all achievements list"""
    dm = DataManager()
    result = []
    for ach_id, info in ACHIEVEMENTS.items():
        result.append({
            "id": ach_id,
            "unlocked": dm.has_achievement(ach_id),
            **info,
        })
    return result
