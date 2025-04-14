from minio import Minio
from typing import Optional, Dict, Any, List
import io
from loguru import logger
from uuid import uuid4
import os
from datetime import datetime
import json

class MinioStorage:
    def __init__(
        self,
        endpoint: str = "localhost:9000",
        access_key: str = "minioadmin",
        secret_key: str = "minioadmin",
        secure: bool = False,
        bucket_name: str = "images"
    ):
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        self.bucket_name = bucket_name
        self._ensure_bucket()
        
    def _ensure_bucket(self):
        """确保存储桶存在"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"创建存储桶: {self.bucket_name}")
        except Exception as e:
            logger.error(f"创建存储桶时发生错误: {e}")
            
    def _generate_object_name(
        self,
        task_id: str,
        image_hash: str,
        suffix: str = "raw"
    ) -> str:
        """生成对象存储路径"""
        return f"{task_id}/{suffix}/{image_hash}.jpg"
        
    async def upload_image(
        self,
        image_data: bytes,
        metadata: Dict[str, Any],
        task_id: Optional[str] = None
    ) -> bool:
        """上传图片到MinIO"""
        try:
            # 如果没有提供task_id，生成一个
            if not task_id:
                task_id = str(uuid4())
                
            # 生成存储路径
            object_name = self._generate_object_name(
                task_id,
                metadata.get('hash', str(uuid4()))
            )
            
            # 准备元数据
            minio_metadata = {
                'url': metadata.get('url', ''),
                'source_domain': metadata.get('source_domain', ''),
                'created_at': metadata.get('created_at', datetime.now().isoformat()),
                'size': str(metadata.get('size', len(image_data))),
                'hash': metadata.get('hash', ''),
                'task_id': task_id
            }
            
            # 添加关键词到元数据
            keywords = metadata.get('keywords', [])
            if keywords:
                # 将关键词列表转换为JSON字符串
                minio_metadata['keywords'] = json.dumps(keywords)
                # 同时添加每个关键词作为单独的元数据字段
                for i, keyword in enumerate(keywords):
                    minio_metadata[f'keyword_{i}'] = keyword
            
            # 上传图片
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=io.BytesIO(image_data),
                length=len(image_data),
                metadata=minio_metadata
            )
            
            logger.info(f"图片上传成功: {object_name}")
            return True
            
        except Exception as e:
            logger.error(f"上传图片时发生错误: {e}")
            return False
            
    def get_image_metadata(
        self,
        object_name: str
    ) -> Optional[Dict[str, Any]]:
        """获取图片元数据"""
        try:
            stat = self.client.stat_object(self.bucket_name, object_name)
            return dict(stat.metadata)
        except Exception as e:
            logger.error(f"获取图片元数据时发生错误: {e}")
            return None
            
    def download_image(
        self,
        object_name: str
    ) -> Optional[bytes]:
        """下载图片"""
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            return response.read()
        except Exception as e:
            logger.error(f"下载图片时发生错误: {e}")
            return None
            
    def list_task_images(
        self,
        task_id: str,
        prefix: str = "raw"
    ) -> List[Dict[str, Any]]:
        """列出任务相关的所有图片"""
        try:
            objects = self.client.list_objects(
                self.bucket_name,
                prefix=f"{task_id}/{prefix}/"
            )
            
            results = []
            for obj in objects:
                metadata = self.get_image_metadata(obj.object_name)
                if metadata:
                    results.append({
                        'object_name': obj.object_name,
                        'size': obj.size,
                        'last_modified': obj.last_modified,
                        'metadata': metadata
                    })
                    
            return results
            
        except Exception as e:
            logger.error(f"列出任务图片时发生错误: {e}")
            return []
            
    def delete_image(self, object_name: str) -> bool:
        """删除图片"""
        try:
            self.client.remove_object(self.bucket_name, object_name)
            logger.info(f"成功删除图片: {object_name}")
            return True
        except Exception as e:
            logger.error(f"删除图片时发生错误: {e}")
            return False 