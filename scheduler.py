#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务调度器

用于定期运行银行招聘爬虫
可以通过crontab或直接运行此脚本来实现定时任务
"""

import schedule
import time
import logging
import threading
from datetime import datetime
from crawler import BankJobCrawler
from health_check import start_health_server

def run_crawler():
    """运行爬虫任务"""
    try:
        print(f"\n{'='*50}")
        print(f"开始执行定时任务: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}")
        
        crawler = BankJobCrawler()
        crawler.run()
        
        print(f"\n{'='*50}")
        print(f"定时任务执行完成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")
        
    except Exception as e:
        logging.error(f"定时任务执行失败: {e}")
        print(f"任务执行失败: {e}")

def main():
    """主函数 - 设置定时任务"""
    print("银行招聘爬虫定时任务启动")
    print("任务计划: 每天上午9点执行")
    
    # 启动健康检查服务器（后台线程）
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    # 设置定时任务 - 每天上午9点执行
    schedule.every().day.at("09:00").do(run_crawler)
    
    # 也可以设置其他时间，例如:
    # schedule.every().day.at("18:00").do(run_crawler)  # 每天下午6点
    # schedule.every().hour.do(run_crawler)  # 每小时执行
    # schedule.every(30).minutes.do(run_crawler)  # 每30分钟执行
    
    print("定时任务已设置，等待执行...")
    print("健康检查服务已启动在端口 8080")
    print("按 Ctrl+C 停止程序")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        print("\n程序已停止")

if __name__ == '__main__':
    main()