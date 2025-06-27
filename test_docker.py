#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Docker 部署的脚本
用于验证容器是否正常运行
"""

import requests
import time
import sys

def test_health_check():
    """测试健康检查端点"""
    try:
        response = requests.get('http://localhost:8080/health', timeout=5)
        if response.status_code == 200:
            print("✅ 健康检查通过")
            return True
        else:
            print(f"❌ 健康检查失败: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到健康检查端点: {e}")
        return False

def test_status_endpoint():
    """测试状态端点"""
    try:
        response = requests.get('http://localhost:8080/status', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ 状态端点正常")
            print(f"   - 服务状态: {data.get('status', 'unknown')}")
            print(f"   - 启动时间: {data.get('start_time', 'unknown')}")
            print(f"   - 数据文件: {data.get('data_file_exists', 'unknown')}")
            print(f"   - 日志文件: {data.get('log_file_exists', 'unknown')}")
            return True
        else:
            print(f"❌ 状态端点失败: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到状态端点: {e}")
        return False
    except ValueError as e:
        print(f"❌ 状态端点返回无效JSON: {e}")
        return False

def main():
    """主测试函数"""
    print("🐳 开始测试 Docker 部署...")
    print()
    
    # 等待容器启动
    print("⏳ 等待容器启动...")
    time.sleep(3)
    
    # 测试健康检查
    print("🔍 测试健康检查端点...")
    health_ok = test_health_check()
    print()
    
    # 测试状态端点
    print("📊 测试状态端点...")
    status_ok = test_status_endpoint()
    print()
    
    # 总结
    if health_ok and status_ok:
        print("🎉 Docker 部署测试通过！")
        print("💡 提示: 您可以通过以下命令查看日志:")
        print("   ./deploy.sh logs")
        sys.exit(0)
    else:
        print("❌ Docker 部署测试失败")
        print("💡 请检查:")
        print("   1. 容器是否正在运行: docker ps")
        print("   2. 查看容器日志: ./deploy.sh logs")
        print("   3. 检查端口是否被占用: lsof -i :8080")
        sys.exit(1)

if __name__ == '__main__':
    main()