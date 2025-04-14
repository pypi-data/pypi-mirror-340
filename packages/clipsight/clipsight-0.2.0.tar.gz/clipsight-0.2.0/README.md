# Clip-Sight (剪瞳): 分布式图片爬虫系统 | Distributed Image Crawler System

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![PyPI version](https://badge.fury.io/py/clipsight.svg)](https://badge.fury.io/py/clipsight)

[English](#clip-sight-distributed-image-crawler-system) | [中文](#clip-sight-分布式图片爬虫系统)

## 项目介绍 | Project Introduction

ClipSight (剪瞳) 是一个双关语义的名字：
- Clip（剪切/片段）+ Sight（视野）：模仿自媒体创作者"剪切新闻-获取视野"的工作流
- 中文"剪瞳"暗示用剪刀（工具）打开新视界

## Clip-Sight: Distributed Image Crawler System

A distributed image crawling system based on Playwright, supporting high-concurrency image collection, processing, and storage.

### Features

- Browser instance pool management based on Playwright
- Redis task queue with priority processing
- Asynchronous image download and processing pipeline
- Elasticsearch similar image search
- MinIO distributed storage
- Docker containerization deployment
- Comprehensive monitoring and logging system
- Keyword-based image search with similarity scoring
- Task progress tracking and management
- Automatic retry mechanism for failed operations

### System Requirements

- Python 3.11+
- Redis 6.0+
- Elasticsearch 7.0+
- MinIO Server
- Docker (optional)
- Playwright

### Quick Start

1. Clone the repository
```bash
git clone https://gitee.com/duckweeds7/clip-sight.git
cd clip-sight
```

2. Install dependencies
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

3. Configure environment variables
```bash
cp .env.example .env
# Edit .env file with your configuration
```

4. Start services
```bash
# Start Redis, Elasticsearch, and MinIO using Docker Compose
docker-compose up -d

# Start the worker service
python -m src.worker.main

# Start the web service
python -m src.web.app
```

### Docker Deployment

1. Build the image
```bash
docker build -t clip-sight .
```

2. Run containers
```bash
docker-compose up -d
```

### Architecture

#### Components

1. **Browser Pool**
   - Manages Playwright browser instances
   - Automatic reconnection and error handling
   - Configurable maximum instance count

2. **Task Consumer**
   - Redis task queue management
   - Priority queue support
   - Task deduplication mechanism

3. **Image Pipeline**
   - Asynchronous concurrent downloads
   - Image validation and processing
   - Automatic retry mechanism

4. **Storage**
   - MinIO distributed storage
   - Metadata management
   - Chunked upload support

5. **Search**
   - Elasticsearch integration
   - Similar image search
   - TF-IDF keyword expansion
   - Similarity scoring based on keyword matches

### Monitoring

- Task queue length
- Image download success rate
- Processing latency statistics
- Storage usage
- Search performance metrics

### Data Management

Use the `scripts/reset_data.sh` script to manage your data:

```bash
# Make the script executable
chmod +x scripts/reset_data.sh

# Run the script
./scripts/reset_data.sh
```

Available options:
1. Delete ES indices
2. Delete MinIO images
3. Delete Redis task data
4. Delete all data
5. Delete MinIO images by task ID
6. Check and fix environment variables

### Development

1. **Code Structure**
```
clip-sight/
├── src/
│   ├── worker/         # Worker service
│   ├── web/           # Web interface
│   ├── storage/       # Storage management
│   └── search/        # Search functionality
├── scripts/           # Utility scripts
├── tests/            # Test cases
└── docker/           # Docker configuration
```

2. **Testing**
```bash
# Run tests
pytest tests/
```

### License

MIT License

---

## Clip-Sight: 分布式图片爬虫系统

基于 Playwright 的分布式图片爬虫系统，支持高并发图片采集、处理和存储。

### 特性

- 基于 Playwright 的浏览器实例池管理
- Redis 任务队列和优先级处理
- 异步图片下载和处理管道
- Elasticsearch 相似图片搜索
- MinIO 分布式存储
- Docker 容器化部署
- 完善的监控和日志系统
- 基于关键词的图片搜索和相似度评分
- 任务进度跟踪和管理
- 失败操作自动重试机制

### 系统要求

- Python 3.11+
- Redis 6.0+
- Elasticsearch 7.0+
- MinIO Server
- Docker (可选)
- Playwright

### 快速开始

1. 克隆项目
```bash
git clone https://gitee.com/duckweeds7/clip-sight.git
cd clip-sight
```

2. 安装依赖
```bash
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，配置必要的参数
```

4. 启动服务
```bash
# 使用 Docker Compose 启动 Redis、Elasticsearch 和 MinIO
docker-compose up -d

# 启动 worker 服务
python -m src.worker.main

# 启动 web 服务
python -m src.web.app
```

### Docker 部署

1. 构建镜像
```bash
docker build -t clip-sight .
```

2. 运行容器
```bash
docker-compose up -d
```

### 架构说明

#### 组件

1. **浏览器池**
   - 管理 Playwright 浏览器实例
   - 自动重连和异常处理
   - 可配置最大实例数

2. **任务消费者**
   - Redis 任务队列管理
   - 支持优先级队列
   - 任务去重机制

3. **图片处理管道**
   - 异步并发下载
   - 图片验证和处理
   - 自动重试机制

4. **存储系统**
   - MinIO 分布式存储
   - 元数据管理
   - 分块上传支持

5. **搜索系统**
   - Elasticsearch 集成
   - 相似图片搜索
   - TF-IDF 关键词扩展
   - 基于关键词匹配的相似度评分

### 监控指标

- 任务队列长度
- 图片下载成功率
- 处理延迟统计
- 存储使用情况
- 搜索性能指标

### 数据管理

使用 `scripts/reset_data.sh` 脚本管理数据：

```bash
# 添加执行权限
chmod +x scripts/reset_data.sh

# 运行脚本
./scripts/reset_data.sh
```

可用选项：
1. 删除 ES 索引
2. 删除 MinIO 图片
3. 删除 Redis 任务数据
4. 删除所有数据
5. 按任务 ID 删除 MinIO 图片
6. 检查并修复环境变量

### 开发

1. **代码结构**
```
clip-sight/
├── src/
│   ├── worker/         # Worker 服务
│   ├── web/           # Web 界面
│   ├── storage/       # 存储管理
│   └── search/        # 搜索功能
├── scripts/           # 工具脚本
├── tests/            # 测试用例
└── docker/           # Docker 配置
```

2. **测试**
```bash
# 运行测试
pytest tests/
```

### 许可证

MIT License

## 功能特点

- 支持多任务并行处理
- 基于 Playwright 的浏览器自动化
- MinIO 对象存储
- Elasticsearch 相似图片搜索
- Redis 任务队列
- FastAPI Web 界面
- Docker 容器化部署

## 技术栈

- Python 3.8+
- FastAPI
- Playwright
- MinIO
- Elasticsearch
- Redis
- Celery
- Docker

## 安装说明

### 使用 pip 安装

```bash
# 安装包
pip install clipsight

# 安装 Playwright 浏览器
playwright install chromium

# 创建配置文件
cp .env.example .env
```

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/duckweeds7/clip-sight.git
cd clip-sight

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium

# 创建配置文件
cp .env.example .env
```

## 使用说明

### 启动服务

1. 使用 Docker Compose（推荐）：
```bash
docker-compose up -d
```

2. 手动启动：
```bash
# 启动 web 服务
clipsight

# 启动 worker
clipsight-worker
```

### 访问 Web 界面

打开浏览器访问：http://localhost:8000

### 创建爬虫任务

1. 通过 Web 界面：
   - 访问 http://localhost:8000
   - 点击"新建任务"
   - 输入关键词和数量
   - 点击"开始爬取"

2. 通过 API：
```bash
curl -X POST "http://localhost:8000/api/tasks" \
     -H "Content-Type: application/json" \
     -d '{"keywords": ["cat", "dog"], "max_images": 100}'
```

### 查看任务状态

1. 通过 Web 界面：
   - 访问 http://localhost:8000
   - 在任务列表中查看状态

2. 通过 API：
```bash
curl "http://localhost:8000/api/tasks"
```

## 开发指南

### 项目结构

```
clip-sight/
├── src/                    # 源代码
│   ├── browser/           # 浏览器管理
│   ├── crawler/           # 爬虫实现
│   ├── pipeline/          # 数据处理管道
│   ├── search/            # 相似图片搜索
│   ├── storage/           # 存储管理
│   ├── web/               # Web 界面
│   └── worker/            # 后台任务
├── tests/                 # 测试用例
├── docker/                # Docker 配置
├── scripts/               # 工具脚本
└── docs/                  # 文档
```

### 开发环境设置

1. 安装开发依赖：
```bash
pip install -r requirements-dev.txt
```

2. 运行测试：
```bash
pytest
```

3. 代码格式化：
```bash
black .
isort .
```

### 提交代码

1. 创建新分支：
```bash
git checkout -b feature/your-feature
```

2. 提交更改：
```bash
git add .
git commit -m "feat: add your feature"
```

3. 推送到远程：
```bash
git push origin feature/your-feature
```

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件
