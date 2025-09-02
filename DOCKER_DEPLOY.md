# Docker 部署指南

本指南将帮助您在服务器上使用 Docker 部署银行招聘爬虫，实现自动爬取并推送微信通知。

## 前置要求

- Docker 和 Docker Compose 已安装
- Server酱账号和API密钥
- 服务器具备网络访问权限

## 快速部署

### 1. 克隆项目

```bash
git clone https://github.com/Vstay97/bank-crawler.git
cd bank-crawler
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置您的 Server酱 API 密钥：

```bash
SERVER_CHAN_KEY=your_actual_server_chan_key_here
```

### 3. 构建并启动容器

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

### 4. 验证部署

```bash
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f bank-crawler

# 健康检查
curl http://localhost:8080/health

# 测试微信通知功能
./deploy.sh test-notification
```

**首次部署自动通知**：使用 `./deploy.sh deploy` 进行首次部署时，系统会自动发送测试通知到您的微信，确认以下功能正常：
- ✅ 服务器网络连接
- ✅ Server酱配置正确
- ✅ 微信通知功能可用
- ✅ 爬虫服务已启动

如果没有收到测试通知，请检查 `SERVER_CHAN_KEY` 配置和网络连接。

## 详细配置

### 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `SERVER_CHAN_KEY` | Server酱API密钥，支持多个密钥用逗号分隔 | 必须设置 |
| `BASE_URL` | 银行招聘网站基础URL | `http://www.yinhangzhaopin.com` |
| `LIST_URL` | 职位列表页面URL | 默认社会招聘页面 |
| `REQUEST_DELAY` | 请求间隔（秒） | `1` |
| `TIMEOUT` | 请求超时时间（秒） | `30` |
| `RETRY_TIMES` | 重试次数 | `3` |

#### 多个接收者配置示例

如果您希望多个人都能接收到招聘信息通知，可以配置多个Server酱密钥：

**单个密钥（原有方式）：**
```bash
SERVER_CHAN_KEY=SCT123456abcdef
```

**多个密钥（用逗号分隔）：**
```bash
SERVER_CHAN_KEY=SCT123456abcdef,SCT789012ghijkl,SCT345678mnopqr
```

**多个密钥（用分号分隔）：**
```bash
SERVER_CHAN_KEY=SCT123456abcdef;SCT789012ghijkl;SCT345678mnopqr
```

配置多个密钥后，每当发现新的招聘信息时，系统会自动向所有配置的接收者发送通知。

### 定时任务配置

默认配置为每天上午9点执行爬虫任务。如需修改，请编辑 `scheduler.py` 文件：

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

### 数据持久化

容器会将以下目录挂载到宿主机：

- `./data` - 存储爬取的职位数据和历史记录
- `./logs` - 存储运行日志

这确保了容器重启后数据不会丢失。

## 监控和维护

### 健康检查

容器提供了健康检查端点：

```bash
# 基础健康检查
curl http://localhost:8080/health

# 详细状态信息
curl http://localhost:8080/status
```

### 查看日志

```bash
# 实时查看日志
docker-compose logs -f bank-crawler

# 查看最近100行日志
docker-compose logs --tail=100 bank-crawler
```

### 重启服务

```bash
# 重启容器
docker-compose restart bank-crawler

# 重新构建并启动
docker-compose up -d --build
```

### 停止服务

```bash
# 停止容器
docker-compose stop

# 停止并删除容器
docker-compose down
```

## 故障排除

### 常见问题

1. **容器启动失败**
   ```bash
   # 检查日志
   docker-compose logs bank-crawler
   ```

2. **无法接收微信通知**
   - 检查 `SERVER_CHAN_KEY` 是否正确设置
   - 确认 Server酱 服务正常
   - 查看容器日志中的错误信息

3. **网络连接问题**
   - 确认服务器可以访问目标网站
   - 检查防火墙设置
   - 验证DNS解析

4. **数据目录权限问题**
   ```bash
   # 修复权限
   sudo chown -R $USER:$USER ./data ./logs
   ```

### 调试模式

如需调试，可以进入容器：

```bash
# 进入运行中的容器
docker-compose exec bank-crawler bash

# 手动运行爬虫
python crawler.py
```

## 生产环境建议

1. **使用外部数据库**：考虑使用 PostgreSQL 或 MySQL 替代 JSON 文件存储

2. **日志管理**：配置日志轮转，避免日志文件过大

3. **监控告警**：集成 Prometheus + Grafana 进行监控

4. **备份策略**：定期备份 `data` 目录

5. **安全加固**：
   - 使用非 root 用户运行容器
   - 限制容器资源使用
   - 定期更新基础镜像

## 自定义配置

### 修改爬取频率

编辑 `docker-compose.yml`，添加环境变量：

```yaml
environment:
  - SCHEDULE_TIME=09:00  # 自定义执行时间
```

### 添加多个通知渠道

可以扩展 `crawler.py` 支持多种通知方式（邮件、钉钉、企业微信等）。

### 集群部署

对于高可用需求，可以使用 Docker Swarm 或 Kubernetes 进行集群部署。

---

**注意**：请确保遵守目标网站的 robots.txt 和使用条款，合理设置爬取频率，避免对服务器造成过大压力。