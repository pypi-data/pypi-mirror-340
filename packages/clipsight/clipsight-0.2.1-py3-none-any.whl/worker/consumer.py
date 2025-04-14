import asyncio
import json
from typing import Optional, Dict, Any
import redis
from loguru import logger
from datetime import datetime
import hashlib

class TaskConsumer:
    def __init__(
        self,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        task_queue: str = "image_tasks",
        priority_queue: str = "priority_tasks",
        dedup_key: str = "task_dedup"
    ):
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True
        )
        self.task_queue = task_queue
        self.priority_queue = priority_queue
        self.dedup_key = dedup_key
        self.task_status_prefix = "task_status:"
        
    def _generate_task_id(self, task_data: Dict[str, Any]) -> str:
        """生成任务唯一标识"""
        task_str = json.dumps(task_data, sort_keys=True)
        return hashlib.md5(task_str.encode()).hexdigest()
        
    def is_duplicate(self, task_id: str) -> bool:
        """检查任务是否重复"""
        return self.redis_client.sismember(self.dedup_key, task_id)
        
    def mark_task_processed(self, task_id: str):
        """标记任务已处理"""
        self.redis_client.sadd(self.dedup_key, task_id)
        
    async def get_next_task(self) -> Optional[Dict[str, Any]]:
        """获取下一个任务"""
        try:
            # 从队列中获取任务
            task_data = self.redis_client.rpop(self.task_queue)
            if task_data:
                task = json.loads(task_data)
                # 更新任务状态为处理中
                await self.update_task_status(task['task_id'], 'processing')
                return task
        except Exception as e:
            logger.error(f"获取任务时发生错误: {e}")
        return None
        
    async def update_task_status(
        self,
        task_id: str,
        status: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """更新任务状态"""
        try:
            status_key = f"{self.task_status_prefix}{task_id}"
            status_data = {
                'status': status,
                'updated_at': datetime.now().isoformat()
            }
            if metadata:
                status_data.update(metadata)
            self.redis_client.hmset(status_key, status_data)
            # 设置过期时间（24小时）
            self.redis_client.expire(status_key, 24 * 60 * 60)
        except Exception as e:
            logger.error(f"更新任务状态时发生错误: {e}")
            
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        try:
            status_key = f"{self.task_status_prefix}{task_id}"
            status_data = self.redis_client.hgetall(status_key)
            if status_data:
                return status_data
        except Exception as e:
            logger.error(f"获取任务状态时发生错误: {e}")
        return None
        
    async def process_task(self, task_data: Dict[str, Any]):
        """处理单个任务"""
        task_id = self._generate_task_id(task_data)
        
        if self.is_duplicate(task_id):
            logger.info(f"跳过重复任务: {task_id}")
            return
            
        try:
            # TODO: 实现具体的任务处理逻辑
            logger.info(f"处理任务: {task_id}")
            
            # 标记任务已处理
            self.mark_task_processed(task_id)
            
        except Exception as e:
            logger.error(f"任务处理失败: {task_id}, 错误: {e}")
            # 可以将失败的任务放入重试队列
            self.redis_client.rpush("failed_tasks", json.dumps({
                "task_id": task_id,
                "task_data": task_data,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }))
            
    async def start_consuming(self):
        """开始消费任务"""
        logger.info("开始消费任务...")
        while True:
            try:
                task_data = await self.get_next_task()
                if task_data:
                    await self.process_task(task_data)
                else:
                    # 没有任务时短暂休眠
                    await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"任务消费过程发生错误: {e}")
                await asyncio.sleep(5)  # 发生错误时较长休眠 