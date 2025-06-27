#!/bin/bash

# 银行招聘爬虫启动脚本
# 用于在Linux服务器上部署和运行爬虫

set -e

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# 检查Python环境
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        log_error "未找到Python环境，请先安装Python 3.8+"
        exit 1
    fi
    
    log_info "使用Python命令: $PYTHON_CMD"
}

# 检查依赖
check_dependencies() {
    log_info "检查依赖包..."
    
    if [ -f "requirements.txt" ]; then
        $PYTHON_CMD -c "import requests, bs4, schedule, dotenv" 2>/dev/null || {
            log_warn "依赖包不完整，正在安装..."
            $PYTHON_CMD -m pip install -r requirements.txt
        }
    else
        log_error "未找到requirements.txt文件"
        exit 1
    fi
}

# 检查配置文件
check_config() {
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            log_warn "未找到.env配置文件，正在复制模板..."
            cp .env.example .env
            log_warn "请编辑.env文件，配置Server酱密钥等参数"
            log_warn "配置完成后重新运行此脚本"
            exit 1
        else
            log_error "未找到配置文件模板"
            exit 1
        fi
    fi
    
    # 检查关键配置
    if ! grep -q "SERVER_CHAN_KEY=your_server_chan_key_here" .env; then
        log_info "配置文件已更新"
    else
        log_warn "请在.env文件中配置正确的SERVER_CHAN_KEY"
    fi
}

# 创建必要目录
setup_directories() {
    log_info "创建必要目录..."
    mkdir -p data logs
}

# 显示帮助信息
show_help() {
    echo "银行招聘爬虫启动脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  run         运行一次爬虫"
    echo "  test        运行测试脚本"
    echo "  schedule    启动定时任务"
    echo "  install     安装依赖"
    echo "  status      查看运行状态"
    echo "  logs        查看日志"
    echo "  setup       初始化环境"
    echo "  help        显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 setup     # 初始化环境"
    echo "  $0 test      # 运行测试"
    echo "  $0 run       # 运行一次爬虫"
    echo "  $0 schedule  # 启动定时任务"
}

# 安装依赖
install_dependencies() {
    log_info "安装依赖包..."
    check_python
    
    if command -v uv &> /dev/null; then
        log_info "使用uv安装依赖"
        uv sync
    else
        log_info "使用pip安装依赖"
        $PYTHON_CMD -m pip install -r requirements.txt
    fi
    
    log_info "依赖安装完成"
}

# 初始化环境
setup_environment() {
    log_info "初始化环境..."
    check_python
    setup_directories
    install_dependencies
    check_config
    log_info "环境初始化完成"
}

# 运行爬虫
run_crawler() {
    log_info "运行银行招聘爬虫..."
    check_python
    check_dependencies
    check_config
    setup_directories
    
    $PYTHON_CMD crawler.py
}

# 运行测试
run_test() {
    log_info "运行测试脚本..."
    check_python
    check_dependencies
    check_config
    setup_directories
    
    $PYTHON_CMD test_crawler.py
}

# 启动定时任务
run_schedule() {
    log_info "启动定时任务..."
    check_python
    check_dependencies
    check_config
    setup_directories
    
    log_info "定时任务已启动，按Ctrl+C停止"
    $PYTHON_CMD scheduler.py
}

# 查看运行状态
show_status() {
    log_info "检查运行状态..."
    
    # 检查进程
    if pgrep -f "python.*crawler.py" > /dev/null; then
        log_info "爬虫进程正在运行"
        pgrep -f "python.*crawler.py" | while read pid; do
            echo "  PID: $pid"
        done
    else
        log_info "爬虫进程未运行"
    fi
    
    if pgrep -f "python.*scheduler.py" > /dev/null; then
        log_info "定时任务进程正在运行"
        pgrep -f "python.*scheduler.py" | while read pid; do
            echo "  PID: $pid"
        done
    else
        log_info "定时任务进程未运行"
    fi
    
    # 检查日志文件
    if [ -f "logs/crawler.log" ]; then
        log_info "最近的日志记录:"
        tail -5 logs/crawler.log
    else
        log_warn "未找到日志文件"
    fi
}

# 查看日志
show_logs() {
    if [ -f "logs/crawler.log" ]; then
        log_info "显示爬虫日志 (按q退出):"
        less logs/crawler.log
    else
        log_warn "未找到日志文件"
    fi
}

# 主函数
main() {
    case "${1:-help}" in
        "run")
            run_crawler
            ;;
        "test")
            run_test
            ;;
        "schedule")
            run_schedule
            ;;
        "install")
            install_dependencies
            ;;
        "setup")
            setup_environment
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            log_error "未知选项: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"