#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康检查服务

为Docker容器提供简单的健康检查端点
"""

import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import json
import os

class HealthCheckHandler(BaseHTTPRequestHandler):
    """健康检查请求处理器"""
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/health':
            self.send_health_response()
        elif self.path == '/status':
            self.send_status_response()
        else:
            self.send_response(404)
            self.end_headers()
    
    def send_health_response(self):
        """发送健康检查响应"""
        try:
            # 检查关键文件是否存在
            crawler_exists = os.path.exists('/app/crawler.py')
            scheduler_exists = os.path.exists('/app/scheduler.py')
            
            if crawler_exists and scheduler_exists:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'status': 'healthy',
                    'timestamp': datetime.now().isoformat(),
                    'service': 'bank-crawler'
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(500)
                self.end_headers()
        except Exception as e:
            self.send_response(500)
            self.end_headers()
    
    def send_status_response(self):
        """发送状态信息响应"""
        try:
            # 获取数据文件信息
            data_file = '/app/data/jobs_history.json'
            log_file = '/app/logs/crawler.log'
            
            status_info = {
                'service': 'bank-crawler',
                'timestamp': datetime.now().isoformat(),
                'uptime': time.time(),
                'files': {
                    'data_exists': os.path.exists(data_file),
                    'log_exists': os.path.exists(log_file)
                }
            }
            
            if os.path.exists(data_file):
                status_info['files']['data_size'] = os.path.getsize(data_file)
                status_info['files']['data_modified'] = datetime.fromtimestamp(
                    os.path.getmtime(data_file)
                ).isoformat()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(status_info, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def log_message(self, format, *args):
        """禁用默认日志输出"""
        pass

def start_health_server():
    """启动健康检查服务器"""
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    print(f"健康检查服务启动在端口 8080")
    print(f"健康检查端点: http://localhost:8080/health")
    print(f"状态信息端点: http://localhost:8080/status")
    server.serve_forever()

if __name__ == '__main__':
    start_health_server()