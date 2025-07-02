# 银行招聘信息爬虫

这是一个用于爬取银行招聘信息的Python脚本，支持自动检测新职位并通过微信推送通知。

## 功能特性

- 🔍 **自动爬取**: 定期爬取银行招聘网站的最新职位信息
- 📱 **微信通知**: 通过Server酱发送新职位的微信推送
- 💾 **数据存储**: 自动保存历史数据，避免重复通知
- ⏰ **定时任务**: 支持定时运行，适合部署在服务器上
- 🛡️ **错误处理**: 完善的异常处理和重试机制
- 📊 **日志记录**: 详细的运行日志，便于调试和监控

## 项目结构

```
bank-crawler/
├── crawler.py          # 主爬虫脚本
├── scheduler.py        # 定时任务调度器
├── test_crawler.py     # 测试脚本
├── check_config.py     # 配置检查脚本
├── run.sh              # 启动脚本（Linux部署）
├── pyproject.toml      # 项目配置文件（uv）
├── requirements.txt    # 依赖包列表（pip）
├── crontab.example     # 定时任务配置示例
├── .env.example        # 环境变量模板
├── .env                # 环境变量配置（需要创建）
├── README.md           # 项目说明文档
├── data/               # 数据存储目录
│   └── jobs_history.json
├── logs/               # 日志文件目录
│   ├── crawler.log
│   └── cron.log
└── page_examples/      # 网页示例文件
    ├── README.md
    ├── job_lists.html
    └── job_detail.html
```

## 安装和配置

### 1. 环境要求

- Python 3.8+
- uv (推荐) 或 pip

### 2. 安装依赖

使用 uv (推荐):
```bash
# 安装 uv (如果还没有安装)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装项目依赖
uv sync
```

或使用 pip:
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制配置模板并编辑:
```bash
cp .env.example .env
```

编辑 `.env` 文件，配置以下参数:

```bash
# Server酱配置 (必需) - 支持多个密钥，用逗号分隔
# 单个密钥示例：
SERVER_CHAN_KEY=your_server_chan_key_here
# 多个密钥示例（多人接收通知）：
# SERVER_CHAN_KEY=key1,key2,key3

# 爬虫配置 (可选)
BASE_URL=http://www.yinhangzhaopin.com
LIST_URL=http://www.yinhangzhaopin.com/tag/shehuizhaopin_13698_1.html

# 数据存储配置 (可选)
DATA_FILE=data/jobs_history.json
LOG_FILE=logs/crawler.log

# 请求配置 (可选)
REQUEST_DELAY=1
TIMEOUT=30
RETRY_TIMES=3
```

### 4. 获取Server酱密钥

1. 访问 [Server酱官网](https://sct.ftqq.com/)
2. 使用微信扫码登录
3. 获取SendKey
4. 将SendKey填入 `.env` 文件的 `SERVER_CHAN_KEY` 字段

#### 多人接收通知配置

如果您希望多个人都能接收到招聘信息通知，可以配置多个Server酱密钥：

**单个密钥（原有方式）：**
```bash
SERVER_CHAN_KEY=SCT123456abcdef
```

**多个密钥（推荐用逗号分隔）：**
```bash
SERVER_CHAN_KEY=SCT123456abcdef,SCT789012ghijkl,SCT345678mnopqr
```

**多个密钥（也可用分号分隔）：**
```bash
SERVER_CHAN_KEY=SCT123456abcdef;SCT789012ghijkl;SCT345678mnopqr
```

配置多个密钥后，每当发现新的招聘信息时，系统会自动向所有配置的接收者发送微信通知。

## 使用方法

### 🐳 Docker 部署（推荐）

如果您希望在服务器上持续运行爬虫，推荐使用 Docker 部署方式：

#### 快速开始

```bash
# 1. 克隆项目
git clone <your-repository-url>
cd bank-crawler

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置您的 SERVER_CHAN_KEY

# 3. 一键部署
./deploy.sh deploy
```

#### Docker 管理命令

```bash
# 查看服务状态
./deploy.sh status

# 查看实时日志
./deploy.sh logs

# 重启服务
./deploy.sh restart

# 停止服务
./deploy.sh stop

# 清理服务
./deploy.sh clean

# 测试微信通知功能
./deploy.sh test-notification
```

#### 健康检查

```bash
# 基础健康检查
curl http://localhost:8080/health

# 详细状态信息
curl http://localhost:8080/status
```

#### 微信通知测试

首次部署时，系统会自动发送测试通知到您的微信，确认网络连通性。您也可以随时手动测试：

```bash
# 测试微信通知功能
./deploy.sh test-notification
```

**测试通知包含以下信息：**
- ✅ 部署成功确认
- 🌐 网络连接状态
- 📱 微信通知功能状态
- 🔧 系统基本信息

如果测试失败，请检查：
1. `SERVER_CHAN_KEY` 配置是否正确
2. 网络连接是否正常
3. Server酱服务是否可用

详细的 Docker 部署说明请参考：[DOCKER_DEPLOY.md](DOCKER_DEPLOY.md)

### 📦 本地开发部署

#### 1. 环境检查

```bash
# 检查环境配置是否正确
python check_config.py
# 或使用启动脚本
./run.sh setup
```

### 2. 测试运行

首次使用建议先运行测试脚本:

```bash
# 使用 uv
uv run test_crawler.py

# 或直接使用 python
python test_crawler.py

# 或使用启动脚本
./run.sh test
```

### 3. 单次运行

```bash
# 使用 uv
uv run crawler.py

# 或直接使用 python
python crawler.py

# 或使用启动脚本
./run.sh run
```

### 4. 定时运行

#### 方式一：使用内置调度器

```bash
# 使用 uv
uv run scheduler.py

# 或直接使用 python
python scheduler.py

# 或使用启动脚本
./run.sh schedule
```

#### 方式二：使用系统crontab（推荐）

```bash
# 1. 复制crontab配置模板
cp crontab.example my_crontab

# 2. 编辑配置文件，修改路径
vim my_crontab

# 3. 安装定时任务
crontab my_crontab

# 4. 查看已安装的定时任务
crontab -l
```

## 数据格式

### 职位信息结构

```json
{
  "id": "198118",
  "title": "[湖北]2025年湖北银行总行部室社会招聘公告（6.27）",
  "location": "湖北",
  "company": "湖北银行招聘",
  "url": "http://www.yinhangzhaopin.com/hbbank/2025-06-27/198118.htm",
  "date_info": "6.27",
  "crawl_time": "2025-01-14T10:30:00",
  "details": "职位详细描述..."
}
```

### 微信通知格式

```
发现 3 个新的银行招聘职位

**[湖北]2025年湖北银行总行部室社会招聘公告（6.27）**
- 单位: 湖北银行招聘
- 地点: 湖北
- 链接: http://www.yinhangzhaopin.com/hbbank/2025-06-27/198118.htm

**[浙江]2025年浙江稠州商业银行社会招聘公告（6.27）**
- 单位: 浙江稠州商业银行
- 地点: 浙江
- 链接: http://www.yinhangzhaopin.com/zjczcb/2025-06-27/198115.htm
```

## 配置说明

### 环境变量详解

| 变量名 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| `SERVER_CHAN_KEY` | Server酱推送密钥 | - | 是 |
| `BASE_URL` | 网站基础URL | `http://www.yinhangzhaopin.com` | 否 |
| `LIST_URL` | 招聘列表页面URL | 社会招聘列表页 | 否 |
| `DATA_FILE` | 历史数据存储文件 | `data/jobs_history.json` | 否 |
| `LOG_FILE` | 日志文件路径 | `logs/crawler.log` | 否 |
| `REQUEST_DELAY` | 请求间隔(秒) | `1` | 否 |
| `TIMEOUT` | 请求超时时间(秒) | `30` | 否 |
| `RETRY_TIMES` | 重试次数 | `3` | 否 |

### 定时任务配置

在 `scheduler.py` 中可以修改定时规则:

```python
# 每天上午9点
schedule.every().day.at("09:00").do(run_crawler)

# 每天下午6点
schedule.every().day.at("18:00").do(run_crawler)

# 每小时执行
schedule.every().hour.do(run_crawler)

# 每30分钟执行
schedule.every(30).minutes.do(run_crawler)
```

## Linux部署指南

### 快速部署

```bash
# 1. 克隆或上传项目到服务器
# 2. 进入项目目录
cd /path/to/bank-crawler

# 3. 初始化环境
./run.sh setup

# 4. 配置环境变量
vim .env

# 5. 测试运行
./run.sh test

# 6. 设置定时任务
cp crontab.example my_crontab
vim my_crontab  # 修改路径
crontab my_crontab
```

### 启动脚本说明

`run.sh` 脚本提供了完整的部署和运行功能：

```bash
./run.sh setup     # 初始化环境
./run.sh test      # 运行测试
./run.sh run       # 运行一次爬虫
./run.sh schedule  # 启动定时任务
./run.sh status    # 查看运行状态
./run.sh logs      # 查看日志
./run.sh install   # 安装依赖
./run.sh help      # 显示帮助
```

## 故障排除

### 环境检查

```bash
# 运行配置检查脚本
python check_config.py
# 或
./run.sh setup
```

### 常见问题

1. **网络连接失败**
   - 检查网络连接
   - 确认目标网站可访问
   - 调整请求延迟和超时时间

2. **Server酱推送失败**
   - 检查SERVER_CHAN_KEY是否正确
   - 确认Server酱服务状态
   - 查看日志文件中的错误信息

3. **解析失败**
   - 网站结构可能发生变化
   - 检查HTML选择器是否正确
   - 更新解析逻辑

4. **权限问题**
   - 确保数据和日志目录有写入权限
   - 检查文件路径是否正确

5. **定时任务不运行**
   - 检查crontab配置：`crontab -l`
   - 查看cron日志：`tail -f logs/cron.log`
   - 确认脚本路径和权限

### 日志查看

```bash
# 查看最新日志
tail -f logs/crawler.log

# 查看错误日志
grep "ERROR" logs/crawler.log

# 查看cron日志
tail -f logs/cron.log

# 使用启动脚本查看日志
./run.sh logs

# 查看运行状态
./run.sh status
```

## 开发和扩展

### 添加新的数据源

1. 在 `extract_job_list` 方法中添加新的解析逻辑
2. 根据新网站的HTML结构调整选择器
3. 更新 `_parse_job_basic_info` 方法以适应新的数据格式

### 自定义通知格式

修改 `_format_notification_content` 方法来自定义通知内容格式。

### 添加新的通知渠道

在 `send_notification` 方法中添加其他通知服务的支持，如钉钉、企业微信等。

## 许可证

本项目仅供个人学习和求职使用，请遵守目标网站的robots.txt和使用条款。

## 更新日志

### v0.1.0 (2025-01-14)
- 初始版本发布
- 支持银行招聘网站爬取
- 集成Server酱微信推送
- 添加定时任务支持
- 完善错误处理和日志记录