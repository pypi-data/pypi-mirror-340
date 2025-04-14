import asyncio
import os
from typing import List, Optional
from loguru import logger
from playwright.async_api import Page, Browser, TimeoutError
from urllib.parse import quote_plus, unquote
import random
import re

class GoogleImageCrawler:
    def __init__(self, browser: Browser):
        self.browser = browser
        
    async def _wait_for_images(self, page: Page, timeout: int = 10000) -> bool:
        """等待图片加载完成"""
        try:
            # 等待图片容器加载
            await page.wait_for_selector('div[jsname="dTDiAc"]', timeout=timeout)
            # 等待图片元素加载
            await page.wait_for_selector('div[jsname="dTDiAc"] img', timeout=timeout)
            return True
        except TimeoutError:
            logger.warning("等待图片加载超时")
            return False
            
    async def _extract_real_url(self, href: str) -> Optional[str]:
        """从Google重定向链接中提取真实URL"""
        try:
            if 'url=' in href:
                # 提取url参数
                url_match = re.search(r'url=([^&]+)', href)
                if url_match:
                    real_url = unquote(url_match.group(1))
                    if real_url.startswith('http'):
                        return real_url
            return None
        except Exception as e:
            logger.error(f"提取真实URL时发生错误: {e}")
            return None
            
    async def _get_image_url(self, page: Page, element) -> Optional[str]:
        """点击图片并获取真实URL"""
        try:
            # 检查元素是否存在
            if not element:
                logger.warning("未找到图片元素")
                return None
                
            # 获取元素位置
            box = await element.bounding_box()
            if not box:
                logger.warning("无法获取图片元素位置")
                return None
                
            # 滚动到元素位置
            await page.evaluate('''(y) => {
                window.scrollTo({
                    top: y - window.innerHeight / 2,
                    behavior: 'smooth'
                });
            }''', box['y'])
            
            # 等待滚动完成
            await asyncio.sleep(1)
            
            # 点击图片
            try:
                await element.click(timeout=5000)
            except Exception as e:
                logger.warning(f"点击图片失败: {e}")
                return None
                
            # 等待大图加载，使用较短的超时时间
            try:
                await page.wait_for_selector('img[jsname="kn3ccd"]', timeout=3000)
            except TimeoutError:
                # 如果超时，尝试其他选择器
                try:
                    await page.wait_for_selector('img.sFlh5c.FyHeAf.iPVvYb', timeout=3000)
                except TimeoutError:
                    # 如果还是超时，尝试从链接获取
                    pass
            
            # 首先尝试从链接中获取URL
            image_url = await page.evaluate('''() => {
                const link = document.querySelector('a[data-ved]');
                return link ? link.getAttribute('href') : null;
            }''')
            
            if image_url:
                real_url = await self._extract_real_url(image_url)
                if real_url:
                    logger.debug(f"从链接中获取图片URL: {real_url}")
                    return real_url
            
            # 获取大图URL
            image_url = await page.evaluate('''() => {
                const img = document.querySelector('img[jsname="kn3ccd"]');
                return img ? img.src : null;
            }''')
            
            if image_url and image_url.startswith('http'):
                logger.debug(f"成功获取图片URL: {image_url}")
                return image_url
                
            # 尝试其他选择器
            image_url = await page.evaluate('''() => {
                const img = document.querySelector('img.sFlh5c.FyHeAf.iPVvYb');
                return img ? img.src : null;
            }''')
            
            if image_url and image_url.startswith('http'):
                logger.debug(f"通过备用选择器获取图片URL: {image_url}")
                return image_url
            
            # 如果所有方法都失败，尝试直接从缩略图获取URL
            image_url = await page.evaluate('''() => {
                const img = document.querySelector('div[jsname="dTDiAc"] img');
                return img ? img.src : null;
            }''')
            
            if image_url and image_url.startswith('http'):
                logger.debug(f"从缩略图获取图片URL: {image_url}")
                return image_url
                
            logger.warning("未找到有效的图片URL")
            return None
            
        except TimeoutError:
            logger.warning("获取图片URL超时，跳过当前图片")
            return None
        except Exception as e:
            logger.error(f"获取图片URL时发生错误: {e}")
            return None
            
    async def _scroll_page(self, page: Page, max_scrolls: int = 5):
        """滚动页面加载更多图片"""
        for i in range(max_scrolls):
            try:
                # 滚动到底部
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                # 随机等待
                await asyncio.sleep(random.uniform(1, 2))
                
                # 检查是否有新图片加载
                new_images = await page.query_selector_all('div[jsname="dTDiAc"]')
                if new_images:
                    logger.debug(f"第 {i+1} 次滚动，发现 {len(new_images)} 张新图片")
                    
            except Exception as e:
                logger.error(f"滚动页面时发生错误: {e}")
                break
                
    async def _extract_image_urls(self, page: Page, max_images: int = 20) -> List[str]:
        """提取图片URL列表"""
        image_urls = []
        processed_count = 0
        
        try:
            # 使用更稳定的选择器
            image_elements = await page.query_selector_all('div[jsname="dTDiAc"]')
            logger.info(f"找到 {len(image_elements)} 个图片元素")
            
            for i, element in enumerate(image_elements):
                if processed_count >= max_images:
                    break
                    
                try:
                    # 直接使用元素而不是构建选择器
                    image_url = await self._get_image_url(page, element)
                    if image_url:
                        image_urls.append(image_url)
                        processed_count += 1
                        logger.info(f"已处理 {processed_count}/{max_images} 张图片")
                        
                    # 随机等待，避免被检测
                    await asyncio.sleep(random.uniform(0.5, 1.5))
                    
                except Exception as e:
                    logger.error(f"处理第 {i+1} 张图片时发生错误: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"提取图片URL时发生错误: {e}")
            
        return image_urls
        
    async def crawl_images(self, keyword: str, max_images: int = 20, proxy: Optional[str] = None) -> List[str]:
        """爬取Google图片搜索结果"""
        all_image_urls = []
        
        try:
            # 构建搜索URL，不添加start参数
            search_url = f"https://www.google.com/search?q={quote_plus(keyword)}&tbm=isch"
            logger.info(f"正在爬取图片: {search_url}, 目标数量: {max_images}")
            
            # 创建新页面
            context_options = {
                'ignore_https_errors': True,
                'java_script_enabled': True,
                'viewport': {'width': 1920, 'height': 1080}
            }
            
            # 添加代理支持
            if proxy:
                context_options['proxy'] = {
                    'server': proxy
                }
                logger.info(f"使用代理: {proxy}")
                
            context = await self.browser.new_context(**context_options)
            page = await context.new_page()
            
            # 设置全屏
            await page.evaluate('''() => {
                const elem = document.documentElement;
                if (elem.requestFullscreen) {
                    elem.requestFullscreen();
                } else if (elem.webkitRequestFullscreen) {
                    elem.webkitRequestFullscreen();
                } else if (elem.msRequestFullscreen) {
                    elem.msRequestFullscreen();
                }
            }''')
            
            try:
                # 访问搜索页面
                await page.goto(search_url, wait_until='networkidle')
                
                # 等待图片加载
                if not await self._wait_for_images(page):
                    logger.warning("页面加载失败")
                    return []
                    
                # 滚动页面加载更多图片，直到达到目标数量或无法加载更多
                scroll_count = 0
                while len(all_image_urls) < max_images and scroll_count < 10:  # 最多滚动10次
                    await self._scroll_page(page)
                    scroll_count += 1
                    
                    # 提取图片URL
                    new_urls = await self._extract_image_urls(page, max_images - len(all_image_urls))
                    all_image_urls.extend(new_urls)
                    
                    if len(new_urls) == 0:
                        logger.info("没有更多图片可加载")
                        break
                        
                    logger.info(f"当前已获取 {len(all_image_urls)}/{max_images} 张图片")
                    
                logger.info(f"爬取完成，获取到 {len(all_image_urls)} 张图片")
                
            finally:
                await page.close()
                await context.close()
                
        except Exception as e:
            logger.error(f"爬取图片时发生错误: {e}")
            
        return all_image_urls[:max_images]  # 确保不超过请求的数量 