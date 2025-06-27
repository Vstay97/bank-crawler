#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行招聘爬虫配置检查脚本
用于验证环境配置是否正确
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"   ✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print("   需要Python 3.8或更高版本")
        return False

def check_dependencies():
    """检查依赖包"""
    print("\n📦 检查依赖包...")
    dependencies = {
        'requests': 'HTTP请求库',
        'bs4': 'BeautifulSoup HTML解析库',
        'lxml': 'XML/HTML解析器',
        'schedule': '定时任务库',
        'dotenv': '环境变量管理库'
    }
    
    all_ok = True
    for package, description in dependencies.items():
        try:
            if package == 'bs4':
                import bs4
            else:
                __import__(package)
            print(f"   ✅ {package}: {description}")
        except ImportError:
            print(f"   ❌ {package}: {description} - 未安装")
            all_ok = False
    
    return all_ok

def check_env_file():
    """检查环境配置文件"""
    print("\n⚙️  检查环境配置...")
    
    # 检查.env文件是否存在
    env_file = Path('.env')
    if not env_file.exists():
        print("   ❌ .env文件不存在")
        
        # 检查是否有模板文件
        example_file = Path('.env.example')
        if example_file.exists():
            print("   💡 发现.env.example模板文件")
            print("   请复制.env.example为.env并配置相关参数")
        return False
    
    print("   ✅ .env文件存在")
    
    # 加载环境变量
    load_dotenv()
    
    # 检查关键配置项
    configs = {
        'SERVER_CHAN_KEY': 'Server酱推送密钥',
        'BASE_URL': '基础URL',
        'LIST_URL': '列表页URL',
        'DATA_FILE': '数据文件路径',
        'LOG_FILE': '日志文件路径'
    }
    
    all_configured = True
    for key, description in configs.items():
        value = os.getenv(key)
        if not value or value == f'your_{key.lower()}_here':
            print(f"   ⚠️  {key}: {description} - 未配置或使用默认值")
            if key == 'SERVER_CHAN_KEY':
                all_configured = False
        else:
            # 隐藏敏感信息
            if 'KEY' in key or 'TOKEN' in key:
                display_value = value[:8] + '...' if len(value) > 8 else '***'
            else:
                display_value = value
            print(f"   ✅ {key}: {display_value}")
    
    return all_configured

def check_directories():
    """检查必要目录"""
    print("\n📁 检查目录结构...")
    
    directories = ['data', 'logs']
    all_ok = True
    
    for directory in directories:
        dir_path = Path(directory)
        if dir_path.exists():
            print(f"   ✅ {directory}/ 目录存在")
        else:
            print(f"   ⚠️  {directory}/ 目录不存在，将自动创建")
            try:
                dir_path.mkdir(exist_ok=True)
                print(f"   ✅ {directory}/ 目录创建成功")
            except Exception as e:
                print(f"   ❌ {directory}/ 目录创建失败: {e}")
                all_ok = False
    
    return all_ok

def check_network():
    """检查网络连接"""
    print("\n🌐 检查网络连接...")
    
    # 检查基本网络连接
    try:
        response = requests.get('https://httpbin.org/get', timeout=10)
        if response.status_code == 200:
            print("   ✅ 网络连接正常")
        else:
            print(f"   ⚠️  网络连接异常，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 网络连接失败: {e}")
        return False
    
    # 检查目标网站连接
    load_dotenv()
    base_url = os.getenv('BASE_URL', 'http://www.yinhangzhaopin.com')
    
    try:
        response = requests.get(base_url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        if response.status_code == 200:
            print(f"   ✅ 目标网站连接正常: {base_url}")
        else:
            print(f"   ⚠️  目标网站连接异常，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 目标网站连接失败: {e}")
        return False
    
    return True

def check_server_chan():
    """检查Server酱配置"""
    print("\n📱 检查Server酱配置...")
    
    load_dotenv()
    server_chan_key = os.getenv('SERVER_CHAN_KEY')
    
    if not server_chan_key or server_chan_key == 'your_server_chan_key_here':
        print("   ⚠️  Server酱密钥未配置")
        print("   请访问 https://sct.ftqq.com/ 获取密钥")
        return False
    
    # 测试Server酱连接（不发送实际消息）
    test_url = f'https://sctapi.ftqq.com/{server_chan_key}.send'
    
    try:
        # 只测试URL格式，不发送实际请求
        if len(server_chan_key) > 10 and server_chan_key.startswith('SCT'):
            print("   ✅ Server酱密钥格式正确")
            print("   💡 建议运行测试脚本验证推送功能")
            return True
        else:
            print("   ⚠️  Server酱密钥格式可能不正确")
            return False
    except Exception as e:
        print(f"   ❌ Server酱配置检查失败: {e}")
        return False

def main():
    """主函数"""
    print("🔍 银行招聘爬虫配置检查")
    print("=" * 50)
    
    checks = [
        check_python_version,
        check_dependencies,
        check_env_file,
        check_directories,
        check_network,
        check_server_chan
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"   ❌ 检查过程中出现错误: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 检查结果汇总:")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"   🎉 所有检查通过 ({passed}/{total})")
        print("   ✅ 环境配置完成，可以运行爬虫")
        print("\n💡 建议执行以下命令测试:")
        print("   python test_crawler.py")
        print("   ./run.sh test")
    else:
        print(f"   ⚠️  部分检查未通过 ({passed}/{total})")
        print("   请根据上述提示修复配置问题")
        
        if not results[1]:  # 依赖包检查失败
            print("\n💡 安装依赖包:")
            print("   pip install -r requirements.txt")
            print("   或者: ./run.sh install")
        
        if not results[2]:  # 环境配置检查失败
            print("\n💡 配置环境变量:")
            print("   cp .env.example .env")
            print("   编辑 .env 文件，配置相关参数")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)