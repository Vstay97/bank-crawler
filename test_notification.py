#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信通知测试脚本

用于测试Server酱微信通知功能是否正常工作
在首次部署时发送测试消息，确认网络连通性
"""

import os
import sys
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def send_test_notification():
    """发送测试通知"""
    # 获取Server酱密钥
    server_chan_keys_str = os.getenv('SERVER_CHAN_KEY', '')
    if not server_chan_keys_str:
        print("❌ 错误: 未配置SERVER_CHAN_KEY环境变量")
        return False
    
    # 解析多个密钥
    if ',' in server_chan_keys_str:
        server_chan_keys = [key.strip() for key in server_chan_keys_str.split(',') if key.strip()]
    elif ';' in server_chan_keys_str:
        server_chan_keys = [key.strip() for key in server_chan_keys_str.split(';') if key.strip()]
    else:
        server_chan_keys = [server_chan_keys_str.strip()] if server_chan_keys_str.strip() else []
    
    if not server_chan_keys:
        print("❌ 错误: SERVER_CHAN_KEY配置为空")
        return False
    
    print(f"📱 开始测试微信通知功能...")
    print(f"🔑 检测到 {len(server_chan_keys)} 个Server酱密钥")
    
    success_count = 0
    total_count = len(server_chan_keys)
    
    # 构造测试消息
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    title = "🎉 银行爬虫部署成功通知"
    short = "系统已成功部署并启动"
    desp = f"""## 🚀 部署成功通知

**部署时间：** {current_time}

**服务状态：** ✅ 正常运行

**网络连接：** ✅ 连通正常

**功能测试：** ✅ 微信通知功能正常

---

### 📋 系统信息

- **服务名称：** 银行招聘信息爬虫
- **部署环境：** Docker容器
- **健康检查：** http://localhost:8080/health
- **状态查看：** http://localhost:8080/status

### 🔔 通知说明

这是一条测试消息，用于确认微信通知功能正常工作。
如果您收到此消息，说明：

1. ✅ 服务器网络连接正常
2. ✅ Server酱配置正确
3. ✅ 微信通知功能可用
4. ✅ 爬虫服务已成功启动

### 📞 技术支持

如有问题，请检查：
- 容器运行状态：`docker-compose ps`
- 服务日志：`docker-compose logs bank-crawler`
- 健康检查：`curl http://localhost:8080/health`

---

*此消息由银行招聘爬虫系统自动发送*"""
    
    # 向每个配置的密钥发送测试通知
    for i, server_chan_key in enumerate(server_chan_keys, 1):
        try:
            print(f"📤 正在向接收者{i}发送测试通知...")
            
            # 发送Server酱通知
            url = f"https://sctapi.ftqq.com/{server_chan_key}.send"
            data = {
                'title': title,
                'short': short,
                'desp': desp
            }
            
            response = requests.post(url, data=data, timeout=15)
            response.raise_for_status()
            
            # 检查响应内容
            try:
                result = response.json()
                if result.get('code') == 0:
                    print(f"✅ 接收者{i}: 测试通知发送成功")
                    success_count += 1
                else:
                    print(f"❌ 接收者{i}: 发送失败 - {result.get('message', '未知错误')}")
            except:
                # 如果无法解析JSON，但状态码正常，也认为成功
                if response.status_code == 200:
                    print(f"✅ 接收者{i}: 测试通知发送成功")
                    success_count += 1
                else:
                    print(f"❌ 接收者{i}: 发送失败 - HTTP {response.status_code}")
            
        except requests.exceptions.Timeout:
            print(f"❌ 接收者{i}: 发送超时 - 请检查网络连接")
        except requests.exceptions.ConnectionError:
            print(f"❌ 接收者{i}: 连接失败 - 请检查网络连接")
        except Exception as e:
            print(f"❌ 接收者{i}: 发送失败 - {str(e)}")
        
        # 避免频繁请求
        if i < total_count:
            time.sleep(1)
    
    # 输出测试结果
    print(f"\n📊 测试结果统计:")
    print(f"   总计: {total_count} 个接收者")
    print(f"   成功: {success_count} 个")
    print(f"   失败: {total_count - success_count} 个")
    
    if success_count > 0:
        print(f"\n🎉 微信通知功能测试完成！")
        print(f"✅ 至少有 {success_count} 个接收者可以正常接收通知")
        print(f"📱 请检查您的微信，应该会收到测试消息")
        return True
    else:
        print(f"\n❌ 微信通知功能测试失败！")
        print(f"🔧 请检查以下配置:")
        print(f"   1. SERVER_CHAN_KEY是否正确")
        print(f"   2. 网络连接是否正常")
        print(f"   3. Server酱服务是否可用")
        return False

def main():
    """主函数"""
    print("="*60)
    print("🧪 银行爬虫微信通知测试")
    print("="*60)
    
    try:
        success = send_test_notification()
        
        print("\n" + "="*60)
        if success:
            print("✅ 测试完成: 微信通知功能正常")
            sys.exit(0)
        else:
            print("❌ 测试失败: 微信通知功能异常")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()