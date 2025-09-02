#!/bin/bash

# 银行招聘爬虫 Docker 部署脚本
# 用于快速部署和管理 Docker 容器

set -e

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

# 检查 Docker 环境
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
    
    log_info "Docker 环境检查通过"
}

# 检查环境变量配置
check_env() {
    if [ ! -f ".env" ]; then
        log_warn ".env 文件不存在，正在创建..."
        cp .env.example .env
        log_warn "请编辑 .env 文件，设置您的 SERVER_CHAN_KEY"
        log_warn "编辑完成后请重新运行此脚本"
        exit 1
    fi
    
    # 检查关键配置
    if grep -q "your_server_chan_key_here" .env; then
        log_error "请在 .env 文件中设置正确的 SERVER_CHAN_KEY"
        exit 1
    fi
    
    log_info "环境变量配置检查通过"
}

# 创建必要目录
create_dirs() {
    mkdir -p data logs
    log_info "创建数据目录完成"
}

# 构建镜像
build_image() {
    log_info "开始构建 Docker 镜像..."
    docker-compose build
    log_info "Docker 镜像构建完成"
}

# 启动服务
start_service() {
    log_info "启动银行招聘爬虫服务..."
    docker-compose up -d
    log_info "服务启动完成"
}

# 检查服务状态
check_status() {
    log_info "检查服务状态..."
    docker-compose ps
    
    # 等待服务启动
    sleep 5
    
    # 健康检查
    if curl -s http://localhost:8080/health > /dev/null; then
        log_info "健康检查通过 ✓"
    else
        log_warn "健康检查失败，请查看日志"
    fi
}

# 显示日志
show_logs() {
    log_info "显示服务日志（按 Ctrl+C 退出）..."
    docker-compose logs -f bank-crawler
}

# 停止服务
stop_service() {
    log_info "停止银行招聘爬虫服务..."
    docker-compose stop
    log_info "服务已停止"
}

# 重启服务
restart_service() {
    log_info "重启银行招聘爬虫服务..."
    docker-compose restart
    log_info "服务重启完成"
}

# 清理服务
clean_service() {
    log_info "清理银行招聘爬虫服务..."
    docker-compose down
    docker-compose down --volumes
    log_info "服务清理完成"
}

# 显示状态信息
show_status() {
    echo "==========================================="
    echo "银行招聘爬虫 Docker 服务状态"
    echo "==========================================="
    
    # 容器状态
    echo "\n📦 容器状态:"
    docker-compose ps
    
    # 健康检查
    echo "\n🏥 健康检查:"
    if curl -s http://localhost:8080/health > /dev/null; then
        echo "✓ 服务健康"
        curl -s http://localhost:8080/status | python3 -m json.tool
    else
        echo "✗ 服务异常"
    fi
    
    # 数据目录
    echo "\n📁 数据目录:"
    ls -la data/ 2>/dev/null || echo "数据目录为空"
    
    # 最近日志
    echo "\n📋 最近日志:"
    docker-compose logs --tail=10 bank-crawler
}

# 显示帮助信息
show_help() {
    echo "银行招聘爬虫 Docker 部署脚本"
    echo ""
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  deploy           - 完整部署（检查环境、构建、启动）"
    echo "  start            - 启动服务"
    echo "  stop             - 停止服务"
    echo "  restart          - 重启服务"
    echo "  status           - 显示服务状态"
    echo "  logs             - 显示服务日志"
    echo "  clean            - 清理服务和数据"
    echo "  build            - 重新构建镜像"
    echo "  test-notification - 测试微信通知功能"
    echo "  help             - 显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 deploy            # 首次部署"
    echo "  $0 status            # 查看状态"
    echo "  $0 logs              # 查看日志"
    echo "  $0 test-notification # 测试微信通知"
}

# 主函数
main() {
    case "${1:-help}" in
        deploy)
            check_docker
            check_env
            create_dirs
            build_image
            start_service
            check_status
            
            # 发送部署成功的微信通知
            log_info "正在发送部署成功通知..."
            if docker-compose exec -T bank-crawler python test_notification.py; then
                log_info "✅ 微信通知测试成功！请检查您的微信"
            else
                log_warn "⚠️  微信通知测试失败，但服务已正常启动"
                log_warn "请检查 SERVER_CHAN_KEY 配置或网络连接"
            fi
            
            log_info "部署完成！访问 http://localhost:8080/status 查看状态"
            ;;
        start)
            check_docker
            start_service
            check_status
            ;;
        stop)
            stop_service
            ;;
        restart)
            restart_service
            check_status
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs
            ;;
        clean)
            clean_service
            ;;
        build)
            check_docker
            build_image
            ;;
        test-notification)
            check_docker
            log_info "测试微信通知功能..."
            if docker-compose exec -T bank-crawler python test_notification.py; then
                log_info "✅ 微信通知测试成功！"
            else
                log_error "❌ 微信通知测试失败！"
                exit 1
            fi
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "未知命令: $1"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"