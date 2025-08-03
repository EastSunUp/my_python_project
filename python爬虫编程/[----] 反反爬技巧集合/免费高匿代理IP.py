import requests
from lxml import etree
import user_agent  # 安装: pip install user_agent
import time
import random

# TODO 这份代码没法获得免费的代理IP,还需要改进,请补充后续代码
# 免费高匿代理爬取与验证 (以西刺代理为例)
def crawl_xici_proxies():
    print("开始爬取代理IP !")
    proxies = []
    for page in range(1, 6):  # 爬取前5页
        url = f"https://www.xicidaili.com/nn/{page}"
        headers = {"User-Agent": user_agent.generate_user_agent(),
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                   "Connection": "keep-alive",
                   "Upgrade-Insecure-Requests": "1",
                   "Referer": "https://www.xicidaili.com/nn/" if page > 1 else ""
                   }
        try:
            # 添加随机延迟防止封IP
            time.sleep(random.uniform(1.5, 3.5))
            res = requests.get(url, headers=headers, timeout=10)
            res.encoding = 'utf-8'  # 确保正确编码
            if res.status_code != 200:
                print(f"页面 {page} 请求失败, 状态码: {res.status_code}")
                continue
            # 这里是把txt文本中的内容的格式变成HTML的树状结构
            html = etree.HTML(res.text)
            print(f"成功获取页面 {page} 的HTML")

            # 提取高匿代理行（td[5]为匿名类型）
            # rows = html.xpath("//table[@id='ip_list']/tr[position()>1][td[5]='高匿']")
            # 更新XPath表达式 - 匹配所有tr标签，跳过表头
            rows = html.xpath("//table[@id='ip_list']/tr[position()>1]")
            if not rows:
                print(f"页面 {page} 未找到代理行,尝试备用选择器...")
                # 备用选择器
                rows = html.xpath("//table/tr[position()>1]")

            print(f"找到 {len(rows)} 个代理行")

            for row in rows:
                # 获取匿名类型
                anonymity = row.xpath("./td[5]/text()")[0].strip()
                if anonymity != "高匿":
                    continue
                ip = row.xpath("./td[2]/text()")[0]
                port = row.xpath("./td[3]/text()")[0]
                proxy = f"{ip}:{port}"
                print(f"找到高匿代理: {proxy}")

                # 匿名性验证 (关键步骤)
                if verify_anonymity(proxy):
                    print(f"代理 {proxy} 验证成功!")
                    proxies.append({
                        "http": f"http://{proxy}",
                        "https": f"https://{proxy}"
                    })
                else:
                    print(f"代理 {proxy} 验证失败!")
        except Exception as e:
            print(f"Page {page} error: {str(e)}")
    print(f"爬取完成,共找到 {len(proxies)} 个有效代理")
    return proxies

def verify_anonymity(proxy):
    """ 通过httpbin检测是否暴露真实IP """
    test_urls = [
        "http://httpbin.org/get?show_env=1",
        "http://httpbin.org/ip"
    ]
    for test_url in test_urls:
        try:
            res = requests.get(
                test_url,
                proxies={"http": f"http://{proxy}","https": f"https://{proxy}"},
                timeout=8
            )
            if res.status_code != 200:
                return False
            data = res.json()
            headers = data.get("headers", {})
            # 检查是否暴露真实IP
            if ("X-Forwarded-For" in headers or
                    "Via" in headers or
                    "Proxy-Connection" in headers):
                return False
            # 检查返回的IP是否是代理IP
            if "origin" in data:
                origins = data["origin"].split(", ")
                if len(origins) > 1:  # 如果有多个IP，说明不是高匿
                    return False
        except Exception as e:
            print(f"验证代理 {proxy} 时出错: {str(e)}")
            return False
    return True

# 运行爬虫
if __name__ == "__main__":
    valid_proxies = crawl_xici_proxies()
    print("\n有效代理列表:")
    for proxy in valid_proxies:
        print(proxy)
