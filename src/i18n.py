# -*- coding: utf-8 -*-
# @Function: 国际化模块 - 中英文文本映射
# @Function: Internationalization module - Chinese/English text mapping

from typing import Dict

# 当前语言（默认中文）/ Current language (default Chinese)
_current_lang: str = "zh"


# 中英文字符串映射 / Chinese-English string mapping
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # === 通用 / General ===
    "app_name": {"zh": "2048 经典游戏", "en": "2048 Classic"},

    # === 主菜单 / Main Menu ===
    "current_score": {"zh": "当前分数", "en": "Score"},
    "best_score": {"zh": "最高分", "en": "Best"},
    "total_games": {"zh": "总局数", "en": "Games"},
    "menu_subtitle": {"zh": "挑战你的数字极限", "en": "Push your number limits"},
    "menu_hint": {"zh": "方向键 / WASD / 鼠标滑动 操作方块 · ESC 暂停",
                  "en": "Arrows / WASD / Swipe to move · ESC to pause"},
    "time_challenge": {"zh": "计时挑战", "en": "Time Challenge"},
    "challenge_mode": {"zh": "挑战模式", "en": "Challenge Mode"},
    "settings": {"zh": "设置", "en": "Settings"},
    "achievements": {"zh": "成就", "en": "Awards"},
    "login": {"zh": "登录", "en": "Login"},
    "exit": {"zh": "退出", "en": "Exit"},

    # === 游戏模式（卡片）/ Game Modes (cards) ===
    "mode_classic": {"zh": "经典模式", "en": "Classic"},
    "mode_timed": {"zh": "限时模式", "en": "Timed"},
    "mode_challenge": {"zh": "挑战模式", "en": "Challenge"},
    "mode_classic_desc": {"zh": "不限时间，挑战最高分！", "en": "No timer. Chase your best score!"},
    "mode_timed_desc": {"zh": "60 秒内挑战目标分数！", "en": "Hit the target in 60 seconds!"},
    "mode_challenge_desc": {"zh": "限定步数内合成目标方块！", "en": "Reach the target tile in limited moves!"},

    # === 游戏页面 / Game Page ===
    "back": {"zh": "← 返回", "en": "← Back"},
    "pause": {"zh": "暂停", "en": "Pause"},
    "undo": {"zh": "撤销", "en": "Undo"},
    "clean": {"zh": "清理", "en": "Clear"},
    "revive": {"zh": "复活", "en": "Revive"},
    "props": {"zh": "道具", "en": "Props"},
    "mode_chip_classic": {"zh": "经典模式", "en": "Classic"},
    "mode_chip_timed": {"zh": "限时模式 · 剩余 {time}", "en": "Timed · {time} left"},
    "mode_chip_challenge": {"zh": "挑战模式 · 剩余 {moves} 步", "en": "Challenge · {moves} moves left"},
    "final_score_short": {"zh": "最终得分 {score}", "en": "Score {score}"},

    # === 暂停页面 / Pause Page ===
    "game_paused": {"zh": "游戏暂停", "en": "Paused"},
    "continue_game": {"zh": "继续游戏", "en": "Resume"},
    "restart": {"zh": "重新开始", "en": "Restart"},
    "back_to_menu": {"zh": "返回主菜单", "en": "Main Menu"},

    # === 结算页面 / Result Page ===
    "you_win": {"zh": "恭喜获胜!", "en": "You Won!"},
    "game_over": {"zh": "游戏结束", "en": "Game Over"},
    "final_score": {"zh": "最终得分", "en": "Final Score"},
    "new_record": {"zh": "新纪录！", "en": "New Record!"},
    "max_tile": {"zh": "最大方块", "en": "Max Tile"},
    "move_count": {"zh": "移动步数", "en": "Moves"},
    "elapsed_time": {"zh": "用时", "en": "Time"},
    "mode_label": {"zh": "模式", "en": "Mode"},
    "play_again": {"zh": "再来一局", "en": "Play Again"},

    # === 设置页面 / Settings Page ===
    "settings": {"zh": "设置", "en": "Settings"},
    "sound": {"zh": "音效", "en": "Sound"},
    "music": {"zh": "音乐", "en": "Music"},
    "on": {"zh": "开", "en": "On"},
    "off": {"zh": "关", "en": "Off"},
    "language": {"zh": "语言", "en": "Language"},
    "tap_to_switch": {"zh": "点击切换", "en": "Tap to switch"},
    "reset_data": {"zh": "重置数据", "en": "Reset Data"},
    "confirm_reset": {"zh": "确认重置所有数据？此操作不可撤销。", "en": "Reset all data? This cannot be undone."},
    "confirm": {"zh": "确认", "en": "Confirm"},
    "cancel": {"zh": "取消", "en": "Cancel"},

    # === 登录页面 / Login Page ===
    "user_login": {"zh": "用户登录", "en": "Sign In"},
    "login_desc": {"zh": "登录后可云端同步游戏进度", "en": "Sync your progress via cloud"},
    "username": {"zh": "用户名", "en": "Username"},
    "password": {"zh": "密码", "en": "Password"},
    "login_empty_warn": {"zh": "请输入用户名和密码", "en": "Enter username and password"},
    "login_dev_msg": {"zh": "云端同步功能开发中...", "en": "Cloud sync coming soon..."},

    # === 成就页面 / Achievement Page ===
    "achievements_title": {"zh": "成就", "en": "Awards"},
    "achieved": {"zh": "已达成", "en": "Done"},
    "locked": {"zh": "未达成", "en": "Locked"},
    "no_achievements_hint": {"zh": "继续游戏解锁更多成就", "en": "Keep playing to unlock"},
}

# 语义别名（兼容旧调用）/ semantic aliases for legacy callers
TRANSLATIONS["settings_title"] = TRANSLATIONS["settings"]
TRANSLATIONS["paused"] = TRANSLATIONS["game_paused"]
TRANSLATIONS["resume"] = TRANSLATIONS["continue_game"]
TRANSLATIONS["back_to_menu_short"] = TRANSLATIONS["back_to_menu"]
TRANSLATIONS["unlocked"] = TRANSLATIONS["achieved"]


def t(key: str, **kwargs) -> str:
    """翻译函数：根据当前语言返回对应文本，支持 {name} 插值 / Translate with optional interpolation"""
    if key in TRANSLATIONS:
        text = TRANSLATIONS[key].get(_current_lang, key)
    else:
        text = key
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError, ValueError):
            pass
    return text


def get_current_lang() -> str:
    """获取当前语言 / Get current language"""
    return _current_lang


def set_language(lang: str) -> None:
    """设置当前语言 / Set current language"""
    global _current_lang
    if lang in ("zh", "en"):
        _current_lang = lang


def toggle_language() -> str:
    """切换语言并返回新语言 / Toggle language and return new language"""
    global _current_lang
    _current_lang = "en" if _current_lang == "zh" else "zh"
    return _current_lang


# 别名：兼容 settings_page 等模块导入 get_language
get_language = get_current_lang
