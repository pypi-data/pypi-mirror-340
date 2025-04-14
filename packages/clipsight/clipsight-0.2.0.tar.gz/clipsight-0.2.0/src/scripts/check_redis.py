import redis
from loguru import logger
import sys
import os
from dotenv import load_dotenv

def check_redis_connection():
    """检查Redis连接"""
    try:
        # 加载环境变量
        load_dotenv()
        
        # 从环境变量获取Redis配置
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        redis_db = int(os.getenv('REDIS_DB', 0))
        
        logger.info(f"尝试连接到Redis服务器: {redis_host}:{redis_port}")
        redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True,
            socket_timeout=5
        )
        
        # 测试连接
        if redis_client.ping():
            logger.info("Redis连接成功!")
            
            # 获取Redis信息
            info = redis_client.info()
            logger.info(f"Redis版本: {info.get('redis_version', 'unknown')}")
            logger.info(f"已连接客户端: {info.get('connected_clients', 'unknown')}")
            logger.info(f"已使用内存: {info.get('used_memory_human', 'unknown')}")
            
            return True
        else:
            logger.error("Redis连接失败: ping 命令未返回预期结果")
            return False
            
    except redis.ConnectionError as e:
        logger.error(f"Redis连接错误: {e}")
        logger.info("请确保Redis服务器已启动并正在运行")
        logger.info("在Windows上，您可以使用以下命令启动Redis:")
        logger.info("1. 安装Redis: https://github.com/microsoftarchive/redis/releases")
        logger.info("2. 启动Redis服务: redis-server")
        return False
    except Exception as e:
        logger.error(f"检查Redis连接时发生错误: {e}")
        return False

if __name__ == "__main__":
    if not check_redis_connection():
        sys.exit(1) 