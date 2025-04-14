import asyncio
from typing import Optional, List
from playwright.async_api import async_playwright, Browser, BrowserContext
from loguru import logger
import random
import time
import os

class PlaywrightPool:
    def __init__(self, max_instances: int = 3):
        self.max_instances = max_instances
        self.available_browsers: List[Browser] = []
        self.in_use_browsers: List[Browser] = []
        self._lock = asyncio.Lock()
        self.playwright = None
        
    async def initialize(self):
        """初始化 Playwright 和浏览器实例池"""
        self.playwright = await async_playwright().start()
        for _ in range(self.max_instances):
            browser = await self._create_browser()
            if browser:
                self.available_browsers.append(browser)
                
    async def _create_browser(self) -> Optional[Browser]:
        """创建新的浏览器实例"""
        try:
            # 添加随机延迟，避免同时启动多个实例
            await asyncio.sleep(random.uniform(0.5, 2))
            
            # 从环境变量获取浏览器显示模式
            headless = os.getenv('BROWSER_HEADLESS', 'true').lower() == 'true'
            if not headless:
                logger.info("浏览器将以有界面模式运行")
            else:
                logger.info("浏览器将以无界面模式运行")
                
            browser = await self.playwright.chromium.launch(
                headless=headless,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            return browser
        except Exception as e:
            logger.error(f"Failed to create browser instance: {e}")
            return None
            
    async def get_browser(self) -> Optional[Browser]:
        """获取一个可用的浏览器实例"""
        async with self._lock:
            if self.available_browsers:
                browser = self.available_browsers.pop()
                self.in_use_browsers.append(browser)
                return browser
            elif len(self.in_use_browsers) < self.max_instances:
                browser = await self._create_browser()
                if browser:
                    self.in_use_browsers.append(browser)
                    return browser
            return None
            
    async def release_browser(self, browser: Browser):
        """释放浏览器实例回池中"""
        async with self._lock:
            if browser in self.in_use_browsers:
                self.in_use_browsers.remove(browser)
                try:
                    # 检查浏览器是否仍然可用
                    context = await browser.new_context()
                    await context.close()
                    self.available_browsers.append(browser)
                except Exception as e:
                    logger.error(f"Browser instance is broken, destroying: {e}")
                    await self._destroy_browser(browser)
                    
    async def _destroy_browser(self, browser: Browser):
        """销毁不可用的浏览器实例"""
        try:
            await browser.close()
        except Exception as e:
            logger.error(f"Error while destroying browser: {e}")
            
    async def cleanup(self):
        """清理所有浏览器实例和 Playwright"""
        for browser in self.available_browsers + self.in_use_browsers:
            await self._destroy_browser(browser)
        if self.playwright:
            await self.playwright.stop()
            
    async def __aenter__(self):
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup() 