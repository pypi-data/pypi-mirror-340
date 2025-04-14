import os
import sys

# 添加项目根目录到Python路径
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

from src.web.app import app
from loguru import logger
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

if __name__ == "__main__":
    # 获取配置
    host = os.getenv("WEB_HOST", "0.0.0.0")
    port = int(os.getenv("WEB_PORT", "8000"))
    reload = os.getenv("WEB_RELOAD", "true").lower() == "true"
    
    logger.info(f"启动Web服务器: {host}:{port}")
    
    # 启动服务器
    import uvicorn
    uvicorn.run(
        "src.web.app:app",
        host=host,
        port=port,
        reload=reload
    ) 