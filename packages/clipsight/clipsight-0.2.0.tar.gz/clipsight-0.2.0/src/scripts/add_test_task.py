import redis
import json
from loguru import logger
import sys
import os
from dotenv import load_dotenv
import argparse
from uuid import uuid4

def add_test_task(keywords=None, max_images=20, priority=False, task_id=None):
    """添加测试任务到Redis队列"""
    try:
        # 加载环境变量
        load_dotenv()
        
        # 从环境变量获取Redis配置
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        redis_db = int(os.getenv('REDIS_DB', 0))
        task_queue = os.getenv('TASK_QUEUE', 'image_tasks')
        
        # 连接Redis
        redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True
        )
        
        # 如果没有提供关键词，使用默认值
        if not keywords:
            keywords = ["cat", "dog"]
            
        # 如果没有提供任务ID，生成一个
        if not task_id:
            task_id = f"task_{uuid4().hex[:8]}"
        
        # 创建测试任务
        test_task = {
            "task_id": task_id,
            "keywords": keywords,  # 关键词列表
            "max_images": max_images,  # 每个关键词爬取图片数量
            "proxy": None,  # 不使用代理
            "metadata": {
                "source": "test",
                "description": f"测试任务: {' '.join(keywords)}"
            }
        }
        
        # 选择队列
        queue_name = "priority_tasks" if priority else task_queue
        
        # 将任务添加到队列
        redis_client.rpush(queue_name, json.dumps(test_task))
        logger.info(f"成功添加测试任务到队列: {queue_name}")
        
        # 打印任务详情
        logger.info("任务详情:")
        logger.info(json.dumps(test_task, indent=2, ensure_ascii=False))
        
        return task_id
        
    except Exception as e:
        logger.error(f"添加测试任务失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="添加图片爬取任务")
    parser.add_argument("--keywords", nargs="+", help="关键词列表，用空格分隔")
    parser.add_argument("--max-images", type=int, default=20, help="每个关键词爬取图片数量")
    parser.add_argument("--priority", action="store_true", help="是否添加到优先队列")
    parser.add_argument("--task-id", help="任务ID，不提供则自动生成")
    
    args = parser.parse_args()
    
    # 添加任务
    task_id = add_test_task(
        keywords=args.keywords,
        max_images=args.max_images,
        priority=args.priority,
        task_id=args.task_id
    )
    
    logger.info(f"任务ID: {task_id}") 