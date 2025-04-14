#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据重置脚本
用于选择性删除历史数据，包括ES索引、MinIO图片和Redis任务数据
"""

import os
import sys
import argparse
import json
from pathlib import Path
import redis
from elasticsearch import Elasticsearch
from minio import Minio
from loguru import logger
import time
from dotenv import load_dotenv, set_key

# 加载环境变量
load_dotenv()

# 配置日志
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/reset_data_{time}.log", rotation="10 MB")

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# 环境变量默认值
DEFAULT_ENV_VARS = {
    'ES_HOST': 'localhost',
    'ES_PORT': '9200',
    'ES_INDEX': 'images',
    'MINIO_ENDPOINT': 'localhost:9000',
    'MINIO_ACCESS_KEY': 'minioadmin',
    'MINIO_SECRET_KEY': 'minioadmin',
    'MINIO_BUCKET': 'images',
    'REDIS_HOST': 'localhost',
    'REDIS_PORT': '6379',
    'REDIS_DB': '0'
}

def clean_env_value(value):
    """清理环境变量值，移除首尾空格、引号和其他非法字符"""
    if not value:
        return value
        
    # 处理注释
    if '#' in value:
        value = value.split('#')[0]
    
    # 移除首尾空格
    value = value.strip()
    
    # 移除首尾引号
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    
    # 再次移除空格
    value = value.strip()
    
    # 处理特殊情况
    if ':' in value:  # 处理带端口的地址
        host, port = value.split(':', 1)
        return f"{host.strip()}:{port.strip()}"
    
    # 移除URL中的非法字符
    return ''.join(c for c in value if c.isprintable() and c not in '#?{}[]<>').strip()

def check_and_fix_env():
    """检查并修复环境变量"""
    env_file = project_root / '.env'
    env_exists = env_file.exists()
    
    if env_exists:
        # 读取现有的.env文件，使用UTF-8编码
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                existing_vars = {}
                needs_update = False
                lines = f.readlines()
                updated_lines = []
                
                for line in lines:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        key = key.strip()
                        original_value = value
                        
                        # 保存注释
                        comment = ''
                        if '#' in value:
                            value, comment = value.split('#', 1)
                            comment = f"  # {comment.strip()}"
                        
                        value = clean_env_value(value)
                        existing_vars[key] = value
                        
                        # 检查是否需要更新文件
                        if original_value.split('#')[0].strip() != value:
                            needs_update = True
                            print(f"清理环境变量 {key}: '{original_value.split('#')[0].strip()}' -> '{value}'")
                        
                        # 更新行，保留注释
                        updated_lines.append(f"{key}={value}{comment}\n")
                    else:
                        updated_lines.append(line)
                
                # 如果需要更新文件，重写.env文件
                if needs_update:
                    print("\n正在更新.env文件...")
                    with open(env_file, 'w', encoding='utf-8') as f:
                        f.writelines(updated_lines)
                    print("环境变量文件更新完成")
                
        except UnicodeDecodeError:
            # 如果UTF-8解码失败，尝试使用系统默认编码
            with open(env_file, 'r') as f:
                existing_vars = {}
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        key = key.strip()
                        value = clean_env_value(value)
                        existing_vars[key] = value
    else:
        existing_vars = {}
    
    # 检查并修复缺失的变量
    missing_vars = []
    for var, default in DEFAULT_ENV_VARS.items():
        if var not in existing_vars:
            missing_vars.append(f"{var}={default}")
    
    if missing_vars:
        print(f"发现 {len(missing_vars)} 个缺失的环境变量:")
        for var in missing_vars:
            print(f"  - {var}")
        
        # 添加缺失的变量到.env文件，使用UTF-8编码
        with open(env_file, 'a' if env_exists else 'w', encoding='utf-8') as f:
            if not env_exists:
                f.write("# 自动生成的环境变量文件\n\n")
            for var in missing_vars:
                f.write(f"{var}\n")
        
        print(f"\n已添加缺失的环境变量到 {env_file}")
    else:
        print("所有必需的环境变量都已存在")
    
    # 验证连接
    print("\n验证服务连接:")
    
    # 验证ES连接
    try:
        es_host = clean_env_value(os.getenv('ES_HOST', DEFAULT_ENV_VARS['ES_HOST']))
        es_port = clean_env_value(os.getenv('ES_PORT', DEFAULT_ENV_VARS['ES_PORT']))
        es = Elasticsearch([f"http://{es_host}:{es_port}"])
        if es.ping():
            print("✓ Elasticsearch连接成功")
        else:
            print("✗ Elasticsearch连接失败")
    except Exception as e:
        print(f"✗ Elasticsearch连接错误: {e}")
    
    # 验证MinIO连接
    try:
        minio_endpoint = clean_env_value(os.getenv('MINIO_ENDPOINT', DEFAULT_ENV_VARS['MINIO_ENDPOINT']))
        minio_access_key = clean_env_value(os.getenv('MINIO_ACCESS_KEY', DEFAULT_ENV_VARS['MINIO_ACCESS_KEY']))
        minio_secret_key = clean_env_value(os.getenv('MINIO_SECRET_KEY', DEFAULT_ENV_VARS['MINIO_SECRET_KEY']))
        minio_bucket = clean_env_value(os.getenv('MINIO_BUCKET', DEFAULT_ENV_VARS['MINIO_BUCKET']))
        
        print(f"MinIO连接参数:")
        print(f"  - Endpoint: {minio_endpoint}")
        print(f"  - Access Key: {minio_access_key}")
        print(f"  - Bucket: {minio_bucket}")
        
        minio_client = Minio(
            minio_endpoint,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=False
        )
        if minio_client.bucket_exists(minio_bucket):
            print("✓ MinIO连接成功")
        else:
            print("✗ MinIO连接失败: bucket不存在")
    except Exception as e:
        print(f"✗ MinIO连接错误: {e}")
    
    # 验证Redis连接
    try:
        redis_host = clean_env_value(os.getenv('REDIS_HOST', DEFAULT_ENV_VARS['REDIS_HOST']))
        redis_port = int(clean_env_value(os.getenv('REDIS_PORT', DEFAULT_ENV_VARS['REDIS_PORT'])))
        redis_db = int(clean_env_value(os.getenv('REDIS_DB', DEFAULT_ENV_VARS['REDIS_DB'])))
        
        redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db
        )
        if redis_client.ping():
            print("✓ Redis连接成功")
        else:
            print("✗ Redis连接失败")
    except Exception as e:
        print(f"✗ Redis连接错误: {e}")

def delete_es_indices():
    """删除ES索引"""
    es_host = clean_env_value(os.getenv('ES_HOST', DEFAULT_ENV_VARS['ES_HOST']))
    es_port = clean_env_value(os.getenv('ES_PORT', DEFAULT_ENV_VARS['ES_PORT']))
    es_index = clean_env_value(os.getenv('ES_INDEX', DEFAULT_ENV_VARS['ES_INDEX']))
    
    es = Elasticsearch([f"http://{es_host}:{es_port}"])
    if es.indices.exists(index=es_index):
        es.indices.delete(index=es_index)
        print(f"已删除ES索引: {es_index}")
    else:
        print(f"ES索引不存在: {es_index}")

def delete_minio_images(prefix=None):
    """删除MinIO图片"""
    minio_endpoint = clean_env_value(os.getenv('MINIO_ENDPOINT', DEFAULT_ENV_VARS['MINIO_ENDPOINT']))
    minio_access_key = clean_env_value(os.getenv('MINIO_ACCESS_KEY', DEFAULT_ENV_VARS['MINIO_ACCESS_KEY']))
    minio_secret_key = clean_env_value(os.getenv('MINIO_SECRET_KEY', DEFAULT_ENV_VARS['MINIO_SECRET_KEY']))
    minio_bucket = clean_env_value(os.getenv('MINIO_BUCKET', DEFAULT_ENV_VARS['MINIO_BUCKET']))
    
    minio_client = Minio(
        minio_endpoint,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False
    )
    
    if not minio_client.bucket_exists(minio_bucket):
        print(f"MinIO bucket不存在: {minio_bucket}")
        return
    
    objects = minio_client.list_objects(minio_bucket, prefix=prefix)
    count = 0
    for obj in objects:
        minio_client.remove_object(minio_bucket, obj.object_name)
        count += 1
    
    if prefix:
        print(f"已删除 {count} 个以 '{prefix}' 开头的图片")
    else:
        print(f"已删除 {count} 个图片")

def delete_redis_tasks():
    """删除Redis任务数据"""
    redis_host = clean_env_value(os.getenv('REDIS_HOST', DEFAULT_ENV_VARS['REDIS_HOST']))
    redis_port = int(clean_env_value(os.getenv('REDIS_PORT', DEFAULT_ENV_VARS['REDIS_PORT'])))
    redis_db = int(clean_env_value(os.getenv('REDIS_DB', DEFAULT_ENV_VARS['REDIS_DB'])))
    
    redis_client = redis.Redis(
        host=redis_host,
        port=redis_port,
        db=redis_db
    )
    
    # 删除所有任务相关的键
    keys = redis_client.keys("task:*")
    if keys:
        redis_client.delete(*keys)
        print(f"已删除 {len(keys)} 个任务数据")
    else:
        print("没有找到任务数据")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="数据重置脚本")
    parser.add_argument("--es", action="store_true", help="删除ES索引")
    parser.add_argument("--minio", action="store_true", help="删除MinIO图片")
    parser.add_argument("--redis", action="store_true", help="删除Redis任务数据")
    parser.add_argument("--all", action="store_true", help="删除所有数据")
    parser.add_argument("--prefix", type=str, help="MinIO对象前缀，例如任务ID")
    parser.add_argument("--fix-env", action="store_true", help="检查并修复环境变量")
    
    args = parser.parse_args()
    
    # 如果指定了修复环境变量，则只执行修复
    if args.fix_env:
        check_and_fix_env()
        return
    
    # 如果没有指定任何选项，显示帮助信息
    if not (args.es or args.minio or args.redis or args.all):
        parser.print_help()
        return
    
    # 确认操作
    if args.all:
        confirm = input("确定要删除所有数据吗？此操作不可恢复！(y/n): ")
        if confirm.lower() != 'y':
            logger.info("操作已取消")
            return
    else:
        actions = []
        if args.es:
            actions.append("ES索引")
        if args.minio:
            actions.append("MinIO图片")
        if args.redis:
            actions.append("Redis任务数据")
        
        confirm = input(f"确定要删除以下数据吗？此操作不可恢复！\n{', '.join(actions)}\n(y/n): ")
        if confirm.lower() != 'y':
            logger.info("操作已取消")
            return
    
    # 执行删除操作
    if args.all or args.es:
        delete_es_indices()
    
    if args.all or args.minio:
        delete_minio_images(prefix=args.prefix)
    
    if args.all or args.redis:
        delete_redis_tasks()
    
    logger.info("数据重置完成")

if __name__ == "__main__":
    main() 