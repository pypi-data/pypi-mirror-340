try:
    print("正在导入 playwright 包...")
    from playwright.sync_api import sync_playwright
    print("成功导入 playwright 包!")
    
    print("正在测试 playwright 安装...")
    with sync_playwright() as p:
        print("成功初始化 playwright!")
        print("正在安装浏览器...")
        p.chromium.install()
        print("浏览器安装成功!")
        
except Exception as e:
    print(f"发生错误: {str(e)}")
    raise 