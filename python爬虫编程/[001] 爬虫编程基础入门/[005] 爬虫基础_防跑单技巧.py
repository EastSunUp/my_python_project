

# 在代码中加入客户标识水印（保护权益）
import hashlib

def add_watermark(data, client_id):
    """添加隐形水印"""
    watermark = hashlib.md5(client_id.encode()).hexdigest()[:8]
    return data + f"\n# Generated for Client_{watermark}"
