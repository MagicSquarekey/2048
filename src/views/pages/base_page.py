# -*- coding: utf-8 -*-
# @Function: 页面基类与页面管理器

import pygame
from typing import Dict, Optional, Any


class Page:
    """页面基类"""

    def __init__(self, name: str) -> None:
        self.name = name
        self.active = False

    def on_enter(self, **kwargs: Any) -> None:
        """进入页面时调用"""
        self.active = True

    def on_exit(self) -> None:
        """离开页面时调用"""
        self.active = False

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """
        处理事件
        
        Returns:
            目标页面名称，None 表示留在当前页面
        """
        return None

    def update(self, dt: float) -> Optional[str]:
        """
        更新页面状态
        
        Returns:
            目标页面名称，None 表示留在当前页面
        """
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """绘制页面"""
        pass


class PageManager:
    """页面管理器 - 管理页面切换"""

    _instance: Optional["PageManager"] = None

    def __new__(cls) -> "PageManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._pages = {}
            cls._instance._current_page = None
            cls._instance._page_stack = []
        return cls._instance

    def register_page(self, page: Page) -> None:
        """注册页面"""
        self._pages[page.name] = page

    def get_page(self, name: str) -> Optional[Page]:
        """获取页面"""
        return self._pages.get(name)

    def switch_to(self, page_name: str, **kwargs: Any) -> None:
        """切换到指定页面"""
        if self._current_page:
            self._current_page.on_exit()
        self._current_page = self._pages.get(page_name)
        if self._current_page:
            self._current_page.on_enter(**kwargs)

    def push_page(self, page_name: str, **kwargs: Any) -> None:
        """压入新页面（保留当前页面）"""
        if self._current_page:
            self._page_stack.append(self._current_page)
            self._current_page.active = False
        self._current_page = self._pages.get(page_name)
        if self._current_page:
            self._current_page.on_enter(**kwargs)

    def pop_page(self) -> None:
        """弹出当前页面，返回上一个页面"""
        if self._current_page:
            self._current_page.on_exit()
        if self._page_stack:
            self._current_page = self._page_stack.pop()
            self._current_page.active = True
        else:
            self._current_page = None

    @property
    def current_page(self) -> Optional[Page]:
        """获取当前页面"""
        return self._current_page

    def handle_event(self, event: pygame.event.Event) -> None:
        """分发事件到当前页面"""
        if self._current_page:
            target = self._current_page.handle_event(event)
            if target:
                self.switch_to(target)

    def update(self, dt: float) -> None:
        """更新当前页面"""
        if self._current_page:
            target = self._current_page.update(dt)
            if target:
                self.switch_to(target)

    def draw(self, surface: pygame.Surface) -> None:
        """绘制当前页面"""
        if self._current_page:
            self._current_page.draw(surface)
