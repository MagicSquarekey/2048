# -*- coding: utf-8 -*-
# @Function: 全局配置 - iOS 风格改造后

import os

# ========== 窗口配置 ==========
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "2048"
FPS = 60

# ========== 棋盘配置 ==========
BOARD_SIZE = 4
TILE_SIZE = 90          # 略微缩小以增加间距感
TILE_GAP = 12           # iOS 风格更宽松的间距
BOARD_PADDING = 16      # 优化为8pt网格对齐（原15→16）
BOARD_X = (WINDOW_WIDTH - (TILE_SIZE * BOARD_SIZE + TILE_GAP * (BOARD_SIZE - 1))) // 2
BOARD_Y = 110

# ========== iOS 颜色系统 ==========

# 背景色
COLOR_BG = (242, 242, 247)              # iOS System Gray 6
COLOR_BOARD_BG = (255, 255, 255)        # 纯白棋盘卡片
COLOR_TILE_EMPTY = (230, 230, 235)      # iOS Gray 5

# 方块配色方案（iOS 渐变色系）
TILE_COLORS = {
    2:    ((230, 230, 235), (0, 0, 0)),         # 浅灰 + 黑字
    4:    ((210, 210, 218), (0, 0, 0)),         # 稍深灰 + 黑字
    8:    ((255, 159, 10),  (255, 255, 255)),   # iOS Orange + 白字
    16:   ((255, 94, 58),   (255, 255, 255)),   # iOS Red-Orange + 白字
    32:   ((255, 59, 48),   (255, 255, 255)),   # iOS Red + 白字
    64:   ((191, 64, 69),   (255, 255, 255)),   # 深红 + 白字
    128:  ((255, 204, 0),   (0, 0, 0)),         # iOS Yellow + 黑字
    256:  ((255, 179, 64),  (0, 0, 0)),         # 金黄 + 黑字
    512:  ((255, 149, 0),   (255, 255, 255)),   # iOS Orange + 白字
    1024: ((255, 100, 0),   (255, 255, 255)),   # 深橙 + 白字
    2048: ((255, 214, 10),  (0, 0, 0)),         # 金色 + 黑字
}

# UI 文字颜色（优化对比度，符合WCAG AA标准）
COLOR_TEXT = (0, 0, 0)                   # 主要文字 - 纯黑（对比度21:1）
COLOR_TEXT_SECONDARY = (48, 48, 54)      # 次要文字 - iOS Gray（对比度≥4.5:1，原60→48）
COLOR_TEXT_TERTIARY = (100, 100, 108)    # 第三级文字（优化对比度5.2:1，原120→100）
COLOR_TEXT_QUATERNARY = (142, 142, 147)  # 第四级文字（仅装饰性，对比度3.5:1）

# 兼容旧代码的常量别名
COLOR_TEXT_LIGHT = (255, 255, 255)       # 浅色文字 - 白色（按钮文字用）
COLOR_TEXT_LIGHT_SECONDARY = (242, 242, 247)  # 浅色次要文字（对比度15:1）

# 按钮颜色（iOS Blue 系统色）
COLOR_BTN_PRIMARY = (0, 122, 255)
COLOR_BTN_PRIMARY_HOVER = (10, 132, 255)
COLOR_BTN_SECONDARY = (242, 242, 247)
COLOR_BTN_SECONDARY_HOVER = (230, 230, 235)
COLOR_BTN_DANGER = (255, 59, 48)
COLOR_BTN_DANGER_HOVER = (255, 69, 58)

# iOS 系统色
COLOR_GREEN = (52, 199, 89)           # iOS Green (成功/开)
COLOR_ORANGE = (255, 149, 0)          # iOS Orange
COLOR_TEAL = (90, 200, 250)           # iOS Teal (信息提示)
COLOR_INDIGO = (88, 86, 214)          # iOS Indigo (链接)
COLOR_PINK = (255, 45, 85)            # iOS Pink (强调)
COLOR_YELLOW = (255, 204, 0)          # iOS Yellow (警告)
COLOR_RED = (255, 59, 48)             # iOS Red (错误/危险)

# 分数显示
COLOR_SCORE_BG = (230, 230, 235)         # iOS Gray 5 (与页面背景区分)

# 遮罩（iOS 更浅）
COLOR_OVERLAY = (0, 0, 0, 40)

# 交互参数
SWIPE_THRESHOLD = 30  # 滑动最小距离（像素）

# ========== 游戏参数 ==========
INITIAL_TILES = 2
WIN_TILE = 2048
UNDO_LIMIT_DEFAULT = 3
CLEAN_LIMIT_DEFAULT = 1

# 随机生成概率
TILE_2_PROBABILITY = 0.9

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

# ========== 动画配置（iOS 弹簧动画） ==========
ANIMATION_MOVE_DURATION = 150       # 移动动画（ms）- 保持快速响应
ANIMATION_MERGE_DURATION = 200      # 合并动画（ms）
ANIMATION_SPAWN_DURATION = 150      # 生成动画（ms）
ANIMATION_FADE_DURATION = 300       # 淡入淡出（ms）

# 弹簧动画参数 - 优化为更平滑
SPRING_DAMPING = 0.85              # 增加阻尼，减少弹跳
SPRING_FREQUENCY = 1.8             # 降低频率，更自然

# ========== 字号配置（iOS 8pt 网格） ==========
def _find_chinese_font() -> str:
    """查找系统中可用的中文字体"""
    font_candidates = [
        # Windows字体（优先）
        "msyh.ttc",         # 微软雅黑
        "simhei.ttf",       # 黑体
        "simsun.ttc",       # 宋体
        # macOS字体（仅在macOS系统有效，Windows下会跳过）
        # "PingFang.ttc",   # PingFang SC（仅macOS）
    ]
    for font_name in font_candidates:
        font_path = os.path.join("C:\\Windows\\Fonts", font_name)
        if os.path.exists(font_path):
            return font_path
    return None

FONT_PATH = _find_chinese_font()

# iOS 标准字号（8pt 网格）
FONT_SIZE_CAPTION2 = 11
FONT_SIZE_CAPTION1 = 12
FONT_SIZE_FOOTNOTE = 13
FONT_SIZE_SUBHEAD = 15
FONT_SIZE_BODY = 17
FONT_SIZE_TITLE3 = 20
FONT_SIZE_TITLE2 = 22
FONT_SIZE_TITLE1 = 28
FONT_SIZE_LARGE_TITLE = 34

# 兼容旧接口
FONT_SIZE_LARGE = FONT_SIZE_LARGE_TITLE
FONT_SIZE_MEDIUM = FONT_SIZE_BODY
FONT_SIZE_SMALL = FONT_SIZE_FOOTNOTE
FONT_SIZE_TINY = FONT_SIZE_CAPTION1

# 方块数字字号映射
TILE_FONT_SIZES = {
    2: 36, 4: 36, 8: 36,
    16: 34, 32: 34, 64: 34,
    128: 30, 256: 30, 512: 30,
    1024: 26, 2048: 26,
}

# ========== 圆角配置 ==========
RADIUS_SM = 8        # 小圆角
RADIUS_MD = 12       # 中圆角
RADIUS_LG = 16       # 大圆角
RADIUS_XL = 20       # 棋盘

# ========== iOS 8pt网格间距系统 ==========
IOS_SPACING_BASE = 8   # 基础间距单位

# 间距令牌
IOS_SPACING_XXS = 2    # 极小间距（特殊情况）
IOS_SPACING_XS = 4     # 4pt
IOS_SPACING_SM = 8     # 8pt（基础单位）
IOS_SPACING_MD = 16    # 16pt（2倍基础）
IOS_SPACING_LG = 24    # 24pt（3倍基础）
IOS_SPACING_XL = 32    # 32pt（4倍基础）
IOS_SPACING_XXL = 40   # 40pt（5倍基础）
IOS_SPACING_XXXL = 48  # 48pt（6倍基础）

# 兼容旧接口
SPACING_TINY = IOS_SPACING_XS
SPACING_SMALL = IOS_SPACING_SM
SPACING_MEDIUM = IOS_SPACING_MD
SPACING_LARGE = IOS_SPACING_LG
SPACING_HUGE = IOS_SPACING_XL

# ========== 道具配置 ==========
FREE_DAILY_LIMIT = 5
AD_REWARD_AMOUNT = 1
AD_COOLDOWN = 30

# ========== 数据存储路径 ==========
DATA_DIR = os.path.join(os.path.expanduser("~"), "AppData", "Local", "2048_Game")
DATA_FILE = os.path.join(DATA_DIR, "game_data.json")
os.makedirs(DATA_DIR, exist_ok=True)

# ========== 页面枚举 ==========
PAGE_SPLASH = "splash"
PAGE_MENU = "menu"
PAGE_GAME = "game"
PAGE_RESULT = "result"
PAGE_SETTINGS = "settings"
PAGE_MODES = "modes"
