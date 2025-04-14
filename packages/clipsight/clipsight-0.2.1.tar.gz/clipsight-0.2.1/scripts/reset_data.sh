#!/bin/bash

echo "数据重置工具"
echo "============="
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python，请确保已安装Python"
    exit 1
fi

# 检查虚拟环境是否存在
if [ -d "../venv" ]; then
    echo "使用虚拟环境"
    source ../venv/bin/activate
else
    echo "警告: 未找到虚拟环境，将使用系统Python"
    echo
fi

# 加载环境变量
source .env

# 删除 ES 索引
echo "删除 ES 索引..."
curl -X DELETE "http://${ES_HOST}:${ES_PORT}/images"

# 删除 MinIO 中的所有对象
echo "删除 MinIO 中的所有对象..."
mc rm --recursive --force minio/images/

# 重新创建 MinIO bucket
echo "重新创建 MinIO bucket..."
mc mb minio/images || true

# 设置 MinIO bucket 策略
echo "设置 MinIO bucket 策略..."
mc policy set public minio/images

echo "数据清理完成！"

while true; do
    echo "请选择要执行的操作:"
    echo "1. 删除ES索引"
    echo "2. 删除MinIO图片"
    echo "3. 删除Redis任务数据"
    echo "4. 删除所有数据"
    echo "5. 按任务ID删除MinIO图片"
    echo "6. 检查并修复环境变量"
    echo "0. 退出"
    echo

    read -p "请输入选项编号: " choice

    case $choice in
        0)
            echo "退出程序"
            exit 0
            ;;
        1)
            python3 reset_data.py --es
            ;;
        2)
            python3 reset_data.py --minio
            ;;
        3)
            python3 reset_data.py --redis
            ;;
        4)
            python3 reset_data.py --all
            ;;
        5)
            read -p "请输入任务ID: " task_id
            python3 reset_data.py --minio --prefix "$task_id"
            ;;
        6)
            python3 reset_data.py --fix-env
            ;;
        *)
            echo "无效的选项"
            ;;
    esac

    echo
    echo "操作完成"
    echo
done 