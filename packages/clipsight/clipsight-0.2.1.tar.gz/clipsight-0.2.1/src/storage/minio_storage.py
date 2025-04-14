from minio import Minio
from loguru import logger
from typing import List, Any, Dict
import os
import io
from datetime import timedelta

class MinioStorage:
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket_name: str = "images",
        secure: bool = False
    ):
        """初始化MinIO存储客户端
        
        Args:
            endpoint: MinIO服务器地址
            access_key: 访问密钥
            secret_key: 密钥
            bucket_name: 存储桶名称
            secure: 是否使用HTTPS
        """
        try:
            self.client = Minio(
                endpoint=endpoint,
                access_key=access_key,
                secret_key=secret_key,
                secure=secure
            )
            self.bucket_name = bucket_name
            
            # 确保存储桶存在
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                logger.info(f"创建存储桶: {bucket_name}")
                
        except Exception as e:
            logger.error(f"初始化MinIO客户端失败: {e}")
            raise

    def list_images(self, prefix: str = "") -> List[Any]:
        """获取图片列表"""
        try:
            objects = self.client.list_objects(
                bucket_name=self.bucket_name,
                prefix=prefix,
                recursive=True
            )
            return list(objects)
        except Exception as e:
            logger.error(f"获取图片列表失败: {e}")
            return []
            
    def get_image_metadata(self, object_name: str) -> dict:
        """获取图片元数据"""
        try:
            # 获取对象信息
            stat = self.client.stat_object(
                bucket_name=self.bucket_name,
                object_name=object_name
            )
            
            # 解析元数据
            metadata = {}
            for key, value in stat.metadata.items():
                # MinIO的元数据键名通常以'x-amz-meta-'开头
                if key.startswith('x-amz-meta-'):
                    metadata[key[11:]] = value
                else:
                    metadata[key] = value
                    
            return metadata
        except Exception as e:
            logger.error(f"获取图片元数据失败: {e}")
            return {}
            
    def get_image_url(self, object_name: str, expires: int = 7 * 24 * 3600) -> str:
        """获取图片URL
        
        Args:
            object_name: 对象名称
            expires: 过期时间（秒）
            
        Returns:
            str: 预签名URL
        """
        try:
            # 将秒数转换为timedelta对象
            expiry = timedelta(seconds=expires)
            
            url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                expires=expiry
            )
            return url
        except Exception as e:
            logger.error(f"获取图片URL失败: {e}")
            return ""
            
    def upload_image(
        self,
        image_data: bytes,
        object_name: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """上传图片到MinIO"""
        try:
            # 将bytes对象转换为可读的文件对象
            image_stream = io.BytesIO(image_data)
            
            # 上传图片
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=image_stream,
                length=len(image_data),
                metadata=metadata
            )
            
            logger.info(f"图片上传成功: {object_name}")
            return True
            
        except Exception as e:
            logger.error(f"上传图片失败: {e}")
            return False 