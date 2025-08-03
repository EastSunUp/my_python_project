import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk


class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片比例缩放工具")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f5f5")

        # 设置应用图标
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # 创建主框架
        main_frame = tk.Frame(root, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = tk.Label(
            main_frame,
            text="图片比例缩放工具",
            font=("Arial", 18, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 15))

        # 说明文字
        desc_text = "将图片按比例缩小到260×260像素，保持原始内容不变形\n空白区域将使用背景色填充"
        desc_label = tk.Label(
            main_frame,
            text=desc_text,
            font=("Arial", 10),
            bg="#f5f5f5",
            fg="#7f8c8d"
        )
        desc_label.pack(pady=(0, 20))

        # 创建左右面板
        control_frame = tk.Frame(main_frame, bg="#ecf0f1", padx=15, pady=15, bd=1, relief=tk.GROOVE)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))

        preview_frame = tk.Frame(main_frame, bg="#ffffff", padx=15, pady=15, bd=1, relief=tk.GROOVE)
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # ====================== 控制面板 ======================
        control_label = tk.Label(
            control_frame,
            text="控制面板",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        control_label.pack(pady=(0, 15))

        # 文件选择
        file_frame = tk.Frame(control_frame, bg="#ecf0f1")
        file_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            file_frame,
            text="选择图片:",
            bg="#ecf0f1",
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.file_entry = tk.Entry(file_frame, width=25, font=("Arial", 9))
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        browse_btn = tk.Button(
            file_frame,
            text="浏览...",
            command=self.browse_file,
            bg="#3498db",
            fg="white",
            relief=tk.FLAT,
            font=("Arial", 9)
        )
        browse_btn.pack(side=tk.LEFT)

        # 背景颜色选择
        color_frame = tk.Frame(control_frame, bg="#ecf0f1")
        color_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            color_frame,
            text="背景颜色:",
            bg="#ecf0f1",
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.bg_color = tk.StringVar(value="#FFFFFF")
        colors = ["白色 (#FFFFFF)", "黑色 (#000000)", "浅灰色 (#F0F0F0)", "自定义..."]
        color_combo = ttk.Combobox(
            color_frame,
            textvariable=self.bg_color,
            values=colors,
            width=20,
            state="readonly"
        )
        color_combo.pack(side=tk.LEFT)

        # 输出格式
        format_frame = tk.Frame(control_frame, bg="#ecf0f1")
        format_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            format_frame,
            text="输出格式:",
            bg="#ecf0f1",
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.format_var = tk.StringVar(value="PNG")
        tk.Radiobutton(
            format_frame,
            text="PNG (高质量)",
            variable=self.format_var,
            value="PNG",
            bg="#ecf0f1",
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Radiobutton(
            format_frame,
            text="JPG (较小文件)",
            variable=self.format_var,
            value="JPG",
            bg="#ecf0f1",
            font=("Arial", 9)
        ).pack(side=tk.LEFT)

        # 输出路径
        output_frame = tk.Frame(control_frame, bg="#ecf0f1")
        output_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            output_frame,
            text="保存位置:",
            bg="#ecf0f1",
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.output_entry = tk.Entry(output_frame, width=25, font=("Arial", 9))
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        output_btn = tk.Button(
            output_frame,
            text="浏览...",
            command=self.browse_output,
            bg="#3498db",
            fg="white",
            relief=tk.FLAT,
            font=("Arial", 9)
        )
        output_btn.pack(side=tk.LEFT)

        # 处理按钮
        btn_frame = tk.Frame(control_frame, bg="#ecf0f1")
        btn_frame.pack(fill=tk.X, pady=20)

        preview_btn = tk.Button(
            btn_frame,
            text="预览效果",
            command=self.preview,
            bg="#2ecc71",
            fg="white",
            relief=tk.FLAT,
            font=("Arial", 10, "bold"),
            width=10,
            height=1
        )
        preview_btn.pack(side=tk.LEFT, padx=(0, 10))

        save_btn = tk.Button(
            btn_frame,
            text="保存图片",
            command=self.save_image,
            bg="#e74c3c",
            fg="white",
            relief=tk.FLAT,
            font=("Arial", 10, "bold"),
            width=10,
            height=1
        )
        save_btn.pack(side=tk.LEFT)

        # 状态信息
        self.status_var = tk.StringVar(value="就绪：请选择图片文件")
        status_bar = tk.Label(
            control_frame,
            textvariable=self.status_var,
            bg="#ecf0f1",
            fg="#7f8c8d",
            font=("Arial", 9),
            anchor=tk.W
        )
        status_bar.pack(fill=tk.X, pady=(20, 0))

        # ====================== 预览面板 ======================
        preview_label = tk.Label(
            preview_frame,
            text="图片预览",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        preview_label.pack(pady=(0, 15))

        # 创建左右预览区域
        preview_container = tk.Frame(preview_frame, bg="#ffffff")
        preview_container.pack(fill=tk.BOTH, expand=True)

        # 原始图片预览
        orig_frame = tk.LabelFrame(
            preview_container,
            text="原始图片",
            bg="#ffffff",
            padx=10,
            pady=10
        )
        orig_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.before_label = tk.Label(
            orig_frame,
            text="未加载图片",
            bg="#f8f9fa",
            width=30,
            height=15
        )
        self.before_label.pack(fill=tk.BOTH, expand=True)

        # 处理后图片预览
        result_frame = tk.LabelFrame(
            preview_container,
            text="处理后图片 (260×260)",
            bg="#ffffff",
            padx=10,
            pady=10
        )
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.after_label = tk.Label(
            result_frame,
            text="请先预览效果",
            bg="#f8f9fa",
            width=30,
            height=15
        )
        self.after_label.pack(fill=tk.BOTH, expand=True)

        # 初始化变量
        self.original_image = None
        self.resized_image = None
        self.image_path = ""

        # 设置默认输出路径
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        self.output_entry.insert(0, os.path.join(desktop, "resized_image.png"))

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="选择图片文件",
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            self.image_path = file_path
            self.load_image()

    def browse_output(self):
        default_ext = ".png" if self.format_var.get() == "PNG" else ".jpg"
        default_name = "resized_image" + default_ext

        file_path = filedialog.asksaveasfilename(
            title="保存处理后的图片",
            defaultextension=default_ext,
            initialfile=default_name,
            filetypes=[
                ("PNG 图片", "*.png"),
                ("JPEG 图片", "*.jpg"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)

    def load_image(self):
        if not self.image_path:
            return

        try:
            self.original_image = Image.open(self.image_path)
            self.update_preview(self.original_image, self.before_label)

            # 更新状态
            filename = os.path.basename(self.image_path)
            w, h = self.original_image.size
            self.status_var.set(f"已加载: {filename} ({w}×{h}像素)")
        except Exception as e:
            messagebox.showerror("错误", f"无法加载图片: {str(e)}")
            self.status_var.set("错误: 无法加载图片")

    def update_preview(self, image, label):
        # 调整预览大小
        preview_size = (320, 240)
        preview_img = image.copy()
        preview_img.thumbnail(preview_size, Image.LANCZOS)

        # 转换为Tkinter可显示的格式
        tk_img = ImageTk.PhotoImage(preview_img)

        # 更新预览
        label.configure(image=tk_img, text="")
        label.image = tk_img

    def get_background_color(self):
        color = self.bg_color.get()

        # 处理预设颜色
        if "白色" in color:
            return "#FFFFFF"
        elif "黑色" in color:
            return "#000000"
        elif "浅灰色" in color:
            return "#F0F0F0"
        elif "自定义" in color:
            return "#FFFFFF"  # 默认白色
        else:
            return color  # 直接使用十六进制值

    def resize_image(self):
        """按比例缩小图片到260×260像素，保持原始内容不变形"""
        if not self.original_image:
            messagebox.showwarning("警告", "请先选择图片!")
            return None

        try:
            # 目标尺寸
            target_size = (260, 260)

            # 原始尺寸
            width, height = self.original_image.size

            # 计算缩放比例（保持宽高比）
            ratio = min(target_size[0] / width, target_size[1] / height)
            new_size = (int(width * ratio), int(height * ratio))

            # 高质量缩小图片
            resized_img = self.original_image.resize(new_size, Image.LANCZOS)

            # 创建目标尺寸的背景
            bg_color = self.get_background_color()
            background = Image.new("RGB", target_size, bg_color)

            # 计算图片在背景上的位置（居中）
            position = (
                (target_size[0] - new_size[0]) // 2,
                (target_size[1] - new_size[1]) // 2
            )

            # 将缩小后的图片粘贴到背景上
            background.paste(resized_img, position)

            return background
        except Exception as e:
            messagebox.showerror("错误", f"处理图片时出错: {str(e)}")
            return None

    def preview(self):
        resized = self.resize_image()
        if resized:
            self.resized_image = resized
            self.update_preview(resized, self.after_label)
            self.status_var.set("预览已生成 - 260×260像素")

    def save_image(self):
        if not self.resized_image:
            messagebox.showwarning("警告", "请先生成预览!")
            return

        output_path = self.output_entry.get()
        if not output_path:
            messagebox.showwarning("警告", "请选择保存位置!")
            return

        # 确保文件扩展名正确
        if self.format_var.get() == "JPG":
            if not output_path.lower().endswith(('.jpg', '.jpeg')):
                output_path += ".jpg"
        else:
            if not output_path.lower().endswith('.png'):
                output_path += ".png"

        try:
            # 保存图片
            if output_path.lower().endswith(('.jpg', '.jpeg')):
                self.resized_image.save(output_path, "JPEG", quality=95)
            else:
                self.resized_image.save(output_path, "PNG")

            # 更新状态
            filename = os.path.basename(output_path)
            self.status_var.set(f"图片已保存: {filename}")

            # 显示成功消息
            messagebox.showinfo("成功", "图片已成功保存!")
        except Exception as e:
            messagebox.showerror("错误", f"保存图片时出错: {str(e)}")
            self.status_var.set("错误: 保存失败")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()

