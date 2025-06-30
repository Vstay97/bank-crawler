#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行招聘信息爬虫

功能：
1. 爬取银行招聘列表页面
2. 提取每个职位的详细信息
3. 检测新增职位并推送通知
4. 支持定时任务运行
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class BankJobCrawler:
    """银行招聘信息爬虫类"""
    
    def __init__(self):
        self.base_url = os.getenv('BASE_URL', 'http://www.yinhangzhaopin.com')
        self.list_url = os.getenv('LIST_URL', 'http://www.yinhangzhaopin.com/tag/shehuizhaopin_13698_1.html')
        self.data_file = os.getenv('DATA_FILE', 'data/jobs_history.json')
        self.backup_file = os.getenv('BACKUP_FILE', 'data/jobs_backup.txt')
        self.log_file = os.getenv('LOG_FILE', 'logs/crawler.log')
        # 支持多个Server酱密钥
        server_chan_keys_str = os.getenv('SERVER_CHAN_KEY', '')
        if server_chan_keys_str:
            # 支持逗号或分号分隔的多个密钥
            if ',' in server_chan_keys_str:
                self.server_chan_keys = [key.strip() for key in server_chan_keys_str.split(',') if key.strip()]
            elif ';' in server_chan_keys_str:
                self.server_chan_keys = [key.strip() for key in server_chan_keys_str.split(';') if key.strip()]
            else:
                # 单个密钥
                self.server_chan_keys = [server_chan_keys_str.strip()] if server_chan_keys_str.strip() else []
        else:
            self.server_chan_keys = []
        
        # 请求配置
        self.request_delay = float(os.getenv('REQUEST_DELAY', '1'))
        self.timeout = int(os.getenv('TIMEOUT', '30'))
        self.retry_times = int(os.getenv('RETRY_TIMES', '3'))
        
        # 设置请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # 初始化日志
        self._setup_logging()
        
        # 创建必要的目录
        self._create_directories()
        
        # 加载历史数据
        self.jobs_history = self._load_history()
    
    def _setup_logging(self):
        """设置日志配置"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _create_directories(self):
        """创建必要的目录"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def _load_history(self) -> Dict:
        """加载历史数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"加载历史数据失败: {e}")
                return {}
        return {}
    
    def _save_history(self):
        """保存历史数据"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.jobs_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"保存历史数据失败: {e}")
    
    def _save_jobs_backup(self, new_jobs: List[Dict]):
        """保存新职位到备份文件（新内容在顶部）"""
        if not new_jobs:
            return
        
        try:
            # 读取现有内容
            existing_content = ""
            if os.path.exists(self.backup_file):
                with open(self.backup_file, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
            
            # 格式化新职位信息
            new_content_lines = []
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            new_content_lines.append(f"=== 更新时间: {current_time} ===")
            new_content_lines.append(f"新增职位数量: {len(new_jobs)}")
            new_content_lines.append("")
            
            for i, job in enumerate(new_jobs, 1):
                new_content_lines.append(f"【职位 {i}】")
                new_content_lines.append(f"标题: {job.get('title', '未知')}")
                new_content_lines.append(f"公司: {job.get('company', '未知')}")
                new_content_lines.append(f"地点: {job.get('location', '未知')}")
                new_content_lines.append(f"链接: {job.get('url', '未知')}")
                new_content_lines.append("")
                
                # 添加职位详情
                details = job.get('details', '暂无详情')
                if details and details != '暂无详情':
                    new_content_lines.append("职位详情:")
                    new_content_lines.append("-" * 50)
                    new_content_lines.append(details)
                    new_content_lines.append("-" * 50)
                else:
                    new_content_lines.append("职位详情: 暂无详情")
                
                new_content_lines.append("")
                new_content_lines.append("=" * 80)
                new_content_lines.append("")
            
            # 将新内容写入文件顶部
            new_content = "\n".join(new_content_lines)
            
            # 如果有现有内容，在新内容后添加分隔符和现有内容
            if existing_content.strip():
                final_content = new_content + "\n" + existing_content
            else:
                final_content = new_content
            
            # 写入文件
            with open(self.backup_file, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            self.logger.info(f"备份文件已更新: {self.backup_file}，新增 {len(new_jobs)} 个职位")
            
        except Exception as e:
            self.logger.error(f"保存备份文件失败: {e}")
    
    def _make_request(self, url: str, encoding: str = 'gbk') -> Optional[BeautifulSoup]:
        """发送HTTP请求并返回BeautifulSoup对象"""
        for attempt in range(self.retry_times):
            try:
                self.logger.info(f"请求URL: {url} (尝试 {attempt + 1}/{self.retry_times})")
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                response.encoding = encoding
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'lxml')
                time.sleep(self.request_delay)  # 请求间隔
                return soup
                
            except Exception as e:
                self.logger.warning(f"请求失败 (尝试 {attempt + 1}/{self.retry_times}): {e}")
                if attempt < self.retry_times - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                else:
                    self.logger.error(f"请求最终失败: {url}")
        
        return None
    
    def extract_job_list(self) -> List[Dict]:
        """提取招聘列表信息"""
        soup = self._make_request(self.list_url)
        if not soup:
            return []
        
        jobs = []
        
        # 根据HTML结构提取职位信息
        # 从示例HTML可以看出，职位链接在 <dt><a href="..." title="...">...</a></dt> 结构中
        job_links = soup.find_all('dt')
        
        for dt in job_links:
            link = dt.find('a')
            if not link or not link.get('href'):
                continue
            
            href = link.get('href')
            title = link.get('title', '').strip()
            
            # 跳过非职位链接
            if not href.endswith('.htm') or not title:
                continue
            
            # 构造完整URL
            full_url = urljoin(self.base_url, href)
            
            # 解析基本信息
            job_info = self._parse_job_basic_info(title, full_url)
            if job_info:
                jobs.append(job_info)
        
        self.logger.info(f"提取到 {len(jobs)} 个职位信息")
        return jobs
    
    def _parse_job_basic_info(self, title: str, url: str) -> Optional[Dict]:
        """解析职位基本信息"""
        try:
            # 解析标题格式: [地区]年份+银行名称+招聘公告(日期)
            # 例如: [湖北]2025年湖北银行总行部室社会招聘公告（6.27）
            
            parts = title.split(']', 1)
            if len(parts) != 2:
                return None
            
            location = parts[0].replace('[', '').strip()
            remaining = parts[1].strip()
            
            # 提取日期（如果有）
            date_info = ''
            if '（' in remaining and '）' in remaining:
                date_start = remaining.rfind('（')
                date_end = remaining.rfind('）')
                if date_start < date_end:
                    date_info = remaining[date_start+1:date_end]
                    remaining = remaining[:date_start].strip()
            
            # 生成唯一ID
            job_id = self._generate_job_id(url)
            
            return {
                'id': job_id,
                'title': title,
                'location': location,
                'company': self._extract_company_name(remaining),
                'url': url,
                'date_info': date_info,
                'crawl_time': datetime.now().isoformat(),
                'details': None  # 详情将在后续获取
            }
        
        except Exception as e:
            self.logger.warning(f"解析职位基本信息失败: {title}, 错误: {e}")
            return None
    
    def _extract_company_name(self, text: str) -> str:
        """从标题中提取公司名称"""
        # 简单的公司名称提取逻辑，可以根据实际情况优化
        if '银行' in text:
            # 查找包含"银行"的部分
            words = text.split()
            for word in words:
                if '银行' in word:
                    return word
        return text.split()[0] if text.split() else '未知'
    
    def _generate_job_id(self, url: str) -> str:
        """根据URL生成唯一的职位ID"""
        # 从URL中提取文件名作为ID
        parsed = urlparse(url)
        path_parts = parsed.path.split('/')
        if path_parts:
            filename = path_parts[-1]
            return filename.replace('.htm', '').replace('.html', '')
        return str(hash(url))
    
    def get_job_details(self, job: Dict) -> Dict:
        """获取职位详细信息"""
        soup = self._make_request(job['url'])
        if not soup:
            return job
        
        try:
            # 提取职位详情内容
            # 根据实际HTML结构，详情在class为'newstxt'的div中
            content_div = soup.find('div', class_='newstxt')
            
            if not content_div:
                # 尝试其他可能的选择器
                content_div = soup.find('div', class_='content') or soup.find('div', {'id': 'content'})
                if not content_div:
                    content_div = soup.find('div', class_='article-content') or soup.find('div', class_='job-content')
            
            if content_div:
                # 移除广告和无关内容
                # 移除script标签
                for script in content_div.find_all('script'):
                    script.decompose()
                
                # 移除广告相关的div
                for ad_div in content_div.find_all('div', class_=['yindao', 'zhezhao']):
                    ad_div.decompose()
                
                # 移除分享相关内容
                for share_div in content_div.find_all('div', {'id': 'ckepop'}):
                    share_div.decompose()
                
                # 移除免责声明等
                for disclaimer in content_div.find_all('div', style=lambda x: x and 'color:#666' in x):
                    disclaimer.decompose()
                
                # 清理HTML标签，提取纯文本
                details = content_div.get_text(separator='\n', strip=True)
                
                # 进一步清理文本
                lines = details.split('\n')
                cleaned_lines = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('分享到:') and not line.startswith('联系我们时'):
                        cleaned_lines.append(line)
                
                job['details'] = '\n'.join(cleaned_lines)
            else:
                job['details'] = '无法获取详细信息'
            
            self.logger.info(f"获取职位详情成功: {job['title']}")
            
        except Exception as e:
            self.logger.error(f"获取职位详情失败: {job['title']}, 错误: {e}")
            job['details'] = f'获取详情时出错: {e}'
        
        return job
    
    def check_new_jobs(self, current_jobs: List[Dict]) -> List[Dict]:
        """检查新增的职位"""
        new_jobs = []
        
        for job in current_jobs:
            job_id = job['id']
            if job_id not in self.jobs_history:
                new_jobs.append(job)
                self.jobs_history[job_id] = job
        
        if new_jobs:
            self.logger.info(f"发现 {len(new_jobs)} 个新职位")
        else:
            self.logger.info("没有发现新职位")
        
        return new_jobs
    
    def _format_job_details_markdown(self, job: Dict) -> str:
        """将职位详情格式化为markdown"""
        details = job.get('details', '暂无详细信息')
        
        # 基本信息
        markdown_content = []
        markdown_content.append(f"## 📋 {job.get('title', '未知职位')}")
        markdown_content.append("")
        markdown_content.append(f"**🏢 招聘单位：** {job.get('company', '未知单位')}")
        markdown_content.append(f"**📍 工作地点：** {job.get('location', '未知地区')}")
        markdown_content.append(f"**📅 发布日期：** {job.get('date', '未知日期')}")
        markdown_content.append("")
        
        # 详细信息
        if details and details != '暂无详细信息':
            markdown_content.append("## 📝 职位详情")
            markdown_content.append("")
            
            # 清理和格式化详情内容
            cleaned_details = details.strip()
            
            # 按段落分割
            paragraphs = [p.strip() for p in cleaned_details.split('\n') if p.strip()]
            
            for paragraph in paragraphs:
                # 检查是否是标题行（通常包含特定关键词）
                if any(keyword in paragraph for keyword in ['招聘', '岗位', '条件', '要求', '职责', '待遇', '福利', '联系']):
                    markdown_content.append(f"### {paragraph}")
                else:
                    markdown_content.append(paragraph)
                markdown_content.append("")
        
        # 添加链接
        if job.get('url'):
            markdown_content.append("---")
            markdown_content.append(f"🔗 [查看详情]({job['url']})")
        
        return "\n".join(markdown_content)
    
    def send_notification(self, new_jobs: List[Dict]):
        """发送新职位通知"""
        if not new_jobs or not self.server_chan_keys:
            if not self.server_chan_keys:
                self.logger.warning("未配置Server酱密钥，跳过通知发送")
            return
        
        self.logger.info(f"准备向 {len(self.server_chan_keys)} 个接收者发送通知")
        
        try:
            # 为每个新职位发送单独的通知
            for job in new_jobs:
                # 构造通知内容
                title = job.get('title', '未知职位')      # title: 对应爬取到的title
                short = job.get('location', '未知地区')  # short: 对应爬取到的location
                desp = self._format_job_details_markdown(job)  # desp: 格式化的岗位详情
                
                # 向每个配置的密钥发送通知
                for i, server_chan_key in enumerate(self.server_chan_keys, 1):
                    try:
                        # 发送Server酱通知
                        url = f"https://sctapi.ftqq.com/{server_chan_key}.send"
                        data = {
                            'title': title,
                            'short': short,
                            'desp': desp
                        }
                        
                        response = requests.post(url, data=data, timeout=10)
                        response.raise_for_status()
                        
                        self.logger.info(f"通知发送成功 (接收者{i}): {title} - {short}")
                        
                    except Exception as e:
                        self.logger.error(f"向接收者{i}发送通知失败: {title} - {e}")
                    
                    # 避免频繁请求，添加延迟
                    time.sleep(0.5)
                
                # 每个职位发送完成后稍作延迟
                time.sleep(1)
            
        except Exception as e:
            self.logger.error(f"发送通知过程中出现错误: {e}")
    
    def _format_notification_content(self, jobs: List[Dict]) -> str:
        """格式化通知内容"""
        content_lines = []
        
        for job in jobs[:10]:  # 最多显示10个职位
            lines = [
                f"**{job['title']}**",
                f"- 单位: {job['company']}",
                f"- 地点: {job['location']}",
                f"- 链接: {job['url']}",
                ""
            ]
            content_lines.extend(lines)
        
        if len(jobs) > 10:
            content_lines.append(f"... 还有 {len(jobs) - 10} 个职位")
        
        return "\n".join(content_lines)
    
    def run(self):
        """运行爬虫"""
        self.logger.info("开始运行银行招聘爬虫")
        
        try:
            # 1. 获取职位列表
            jobs = self.extract_job_list()
            if not jobs:
                self.logger.warning("未获取到任何职位信息")
                return
            
            # 2. 检查新职位
            new_jobs = self.check_new_jobs(jobs)
            
            # 3. 获取新职位的详细信息
            for job in new_jobs:
                self.get_job_details(job)
                self.jobs_history[job['id']] = job  # 更新历史记录
            
            # 4. 保存历史数据
            self._save_history()
            
            # 5. 保存新职位到备份文件
            if new_jobs:
                self._save_jobs_backup(new_jobs)
            
            # 6. 发送通知
            if new_jobs:
                self.send_notification(new_jobs)
            
            self.logger.info(f"爬虫运行完成，处理了 {len(jobs)} 个职位，新增 {len(new_jobs)} 个")
            
        except Exception as e:
            self.logger.error(f"爬虫运行出错: {e}")
            raise

def main():
    """主函数"""
    crawler = BankJobCrawler()
    crawler.run()

if __name__ == '__main__':
    main()