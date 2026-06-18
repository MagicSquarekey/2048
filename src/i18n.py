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
    "start_game": {"zh": "开始游戏", "en": "Start Game"},
    "time_challenge": {"zh": "计时挑战", "en": "Time Challenge"},
    "challenge_mode": {"zh": "挑战模式", "en": "Challenge Mode"},
    "settings": {"zh": "设置", "en": "Settings"},
    "achievements": {"zh": "成就", "en": "Achievements"},
    "login": {"zh": "登录", "en": "Login"},
    "exit": {"zh": "退出", "en": "Exit"},

    # === 游戏页面 / Game Page ===
    "back": {"zh": "← 返回", "en": "← Back"},
    "pause": {"zh": "暂停", "en": "Pause"},
    "undo": {"zh": "撤销", "en": "Undo"},
    "combo": {"zh": "连击", "en": "Combo"},
    "clean_mode": {"zh": "清洁模式", "en": "Clean"},
    "undo_available": {"zh": "剩余", "en": "Left"},

    # === 计时挑战 / Timed Challenge ===
    "time_remaining": {"zh": "剩余", "en": "Time"},
    "seconds": {"zh": "秒", "en": "sec"},
    "seconds_short": {"zh": "s", "en": "s"},

    # === 挑战模式 / Challenge Mode ===
    "moves_remaining": {"zh": "剩余", "en": "Moves"},
    "target": {"zh": "目标", "en": "Target"},

    # === 暂停页面 ===
    "paused": {"zh": "游戏暂停", "en": "Paused"},
    "resume": {"zh": "继续游戏", "en": "Resume"},
    "restart": {"zh": "重新开始", "en": "Restart"},
    "back_to_menu": {"zh": "返回主菜单", "en": "Back to Menu"},

    # === 结算页面 / Result Page ===
    "you_win": {"zh": "恭喜获胜!", "en": "You Won!"},
    "max_tile": {"zh": "最大方块", "en": "Max Tile"},
    "move_count": {"zh": "移动步数", "en": "Moves"},
    "elapsed_time": {"zh": "用时", "en": "Time"},
    "mode_classic": {"zh": "经典", "en": "Classic"},
    "mode_timed": {"zh": "限时", "en": "Timed"},
    "mode_challenge": {"zh": "挑战", "en": "Challenge"},
    "mode_label": {"zh": "模式", "en": "Mode"},
    "game_over": {"zh": "游戏结束", "en": "Game Over"},
    "final_score": {"zh": "最终得分", "en": "Final Score"},
    "total_moves": {"zh": "总步数", "en": "Moves"},
    "play_again": {"zh": "再来一局", "en": "Play Again"},
    "back_to_menu_short": {"zh": "返回菜单", "en": "Back"},
    "share_score": {"zh": "分享成绩", "en": "Share"},

    # === 设置页面 / Settings Page ===
    "settings_title": {"zh": "游戏设置", "en": "Settings"},
    "sound": {"zh": "音效", "en": "Sound"},
    "music": {"zh": "音乐", "en": "Music"},
    "on": {"zh": "开", "en": "On"},
    "off": {"zh": "关", "en": "Off"},
    "language": {"zh": "语言", "en": "Language"},
    "chinese": {"zh": "中文", "en": "中文"},
    "english": {"zh": "English", "en": "English"},
    "reset_data": {"zh": "重置数据", "en": "Reset Data"},
    "reset_confirm": {"zh": "确认重置所有游戏数据？", "en": "Reset all game data?"},
    "confirm": {"zh": "确认", "en": "Confirm"},
    "cancel": {"zh": "取消", "en": "Cancel"},

    # === 登录页面 / Login Page ===
    "guest_login": {"zh": "游客登录", "en": "Guest Login"},
    "input_name": {"zh": "请输入昵称", "en": "Enter nickname"},

    # === 成就页面 / Achievement Page ===
    "achievements_title": {"zh": "成就系统", "en": "Achievements"},
    "unlocked": {"zh": "已解锁", "en": "Unlocked"},
    "locked": {"zh": "未解锁", "en": "Locked"},

    # === 成就名称 / Achievement Names ===
    "ach_first_win": {"zh": "初次胜利", "en": "First Win"},
    "ach_tile_1024": {"zh": "突破千分", "en": "Tile 1024"},
    "ach_tile_2048": {"zh": "终极挑战", "en": "Tile 2048"},
    "ach_combo_5": {"zh": "连击达人", "en": "Combo Master"},
    "ach_games_10": {"zh": "十局老手", "en": "10 Games"},
    "ach_games_100": {"zh": "百局传奇", "en": "100 Games"},
    "ach_speedrun": {"zh": "极速通关", "en": "Speed Run"},
    "ach_no_undo": {"zh": "无悔挑战", "en": "No Undo"},

    # === 游戏页面补充 / Game Page (Extended) ===
    "clean": {"zh": "清理", "en": "Clean"},
    "props": {"zh": "道具", "en": "Props"},
    "revive": {"zh": "复活", "en": "Revive"},
    "score_label": {"zh": "得分", "en": "Score"},
    "time_label": {"zh": "用时", "en": "Time"},
    "moves_label": {"zh": "步数", "en": "Moves"},

    # === 设置补充 / Settings (Extended) ===
    "settings_title": {"zh": "游戏设置", "en": "Game Settings"},
    "board_size": {"zh": "棋盘大小", "en": "Board Size"},
    "game_mode": {"zh": "游戏模式", "en": "Game Mode"},
    "mode_classic": {"zh": "经典模式", "en": "Classic"},
    "mode_timed": {"zh": "限时模式", "en": "Timed"},
    "mode_challenge": {"zh": "挑战模式", "en": "Challenge"},
    "sound_effects": {"zh": "音效", "en": "Sound Effects"},
    "bg_music": {"zh": "背景音乐", "en": "Background Music"},
    "confirm_reset": {"zh": "确认重置所有数据？此操作不可撤销。", "en": "Reset all data? This cannot be undone."},

    # === 结算页面 / Result Page (Extended) ===
    "game_over": {"zh": "游戏结束", "en": "Game Over"},
    "back_to_menu": {"zh": "返回主菜单", "en": "Back to Menu"},
    "play_again": {"zh": "再来一局", "en": "Play Again"},
    "new_record": {"zh": "新纪录！", "en": "New Record!"},

    # === 提示信息 / Notifications ===
    "no_undo_available": {"zh": "没有可用的撤销次数", "en": "No undos available"},
    "no_clean_available": {"zh": "没有可用的清洁次数", "en": "No cleans available"},
    "time_up": {"zh": "时间到！", "en": "Time Up!"},
    "challenge_complete": {"zh": "挑战完成！", "en": "Challenge Complete!"},
    "challenge_failed": {"zh": "挑战失败！", "en": "Challenge Failed!"},
    "game_paused": {"zh": "游戏暂停", "en": "Game Paused"},
    "continue_game": {"zh": "继续游戏", "en": "Continue"},
    "save_quit": {"zh": "保存退出", "en": "Save & Quit"},
    "quit": {"zh": "退出", "en": "Quit"},
}


def t(key: str) -> str:
    """翻译函数：根据当前语言返回对应文本 / Translation function: return text by current language"""
    if key in TRANSLATIONS:
        return TRANSLATIONS[key].get(_current_lang, key)
    return key


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
