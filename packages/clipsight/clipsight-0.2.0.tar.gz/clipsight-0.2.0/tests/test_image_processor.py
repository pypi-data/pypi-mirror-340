import pytest
import io
from unittest.mock import MagicMock, patch
from PIL import Image
import numpy as np
from src.pipeline.image_processor import ImageProcessor

@pytest.fixture
def image_processor():
    """创建ImageProcessor实例的fixture"""
    return ImageProcessor(
        max_concurrent_downloads=2,
        timeout=5,
        min_image_size=100,
        max_image_size=1024*1024
    )

@pytest.fixture
def sample_image():
    """创建测试用图片数据的fixture"""
    # 创建一个简单的测试图片
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

@pytest.mark.asyncio
async def test_download_image_success(image_processor, sample_image):
    """测试成功下载图片"""
    # 准备测试数据
    url = "https://example.com/image.jpg"
    
    # 模拟aiohttp.ClientSession
    with patch('aiohttp.ClientSession') as mock_session:
        # 配置mock
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read = MagicMock(return_value=sample_image)
        
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response
        
        # 调用下载方法
        result = await image_processor.download_image(url)
        
        # 验证结果
        assert result == sample_image

@pytest.mark.asyncio
async def test_download_image_failure(image_processor):
    """测试下载图片失败的情况"""
    # 准备测试数据
    url = "https://example.com/image.jpg"
    
    # 模拟aiohttp.ClientSession
    with patch('aiohttp.ClientSession') as mock_session:
        # 配置mock抛出异常
        mock_session.return_value.__aenter__.return_value.get.side_effect = Exception("Download failed")
        
        # 调用下载方法
        result = await image_processor.download_image(url)
        
        # 验证结果
        assert result is None

@pytest.mark.asyncio
async def test_download_image_wrong_status(image_processor):
    """测试下载图片返回错误状态码的情况"""
    # 准备测试数据
    url = "https://example.com/image.jpg"
    
    # 模拟aiohttp.ClientSession
    with patch('aiohttp.ClientSession') as mock_session:
        # 配置mock返回错误状态码
        mock_response = MagicMock()
        mock_response.status = 404
        
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response
        
        # 调用下载方法
        result = await image_processor.download_image(url)
        
        # 验证结果
        assert result is None

def test_validate_image_size(image_processor):
    """测试图片大小验证"""
    # 测试有效大小
    assert image_processor._validate_image_size(500) is True
    assert image_processor._validate_image_size(1024*1024) is True
    
    # 测试无效大小
    assert image_processor._validate_image_size(50) is False  # 太小
    assert image_processor._validate_image_size(2*1024*1024) is False  # 太大

def test_validate_image_content(image_processor, sample_image):
    """测试图片内容验证"""
    # 测试有效图片
    assert image_processor.validate_image_content(sample_image) is True
    
    # 测试无效图片
    assert image_processor.validate_image_content(b"invalid image data") is False

def test_generate_image_hash(image_processor, sample_image):
    """测试图片哈希生成"""
    # 生成哈希
    hash1 = image_processor.generate_image_hash(sample_image)
    
    # 验证哈希格式
    assert len(hash1) == 32  # MD5哈希长度为32个字符
    assert isinstance(hash1, str)
    
    # 验证相同图片生成相同哈希
    hash2 = image_processor.generate_image_hash(sample_image)
    assert hash1 == hash2
    
    # 验证不同图片生成不同哈希
    different_image = Image.new('RGB', (100, 100), color='blue')
    img_byte_arr = io.BytesIO()
    different_image.save(img_byte_arr, format='JPEG')
    different_image_bytes = img_byte_arr.getvalue()
    
    hash3 = image_processor.generate_image_hash(different_image_bytes)
    assert hash1 != hash3

@pytest.mark.asyncio
async def test_process_image_batch_success(image_processor, sample_image):
    """测试成功批量处理图片"""
    # 准备测试数据
    urls = ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
    keywords = ["test"]
    
    # 模拟download_image方法
    with patch.object(image_processor, 'download_image', return_value=sample_image):
        # 调用处理方法
        result = await image_processor.process_image_batch(urls=urls, keywords=keywords)
        
        # 验证结果
        assert len(result) == 2
        for image_hash, image_data in result.items():
            assert image_data['data'] == sample_image
            assert image_data['url'] in urls
            assert image_data['keywords'] == keywords
            assert 'source_domain' in image_data
            assert 'created_at' in image_data
            assert 'size' in image_data
            assert 'hash' in image_data

@pytest.mark.asyncio
async def test_process_image_batch_partial_failure(image_processor, sample_image):
    """测试部分图片处理失败的情况"""
    # 准备测试数据
    urls = ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
    keywords = ["test"]
    
    # 模拟download_image方法，第一个成功，第二个失败
    async def mock_download(url):
        if url == urls[0]:
            return sample_image
        return None
    
    with patch.object(image_processor, 'download_image', side_effect=mock_download):
        # 调用处理方法
        result = await image_processor.process_image_batch(urls=urls, keywords=keywords)
        
        # 验证结果
        assert len(result) == 1
        for image_hash, image_data in result.items():
            assert image_data['url'] == urls[0]
            assert image_data['data'] == sample_image 