@echo off
echo 数据重置工具
echo =============
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请确保已安装Python并添加到PATH中
    pause
    exit /b 1
)

REM 检查虚拟环境是否存在
if not exist "..\venv" (
    echo 警告: 未找到虚拟环境，将使用系统Python
    echo.
) else (
    echo 使用虚拟环境
    call ..\venv\Scripts\activate
)

echo 请选择要执行的操作:
echo 1. 删除ES索引
echo 2. 删除MinIO图片
echo 3. 删除Redis任务数据
echo 4. 删除所有数据
echo 5. 按任务ID删除MinIO图片
echo 6. 检查并修复环境变量
echo 0. 退出
echo.

set /p choice=请输入选项编号: 

if "%choice%"=="0" (
    echo 退出程序
    exit /b 0
)

if "%choice%"=="1" (
    python reset_data.py --es
) else if "%choice%"=="2" (
    python reset_data.py --minio
) else if "%choice%"=="3" (
    python reset_data.py --redis
) else if "%choice%"=="4" (
    python reset_data.py --all
) else if "%choice%"=="5" (
    set /p task_id=请输入任务ID: 
    python reset_data.py --minio --prefix "%task_id%"
) else if "%choice%"=="6" (
    python reset_data.py --fix-env
) else (
    echo 无效的选项
)

echo.
echo 操作完成
pause 