from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
from loguru import logger
from typing import List, Optional
import json
from datetime import datetime
from pydantic import BaseModel
import redis
from dotenv import load_dotenv
from src.storage.minio_storage import MinioStorage
from src.search.similar_images import SimilarImageSearcher

# 加载环境变量
load_dotenv()

# 获取当前文件所在目录的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 创建FastAPI应用
app = FastAPI(title="ClipSight")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保静态文件和模板目录存在
os.makedirs(os.path.join(BASE_DIR, "static"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "templates"), exist_ok=True)

# 挂载静态文件
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# 配置模板
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# 请求体模型
class TaskCreate(BaseModel):
    keywords: List[str]
    max_images: int = 20

# 初始化Redis客户端
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0))
)

# 初始化MinIO客户端
minio_storage = MinioStorage(
    endpoint=os.getenv('MINIO_ENDPOINT', 'localhost:9000'),
    access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
    secret_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin'),
    bucket_name=os.getenv('MINIO_BUCKET', 'images')
)

# 初始化ES搜索客户端
similar_searcher = SimilarImageSearcher(
    es_host=os.getenv('ES_HOST', 'localhost'),
    es_port=int(os.getenv('ES_PORT', 9200)),
    index_name=os.getenv('ES_INDEX', 'images'),
    min_score=float(os.getenv('ES_MIN_SCORE', 0.3))
)

def get_task_from_redis(task_id: str) -> dict:
    """从Redis获取任务数据"""
    task_data = redis_client.get(f"task:{task_id}")
    if task_data:
        return json.loads(task_data.decode())
    return None

def save_task_to_redis(task_id: str, task_data: dict):
    """保存任务数据到Redis"""
    redis_client.set(f"task:{task_id}", json.dumps(task_data))
    # 将任务ID添加到任务列表集合中
    redis_client.sadd("task_ids", task_id)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """返回Web界面"""
    return templates.TemplateResponse("index.html", {"request": request, "app": app})

@app.post("/api/tasks")
async def create_task(task: TaskCreate):
    """创建新的爬虫任务"""
    try:
        task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        task_data = {
            "task_id": task_id,
            "keywords": task.keywords,
            "max_images": task.max_images,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "images": []
        }
        
        # 保存任务数据到Redis
        save_task_to_redis(task_id, task_data)
        
        # 将任务添加到Redis队列
        redis_client.lpush('image_tasks', json.dumps(task_data))
        logger.info(f"任务已添加到队列: {task_id}")
        
        return {"task_id": task_id, "status": "pending"}
    except Exception as e:
        logger.error(f"创建任务失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tasks")
async def list_tasks():
    """获取所有任务"""
    try:
        # 从Redis获取所有任务ID
        task_ids = redis_client.smembers("task_ids")
        tasks = []
        
        # 获取每个任务的详细信息
        for task_id in task_ids:
            task_id = task_id.decode()
            task_data = get_task_from_redis(task_id)
            if task_data:
                # 更新任务状态
                task_status = redis_client.get(f"task_status:{task_id}")
                if task_status:
                    task_data["status"] = task_status.decode()
                tasks.append(task_data)
                
        # 按创建时间倒序排序
        tasks.sort(key=lambda x: x["created_at"], reverse=True)
        return tasks
    except Exception as e:
        logger.error(f"获取任务列表失败: {e}")
        return []

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    """获取特定任务"""
    task_data = get_task_from_redis(task_id)
    if not task_data:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 从Redis获取任务状态
    task_status = redis_client.get(f"task_status:{task_id}")
    if task_status:
        task_data["status"] = task_status.decode()
    
    return task_data

@app.get("/api/tasks/{task_id}/images")
async def get_task_images(task_id: str):
    """获取任务相关的图片"""
    task_data = get_task_from_redis(task_id)
    if not task_data:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    try:
        # 从MinIO获取图片列表
        images = minio_storage.list_images(prefix=f"{task_id}/")
        
        # 获取每张图片的详细信息
        image_details = []
        for image in images:
            # 获取图片元数据
            metadata = minio_storage.get_image_metadata(image.object_name)
            
            # 获取图片URL
            url = minio_storage.get_image_url(image.object_name)
            
            # 从图片路径中提取图片哈希值
            image_hash = image.object_name.split('/')[-1].split('.')[0]
            
            # 从ES获取图片的标签和描述
            es_data = similar_searcher.get_image_data(image_hash)
            
            # 确保 description 字段有值
            description = es_data.get("description", "")
            if not description and es_data.get("keywords"):
                description = ", ".join(es_data["keywords"])
            
            image_details.append({
                "url": url,
                "object_name": image.object_name,
                "size": image.size,
                "last_modified": image.last_modified.isoformat(),
                "metadata": metadata,
                "tags": es_data.get("tags", []),
                "description": description,  # 使用处理后的描述
                "detected_objects": [image.object_name],  # MinIO 路径
                "task_id": task_id,  # 添加任务ID
                "created_at": es_data.get("created_at", image.last_modified.isoformat())  # 添加创建时间
            })
        
        return image_details
    except Exception as e:
        logger.error(f"获取图片列表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    """获取任务状态"""
    task_data = get_task_from_redis(task_id)
    if not task_data:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 从Redis获取任务状态
    task_status = redis_client.get(f"task_status:{task_id}")
    if task_status:
        status = task_status.decode()
    else:
        status = task_data["status"]
    
    # 获取任务进度
    progress = redis_client.get(f"task_progress:{task_id}")
    if progress:
        progress = int(progress.decode())
    else:
        progress = 0
    
    return {
        "task_id": task_id,
        "status": status,
        "progress": progress
    }

@app.get("/api/search")
async def search_images(
    task_id: Optional[str] = None,
    keywords: Optional[str] = None,
    size: int = 20
):
    """搜索图片
    
    Args:
        task_id: 任务ID
        keywords: 关键词，多个关键词用空格分隔
        size: 返回结果数量
    """
    try:
        # 解析关键词
        keyword_list = None
        if keywords and keywords.strip():
            # 将关键词按逗号分割
            keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
        
        # 搜索图片
        results = similar_searcher.search_images(
            task_id=task_id,
            keywords=keyword_list,
            size=size
        )
        
        # 获取图片URL
        for result in results:
            image_id = result['image_hash']  # 使用 image_hash 作为图片ID
            # 从MinIO获取图片URL
            result_task_id = result.get('task_id', task_id)  # 使用ES中存储的task_id或传入的task_id
            url = minio_storage.get_image_url(f"{result_task_id}/{image_id}.jpg")
            result['url'] = url
            
            # 添加 MinIO 路径
            result['detected_objects'] = [f"{result_task_id}/{image_id}.jpg"]
            
            # 确保所有必要字段都存在
            if 'description' not in result or not result['description']:
                result['description'] = ", ".join(result.get('keywords', []))
            
            # 确保 created_at 字段存在
            if 'created_at' not in result:
                result['created_at'] = datetime.now().isoformat()
                
            # 确保 task_id 字段存在
            if 'task_id' not in result:
                result['task_id'] = result_task_id
                
            # 确保 tags 字段存在
            if 'tags' not in result:
                result['tags'] = []
        
        return results
    except Exception as e:
        logger.error(f"搜索图片失败: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 