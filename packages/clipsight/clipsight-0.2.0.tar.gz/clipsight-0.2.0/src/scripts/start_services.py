import subprocess
import os
import sys
import time
from loguru import logger
from dotenv import load_dotenv

"""
服务启动脚本

使用说明：
1. 开发环境：
   - 直接运行此脚本启动所有服务
   - 需要本地安装Docker
   - 服务将在本地运行

2. 生产环境：
   - 使用docker-compose启动所有服务
   - 命令：docker-compose up -d
   - 服务将在容器中运行

3. 分布式部署：
   - 修改.env文件中的服务地址
   - 确保网络连接正常
   - 服务可以部署在不同的机器上
"""

def start_minio():
    """启动MinIO服务"""
    try:
        # 检查MinIO是否已经运行
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=minio"],
            capture_output=True,
            text=True
        )
        
        if "minio" not in result.stdout:
            logger.info("正在启动MinIO服务...")
            subprocess.run([
                "docker", "run", "-d",
                "--name", "minio",
                "-p", "9000:9000",
                "-p", "9001:9001",
                "-e", "MINIO_ROOT_USER=minioadmin",
                "-e", "MINIO_ROOT_PASSWORD=minioadmin",
                "minio/minio", "server", "/data", "--console-address", ":9001"
            ])
            logger.info("MinIO服务已启动")
        else:
            logger.info("MinIO服务已在运行")
            
    except Exception as e:
        logger.error(f"启动MinIO服务时发生错误: {e}")
        sys.exit(1)

def start_redis():
    """启动Redis服务"""
    try:
        # 检查Redis是否已经运行
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=redis"],
            capture_output=True,
            text=True
        )
        
        if "redis" not in result.stdout:
            logger.info("正在启动Redis服务...")
            subprocess.run([
                "docker", "run", "-d",
                "--name", "redis",
                "-p", "6379:6379",
                "redis:latest"
            ])
            logger.info("Redis服务已启动")
        else:
            logger.info("Redis服务已在运行")
            
    except Exception as e:
        logger.error(f"启动Redis服务时发生错误: {e}")
        sys.exit(1)

def start_elasticsearch():
    """启动Elasticsearch服务"""
    try:
        # 检查Elasticsearch是否已经运行
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=elasticsearch"],
            capture_output=True,
            text=True
        )
        
        if "elasticsearch" not in result.stdout:
            logger.info("正在启动Elasticsearch服务...")
            subprocess.run([
                "docker", "run", "-d",
                "--name", "elasticsearch",
                "-p", "9200:9200",
                "-e", "discovery.type=single-node",
                "-e", "xpack.security.enabled=false",
                "elasticsearch:7.9.3"
            ])
            logger.info("Elasticsearch服务已启动")
        else:
            logger.info("Elasticsearch服务已在运行")
            
    except Exception as e:
        logger.error(f"启动Elasticsearch服务时发生错误: {e}")
        sys.exit(1)

def main():
    """启动所有服务"""
    # 加载环境变量
    load_dotenv()
    
    # 检查是否使用docker-compose
    if os.getenv('USE_DOCKER_COMPOSE', 'false').lower() == 'true':
        logger.info("使用docker-compose启动服务...")
        subprocess.run(["docker-compose", "up", "-d"])
        return
    
    # 启动服务
    # start_minio()
    # start_redis()
    # start_elasticsearch()
    
    # 等待服务启动
    logger.info("等待服务启动...")
    time.sleep(10)
    
    # 启动Web服务
    logger.info("正在启动Web服务...")
    subprocess.run([
        "uvicorn",
        "src.web.app:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])

if __name__ == "__main__":
    main() 