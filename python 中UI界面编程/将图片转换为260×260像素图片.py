

from PIL import Image

def resize_image(input_path, output_path):
    img = Image.open(input_path)
    img = img.resize((260, 260))  # 强制尺寸
    img.save(output_path)

# 示例
resize_image("原始图片.jpg", "输出图片.jpg")

