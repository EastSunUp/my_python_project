# proxy_script.py
from mitmproxy import http

def request(flow: http.HTTPFlow):
    print(f"请求: {flow.request.url}")

def response(flow: http.HTTPFlow):
    print(f"响应: {flow.response.status_code} {flow.request.url}")
