import os
import pytest
import io
from unittest.mock import MagicMock, patch
from src.storage.minio_storage import MinioStorage

@pytest.fixture
def minio_storage():
    """创建MinioStorage实例的fixture"""
    with patch('src.storage.minio_storage.Minio') as mock_minio:
        # 配置mock
        mock_client = MagicMock()
        mock_minio.return_value = mock_client
        
        # 创建MinioStorage实例
        storage = MinioStorage(
            endpoint="localhost:9000",
            access_key="test_access_key",
            secret_key="test_secret_key",
            bucket_name="test_bucket"
        )
        
        # 确保bucket存在
        mock_client.bucket_exists.return_value = True
        
        yield storage, mock_client

def test_upload_image_success(minio_storage):
    """测试成功上传图片"""
    storage, mock_client = minio_storage
    
    # 准备测试数据
    image_data = b"fake_image_data"
    object_name = "test/image.jpg"
    metadata = {
        "keywords": "test",
        "source_url": "https://example.com/image.jpg"
    }
    
    # 调用上传方法
    result = storage.upload_image(
        image_data=image_data,
        object_name=object_name,
        metadata=metadata
    )
    
    # 验证结果
    assert result is True
    mock_client.put_object.assert_called_once()
    
    # 验证调用参数
    call_args = mock_client.put_object.call_args[1]
    assert call_args["bucket_name"] == "test_bucket"
    assert call_args["object_name"] == object_name
    assert call_args["length"] == len(image_data)
    assert call_args["metadata"] == metadata
    assert isinstance(call_args["data"], io.BytesIO)

def test_upload_image_failure(minio_storage):
    """测试上传图片失败的情况"""
    storage, mock_client = minio_storage
    
    # 配置mock抛出异常
    mock_client.put_object.side_effect = Exception("Upload failed")
    
    # 准备测试数据
    image_data = b"fake_image_data"
    object_name = "test/image.jpg"
    metadata = {"keywords": "test"}
    
    # 调用上传方法
    result = storage.upload_image(
        image_data=image_data,
        object_name=object_name,
        metadata=metadata
    )
    
    # 验证结果
    assert result is False

def test_get_image_metadata(minio_storage):
    """测试获取图片元数据"""
    storage, mock_client = minio_storage
    
    # 准备测试数据
    object_name = "test/image.jpg"
    expected_metadata = {
        "keywords": "test",
        "source_url": "https://example.com/image.jpg"
    }
    
    # 配置mock返回值
    mock_stat = MagicMock()
    mock_stat.metadata = expected_metadata
    mock_client.stat_object.return_value = mock_stat
    
    # 调用方法
    result = storage.get_image_metadata(object_name)
    
    # 验证结果
    assert result == expected_metadata
    mock_client.stat_object.assert_called_once_with("test_bucket", object_name)

def test_get_image_metadata_not_found(minio_storage):
    """测试获取不存在的图片元数据"""
    storage, mock_client = minio_storage
    
    # 配置mock抛出异常
    mock_client.stat_object.side_effect = Exception("Not found")
    
    # 调用方法
    result = storage.get_image_metadata("non_existent.jpg")
    
    # 验证结果
    assert result is None

def test_get_image_url(minio_storage):
    """测试获取图片URL"""
    storage, mock_client = minio_storage
    
    # 准备测试数据
    object_name = "test/image.jpg"
    expected_url = "https://localhost:9000/test_bucket/test/image.jpg"
    
    # 配置mock返回值
    mock_client.presigned_get_object.return_value = expected_url
    
    # 调用方法
    result = storage.get_image_url(object_name)
    
    # 验证结果
    assert result == expected_url
    mock_client.presigned_get_object.assert_called_once_with(
        "test_bucket", 
        object_name,
        expires=7*24*60*60  # 7天
    )

def test_list_images(minio_storage):
    """测试列出图片"""
    storage, mock_client = minio_storage
    
    # 准备测试数据
    prefix = "test/"
    mock_objects = [
        MagicMock(object_name="test/image1.jpg", size=1024),
        MagicMock(object_name="test/image2.jpg", size=2048)
    ]
    
    # 配置mock返回值
    mock_client.list_objects.return_value = mock_objects
    
    # 调用方法
    result = storage.list_images(prefix=prefix)
    
    # 验证结果
    assert len(result) == 2
    assert result[0].object_name == "test/image1.jpg"
    assert result[1].object_name == "test/image2.jpg"
    mock_client.list_objects.assert_called_once_with("test_bucket", prefix=prefix) 