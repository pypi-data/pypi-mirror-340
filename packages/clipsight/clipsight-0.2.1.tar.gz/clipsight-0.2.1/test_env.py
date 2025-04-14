import asyncio
from loguru import logger
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def test_environment():
    """测试环境配置"""
    logger.info("开始测试环境配置...")
    
    # 测试环境变量
    required_vars = [
        'REDIS_HOST',
        'REDIS_PORT',
        'ES_HOST',
        'ES_PORT',
        'MINIO_ENDPOINT',
        'MINIO_ACCESS_KEY',
        'MINIO_SECRET_KEY'
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        logger.info(f"{var}: {value}")
        
    # 测试导入
    try:
        from src.browser.pool import PlaywrightPool
        from src.worker.consumer import TaskConsumer
        from src.pipeline.image_processor import ImageProcessor
        from src.search.similar_images import SimilarImageSearcher
        from src.storage.minio_client import MinioStorage
        from src.crawler.google_images import GoogleImageCrawler
        logger.info("所有模块导入成功")
    except Exception as e:
        logger.error(f"模块导入失败: {e}")
        
    logger.info("环境测试完成")

if __name__ == "__main__":
    asyncio.run(test_environment()) 