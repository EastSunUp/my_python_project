
import numpy as np
from PIL import Image

def prepare_image_for_cnn(image_path):
    # 1. 读取图像
    img = Image.open(image_path)
    # 2. 转换为NumPy数组
    img_array = np.array(img)  # 现在数据是NumPy格式了
    # 3. 调整大小
    img_resized = np.array(Image.fromarray(img_array).resize((224, 224)))
    # 4. 归一化
    img_normalized = img_resized / 255.0
    # 5. 添加批次维度
    img_batch = np.expand_dims(img_normalized, axis=0)

    print(f"最终数据形状: {img_batch.shape}")  # (1, 224, 224, 3)
    return img_batch

# 使用示例
cnn_ready_data = prepare_image_for_cnn("example.jpg")


