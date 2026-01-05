
# 使用以下指令安装request库:
# pip install requests
# 除了request之外,还有哪些的库也能实现类似的功能?

import requests
import json

# response.headers  # 响应头信息
# requests.get()    # 发送get请求
# requests.post()   # 发送post请求
# response.text     # 响应内容(文本格式)
# response.json()   # 响应内容(解析为JSON)
# response.content  # 响应内容(二进制格式)
# requests.Session() #
# response.status_code          # HTTP状态码 (200/404等)
# requests.exceptions.Timeout   # 超时异常,用于判断会话是否超时
'''
    requests.post(
        url,        # 目标URL
        data=None,  # 发送表单数据（application/x-www-form-urlencoded）
        json=None,  # 发送JSON数据（自动设置Content-Type: application/json）
        **kwargs
    )
    
    # 其他关键参数 (**kwargs):
    参数名	        类型	            作用
    params	        dict	        URL查询参数（拼接到URL后）
    headers	        dict	        自定义请求头
    cookies	        dict/CookieJar	设置请求Cookies
    files	        dict	        上传文件（multipart/form-data）
    auth	        tuple	        HTTP基础认证,如('user', 'pass')
    timeout	        float	        请求超时时间（秒）
    allow_redirects	bool	        是否允许重定向（默认True）
    proxies	        dict	        设置代理，如{'http': 'http://10.10.1.10:3128'}
    verify	        bool/str	    SSL证书验证（默认True），或CA证书路径
    stream	        bool	        是否流式下载（默认False，立即下载全部内容）
    cert	        str/tuple	    客户端SSL证书路径或(cert, key)元组
'''
'''
    requests.get(
        url, 
        params=None, 
        **kwargs
    )
    # 核心参数说明：
    # 参数名	        类型	    作用	                        示例
    # url	        str	    必需,目标URL	                "https://example.com/search"
    # params	    dict	URL查询参数（自动编码到URL）	params={"q": "爬虫", "page": 2}
    #
    # 其他关键参数 (**kwargs):
    # 与post()的**kwargs完全一致,包括：
    #     headers,        cookies,            auth,   
    #     timeout,        allow_redirects,    proxies, 
    #     verify,         stream,             cert
'''
# 注意: 实际爬虫中需遵守目标网站的robots.txt协议,并设置合理的请求间隔避免被封禁.
# ------------------------------------------------------------------------------------------------
# requests库的基础使用模板
url = "https://api.scraperapi.com/?api_key=你的密钥&url=目标网址"
response = requests.get(url) # 自动处理IP轮换+验证码

# ------------------------------------------------------------------------------------------------
# 使用request库, 发送get请求
url2 = "https://httpbin.org/get"
params = {"key1": "value1", "key2": "value2"}  # URL参数
headers = {"User-Agent": "MyCustomUserAgent/1.0"}  # 自定义请求头

response2 = requests.get(url2, params=params, headers=headers)
print("状态码:", response2.status_code)    # 请求状态码,200,成功,404,未找到
print("响应文本:", response2.text)  # 文本内容
print("JSON响应:", response2.json())  # 自动解析JSON

# ------------------------------------------------------------------------------------------------
# 使用request库, 发送post请求(表单数据)
url = "https://httpbin.org/post"
data = {"username": "test_user", "password": "secret"}  # 表单数据
# 这个包默认发送的就是表单数据
# headers={"User-Agent": "Mozilla/5.0"}
response3 = requests.post(url, data=data)
print("响应:", response3.json())  # 查看服务端返回的数据

# 使用request库, 发送post请求(json数据) # timeout=5
url = "https://httpbin.org/post"
payload = {"name": "Alice", "age": 30}  # JSON数据
headers = {"Content-Type": "application/json"}
# 要发送其它形式的数据,需要特定的函数表头对情况进行说明
response4 = requests.post(url, json=payload, headers=headers)
print("JSON响应:", response4.json())

# ------------------------------------------------------------------------------------------------
def use_request_handdle_Cookies(self):
    # 处理Cookies
    # 获取Cookies
    Cookies_response = requests.get("https://httpbin.org/cookies/set?name=value")
    print("Cookies:", Cookies_response.cookies.get_dict())

    # 发送带Cookies的请求
    cookies = {"session_id": "12345abc"}
    Cookies_response = requests.get("https://httpbin.org/cookies", cookies=cookies)
    print("响应:", Cookies_response.json())

# ------------------------------------------------------------------------------------------------
# 使用会话(Session)保持状态
# 创建会话（自动保留Cookies）
session = requests.Session()
session.get("https://httpbin.org/cookies/set/sessioncookie/123456789")

# 后续请求自动携带Cookies
session_response = session.get("https://httpbin.org/cookies")
print("会话Cookies:", session_response.json())

# ------------------------------------------------------------------------------------------------
# 设置代理
proxies = {
    "http": "http://10.10.1.10:3128",   # HTTP代理
    "https": "http://10.10.1.10:1080",  # HTTPS代理
}

response = requests.get("https://httpbin.org/ip", proxies=proxies)
print("代理IP:", response.json())

# ------------------------------------------------------------------------------------------------
# 设置超时与错误处理
try:
    response = requests.get("https://httpbin.org/delay/5", timeout=3)  # 3秒超时
    print("请求成功!")
except requests.exceptions.Timeout:
    print("请求超时!")
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")

# ------------------------------------------------------------------------------------------------
# 下载文件(图片/二进制)
url = "https://httpbin.org/image/png"
response = requests.get(url)

# 保存二进制文件
with open("image.png", "wb") as f:
    f.write(response.content)
print("图片下载完成!")
#------------------------------------------------------------------------------------------------
# 流式下载大文件
url_large_file = url # 对应的文件??
response = requests.get(url_large_file, stream=True)
with open("bigfile.zip", "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

# ------------------------------------------------------------------------------------------------
# 处理重定向
# 禁用重定向（默认允许）
response = requests.get("https://httpbin.org/redirect/1", allow_redirects=False)
print("状态码:", response.status_code)  # 302重定向
print("重定向地址:", response.headers["Location"])




# ------------------------------------------------------------------------------------------------
# 自定义CA证书
requests.get("https://example.com", verify="/path/to/cert.pem")
# ------------------------------------------------------------------------------------------------
# 关闭SSL验证（生产环境不推荐）:
requests.get("https://example.com", verify=False)
# ------------------------------------------------------------------------------------------------
# 其它用法 (将字典转化为url字符)
requests.get("https://api.com", params={"a": 1, "b": "text"})
# URL变为：https://api.com?a=1&b=text
# 常用请求头
headers = {
    "User-Agent": "Mozilla/5.0",  # 伪装浏览器
    "Referer": "https://google.com",  # 来源页
    "Cookie": "sessionid=abc123",  # 手动设置Cookie
    "Authorization": "Bearer token_value"  # Token认证
}

# Cookies
# 方式1：字典
cookies={"session_id": "123abc"}
# 方式2：CookieJar对象（更灵活）
from requests.cookies import RequestsCookieJar
jar = RequestsCookieJar()
jar.set("session_id", "123abc", domain=".example.com")

# 文件上传格式
files = {
    "file1": open("data.txt", "rb"),  # 简单上传
    "file2": ("filename.xlsx", open("report.xlsx", "rb"), "application/vnd.ms-excel"),  # 指定文件名和MIME类型
    "file3": ("custom.txt", "文本内容", "text/plain")  # 上传文本数据
}
