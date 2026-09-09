# -*- coding: utf-8 -*-
# @Function: 全局配置 - 深空霓虹主题 / Deep-space neon theme

import os

# ========== 窗口配置 ==========
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "2048"
FPS = 60

# ========== 棋盘配置 ==========
BOARD_SIZE = 4
TILE_SIZE = 90          # 略微缩小以增加间距感
TILE_GAP = 12           # 更宽松的间距
BOARD_PADDING = 16      # 8pt网格对齐
BOARD_X = (WINDOW_WIDTH - (TILE_SIZE * BOARD_SIZE + TILE_GAP * (BOARD_SIZE - 1))) // 2
BOARD_Y = 118

# ========== 深空霓虹 - 背景渐变 ==========
BG_GRADIENT_TOP = (22, 24, 48)        # 深靛蓝
BG_GRADIENT_BOTTOM = (44, 36, 84)     # 暗紫
BG_GLOW_BLUE = (64, 110, 255)         # 左上光斑（霓虹蓝）
BG_GLOW_PURPLE = (150, 70, 255)       # 右下光斑（霓虹紫）

# 兼容旧代码：COLOR_BG 作为纯色兜底（页面实际用 blit_background 绘制渐变）
COLOR_BG = BG_GRADIENT_TOP

# ========== 卡片 / 面板 ==========
CARD_BG = (40, 42, 76)                # 玻璃卡片底色
CARD_BG_LIGHT = (52, 55, 94)          # 悬停/高亮卡片
CARD_BORDER = (92, 96, 150)           # 卡片描边
COLOR_BOARD_BG = (32, 34, 64)         # 棋盘卡片
COLOR_TILE_EMPTY = (48, 51, 86)       # 空格子

# ========== 文字颜色（深色背景，高对比） ==========
COLOR_TEXT = (245, 246, 252)                 # 主要文字 - 近白
COLOR_TEXT_SECONDARY = (178, 182, 214)       # 次要文字
COLOR_TEXT_TERTIARY = (132, 136, 170)        # 第三级文字
COLOR_TEXT_QUATERNARY = (102, 106, 140)      # 第四级文字（仅装饰）

# 兼容旧代码的常量别名
COLOR_TEXT_LIGHT = (255, 255, 255)
COLOR_TEXT_LIGHT_SECONDARY = (242, 242, 247)

# ========== 霓虹强调色 ==========
ACCENT_BLUE = (72, 158, 255)          # 霓虹蓝（当前分数/主按钮）
ACCENT_INDIGO = (128, 100, 255)       # 霓虹紫
ACCENT_ORANGE = (255, 152, 64)        # 霓虹橙（最高分）
ACCENT_PINK = (255, 90, 140)          # 霓虹粉（挑战模式）
ACCENT_GREEN = (56, 220, 168)         # 霓虹绿（成功）
ACCENT_GOLD = (255, 208, 84)          # 霓虹金（成就/2048）

# 按钮颜色（兼容旧常量名）
COLOR_BTN_PRIMARY = ACCENT_BLUE
COLOR_BTN_PRIMARY_HOVER = (104, 178, 255)
COLOR_BTN_SECONDARY = CARD_BG_LIGHT
COLOR_BTN_SECONDARY_HOVER = (66, 70, 116)
COLOR_BTN_DANGER = (255, 84, 96)
COLOR_BTN_DANGER_HOVER = (255, 112, 122)

# iOS 系统色别名（兼容旧代码，映射到霓虹色）
COLOR_GREEN = ACCENT_GREEN
COLOR_ORANGE = ACCENT_ORANGE
COLOR_TEAL = (80, 210, 250)
COLOR_INDIGO = ACCENT_INDIGO
COLOR_PINK = ACCENT_PINK
COLOR_YELLOW = ACCENT_GOLD
COLOR_RED = (255, 84, 96)

# 分数显示
COLOR_SCORE_BG = CARD_BG

# ========== 方块配色（深色主题霓虹色系：(底色, 文字色)） ==========
TILE_COLORS = {
    2:    ((94, 98, 140),     (238, 240, 252)),   # 石板蓝 + 近白
    4:    ((116, 121, 170),   (242, 244, 252)),   # 亮石板 + 近白
    8:    ((255, 148, 78),    (255, 255, 255)),   # 柔橙 + 白
    16:   ((255, 122, 64),    (255, 255, 255)),   # 鲜橙 + 白
    32:   ((255, 92, 86),     (255, 255, 255)),   # 珊瑚红 + 白
    64:   ((255, 64, 96),     (255, 255, 255)),   # 霓虹红粉 + 白
    128:  ((255, 202, 72),    (42, 36, 12)),      # 暖金 + 深棕
    256:  ((255, 218, 88),    (42, 36, 12)),      # 亮金 + 深棕
    512:  ((72, 222, 190),    (10, 42, 36)),      # 霓虹薄荷 + 深青
    1024: ((88, 182, 255),    (255, 255, 255)),   # 天蓝 + 白
    2048: ((160, 118, 255),   (255, 255, 255)),   # 霓虹紫 + 白
}

# 遮罩（深色主题用更深的遮罩保证前景可读）
COLOR_OVERLAY = (8, 8, 24, 170)

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
        "icon": "∞",
        "accent": ACCENT_BLUE,
    },
    "timed": {
        "name": "限时模式",
        "description": "60 秒内挑战目标分数！",
        "icon": "60″",
        "accent": ACCENT_ORANGE,
        "time_limit": 60,
        "target_score": 500,
    },
    "challenge": {
        "name": "挑战模式",
        "description": "限定步数内合成目标方块！",
        "icon": "128",
        "accent": ACCENT_PINK,
        "move_limit": 50,
        "target_tile": 128,
    },
}

# ========== 动画配置 ==========
ANIMATION_MOVE_DURATION = 120       # 移动动画（ms）- 快速响应
ANIMATION_MERGE_DURATION = 170      # 合并动画（ms）
ANIMATION_SPAWN_DURATION = 160      # 生成动画（ms）
ANIMATION_FADE_DURATION = 250       # 淡入淡出（ms）

# 弹簧动画参数
SPRING_DAMPING = 0.85
SPRING_FREQUENCY = 1.8

# ========== 输入流畅度配置 ==========
INPUT_QUEUE_MAX = 3            # 动画期间缓存的最大输入数
INPUT_APPLY_PROGRESS = 0.6     # 动画进度达到该比例即应用下一条输入
KEY_REPEAT_DELAY_MS = 220      # 按住方向键首次连发延迟
KEY_REPEAT_INTERVAL_MS = 110   # 按住方向键连发间隔

# ========== 字号配置（8pt 网格） ==========
def _find_chinese_font() -> str:
    """查找系统中可用的中文字体"""
    font_candidates = [
        # Windows字体（优先）
        "msyh.ttc",         # 微软雅黑
        "simhei.ttf",       # 黑体
        "simsun.ttc",       # 宋体
    ]
    for font_name in font_candidates:
        font_path = os.path.join("C:\\Windows\\Fonts", font_name)
        if os.path.exists(font_path):
            return font_path
    return None

FONT_PATH = _find_chinese_font()

# 标准字号（8pt 网格）
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

# ========== 8pt网格间距系统 ==========
IOS_SPACING_BASE = 8   # 基础间距单位

# 间距令牌
IOS_SPACING_XXS = 2
IOS_SPACING_XS = 4
IOS_SPACING_SM = 8
IOS_SPACING_MD = 16
IOS_SPACING_LG = 24
IOS_SPACING_XL = 32
IOS_SPACING_XXL = 40
IOS_SPACING_XXXL = 48

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
# 环境变量 GAME_2048_DATA_DIR 可重定向数据目录（测试隔离用，避免测试重置真实玩家数据）
DATA_DIR = os.environ.get("GAME_2048_DATA_DIR") or os.path.join(
    os.path.expanduser("~"), "AppData", "Local", "2048_Game"
)
DATA_FILE = os.path.join(DATA_DIR, "game_data.json")
os.makedirs(DATA_DIR, exist_ok=True)

# ========== 页面枚举 ==========
PAGE_SPLASH = "splash"
PAGE_MENU = "menu"
PAGE_GAME = "game"
PAGE_RESULT = "result"
PAGE_SETTINGS = "settings"
PAGE_MODES = "modes"
