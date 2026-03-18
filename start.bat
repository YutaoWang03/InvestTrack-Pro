@echo off
chcp 65001 >nul

echo 🚀 启动 InvestTrack 投资组合监控平台...

REM 检查虚拟环境
if not exist ".venv" (
    echo 📦 创建虚拟环境...
    python -m venv .venv
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 安装依赖
echo 📚 安装依赖包...
pip install -r requirements.txt

REM 数据库迁移
echo 🗄️ 执行数据库迁移...
python manage.py migrate

echo ✅ 启动完成！
echo 🌐 访问地址: http://127.0.0.1:8000/
echo ⚙️ 管理后台: http://127.0.0.1:8000/admin/
echo.
echo 🎯 启动开发服务器...
python manage.py runserver

pause