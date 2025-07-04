# 微信通知测试功能说明

## 功能概述

为了确保银行爬虫部署后能够正常发送微信通知，我们添加了自动测试通知功能。这个功能会在首次部署时自动运行，也可以随时手动执行。

## 主要特性

### 🚀 自动部署通知
- 首次使用 `./deploy.sh deploy` 部署时自动发送测试通知
- 确认服务器网络连接正常
- 验证Server酱配置正确
- 测试微信通知功能可用

### 🧪 手动测试功能
- 随时可以手动测试微信通知
- 支持多个Server酱密钥测试
- 详细的测试结果反馈

## 使用方法

### 自动测试（首次部署）

```bash
# 首次部署时会自动发送测试通知
./deploy.sh deploy
```

部署完成后，您应该会在微信中收到一条测试消息，包含：
- 部署成功确认
- 系统基本信息
- 网络连接状态
- 功能测试结果

### 手动测试

```bash
# 随时测试微信通知功能
./deploy.sh test-notification
```

## 测试消息内容

测试通知包含以下信息：

```
🎉 银行爬虫部署成功通知

部署时间：2025-01-14 15:30:00
服务状态：✅ 正常运行
网络连接：✅ 连通正常
功能测试：✅ 微信通知功能正常

系统信息：
- 服务名称：银行招聘信息爬虫
- 部署环境：Docker容器
- 健康检查：http://localhost:8080/health
- 状态查看：http://localhost:8080/status
```

## 故障排除

### 测试失败的常见原因

1. **SERVER_CHAN_KEY配置错误**
   - 检查 `.env` 文件中的密钥是否正确
   - 确认密钥格式：`SCT` 开头的字符串
   - 多个密钥用逗号分隔

2. **网络连接问题**
   - 确认服务器可以访问 `sctapi.ftqq.com`
   - 检查防火墙设置
   - 验证DNS解析

3. **Server酱服务问题**
   - 访问 [Server酱官网](https://sct.ftqq.com/) 确认服务状态
   - 检查密钥是否过期
   - 确认微信已关注Server酱公众号

### 调试步骤

```bash
# 1. 检查容器状态
docker-compose ps

# 2. 查看详细日志
docker-compose logs bank-crawler

# 3. 进入容器手动测试
docker-compose exec bank-crawler python test_notification.py

# 4. 检查环境变量
docker-compose exec bank-crawler env | grep SERVER_CHAN_KEY
```

## 技术实现

### 文件结构

- `test_notification.py` - 独立的测试通知脚本
- `deploy.sh` - 部署脚本（已集成自动测试）
- `crawler.py` - 主爬虫程序（包含通知功能）

### 测试流程

1. 读取环境变量中的Server酱密钥
2. 解析多个密钥（支持逗号或分号分隔）
3. 构造测试消息内容
4. 向每个密钥发送测试通知
5. 统计成功/失败结果
6. 输出详细的测试报告

### 安全考虑

- 测试脚本不会记录或泄露密钥信息
- 支持多密钥配置，提高可靠性
- 包含适当的错误处理和重试机制

## 更新日志

### v1.0.0 (2025-01-14)
- ✨ 新增自动部署通知功能
- ✨ 新增手动测试通知命令
- ✨ 支持多Server酱密钥测试
- 📝 完善文档说明
- 🔧 优化部署脚本

---

**注意**：此功能仅用于测试通知系统是否正常工作，不会影响正常的爬虫功能和职位通知。