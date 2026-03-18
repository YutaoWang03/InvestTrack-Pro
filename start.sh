#!/bin/bash

# InvestTrack 启动脚本

echo "🚀 启动 InvestTrack 投资组合监控平台..."

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv .venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source .venv/bin/activate

# 安装依赖
echo "📚 安装依赖包..."
pip install -r requirements.txt

# 数据库迁移
echo "🗄️ 执行数据库迁移..."
python manage.py migrate

# 检查是否有数据，如果没有则创建示例数据
echo "📊 检查数据库数据..."
DATA_COUNT=$(python manage.py shell -c "
from apps.investments.models import AccountSnapshot
print(AccountSnapshot.objects.count())
" 2>/dev/null | tail -1)

if [ "$DATA_COUNT" = "0" ]; then
    echo "📝 数据库为空，创建示例数据..."
    python create_sample_data.py
else
    echo "✅ 数据库已有数据 ($DATA_COUNT 条账户快照)"
fi

# 收集静态文件（如果需要）
# python manage.py collectstatic --noinput

echo "✅ 启动完成！"
echo "🌐 访问地址: http://127.0.0.1:8000/"
echo "⚙️ 管理后台: http://127.0.0.1:8000/admin/"
echo ""
echo "🎯 启动开发服务器..."
python manage.py runserver