
from PIL import Image
import os

def extract_first_frame_from_gif(gif_path, output_name=None):
    """
    提取GIF第一帧并保存为PNG到桌面

    参数:
    gif_path: GIF文件的完整路径
    output_name: 输出文件名（可选，不包含扩展名）
    """
    try:
        # 1. 打开GIF文件
        with Image.open(gif_path) as img:
            # 2. 定位到第一帧
            img.seek(0)

            # 3. 将第一帧转换为RGB（如果GIF是调色板模式）
            if img.mode in ['P', 'RGBA']:
                # 处理透明背景
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
                frame = rgb_img
            else:
                frame = img.convert('RGB')

            # 4. 获取桌面路径
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

            # 5. 设置输出文件名
            if output_name:
                filename = f"{output_name}.png"
            else:
                # 使用原始GIF文件名
                original_name = os.path.splitext(os.path.basename(gif_path))[0]
                filename = f"{original_name}_first_frame.png"

            # 6. 完整输出路径
            output_path = os.path.join(desktop_path, filename)

            # 7. 保存为PNG
            frame.save(output_path, 'PNG')

            print(f"成功提取第一帧！")
            print(f"GIF文件: {gif_path}")
            print(f"保存位置: {output_path}")

            return output_path

    except FileNotFoundError:
        print(f"错误: 找不到文件 '{gif_path}'")
        print("请确保输入了正确的文件路径")
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")

# 使用示例
if __name__ == "__main__":
    # 方法1: 使用完整路径
    gif_path = r"C:\Users\YourName\Pictures\example.gif"  # Windows
    # gif_path = "/Users/YourName/Pictures/example.gif"   # macOS/Linux

    # 方法2: 使用相对路径（如果GIF在当前脚本同目录）
    # gif_path = "example.gif"

    # 方法3: 让用户输入路径
    # gif_path = input("请输入GIF文件的完整路径: ").strip().strip('"').strip("'")

    # 调用函数
    extract_first_frame_from_gif(gif_path)

    # 或者指定输出文件名
    # extract_first_frame_from_gif(gif_path, "my_first_frame")
