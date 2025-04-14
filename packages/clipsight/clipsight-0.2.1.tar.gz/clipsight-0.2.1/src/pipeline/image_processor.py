import asyncio
import aiohttp
from typing import Optional, List, Dict, Any
from PIL import Image
import io
from loguru import logger
import random
from datetime import datetime
import hashlib

class ImageProcessor:
    def __init__(
        self,
        max_concurrent_downloads: int = 5,
        timeout: int = 30,
        min_image_size: int = 1024,  # 1KB
        max_image_size: int = 10 * 1024 * 1024  # 10MB
    ):
        self.max_concurrent_downloads = max_concurrent_downloads
        self.timeout = timeout
        self.min_image_size = min_image_size
        self.max_image_size = max_image_size
        self.semaphore = asyncio.Semaphore(max_concurrent_downloads)
        
    async def download_image(self, url: str, proxy: Optional[str] = None) -> Optional[bytes]:
        """异步下载图片"""
        async with self.semaphore:
            try:
                # 添加随机延迟
                await asyncio.sleep(random.uniform(0.5, 3))
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        url,
                        proxy=proxy,
                        timeout=self.timeout
                    ) as response:
                        if response.status == 200:
                            data = await response.read()
                            if self._validate_image_size(len(data)):
                                return data
                            else:
                                logger.warning(f"图片大小不符合要求: {url}")
                        else:
                            logger.warning(f"下载失败，状态码: {response.status}, URL: {url}")
            except Exception as e:
                logger.error(f"下载图片时发生错误: {url}, 错误: {e}")
            return None
            
    def _validate_image_size(self, size: int) -> bool:
        """验证图片大小是否在允许范围内"""
        return self.min_image_size <= size <= self.max_image_size
        
    def validate_image_content(self, image_data: bytes) -> bool:
        """验证图片内容是否有效"""
        try:
            img = Image.open(io.BytesIO(image_data))
            img.verify()  # 验证图片完整性
            return True
        except Exception as e:
            logger.error(f"图片验证失败: {e}")
            return False
            
    def generate_image_hash(self, image_data: bytes) -> str:
        """生成图片哈希值用于去重"""
        return hashlib.md5(image_data).hexdigest()
        
    async def process_image_batch(
        self,
        urls: List[str],
        proxy: Optional[str] = None,
        keywords: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """批量处理图片"""
        tasks = [self.download_image(url, proxy) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        processed_images = {}
        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                logger.error(f"处理图片时发生错误: {url}, 错误: {result}")
                continue
                
            if result and self.validate_image_content(result):
                image_hash = self.generate_image_hash(result)
                processed_images[image_hash] = {
                    'data': result,
                    'url': url,
                    'source_domain': self._extract_domain(url),
                    'created_at': datetime.now().isoformat(),
                    'size': len(result),
                    'hash': image_hash,
                    'keywords': keywords or []  # 添加关键词列表
                }
            else:
                logger.warning(f"图片验证失败或下载失败: {url}")
                
        return processed_images
        
    def _extract_domain(self, url: str) -> str:
        """从URL中提取域名"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except Exception:
            return "" 