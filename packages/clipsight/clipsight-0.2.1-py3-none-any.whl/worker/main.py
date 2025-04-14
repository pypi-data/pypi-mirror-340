import asyncio
import os
from dotenv import load_dotenv
from loguru import logger
from typing import Dict, Any, List
import json
from datetime import datetime
import sys
import redis

# 配置日志
logger.remove()
logger.add(sys.stderr, level="DEBUG")
logger.add("worker.log", rotation="500 MB")

# 加载环境变量
logger.info("正在加载环境变量...")
load_dotenv()
logger.info("环境变量加载完成")

from src.browser.pool import PlaywrightPool
from src.worker.consumer import TaskConsumer
from src.pipeline.image_processor import ImageProcessor
from src.search.similar_images import SimilarImageSearcher
from src.storage.minio_storage import MinioStorage
from src.crawler.google_images import GoogleImageCrawler

class ImageCrawlerWorker:
    def __init__(self):
        logger.info("初始化工作进程...")
        # 初始化Redis客户端
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0))
        )
        logger.info("Redis客户端初始化完成")
        
        # 初始化组件
        self.browser_pool = PlaywrightPool(
            max_instances=int(os.getenv('MAX_BROWSER_INSTANCES', 3))
        )
        logger.info("浏览器池初始化完成")
        
        self.task_consumer = TaskConsumer(
            redis_host=os.getenv('REDIS_HOST', 'localhost'),
            redis_port=int(os.getenv('REDIS_PORT', 6379)),
            redis_db=int(os.getenv('REDIS_DB', 0))
        )
        logger.info("任务消费者初始化完成")
        
        self.image_processor = ImageProcessor(
            max_concurrent_downloads=int(os.getenv('MAX_CONCURRENT_DOWNLOADS', 5))
        )
        logger.info("图片处理器初始化完成")
        
        self.similar_searcher = SimilarImageSearcher(
            es_host=os.getenv('ES_HOST', 'localhost'),
            es_port=int(os.getenv('ES_PORT', 9200))
        )
        logger.info("相似图片搜索器初始化完成")
        
        self.storage = MinioStorage(
            endpoint=os.getenv('MINIO_ENDPOINT', 'localhost:9000'),
            access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
            secret_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin'),
            bucket_name=os.getenv('MINIO_BUCKET', 'images')
        )
        logger.info("存储客户端初始化完成")
        
    async def initialize(self):
        """初始化所有组件"""
        logger.info("正在初始化浏览器池...")
        await self.browser_pool.initialize()
        logger.info("浏览器池初始化完成")
        
    async def process_task(self, task_data: dict):
        """处理单个任务"""
        task_id = task_data.get('task_id')
        keywords = task_data.get('keywords', [])
        max_images = task_data.get('max_images', 20)
        
        try:
            # 更新任务状态为处理中
            self.redis_client.set(f"task_status:{task_id}", "processing")
            self.redis_client.set(f"task_progress:{task_id}", "0")
            
            # 获取浏览器实例
            browser = await self.browser_pool.get_browser()
            if not browser:
                raise Exception("无法获取浏览器实例")
            
            try:
                # 创建爬虫实例
                crawler = GoogleImageCrawler(browser)
                
                # 将所有关键词合并成一个搜索字符串
                search_query = " ".join(keywords)
                logger.info(f"使用合并关键词搜索: {search_query}")
                
                # 爬取图片
                images = await crawler.crawl_images(
                    keyword=search_query,
                    max_images=max_images
                )
                
                if not images:
                    logger.warning(f"未找到图片: {search_query}")
                    self.redis_client.set(f"task_status:{task_id}", "completed")
                    return
                
                # 处理图片
                processed_images = await self.image_processor.process_image_batch(
                    urls=images,
                    keywords=keywords  # 传递所有关键词
                )
                
                # 上传图片到MinIO
                total_images = 0
                for image_id, image_data in processed_images.items():
                    if total_images >= max_images:
                        break
                        
                    # 上传图片
                    object_name = f"{task_id}/{image_id}.jpg"
                    self.storage.upload_image(
                        image_data=image_data['data'],
                        object_name=object_name,
                        metadata={
                            'keywords': ','.join(keywords),  # 保存所有关键词
                            'source_url': image_data['url'],
                            'detected_objects': ','.join(image_data.get('detected_objects', [])),
                            'tags': ','.join(image_data.get('tags', [])),
                            'description': image_data.get('description', '')
                        }
                    )
                    
                    # 索引图片
                    self.similar_searcher.index_image(
                        image_id=image_id,
                        metadata={
                            'url': image_data['url'],
                            'detected_objects': image_data.get('detected_objects', []),
                            'source_domain': image_data.get('source_domain', ''),
                            'tags': image_data.get('tags', []),
                            'description': image_data.get('description', ''),
                            'created_at': datetime.now().isoformat(),
                            'image_hash': image_id,
                            'keywords': keywords,  # 保存所有关键词
                            'task_id': task_id
                        }
                    )
                    
                    total_images += 1
                    
                    # 更新任务进度
                    progress = int((total_images / max_images) * 100)
                    self.redis_client.set(f"task_progress:{task_id}", str(progress))
                
                # 更新任务状态为完成
                self.redis_client.set(f"task_status:{task_id}", "completed")
                
            finally:
                # 释放浏览器实例
                await self.browser_pool.release_browser(browser)
                
        except Exception as e:
            logger.error(f"处理任务失败: {e}")
            # 更新任务状态为失败
            self.redis_client.set(f"task_status:{task_id}", "failed")
            raise
            
    async def run(self):
        """运行工作进程"""
        logger.info("启动图片爬虫工作进程...")
        
        # 初始化组件
        await self.initialize()
        
        while True:
            try:
                # 获取任务
                logger.debug("正在等待新任务...")
                task_data = await self.task_consumer.get_next_task()
                if task_data:
                    logger.info("收到新任务")
                    await self.process_task(task_data)
                else:
                    await asyncio.sleep(1)
                    
            except Exception as e:
                logger.error(f"工作进程发生错误: {e}")
                logger.exception(e)  # 打印完整的错误堆栈
                await asyncio.sleep(5)
                
async def main():
    """主函数"""
    logger.info("正在启动主程序...")
    worker = ImageCrawlerWorker()
    await worker.run()
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序发生错误: {e}")
        logger.exception(e)
        sys.exit(1) 