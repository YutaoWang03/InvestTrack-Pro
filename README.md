# InvestTrack Pro 📈

**专业投资组合监控平台 | Professional Investment Portfolio Monitoring Platform**

一个基于Django的现代化投资组合管理和监控系统，为个人投资者和专业机构提供全面的资产管理解决方案。

## ✨ 核心特性

### 📊 专业金融功能
- **资产看板**: 实时投资组合总览和净值监控
- **仓位管理**: 持仓风险分析和策略执行监控
- **交易记录**: 完整的交易流水和持仓变动管理
- **数据中心**: 行情数据导入和系统配置管理
- **沙盘模拟**: 投资策略回测和风险测试

### 💼 专业金融指标
- **AUM** (Assets Under Management) - 资产管理规模
- **VaR** (Value at Risk) - 在险价值计算
- **夏普比率** - 风险调整后收益评估
- **最大回撤** - 投资组合风险度量
- **Beta系数** - 市场风险敏感度分析
- **波动率监控** - 实时风险预警系统

### 🎨 现代化用户界面
- **专业设计**: 符合金融行业标准的界面设计
- **响应式布局**: 完美适配桌面、平板和移动设备
- **深色模式**: 支持浅色/深色主题切换
- **智能侧边栏**: 可折叠导航，状态记忆功能
- **专业工具提示**: 详细的功能说明和术语解释

### 🔧 技术特性
- **Django 6.0**: 现代化Python Web框架
- **SQLite数据库**: 轻量级数据存储解决方案
- **ECharts图表**: 专业的数据可视化
- **Font Awesome图标**: 丰富的图标库
- **CSS变量**: 灵活的主题系统
- **JavaScript ES6+**: 现代化前端交互

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Django 6.0+
- 现代浏览器 (Chrome, Firefox, Safari, Edge)

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/YutaoWang03/InvestTrack-Pro.git
cd InvestTrack-Pro
```

2. **创建虚拟环境**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **数据库迁移**
```bash
python manage.py migrate
```

5. **创建示例数据**
```bash
python create_sample_data.py
```

6. **启动开发服务器**
```bash
python manage.py runserver
```

7. **访问应用**
打开浏览器访问: `http://127.0.0.1:8000`

### 快速启动脚本

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```cmd
start.bat
```

## 📱 功能模块

### 🏠 资产看板 (Dashboard)
- 投资组合总览
- 实时净值走势图
- 资产分配饼图
- KPI指标面板
- 风险监控预警

### 📊 仓位管理 (Position Management)
- 持仓详情列表
- 风险暴露分析
- 止损价格计算
- 收益率统计
- 资产配置建议

### 💰 交易记录 (Transaction History)
- 交易流水查询
- 筛选和分页功能
- 交易统计分析
- 手续费计算
- 备注管理

### 🗄️ 数据中心 (Data Center)
- 行情数据导入
- 系统状态监控
- 配置参数管理
- 数据同步状态
- 错误日志查看

### 🧪 沙盘模拟 (Sandbox)
- 策略回测功能
- 风险压力测试
- 模拟交易环境
- 性能评估报告
- 参数优化建议

## 🏗️ 项目结构

```
InvestTrack-Pro/
├── core/                   # Django核心配置
│   ├── settings.py        # 项目设置
│   ├── urls.py           # 主URL配置
│   └── wsgi.py           # WSGI配置
├── apps/                   # 应用模块
│   ├── investments/       # 投资管理
│   ├── risk_engine/       # 风险引擎
│   ├── data_loader/       # 数据加载
│   └── users/            # 用户管理
├── templates/             # HTML模板
│   ├── base.html         # 基础模板
│   ├── dashboard.html    # 资产看板
│   ├── position.html     # 仓位管理
│   ├── transaction.html  # 交易记录
│   ├── data_center.html  # 数据中心
│   └── sandbox.html      # 沙盘模拟
├── data/                  # 数据文件
├── docs/                  # 项目文档
├── requirements.txt       # Python依赖
├── manage.py             # Django管理脚本
├── create_sample_data.py # 示例数据生成
├── start.sh              # Linux/Mac启动脚本
└── start.bat             # Windows启动脚本
```

## 🎯 技术亮点

### 前端技术
- **现代CSS**: 使用CSS变量和Flexbox/Grid布局
- **响应式设计**: 移动优先的设计理念
- **交互动画**: 平滑的过渡效果和用户反馈
- **无障碍设计**: 符合WCAG标准的可访问性

### 后端架构
- **模块化设计**: 清晰的应用分层架构
- **数据模型**: 完整的金融数据建模
- **API设计**: RESTful风格的数据接口
- **错误处理**: 完善的异常处理机制

### 数据可视化
- **ECharts集成**: 专业的图表库
- **实时更新**: 动态数据刷新
- **多种图表**: 折线图、饼图、柱状图等
- **交互功能**: 缩放、筛选、导出等

## 🔮 未来规划

### 短期目标 (1-2个月)
- [ ] 实时数据接入 (WebSocket)
- [ ] 更多技术指标 (MACD, RSI, KDJ)
- [ ] 移动端APP开发
- [ ] 数据导出功能

### 中期目标 (3-6个月)
- [ ] AI智能分析
- [ ] 多账户管理
- [ ] 社交功能
- [ ] 插件系统

### 长期愿景 (6个月+)
- [ ] 机构版本
- [ ] 国际化支持
- [ ] 云端部署
- [ ] 开放API平台

## 🤝 贡献指南

我们欢迎所有形式的贡献！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- **项目主页**: https://github.com/YutaoWang03/InvestTrack-Pro
- **问题反馈**: https://github.com/YutaoWang03/InvestTrack-Pro/issues
- **功能建议**: https://github.com/YutaoWang03/InvestTrack-Pro/discussions

## 🙏 致谢

感谢以下开源项目的支持：
- [Django](https://djangoproject.com/) - Web框架
- [ECharts](https://echarts.apache.org/) - 数据可视化
- [Font Awesome](https://fontawesome.com/) - 图标库
- [Inter Font](https://rsms.me/inter/) - 字体

---

**InvestTrack Pro** - 让投资管理更专业、更智能、更高效 🚀