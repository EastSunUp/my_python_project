import socket

def get_local_ip():
    """获取本机内网IP地址"""
    try:
        # 创建一个临时socket连接到公共DNS服务器
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google公共DNS
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"  # 失败时返回本地回环地址

# 使用示例
if __name__ == "__main__":
    local_ip = get_local_ip()
    print(f"您的内网IP地址是: {local_ip}")
