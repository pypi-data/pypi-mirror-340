import asyncio
import os
import argparse
from loguru import logger
from dotenv import load_dotenv
from src.storage.minio_client import MinioStorage
from src.search.similar_images import SimilarImageSearcher

async def download_by_task_id(task_id: str, output_dir: str):
    """通过任务ID下载图片"""
    storage = MinioStorage()
    searcher = SimilarImageSearcher()
    
    # 获取任务相关的所有图片
    images = storage.list_task_images(task_id)
    if not images:
        logger.warning(f"未找到任务 {task_id} 的图片")
        return
        
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 下载图片
    for image in images:
        try:
            image_data = storage.download_image(image['object_name'])
            if image_data:
                # 使用图片哈希作为文件名
                filename = f"{image['metadata'].get('hash', 'unknown')}.jpg"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                logger.info(f"已下载图片: {filepath}")
                
        except Exception as e:
            logger.error(f"下载图片失败: {e}")
            
async def download_by_keywords(keywords: list, output_dir: str, max_images: int = 20):
    """通过关键词下载图片"""
    searcher = SimilarImageSearcher()
    storage = MinioStorage()
    
    # 搜索图片
    results = searcher.search_similar_images(keywords, size=max_images)
    if not results:
        logger.warning(f"未找到关键词 {keywords} 相关的图片")
        return
        
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 下载图片
    for result in results:
        try:
            image_id = result['id']
            image_data = storage.download_image(f"raw/{image_id}.jpg")
            if image_data:
                filename = f"{image_id}.jpg"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                logger.info(f"已下载图片: {filepath}")
                
        except Exception as e:
            logger.error(f"下载图片失败: {e}")
            
def main():
    parser = argparse.ArgumentParser(description='下载图片工具')
    parser.add_argument('--task-id', help='任务ID')
    parser.add_argument('--keywords', nargs='+', help='关键词列表')
    parser.add_argument('--output-dir', default='downloads', help='输出目录')
    parser.add_argument('--max-images', type=int, default=20, help='最大图片数量')
    
    args = parser.parse_args()
    
    if not args.task_id and not args.keywords:
        parser.error('必须提供任务ID或关键词')
        
    if args.task_id:
        asyncio.run(download_by_task_id(args.task_id, args.output_dir))
    else:
        asyncio.run(download_by_keywords(args.keywords, args.output_dir, args.max_images))
        
if __name__ == '__main__':
    load_dotenv()
    main() 