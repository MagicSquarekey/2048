# -*- coding: utf-8 -*-
# @Function: 全局配置 - 颜色、尺寸、字体、游戏参数

import os

# ========== 窗口配置 ==========
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "2048 休闲游戏"
FPS = 60

# ========== 棋盘配置 ==========
BOARD_SIZE = 4          # 4×4 棋盘
TILE_SIZE = 100         # 方块尺寸（像素）
TILE_GAP = 10           # 方块间距（像素）
BOARD_PADDING = 20      # 棋盘内边距
BOARD_X = (WINDOW_WIDTH - (TILE_SIZE * BOARD_SIZE + TILE_GAP * (BOARD_SIZE - 1))) // 2
BOARD_Y = 150           # 棋盘起始 Y 坐标

# ========== 颜色方案（低饱和度柔和风格） ==========
# 背景色
COLOR_BG = (250, 248, 239)              # 游戏背景 - 米白
COLOR_BOARD_BG = (187, 173, 160)        # 棋盘背景 - 深米色
COLOR_TILE_EMPTY = (205, 193, 180)      # 空方块 - 浅米色

# 方块颜色方案（值 -> (背景色, 文字色)）
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

# UI 颜色
COLOR_TEXT = (119, 110, 101)             # 主文字 - 深棕
COLOR_TEXT_LIGHT = (249, 246, 242)       # 浅色文字 - 白
COLOR_TEXT_SCORE = (249, 246, 242)       # 分数文字

# 按钮颜色
COLOR_BTN_PRIMARY = (119, 110, 101)
COLOR_BTN_PRIMARY_HOVER = (140, 130, 120)
COLOR_BTN_SECONDARY = (186, 173, 160)
COLOR_BTN_SECONDARY_HOVER = (200, 190, 180)
COLOR_BTN_DANGER = (200, 80, 80)
COLOR_BTN_DANGER_HOVER = (220, 100, 100)

# 交互参数
SWIPE_THRESHOLD = 30  # 滑动最小距离（像素）- 白
COLOR_SCORE_BG = (187, 173, 160)         # 分数背景 - 深米色

# 按钮颜色
COLOR_BTN_PRIMARY = (143, 122, 102)      # 主按钮 - 棕色
COLOR_BTN_PRIMARY_HOVER = (163, 142, 122)
COLOR_BTN_SECONDARY = (187, 173, 160)    # 次按钮 - 米色
COLOR_BTN_SECONDARY_HOVER = (207, 193, 180)
COLOR_BTN_DANGER = (246, 94, 59)         # 危险按钮 - 红色
COLOR_BTN_DANGER_HOVER = (256, 114, 79)

# 遮罩颜色
COLOR_OVERLAY = (0, 0, 0, 150)          # 半透明黑色遮罩

# ========== 游戏参数 ==========
INITIAL_TILES = 2           # 初始方块数量
WIN_TILE = 2048             # 获胜目标数字
UNDO_LIMIT_DEFAULT = 2      # 新用户默认撤销次数
CLEAN_LIMIT_DEFAULT = 0     # 新用户默认清理次数
AD_COOLDOWN = 20            # 广告冷却时间（秒）
MAX_AD_PER_DAY = 5          # 每日广告上限

# 随机生成概率
TILE_2_PROBABILITY = 0.9    # 生成 2 的概率（90%）

# 分数计算
SCORE_MULTIPLIERS = {
    "classic": 1.0,
    "timed": 1.5,
    "challenge": 2.0,
}

# ========== 游戏模式配置 ==========
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

# ========== 动画配置 ==========
ANIMATION_MOVE_DURATION = 150       # 方块移动动画时长（毫秒）
ANIMATION_MERGE_DURATION = 200      # 方块合并动画时长（毫秒）
ANIMATION_SPAWN_DURATION = 150      # 方块生成动画时长（毫秒）
ANIMATION_FADE_DURATION = 300       # 淡入淡出动画时长（毫秒）

# ========== 字体配置 ==========
FONT_PATH = None  # 使用 Pygame 默认字体
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24
FONT_SIZE_TINY = 18

# 方块数字大小映射
TILE_FONT_SIZES = {
    2: 40, 4: 40, 8: 40,
    16: 36, 32: 36, 64: 36,
    128: 32, 256: 32, 512: 32,
    1024: 28, 2048: 28,
}

# ========== 道具配置 ==========
UNDO_LIMIT_DEFAULT = 3       # 每局默认撤销次数
CLEAN_LIMIT_DEFAULT = 1      # 每局默认清除次数

# ========== 广告/激励配置 ==========
FREE_DAILY_LIMIT = 5         # 每日免费观看广告次数
AD_REWARD_AMOUNT = 1         # 每次观看广告获得的道具数量
AD_COOLDOWN = 30             # 广告冷却时间（秒）

# ========== 数据存储路径 ==========
DATA_DIR = os.path.join(os.path.expanduser("~"), "AppData", "Local", "2048_Game")
DATA_FILE = os.path.join(DATA_DIR, "game_data.json")

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

# ========== 页面枚举 ==========
PAGE_SPLASH = "splash"
PAGE_MENU = "menu"
PAGE_GAME = "game"
PAGE_RESULT = "result"
PAGE_SETTINGS = "settings"
PAGE_MODES = "modes"
