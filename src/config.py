# -*- coding: utf-8 -*-
# @Function: 全局配置 - 颜色、尺寸、字体、游戏参数
# @Function: Global configuration - colors, dimensions, fonts, game parameters

import os

# ========== 窗口配置 / Window Settings ==========
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "2048 休闲游戏"
FPS = 60

# ========== 棋盘配置 / Board Settings ==========
BOARD_SIZE = 4          # 4×4 棋盘
TILE_SIZE = 95          # 方块尺寸（像素）- 适配 600px 窗口高度
TILE_GAP = 8            # 方块间距（像素）
BOARD_PADDING = 15      # 棋盘内边距
BOARD_X = (WINDOW_WIDTH - (TILE_SIZE * BOARD_SIZE + TILE_GAP * (BOARD_SIZE - 1))) // 2
BOARD_Y = 110           # 棋盘起始 Y 坐标 - 适配 600px 窗口高度

# ========== 颜色方案（低饱和度柔和风格） / Color Scheme (Low Saturation Soft Style) ==========
# 背景色 / Background Colors
COLOR_BG = (250, 248, 239)              # 游戏背景 - 米白
COLOR_BOARD_BG = (187, 173, 160)        # 棋盘背景 - 深米色
COLOR_TILE_EMPTY = (205, 193, 180)      # 空方块 - 浅米色

# 方块颜色方案（值 -> (背景色, 文字色)） / Tile Color Scheme (value -> (bg, text))
TILE_COLORS = {
    2:    ((238, 228, 218), (119, 110, 101)),
    4:    ((237, 224, 200), (119, 110, 101)),
    8:    ((242, 177, 121), (249, 246, 242)),
    16:   ((245, 149, 99),  (249, 246, 242)),
    32:   ((246, 124, 95),  (249, 246, 242)),
    64:   ((246, 94, 59),   (249, 246, 242)),
    128:  ((237, 207, 114), (249, 246, 242)),
    256:  ((237, 204, 97),  (249, 246, 242)),
    512:  ((237, 200, 80),  (249, 246, 242)),
    1024: ((237, 197, 63),  (249, 246, 242)),
    2048: ((237, 194, 46),  (249, 246, 242)),
}

# UI 颜色 / UI Colors
COLOR_TEXT = (119, 110, 101)             # 主文字 - 深棕
COLOR_TEXT_LIGHT = (249, 246, 242)       # 浅色文字 - 白
COLOR_TEXT_SCORE = (255, 220, 50)        # 分数文字 - 亮黄色，更醒目

# 按钮颜色 / Button Colors
COLOR_BTN_PRIMARY = (119, 110, 101)
COLOR_BTN_PRIMARY_HOVER = (140, 130, 120)
COLOR_BTN_SECONDARY = (186, 173, 160)
COLOR_BTN_SECONDARY_HOVER = (200, 190, 180)
COLOR_BTN_DANGER = (200, 80, 80)
COLOR_BTN_DANGER_HOVER = (220, 100, 100)

# 交互参数 / Interaction Parameters
SWIPE_THRESHOLD = 30  # 滑动最小距离（像素） / Minimum swipe distance (pixels)
COLOR_SCORE_BG = (187, 173, 160)         # 分数背景 - 深米色

# 按钮颜色
COLOR_BTN_PRIMARY = (143, 122, 102)      # 主按钮 - 棕色
COLOR_BTN_PRIMARY_HOVER = (163, 142, 122)
COLOR_BTN_SECONDARY = (187, 173, 160)    # 次按钮 - 米色
COLOR_BTN_SECONDARY_HOVER = (207, 193, 180)
COLOR_BTN_DANGER = (246, 94, 59)         # 危险按钮 - 红色
COLOR_BTN_DANGER_HOVER = (256, 114, 79)

# 遮罩颜色 / Overlay Colors
COLOR_OVERLAY = (0, 0, 0, 150)          # 半透明黑色遮罩 / Semi-transparent black overlay

# ========== 游戏参数 / Game Parameters ==========
INITIAL_TILES = 2           # 初始方块数量 / Initial tile count
WIN_TILE = 2048             # 获胜目标数字 / Winning target number
UNDO_LIMIT_DEFAULT = 2      # 新用户默认撤销次数 / Default undo limit for new users
CLEAN_LIMIT_DEFAULT = 0     # 新用户默认清理次数 / Default clean limit for new users
AD_COOLDOWN = 20            # 广告冷却时间（秒） / Ad cooldown (seconds)
MAX_AD_PER_DAY = 5          # 每日广告上限 / Max ads per day

# 随机生成概率 / Random Generation Probability
TILE_2_PROBABILITY = 0.9    # 生成 2 的概率（90%） / Probability of generating 2 (90%)

# 分数计算 / Score Calculation
SCORE_MULTIPLIERS = {
    "classic": 1.0,
    "timed": 1.5,
    "challenge": 2.0,
}

# ========== 游戏模式配置 / Game Mode Settings ==========
MODE_CONFIG = {
    "classic": {
        "name": "经典模式",
        "description": "不限时间，挑战最高分！",
        "icon": "🎮",
    },
    "timed": {
        "name": "限时模式",
        "description": "60 秒内挑战目标分数！",
        "icon": "⏱️",
        "time_limit": 60,
        "target_score": 500,
    },
    "challenge": {
        "name": "挑战模式",
        "description": "在限定步数内合成目标方块！",
        "icon": "🏆",
        "move_limit": 50,
        "target_tile": 128,
    },
}

# ========== 动画配置 / Animation Settings ==========
ANIMATION_MOVE_DURATION = 150       # 方块移动动画时长（毫秒） / Tile move animation duration (ms)
ANIMATION_MERGE_DURATION = 200      # 方块合并动画时长（毫秒） / Tile merge animation duration (ms)
ANIMATION_SPAWN_DURATION = 150      # 方块生成动画时长（毫秒） / Tile spawn animation duration (ms)
ANIMATION_FADE_DURATION = 300       # 淡入淡出动画时长（毫秒） / Fade in/out animation duration (ms)

# ========== 字体配置 / Font Settings ==========
# 自动检测中文字体，解决中文乱码问题 / Auto-detect Chinese font to fix encoding issues
import subprocess
def _find_chinese_font() -> str:
    """查找系统中可用的中文字体 / Find available Chinese font on system"""
    # 常见中文字体优先级 / Common Chinese font priority
    font_candidates = [
        "simhei.ttf",      # 黑体 / SimHei
        "msyh.ttc",        # 微软雅黑 / Microsoft YaHei
        "simsun.ttc",      # 宋体 / SimSun
        "simkai.ttf",      # 楷体 / SimKai
        "fang.ttf",        # 仿宋 / FangSong
    ]
    for font_name in font_candidates:
        font_path = os.path.join("C:\\Windows\\Fonts", font_name)
        if os.path.exists(font_path):
            return font_path
    return None

FONT_PATH = _find_chinese_font()  # 自动检测中文字体 / Auto-detect Chinese font
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24
FONT_SIZE_TINY = 18

# 方块数字大小映射 / Tile font size mapping
TILE_FONT_SIZES = {
    2: 40, 4: 40, 8: 40,
    16: 36, 32: 36, 64: 36,
    128: 32, 256: 32, 512: 32,
    1024: 28, 2048: 28,
}

# ========== 道具配置 / Item Settings ==========
UNDO_LIMIT_DEFAULT = 3       # 每局默认撤销次数 / Default undo limit per game
CLEAN_LIMIT_DEFAULT = 1      # 每局默认清除次数 / Default clean limit per game

# ========== 广告/激励配置 / Ad/Reward Settings ==========
FREE_DAILY_LIMIT = 5         # 每日免费观看广告次数 / Free daily ad views
AD_REWARD_AMOUNT = 1         # 每次观看广告获得的道具数量 / Items rewarded per ad view
AD_COOLDOWN = 30             # 广告冷却时间（秒） / Ad cooldown (seconds)

# ========== 数据存储路径 / Data Storage Paths ==========
DATA_DIR = os.path.join(os.path.expanduser("~"), "AppData", "Local", "2048_Game")
DATA_FILE = os.path.join(DATA_DIR, "game_data.json")

# 确保数据目录存在 / Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# ========== 页面枚举 / Page Enums ==========
PAGE_SPLASH = "splash"
PAGE_MENU = "menu"
PAGE_GAME = "game"
PAGE_RESULT = "result"
PAGE_SETTINGS = "settings"
PAGE_MODES = "modes"
