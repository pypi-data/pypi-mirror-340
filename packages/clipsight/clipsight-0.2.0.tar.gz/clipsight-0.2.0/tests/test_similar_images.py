import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.search.similar_images import SimilarImageSearcher

@pytest.fixture
def similar_searcher():
    """创建SimilarImageSearcher实例的fixture"""
    with patch('src.search.similar_images.Elasticsearch') as mock_es:
        # 配置mock
        mock_client = MagicMock()
        mock_es.return_value = mock_client
        
        # 创建SimilarImageSearcher实例
        searcher = SimilarImageSearcher(
            es_host="localhost",
            es_port=9200,
            index_name="test_index",
            min_score=0.3
        )
        
        yield searcher, mock_client

def test_index_image_success(similar_searcher):
    """测试成功索引图片"""
    searcher, mock_client = similar_searcher
    
    # 准备测试数据
    image_id = "test_image_id"
    metadata = {
        "url": "https://example.com/image.jpg",
        "detected_objects": ["person", "car"],
        "source_domain": "example.com",
        "tags": ["test", "image"],
        "description": "A test image",
        "keywords": ["test"]
    }
    
    # 调用索引方法
    result = searcher.index_image(image_id=image_id, metadata=metadata)
    
    # 验证结果
    assert result is True
    mock_client.index.assert_called_once()
    
    # 验证调用参数
    call_args = mock_client.index.call_args[1]
    assert call_args["index"] == "test_index"
    assert call_args["id"] == image_id
    
    # 验证文档内容
    document = call_args["body"]
    assert document["url"] == metadata["url"]
    assert document["detected_objects"] == metadata["detected_objects"]
    assert document["source_domain"] == metadata["source_domain"]
    assert document["tags"] == metadata["tags"]
    assert document["description"] == metadata["description"]
    assert document["keywords"] == metadata["keywords"]
    assert "created_at" in document

def test_index_image_failure(similar_searcher):
    """测试索引图片失败的情况"""
    searcher, mock_client = similar_searcher
    
    # 配置mock抛出异常
    mock_client.index.side_effect = Exception("Index failed")
    
    # 准备测试数据
    image_id = "test_image_id"
    metadata = {"url": "https://example.com/image.jpg"}
    
    # 调用索引方法
    result = searcher.index_image(image_id=image_id, metadata=metadata)
    
    # 验证结果
    assert result is False

def test_search_similar_images(similar_searcher):
    """测试搜索相似图片"""
    searcher, mock_client = similar_searcher
    
    # 准备测试数据
    keywords = ["test", "image"]
    filters = {"source_domain": "example.com"}
    size = 5
    
    # 配置mock返回值
    mock_response = {
        "hits": {
            "hits": [
                {
                    "_id": "image1",
                    "_score": 0.8,
                    "_source": {
                        "url": "https://example.com/image1.jpg",
                        "keywords": ["test"],
                        "metadata": {"size": 1024}
                    }
                },
                {
                    "_id": "image2",
                    "_score": 0.5,
                    "_source": {
                        "url": "https://example.com/image2.jpg",
                        "keywords": ["image"],
                        "metadata": {"size": 2048}
                    }
                }
            ]
        }
    }
    mock_client.search.return_value = mock_response
    
    # 调用搜索方法
    result = searcher.search_similar_images(
        keywords=keywords,
        filters=filters,
        size=size
    )
    
    # 验证结果
    assert len(result) == 2
    assert result[0]["id"] == "image1"
    assert result[0]["score"] == 0.8
    assert result[0]["url"] == "https://example.com/image1.jpg"
    assert result[1]["id"] == "image2"
    assert result[1]["score"] == 0.5
    assert result[1]["url"] == "https://example.com/image2.jpg"
    
    # 验证调用参数
    mock_client.search.assert_called_once()
    call_args = mock_client.search.call_args[1]
    assert call_args["index"] == "test_index"
    assert call_args["size"] == size
    
    # 验证查询结构
    query = call_args["body"]
    assert "query" in query
    assert "bool" in query["query"]
    assert "should" in query["query"]["bool"]
    assert "terms" in query["query"]["bool"]["should"][0]
    assert query["query"]["bool"]["should"][0]["terms"]["keywords"] == keywords
    assert "filter" in query["query"]["bool"]
    assert query["query"]["bool"]["filter"][0]["term"]["source_domain"] == "example.com"

def test_search_similar_images_no_results(similar_searcher):
    """测试搜索相似图片没有结果的情况"""
    searcher, mock_client = similar_searcher
    
    # 配置mock返回空结果
    mock_response = {"hits": {"hits": []}}
    mock_client.search.return_value = mock_response
    
    # 调用搜索方法
    result = searcher.search_similar_images(keywords=["test"])
    
    # 验证结果
    assert result == []

def test_search_similar_images_error(similar_searcher):
    """测试搜索相似图片出错的情况"""
    searcher, mock_client = similar_searcher
    
    # 配置mock抛出异常
    mock_client.search.side_effect = Exception("Search failed")
    
    # 调用搜索方法
    result = searcher.search_similar_images(keywords=["test"])
    
    # 验证结果
    assert result == []

def test_get_image_data(similar_searcher):
    """测试获取图片数据"""
    searcher, mock_client = similar_searcher
    
    # 准备测试数据
    image_id = "test_image_id"
    expected_data = {
        "url": "https://example.com/image.jpg",
        "keywords": ["test"]
    }
    
    # 配置mock返回值
    mock_response = {"found": True, "_source": expected_data}
    mock_client.get.return_value = mock_response
    
    # 调用方法
    result = searcher.get_image_data(image_id)
    
    # 验证结果
    assert result == expected_data
    mock_client.get.assert_called_once_with(
        index="test_index",
        id=image_id
    )

def test_get_image_data_not_found(similar_searcher):
    """测试获取不存在的图片数据"""
    searcher, mock_client = similar_searcher
    
    # 配置mock返回值
    mock_response = {"found": False}
    mock_client.get.return_value = mock_response
    
    # 调用方法
    result = searcher.get_image_data("non_existent_id")
    
    # 验证结果
    assert result == {}

def test_get_image_data_error(similar_searcher):
    """测试获取图片数据出错的情况"""
    searcher, mock_client = similar_searcher
    
    # 配置mock抛出异常
    mock_client.get.side_effect = Exception("Get failed")
    
    # 调用方法
    result = searcher.get_image_data("test_id")
    
    # 验证结果
    assert result == {} 