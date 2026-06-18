# -*- coding: utf-8 -*-
# @Function: 页面基类与页面管理器 / Page base class and page manager

import pygame
from typing import Dict, Optional, Any


class Page:
    """页面基类 / Page base class"""

    def __init__(self, name: str) -> None:
        self.name = name
        self.active = False

    def on_enter(self, **kwargs: Any) -> None:
        """进入页面时调用 / Called when entering page"""
        self.active = True

    def on_exit(self) -> None:
        """离开页面时调用 / Called when exiting page"""
        self.active = False

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """
        处理事件 / Handle event
        
        Returns:
            目标页面名称，None 表示留在当前页面 / Target page name, None to stay on current page
        """
        return None

    def update(self, dt: float) -> None:
        """
        更新页面状态 / Update page state
        
        Args:
            dt: 帧间隔时间 / Frame delta time
        """
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """绘制页面 / Draw page"""
        pass

    """页面管理器 - 管理页面切换 / Page manager - manages page switching"""
class PageManager:
    """页面管理器 - 管理页面切换 / Page manager - manages page switching"""

    _instance: Optional["PageManager"] = None

    def __new__(cls) -> "PageManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._pages = {}
            cls._instance._current_page = None
            cls._instance._page_stack = []
        return cls._instance
        """注册页面 / Register page"""
    def register_page(self, page: Page) -> None:
        """注册页面 / Register page"""
        self._pages[page.name] = page
        """获取页面 / Get page"""
    def get_page(self, name: str) -> Optional[Page]:
        """获取页面 / Get page"""
        return self._pages.get(name)
        """切换到指定页面 / Switch to specified page"""
    def switch_to(self, page_name: str, **kwargs: Any) -> None:
        """切换到指定页面 / Switch to specified page"""
        if self._current_page:
            self._current_page.on_exit()
        self._current_page = self._pages.get(page_name)
        if self._current_page:
            self._current_page.on_enter(**kwargs)
        """压入新页面（保留当前页面）/ Push new page (keep current page)"""
    def push_page(self, page_name: str, **kwargs: Any) -> None:
        """压入新页面（保留当前页面）/ Push new page (keep current page)"""
        if self._current_page:
            self._page_stack.append(self._current_page)
            self._current_page.active = False
        self._current_page = self._pages.get(page_name)
        if self._current_page:
            self._current_page.on_enter(**kwargs)

    def pop_page(self) -> None:
        """弹出当前页面，返回上一个页面 / Pop current page, return to previous"""
        if self._current_page:
            self._current_page.on_exit()
        if self._page_stack:
            self._current_page = self._page_stack.pop()
            self._current_page.active = True
        else:
            self._current_page = None

    @property
    def current_page(self) -> Optional[Page]:
        """获取当前页面 / Get current page"""
        return self._current_page

    def handle_event(self, event: pygame.event.Event) -> None:
        """分发事件到当前页面 / Dispatch event to current page"""
        if self._current_page:
            target = self._current_page.handle_event(event)
            if target:
                self.switch_to(target)

    def update(self, dt: float) -> None:
        """更新当前页面 / Update current page"""
        if self._current_page:
            target = self._current_page.update(dt)
            if target:
                self.switch_to(target)

    def draw(self, surface: pygame.Surface) -> None:
        """绘制当前页面 / Draw current page"""
        if self._current_page:
            self._current_page.draw(surface)
