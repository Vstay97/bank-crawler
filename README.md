# Bank Crawler

[![GitHub Actions](https://github.com/Vstay97/bank-crawler/actions/workflows/main.yml/badge.svg)](https://github.com/Vstay97/bank-crawler/actions/workflows/main.yml)

定时爬取银行招聘信息，并推送至微信。

## ✨ 功能特性

- **多渠道支持**：支持多家银行招聘网站。
- **增量更新**：只推送最新的招聘信息，避免重复打扰。
- **多种部署方式**：支持 GitHub Actions、Docker 和本地直接运行。
- **灵活配置**：可通过环境变量轻松配置。
- **微信通知**：通过 Server酱 推送招聘信息至微信。

## 🚀 部署方式

### 1. GitHub Actions 自动部署 (推荐)

这是最简单、最推荐的部署方式。项目已配置好 GitHub Actions，可实现全自动的爬取和通知。

**工作原理:**

1.  **定时触发**: GitHub Actions 工作流配置为每天定时运行 (默认为 UTC 时间 01:00，即北京时间上午 9:00)。
2.  **执行爬虫**: 工作流会检出最新代码，安装依赖，然后运行 `crawler.py` 脚本。
3.  **增量更新**: 爬虫会读取 `data/jobs_history.json` 文件来获取已推送过的岗位。爬取完成后，会将新发现的岗位与历史记录对比，只推送新的岗位。
4.  **持久化记录**: 推送完成后，脚本会将最新的岗位列表更新回 `data/jobs_history.json` 文件，并自动提交回 GitHub 仓库。这确保了下一次运行时，爬虫知道哪些岗位已经是“旧”的。
5.  **发送通知**: 如果有新的岗位，脚本会通过您配置的 `SERVER_CHAN_KEY` 调用 Server酱 API，将消息推送到您的微信。

**配置步骤:**

1.  **Fork 本项目**: 点击页面右上角的 "Fork" 按钮，将此项目复制到您自己的 GitHub 账户下。
2.  **获取 Server酱 SendKey**: 登录 [Server酱](http://sc.ftqq.com/)，获取您的 `SendKey`。
3.  **配置 Secrets**: 在您 Fork 的项目中，进入 `Settings` > `Secrets and variables` > `Actions`。
    *   点击 `New repository secret`。
    *   创建一个名为 `SERVER_CHAN_KEY` 的 Secret，值为您刚刚获取的 `SendKey`。
4.  **启用 Actions**: 在您 Fork 的项目中，进入 `Actions` 标签页，如果看到提示，请点击 "I understand my workflows, go ahead and enable them"。

完成以上步骤后，您的爬虫就已经在云端自动运行了！无需任何服务器，也无需手动干预。

### 2. Docker 部署

如果您偏好使用 Docker，或者希望在自己的服务器上运行，可以采用此方式。

**步骤:**

1.  **克隆项目**:
    ```bash
    git clone https://github.com/YOUR_USERNAME/bank-crawler.git
    cd bank-crawler
    ```
2.  **配置环境变量**:
    *   复制 `.env.example` 文件为 `.env`:
        ```bash
        cp .env.example .env
        ```
    *   编辑 `.env` 文件，填入您的 `SERVER_CHAN_KEY`。
3.  **构建并启动容器**:
    ```bash
    docker-compose up --build -d
    ```
    此命令会以后台模式构建并启动服务。`scheduler.py` 会根据默认的定时设置（每天上午9点）运行爬虫。

**常用命令:**

*   **查看日志**: `docker-compose logs -f`
*   **停止服务**: `docker-compose down`
*   **查看服务状态**: `docker-compose ps`

### 3. 本地部署

如果您想在本地开发或直接在服务器上运行裸机进程，可以采用此方式。

**步骤:**

1.  **克隆项目**:
    ```bash
    git clone https://github.com/YOUR_USERNAME/bank-crawler.git
    cd bank-crawler
    ```
2.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **配置环境变量**:
    *   复制 `.env.example` 文件为 `.env`:
        ```bash
        cp .env.example .env
        ```
    *   编辑 `.env` 文件，填入您的 `SERVER_CHAN_KEY`。
4.  **运行爬虫**:
    *   **立即运行一次**:
        ```bash
        python crawler.py
        ```
    *   **启动定时任务**:
        ```bash
        python scheduler.py
        ```
        这会启动一个调度器，在每天上午9点自动运行爬虫。

## 🛠️ 项目结构

```
.
├── .github/workflows/main.yml  # GitHub Actions 配置文件
├── data/
│   └── jobs_history.json       # 历史岗位记录 (用于增量更新)
├── .env.example                # 环境变量模板
├── crawler.py                  # 核心爬虫逻辑
├── scheduler.py                # 定时任务调度器 (用于 Docker/本地部署)
├── Dockerfile                  # Docker 镜像配置文件
├── docker-compose.yml          # Docker 服务编排文件
├── requirements.txt            # Python 依赖
└── README.md                   # 就是你现在看到的这个文件
```

## ⚙️ 环境和配置

### 环境变量

项目通过 `.env` 文件或 GitHub Secrets 管理配置。

- `SERVER_CHAN_KEY`: **必需**。用于 Server酱 消息推送。
- `TZ`: 时区设置，默认为 `Asia/Shanghai`。

### 定时任务

- **GitHub Actions**: 在 `.github/workflows/main.yml` 中通过 `cron` 表达式配置。默认为 `0 1 * * *` (UTC)，即北京时间上午 9:00。
- **Docker/本地部署**: 在 `scheduler.py` 中通过 `apscheduler` 库配置。默认为每天上午 9:00。

## ❓ 故障排除

- **收不到通知**:
    1.  检查 `SERVER_CHAN_KEY` 是否正确配置。
    2.  在 GitHub Actions 中，检查工作流的运行日志，看是否有错误信息。
    3.  在 Docker/本地部署中，使用 `docker-compose logs -f` 或直接查看终端输出，检查错误。
- **重复收到通知**:
    1.  确保 `data/jobs_history.json` 文件可以被正确读写。
    2.  对于 GitHub Actions，检查工作流是否具有回写仓库的权限 (`permissions: contents: write`)。

## 🤝 贡献

欢迎提交 Pull Request 或 Issue。

## 📄 开源许可

[MIT](LICENSE)