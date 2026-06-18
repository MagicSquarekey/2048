# -*- coding: utf-8 -*-
"""页面子包 — 菜单、游戏、设置、结果等页面 / Page sub-package — menu, game, settings, result, etc."""
from src.views.pages.base_page import Page, PageManager
from src.views.pages.menu_page import MenuPage
from src.views.pages.game_page import GamePage
from src.views.pages.result_page import ResultPage
from src.views.pages.settings_page import SettingsPage
from src.views.pages.achievements_page import AchievementsPage
from src.views.pages.pause_page import PausePage
from src.views.pages.login_page import LoginPage

__all__ = [
    "Page", "PageManager",
    "MenuPage", "GamePage", "ResultPage",
    "SettingsPage", "AchievementsPage",
    "PausePage", "LoginPage",
]
