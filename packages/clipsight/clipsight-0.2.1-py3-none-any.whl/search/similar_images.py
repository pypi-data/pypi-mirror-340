from elasticsearch import Elasticsearch
from elasticsearch.connection import create_ssl_context
from elasticsearch.exceptions import ConnectionError, NotFoundError
from typing import List, Dict, Any
from loguru import logger
import json
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time

class SimilarImageSearcher:
    def __init__(
        self,
        es_host: str = "localhost",
        es_port: int = 9200,
        index_name: str = "images",
        min_score: float = 0.3,
        max_retries: int = 3,
        retry_delay: int = 5
    ):
        """初始化ES搜索客户端
        
        Args:
            es_host: ES服务器地址
            es_port: ES服务器端口
            index_name: 索引名称
            min_score: 最小相似度分数
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
        """
        self.es_client = Elasticsearch(
            f"http://{es_host}:{es_port}",
            verify_certs=False,
            timeout=30,
            max_retries=max_retries,
            retry_on_timeout=True
        )
        self.index_name = index_name
        self.min_score = min_score
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english'
        )
        
        # 确保索引存在
        self._ensure_index_exists()
        
    def _ensure_index_exists(self):
        """确保索引存在，如果不存在则创建"""
        try:
            if not self.es_client.indices.exists(index=self.index_name):
                # 创建索引
                self.es_client.indices.create(
                    index=self.index_name,
                    body={
                        "mappings": {
                            "properties": {
                                "url": {"type": "keyword"},
                                "detected_objects": {"type": "keyword"},
                                "source_domain": {"type": "keyword"},
                                "tags": {"type": "keyword"},
                                "description": {"type": "text"},
                                "created_at": {"type": "date"},
                                "image_hash": {"type": "keyword"},
                                "keywords": {"type": "keyword"},
                                "task_id": {"type": "keyword"}
                            }
                        }
                    }
                )
                logger.info(f"创建索引: {self.index_name}")
        except Exception as e:
            logger.error(f"创建索引失败: {e}")
            
    def _retry_operation(self, operation, *args, **kwargs):
        """重试操作
        
        Args:
            operation: 要重试的操作函数
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            操作结果
        """
        for attempt in range(self.max_retries):
            try:
                return operation(*args, **kwargs)
            except (ConnectionError, NotFoundError) as e:
                if attempt == self.max_retries - 1:
                    raise
                logger.warning(f"操作失败，{self.retry_delay}秒后重试: {e}")
                time.sleep(self.retry_delay)
                
    def _expand_keywords(self, keywords: List[str]) -> List[str]:
        """扩展关键词"""
        # TODO: 实现更复杂的关键词扩展逻辑
        expanded = []
        for keyword in keywords:
            expanded.extend([
                keyword,
                keyword.lower(),
                keyword.replace(' ', '_'),
                keyword.replace(' ', '-')
            ])
        return list(set(expanded))
        
    def _build_search_query(
        self,
        keywords: List[str],
        filters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """构建搜索查询"""
        expanded_keywords = self._expand_keywords(keywords)
        
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": " ".join(expanded_keywords),
                                "fields": [
                                    "detected_objects^2",
                                    "source_domain^1.5",
                                    "tags^1.2",
                                    "description"
                                ],
                                "type": "best_fields",
                                "tie_breaker": 0.3
                            }
                        }
                    ],
                    "filter": []
                }
            },
            "sort": [
                {"_score": {"order": "desc"}},
                {"created_at": {"order": "desc"}}
            ]
        }
        
        if filters:
            for field, value in filters.items():
                query["query"]["bool"]["filter"].append({
                    "term": {field: value}
                })
                
        return query
        
    def search_similar_images(
        self,
        keywords: List[str],
        filters: Dict[str, Any] = None,
        size: int = 10
    ) -> List[Dict[str, Any]]:
        """搜索相似图片"""
        try:
            def search_operation():
                # 构建查询
                query = {
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "multi_match": {
                                        "query": " ".join(keywords),
                                        "fields": ["keywords^3", "description^2", "tags^2", "detected_objects"],
                                        "type": "best_fields",
                                        "operator": "or",
                                        "minimum_should_match": "75%"
                                    }
                                },
                                {
                                    "terms": {
                                        "keywords": keywords
                                    }
                                }
                            ],
                            "minimum_should_match": 1
                        }
                    },
                    "sort": [
                        {
                            "_score": {
                                "order": "desc"
                            }
                        }
                    ],
                    "size": size
                }
                
                # 添加过滤条件
                if filters:
                    query["query"]["bool"]["filter"] = []
                    for key, value in filters.items():
                        query["query"]["bool"]["filter"].append({
                            "term": {
                                key: value
                            }
                        })
                
                # 执行搜索
                response = self.es_client.search(
                    index=self.index_name,
                    body=query,
                    size=size
                )
                
                # 处理结果
                results = []
                for hit in response["hits"]["hits"]:
                    result = hit["_source"]
                    result["score"] = hit["_score"]
                    results.append(result)
                
                return results
            
            return self._retry_operation(search_operation)
            
        except Exception as e:
            logger.error(f"搜索相似图片失败: {e}")
            return []
            
    def calculate_similarity_score(
        self,
        text1: str,
        text2: str
    ) -> float:
        """计算两段文本的相似度分数"""
        try:
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"计算相似度分数时发生错误: {e}")
            return 0.0
            
    def index_image(
        self,
        image_id: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """索引图片元数据"""
        try:
            def index_operation():
                # 确保 task_id 存在
                task_id = metadata.get('task_id')
                if not task_id:
                    logger.warning(f"图片 {image_id} 没有关联的任务ID")
                    return False
                
                document = {
                    'id': image_id,
                    'url': metadata.get('url'),
                    'detected_objects': metadata.get('detected_objects', []),
                    'source_domain': metadata.get('source_domain'),
                    'tags': metadata.get('tags', []),
                    'description': metadata.get('description', ''),
                    'created_at': metadata.get('created_at', datetime.now().isoformat()),
                    'image_hash': metadata.get('image_hash', image_id),
                    'keywords': metadata.get('keywords', []),
                    'task_id': task_id  # 使用已验证的 task_id
                }
                
                # 记录索引操作
                logger.info(f"索引图片 {image_id} 到任务 {task_id}")
                
                self.es_client.index(
                    index=self.index_name,
                    id=image_id,
                    body=document
                )
                return True
                
            return self._retry_operation(index_operation)
        except Exception as e:
            logger.error(f"索引图片元数据时发生错误: {e}")
            return False
            
    async def index_images(self, processed_images: Dict[str, Dict[str, Any]]) -> bool:
        """批量索引图片"""
        try:
            success_count = 0
            for image_hash, image_data in processed_images.items():
                # 构建元数据
                metadata = {
                    'url': image_data.get('url', ''),
                    'detected_objects': image_data.get('detected_objects', []),
                    'source_domain': image_data.get('source_domain', ''),
                    'tags': image_data.get('tags', []),
                    'description': image_data.get('description', ''),
                    'created_at': datetime.now().isoformat(),
                    'image_hash': image_hash,
                    'keywords': image_data.get('keywords', []),
                    'task_id': image_data.get('task_id')
                }
                
                # 索引图片
                if self.index_image(image_hash, metadata):
                    success_count += 1
                    
            logger.info(f"成功索引 {success_count}/{len(processed_images)} 张图片")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"批量索引图片时发生错误: {e}")
            return False
            
    def get_image_data(self, image_id: str) -> dict:
        """获取图片数据
        
        Args:
            image_id: 图片ID（哈希值）
            
        Returns:
            dict: 图片数据，如果未找到则返回空字典
        """
        try:
            def get_operation():
                try:
                    result = self.es_client.get(
                        index=self.index_name,
                        id=image_id
                    )
                    if result['found']:
                        return result['_source']
                    return {}
                except NotFoundError:
                    # 文档不存在，返回空字典
                    return {}
                
            return self._retry_operation(get_operation)
        except Exception as e:
            logger.error(f"获取图片数据失败: {e}")
            return {}

    def search_images(
        self,
        task_id: str = None,
        keywords: List[str] = None,
        size: int = 20
    ) -> List[Dict[str, Any]]:
        """搜索图片
        
        Args:
            task_id: 任务ID
            keywords: 关键词列表
            size: 返回结果数量
        """
        try:
            def search_operation():
                # 构建查询
                query = {
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "match_all": {}
                                }
                            ]
                        }
                    }
                }
                
                # 添加关键词过滤
                if keywords:
                    keyword_terms = []
                    for keyword in keywords:
                        keyword_terms.append({
                            "term": {
                                "keywords": {
                                    "value": keyword,
                                    "boost": 1.0
                                }
                            }
                        })
                    query["query"]["bool"]["must"].extend(keyword_terms)
                
                # 添加任务ID过滤
                if task_id:
                    query["query"]["bool"]["must"].append({
                        "term": {
                            "task_id": task_id
                        }
                    })
                
                # 添加相似度评分
                if keywords:
                    # 计算匹配的关键词数量
                    query["query"] = {
                        "script_score": {
                            "query": {
                                "bool": {
                                    "should": [
                                        {
                                            "terms": {
                                                "keywords": keywords
                                            }
                                        }
                                    ],
                                    "minimum_should_match": 1
                                }
                            },
                            "script": {
                                "source": """
                                double matchedKeywords = 0;
                                double totalKeywords = params.totalKeywords;
                                for (String keyword : params.keywords) {
                                    if (doc['keywords'].contains(keyword)) {
                                        matchedKeywords++;
                                    }
                                }
                                // 如果只搜索一个关键词，匹配度就是 0.5
                                if (totalKeywords == 1) {
                                    return 0.5;
                                }
                                // 如果搜索多个关键词，匹配度是匹配数量除以总关键词数量
                                return matchedKeywords / totalKeywords;
                                """,
                                "params": {
                                    "keywords": keywords,
                                    "totalKeywords": len(keywords)
                                }
                            }
                        }
                    }
                
                # 执行搜索
                response = self._retry_operation(
                    lambda: self.es_client.search(
                        index=self.index_name,
                        body=query,
                        size=size
                    )
                )
                
                # 处理结果
                results = []
                for hit in response["hits"]["hits"]:
                    result = hit["_source"]
                    # 只在关键词搜索时计算相似度
                    if keywords and len(keywords) > 0:
                        # 计算关键词匹配度
                        matched_keywords = set(result.get("keywords", [])) & set(keywords)
                        # 如果只搜索一个关键词，匹配度就是 0.5
                        if len(keywords) == 1:
                            result["score"] = 0.5
                        else:
                            # 如果搜索多个关键词，匹配度是匹配数量除以总关键词数量
                            result["score"] = len(matched_keywords) / len(keywords)
                        # 记录详细的匹配信息
                        logger.info(f"图片 {result.get('image_hash')} 匹配信息:")
                        logger.info(f"  - 搜索关键词: {keywords}")
                        logger.info(f"  - 图片关键词: {result.get('keywords', [])}")
                        logger.info(f"  - 匹配关键词: {matched_keywords}")
                        logger.info(f"  - 相似度: {result['score']}")
                    else:
                        result["score"] = 1.0  # 任务ID搜索时默认相似度为100%
                    
                    # 确保 image_hash 字段存在
                    if "image_hash" not in result:
                        result["image_hash"] = hit["_id"]
                    
                    # 如果没有描述，直接使用关键词列表
                    if not result.get("description"):
                        result["description"] = ", ".join(result.get("keywords", []))
                    
                    results.append(result)
                
                # 记录搜索结果
                logger.info(f"找到 {len(results)} 个匹配的图片")
                
                return results
            
            return self._retry_operation(search_operation)
            
        except Exception as e:
            logger.error(f"搜索图片失败: {e}")
            return [] 