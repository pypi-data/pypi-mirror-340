import sys
import subprocess
from playwright.sync_api import sync_playwright

def install_playwright():
    """安装 Playwright 浏览器"""
    try:
        print("开始安装 Playwright 浏览器...")
        
        # 使用 playwright CLI 命令安装浏览器
        print("正在安装 Chromium 浏览器...")
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("Playwright Chromium 浏览器安装成功!")
            return True
        else:
            print(f"安装失败: {result.stderr}", file=sys.stderr)
            return False
            
    except Exception as e:
        print(f"安装 Playwright 浏览器时发生错误: {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    print("正在启动安装脚本...")
    success = install_playwright()
    if not success:
        sys.exit(1)
    print("安装脚本执行完成.") 