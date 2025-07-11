

'''
    在Python中, 通过随机IP实现反反爬的核心是使用代理IP池技术.
    这种方法通过轮换不同IP地址发送请求, 有效避免被目标网站基于IP的访问频率限制封禁.

对爬虫中的代理IP技术的概念解释:
    代理IP技术的意思是,使用代理服务器向要爬取的url发送对应的请求,
    然后再把爬取到的数据转发到自己的真实的IP
    这样即使IP地址被对应的网站封掉了,也不会影响自己的电脑的IP的访问

实现原理
    获取代理IP:    从免费/付费代理网站抓取IP或使用代理服务API
    IP验证:       筛选出可用的代理IP
    随机选择IP:    每次请求随机选择已验证的代理
    异常处理:      自动切换失效代理
'''

import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent

# 免费代理源（实际使用建议替换为付费代理）
PROXY_SOURCES = [
    "https://www.sslproxies.org/",
    "https://free-proxy-list.net/"
]

class ProxyScraper:
    def __init__(self, max_workers=10):
        self.valid_proxies = []
        self.ua = UserAgent()
        self.max_workers = max_workers

    def scrape_proxies(self):
        """从代理网站抓取代理IP"""
        proxies = []
        for url in PROXY_SOURCES:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    # 简单解析IP:PORT格式（实际需要根据网站结构调整）
                    for line in response.text.split('\n'):
                        if '<tr><td>' in line:
                            parts = line.split('</td><td>')
                            if len(parts) > 1:
                                ip = parts[0].replace('<tr><td>', '')
                                port = parts[1].split('<')[0]
                                proxies.append(f"{ip}:{port}")
                print(f"从 {url} 获取 {len(proxies)} 个代理")
            except:
                continue
        return list(set(proxies))  # 去重

    def validate_proxy(self, proxy):
        """验证代理是否可用"""
        try:
            test_url = "https://httpbin.org/ip"
            headers = {'User-Agent': self.ua.random}
            response = requests.get(test_url, proxies={
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"  # 多数免费代理只支持HTTP
            }, timeout=8, headers=headers)

            if response.status_code == 200:
                print(f"√ 有效代理: {proxy} | 响应IP: {response.json()['origin']}")
                return proxy
        except Exception as e:
            return None
        return None

    def validate_proxies(self, proxies):
        """多线程验证代理池"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(self.validate_proxy, proxies)

        self.valid_proxies = [p for p in results if p is not None]
        print(f"验证完成! 有效代理数量: {len(self.valid_proxies)}")
        return self.valid_proxies

    def get_random_proxy(self):
        """获取随机代理"""
        return random.choice(self.valid_proxies) if self.valid_proxies else None

    def make_request(self, url, retry=3):
        """使用随机代理发送请求"""
        headers = {'User-Agent': self.ua.random}
        for _ in range(retry):
            proxy = self.get_random_proxy()
            if not proxy:
                print("⚠ 无可用代理! 重新获取...")
                self.refresh_proxies()
                continue

            try:
                print(f"使用代理: {proxy} 访问 {url}")
                response = requests.get(url, proxies={
                    "http": f"http://{proxy}",
                    "https": f"http://{proxy}"
                }, timeout=15, headers=headers)

                if response.status_code == 200:
                    return response
                else:
                    print(f"× 状态码 {response.status_code} 移除代理: {proxy}")
                    self.valid_proxies.remove(proxy)
            except Exception as e:
                print(f"× 代理 {proxy} 失败: {str(e)}")
                if proxy in self.valid_proxies:
                    self.valid_proxies.remove(proxy)

        print(f"请求失败: {url}")
        return None

    def refresh_proxies(self):
        """刷新代理池"""
        print("刷新代理池...")
        raw_proxies = self.scrape_proxies()
        self.validate_proxies(raw_proxies)



# ================== 使用示例 ==========================
if __name__ == "__main__":
    # 初始化代理池
    scraper = ProxyScraper()
    scraper.refresh_proxies()

    # 测试请求
    target_url = "https://httpbin.org/headers"
    response = scraper.make_request(target_url)

    if response:
        print("\n=== 请求成功 ===")
        print(f"状态码: {response.status_code}")
        print(f"返回内容:\n{response.text[:500]}...")

    # 持续使用示例
    print("\n持续请求演示（5次随机请求）:")
    for i in range(1, 6):
        print(f"\n请求 #{i}")
        scraper.make_request(f"https://httpbin.org/get?req={i}")
        time.sleep(random.uniform(1, 3))  # 随机延迟

        # 当代理少于5个时刷新
        if len(scraper.valid_proxies) < 5:
            scraper.refresh_proxies()
