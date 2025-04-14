import os
import asyncio
from dotenv import load_dotenv
from loguru import logger
from src.storage.minio_client import MinioStorage

async def main():
    # 加载环境变量
    load_dotenv()
    
    # 初始化存储客户端
    storage = MinioStorage(
        endpoint=os.getenv('MINIO_ENDPOINT', 'localhost:9000'),
        access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
        secret_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin')
    )
    
    # 获取任务ID
    task_id = input("请输入任务ID: ")
    
    # 获取任务相关的所有图片
    images = storage.list_task_images(task_id)
    
    if not images:
        logger.info(f"未找到任务 {task_id} 相关的图片")
        return
        
    # 打印图片信息
    logger.info(f"找到 {len(images)} 张图片:")
    for i, image in enumerate(images, 1):
        logger.info(f"\n图片 {i}:")
        logger.info(f"对象名称: {image['object_name']}")
        logger.info(f"大小: {image['size']} 字节")
        logger.info(f"最后修改时间: {image['last_modified']}")
        logger.info("元数据:")
        for key, value in image['metadata'].items():
            logger.info(f"  {key}: {value}")
            
if __name__ == "__main__":
    asyncio.run(main()) 