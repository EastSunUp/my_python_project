import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os


class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片尺寸转换工具")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # 设置主题
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # 创建主框架
        self.main_frame = ttk.Frame(root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧面板 - 图片预览
        self.preview_frame = ttk.LabelFrame(self.main_frame, text="图片预览", padding=10)
        self.preview_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.preview_label = tk.Label(self.preview_frame, bg="white", width=40, height=20)
        self.preview_label.pack(padx=10, pady=10)

        # 右侧面板 - 控制选项
        self.control_frame = ttk.LabelFrame(self.main_frame, text="调整选项", padding=10)
        self.control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # 文件选择
        ttk.Label(self.control_frame, text="选择图片:").grid(row=0, column=0, sticky="w", pady=5)
        self.file_entry = ttk.Entry(self.control_frame, width=30)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.control_frame, text="浏览...", command=self.browse_file).grid(row=0, column=2, padx=5, pady=5)

        # 目标尺寸
        ttk.Label(self.control_frame, text="目标尺寸:").grid(row=1, column=0, sticky="w", pady=5)
        self.size_var = tk.StringVar(value="260×260")
        ttk.Label(self.control_frame, textvariable=self.size_var).grid(row=1, column=1, sticky="w", pady=5)

        # 处理选项(直接拉伸、裁剪为正方形、填充为正方形)
        self.option_var = tk.StringVar(value="stretch")
        ttk.Radiobutton(self.control_frame, text="直接拉伸(可能变形)",
                        variable=self.option_var, value="stretch").grid(row=2, column=0, columnspan=3, sticky="w",
                                                                        pady=5)
        ttk.Radiobutton(self.control_frame, text="裁剪为正方形(保持比例)",
                        variable=self.option_var, value="crop").grid(row=3, column=0, columnspan=3, sticky="w", pady=5)
        ttk.Radiobutton(self.control_frame, text="填充为正方形(保持比例)",
                        variable=self.option_var, value="fill").grid(row=4, column=0, columnspan=3, sticky="w", pady=5)

        # 背景颜色选项
        ttk.Label(self.control_frame, text="填充背景颜色:").grid(row=5, column=0, sticky="w", pady=5)
        self.color_var = tk.StringVar(value="#FFFFFF")
        color_options = ["白色(#FFFFFF)", "黑色(#000000)", "灰色(#CCCCCC)", "自定义..."]
        ttk.Combobox(
            self.control_frame, textvariable=self.color_var, values=color_options, width=15
        ).grid(row=5,column=1,sticky="w",pady=5)

        # 处理按钮
        ttk.Button(self.control_frame, text="预览效果", command=self.preview_image).grid(row=6, column=0, pady=15,
                                                                                         sticky="ew")
        ttk.Button(self.control_frame, text="保存图片", command=self.save_image).grid(row=6, column=1, pady=15, padx=5,
                                                                                      sticky="ew")

        # 信息区域
        self.info_frame = ttk.LabelFrame(self.main_frame, text="处理信息", padding=10)
        self.info_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.info_text = tk.Text(self.info_frame, height=4, width=80)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        self.info_text.config(state=tk.DISABLED)

        # 初始化变量
        self.original_image = None
        self.resized_image = None
        self.image_path = ""

        # 配置网格权重
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=0)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff")]
        )
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            self.image_path = file_path
            self.load_image()

    def load_image(self):
        try:
            self.original_image = Image.open(self.image_path)   # 传输Image对象,这个对象可以对图片做一系列处理
            self.show_image(self.original_image)
            self.update_info(f"已加载图片: {os.path.basename(self.image_path)}\n"
                             f"原始尺寸: {self.original_image.width}×{self.original_image.height} 像素")
        except Exception as e:
            messagebox.showerror("错误", f"无法加载图片: {str(e)}")

    def show_image(self, image):
        # 调整预览大小
        preview_size = (350, 350)
        preview_img = image.copy()
        preview_img.thumbnail(preview_size) # 调整预览大小?

        # 转换为Tkinter可显示的格式
        tk_img = ImageTk.PhotoImage(preview_img)

        # 更新预览
        self.preview_label.configure(image=tk_img)
        self.preview_label.image = tk_img

    def resize_image(self):
        if not self.original_image:
            messagebox.showwarning("警告", "请先选择图片!")
            return None

        option = self.option_var.get()
        target_size = (260, 260)

        if option == "stretch":
            # 直接拉伸
            return self.original_image.resize(target_size)

        elif option == "crop":
            # 裁剪为正方形
            width, height = self.original_image.size
            crop_size = min(width, height)
            left = (width - crop_size) / 2
            top = (height - crop_size) / 2
            right = (width + crop_size) / 2
            bottom = (height + crop_size) / 2

            cropped = self.original_image.crop((left, top, right, bottom))  # 图片裁剪函数
            return cropped.resize(target_size)

        elif option == "fill":
            # 填充为正方形
            width, height = self.original_image.size
            new_img = Image.new("RGB", target_size, self.get_bg_color())

            # 计算缩放比例
            ratio = min(target_size[0] / width, target_size[1] / height)
            new_size = (int(width * ratio), int(height * ratio))
            resized_img = self.original_image.resize(new_size)

            # 计算位置
            position = (
                (target_size[0] - new_size[0]) // 2,
                (target_size[1] - new_size[1]) // 2
            )

            new_img.paste(resized_img, position)
            return new_img

    def get_bg_color(self):
        color_str = self.color_var.get()
        if color_str.startswith("#") and len(color_str) == 7:
            return color_str

        # 处理预设颜色
        if "白色" in color_str:
            return "#FFFFFF"
        elif "黑色" in color_str:
            return "#000000"
        elif "灰色" in color_str:
            return "#CCCCCC"
        else:
            return "#FFFFFF"  # 默认白色

    def preview_image(self):
        resized = self.resize_image()
        if resized:
            self.resized_image = resized
            self.show_image(resized)
            self.update_info(f"已生成预览: 260×260 像素\n"
                             f"处理方式: {self.get_option_name()}")

    def save_image(self):
        if not self.resized_image:
            messagebox.showwarning("警告", "请先生成预览!")
            return

        # filedialog.asksaveasfilename会发起一个对话框，询问邀请用户选择图片的保存路径位置
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG 图片", "*.png"), ("JPEG 图片", "*.jpg"), ("所有文件", "*.*")]
        )

        if save_path:
            try:
                self.resized_image.save(save_path)
                self.update_info(f"图片已保存至: {save_path}")
                messagebox.showinfo("成功", "图片保存成功!")
            except Exception as e:
                messagebox.showerror("错误", f"保存图片时出错: {str(e)}")

    def get_option_name(self):
        options = {
            "stretch": "直接拉伸",
            "crop": "裁剪为正方形",
            "fill": "填充为正方形"
        }
        return options.get(self.option_var.get(), "未知方式")

    def update_info(self, message):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, message)
        self.info_text.config(state=tk.DISABLED)


# 运行应用
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()
