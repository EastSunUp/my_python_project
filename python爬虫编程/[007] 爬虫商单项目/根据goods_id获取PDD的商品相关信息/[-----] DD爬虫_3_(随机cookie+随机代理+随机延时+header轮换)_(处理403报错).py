import requests
import json
import time
import random
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from urllib.parse import quote
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

'''
用户代理池:
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
'''
class PDDCrawler:
    def __init__(self):
        # 初始化User-Agent生成器
        self.ua = UserAgent()   # 这个包可以随机生成user-agent

        # 初始化会话
        self.session = requests.Session()

        # 设置重试策略
        retry_strategy = Retry(
            total=3,
            status_forcelist=[403, 429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        # 初始化代理池（这里需要您添加实际可用的代理）
        self.proxies = [
            # 格式: 'http://user:pass@ip:port' 或 'http://ip:port'
            # 示例:
            # 'http://123.123.123.123:8080',
            # 'http://user:password@45.45.45.45:3128'
        ]

        # 初始化请求计数器
        self.request_count = 0
        self.last_request_time = 0

    def get_random_headers(self):
        """生成随机的请求头"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://mobile.yangkeduo.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',  # 禁止追踪
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }

    def get_random_proxy(self):
        """获取随机代理"""
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def request_delay(self):
        """智能请求延迟"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time

        # 基本延迟
        base_delay = random.uniform(1.5, 3.0)

        # 根据请求频率增加延迟
        if self.request_count > 10:
            base_delay += random.uniform(1.0, 2.5)
        elif self.request_count > 20:
            base_delay += random.uniform(2.0, 4.0)

        # 确保最小延迟
        if elapsed < base_delay:
            sleep_time = base_delay - elapsed
            time.sleep(sleep_time)

        self.last_request_time = time.time()
        self.request_count += 1

    def get_dynamic_cookie(self):
        """获取动态Cookie"""
        try:
            # 访问首页获取基础Cookie
            home_url = 'https://mobile.yangkeduo.com/'
            headers = self.get_random_headers()
            proxy = self.get_random_proxy()

            self.request_delay()
            self.session.get(
                home_url,
                headers=headers,
                proxies={'http': proxy, 'https': proxy} if proxy else None,
                timeout=15
            )
            return True
        except Exception as e:
            print(f"获取Cookie失败: {e}")
            return False

    def make_api_request(self, url, max_retries=3):
        """执行API请求"""
        for attempt in range(max_retries):
            try:
                self.request_delay()
                headers = self.get_random_headers()
                proxy = self.get_random_proxy()

                # 获取最新Cookie
                self.get_dynamic_cookie()

                response = self.session.get(
                    url,
                    headers=headers,
                    proxies={'http': proxy, 'https': proxy} if proxy else None,
                    timeout=15
                )

                # 检查响应状态
                if response.status_code == 200:
                    return response
                elif response.status_code == 403:
                    print(f"尝试 {attempt + 1}/{max_retries}: 403 Forbidden 错误")
                    if proxy:
                        print(f"移除无效代理: {proxy}")
                        self.proxies.remove(proxy)  # 移除无效代理
                    time.sleep(2 ** attempt)  # 指数退避
                else:
                    print(f"尝试 {attempt + 1}/{max_retries}: 状态码 {response.status_code}")
                    time.sleep(2 ** attempt)
            except Exception as e:
                print(f"尝试 {attempt + 1}/{max_retries}: 请求异常 - {str(e)}")
                time.sleep(2 ** attempt)

        return None

    def search_products(self, keyword, page=1, limit=10):
        """搜索商品"""
        try:
            # 编码关键词
            encoded_keyword = quote(keyword)

            # 构造搜索URL
            api_url = f"https://mobile.yangkeduo.com/proxy/api/search?q={encoded_keyword}&page={page}&size={limit}"

            # 发送请求
            response = self.make_api_request(api_url)
            if not response:
                return []

            # 解析JSON响应
            data = response.json()

            # 提取商品列表
            goods_list = data.get('items', [])

            results = []
            for goods in goods_list:
                if len(results) >= limit:
                    break

                goods_id = goods.get('goods_id')
                name = goods.get('goods_name')
                # 价格处理
                price_info = goods.get('normal_price', 0)
                if isinstance(price_info, int):
                    price = price_info / 100
                else:
                    price = 0

                sales = goods.get('sales', 0)

                if goods_id and name:
                    results.append({
                        'goods_id': goods_id,
                        'name': name,
                        'price': price,
                        'sales': sales
                    })

            return results

        except Exception as e:
            print(f"搜索商品时出错: {e}")
            return []

    def get_product_details(self, goods_id):
        """获取商品详情"""
        try:
            # 构造详情URL
            api_url = f"https://mobile.yangkeduo.com/proxy/api/goods/{goods_id}"

            # 发送请求
            response = self.make_api_request(api_url)
            if not response:
                return None

            # 解析JSON响应
            data = response.json()
            goods_info = data.get('goods', {})
            store_info = data.get('store', {})

            # 提取商品信息
            name = goods_info.get('goods_name', '未知商品')

            # 价格处理
            price_info = goods_info.get('market_price', 0)
            if isinstance(price_info, int):
                price = price_info / 100
            else:
                price = "未知价格"

            sales = goods_info.get('sales', '未知销量')
            shop = store_info.get('store_name', '未知店铺')

            # 商品描述
            desc = goods_info.get('goods_desc', '无描述')

            # 构造结果字典
            result = {
                'goods_id': goods_id,
                'name': name,
                'price': price,
                'sales': sales,
                'shop': shop,
                'description': desc
            }

            return result

        except Exception as e:
            print(f"获取商品详情时出错: {e}")
            return None
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("电商,商品信息爬取工具")
        self.geometry("900x600")
        self.resizable(True, True)

        # 创建爬虫实例
        self.crawler = PDDCrawler()

        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        # 创建标签页
        self.tab_control = ttk.Notebook(self)

        # 搜索标签页
        self.search_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.search_tab, text='商品搜索')

        # 详情标签页
        self.detail_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.detail_tab, text='商品详情')

        self.tab_control.pack(expand=1, fill="both")

        # 配置搜索标签页
        self.setup_search_tab()

        # 配置详情标签页
        self.setup_detail_tab()

    def setup_search_tab(self):
        # 搜索框架
        search_frame = ttk.LabelFrame(self.search_tab, text="搜索设置")
        search_frame.pack(fill="x", padx=10, pady=5)

        # 关键词输入
        ttk.Label(search_frame, text="搜索关键词:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # 页数选择
        ttk.Label(search_frame, text="搜索页数:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.page_spinbox = ttk.Spinbox(search_frame, from_=1, to=10, width=5)
        self.page_spinbox.set(1)
        self.page_spinbox.grid(row=0, column=3, padx=5, pady=5)

        # 每页结果数
        ttk.Label(search_frame, text="每页结果数:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.limit_spinbox = ttk.Spinbox(search_frame, from_=5, to=50, width=5)
        self.limit_spinbox.set(10)
        self.limit_spinbox.grid(row=0, column=5, padx=5, pady=5)

        # 搜索按钮
        self.search_btn = ttk.Button(search_frame, text="开始搜索", command=self.start_search)
        self.search_btn.grid(row=0, column=6, padx=10, pady=5)

        # 结果显示区域
        result_frame = ttk.LabelFrame(self.search_tab, text="搜索结果")
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 树状视图显示结果
        columns = ("goods_id", "name", "price", "sales")
        self.result_tree = ttk.Treeview(result_frame, columns=columns, show="headings")

        # 设置列标题
        self.result_tree.heading("goods_id", text="商品ID")
        self.result_tree.heading("name", text="商品名称")
        self.result_tree.heading("price", text="价格(元)")
        self.result_tree.heading("sales", text="销量")

        # 设置列宽
        self.result_tree.column("goods_id", width=100)
        self.result_tree.column("name", width=300)
        self.result_tree.column("price", width=80)
        self.result_tree.column("sales", width=80)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.result_tree.pack(fill="both", expand=True)

        # 操作按钮
        btn_frame = ttk.Frame(self.search_tab)
        btn_frame.pack(fill="x", padx=10, pady=5)

        self.export_btn = ttk.Button(btn_frame, text="导出CSV", command=self.export_search_results)
        self.export_btn.pack(side="left", padx=5)

        self.clear_btn = ttk.Button(btn_frame, text="清除结果", command=self.clear_search_results)
        self.clear_btn.pack(side="left", padx=5)

    def setup_detail_tab(self):
        # 商品ID输入区域
        id_frame = ttk.LabelFrame(self.detail_tab, text="商品ID")
        id_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(id_frame, text="商品ID:").pack(side="left", padx=5, pady=5)
        self.id_entry = ttk.Entry(id_frame, width=30)
        self.id_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        # 查询按钮
        self.query_btn = ttk.Button(id_frame, text="查询详情", command=self.query_product_details)
        self.query_btn.pack(side="right", padx=10, pady=5)

        # 结果显示区域
        detail_frame = ttk.LabelFrame(self.detail_tab, text="商品详情")
        detail_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 使用文本框显示详情
        self.detail_text = scrolledtext.ScrolledText(detail_frame, wrap=tk.WORD)
        self.detail_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.detail_text.config(state=tk.DISABLED)

        # 操作按钮
        btn_frame = ttk.Frame(self.detail_tab)
        btn_frame.pack(fill="x", padx=10, pady=5)

        self.save_btn = ttk.Button(btn_frame, text="保存详情", command=self.save_product_details)
        self.save_btn.pack(side="left", padx=5)

        self.clear_detail_btn = ttk.Button(btn_frame, text="清除详情", command=self.clear_product_details)
        self.clear_detail_btn.pack(side="left", padx=5)

    def start_search(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showerror("错误", "请输入搜索关键词")
            return

        try:
            page = int(self.page_spinbox.get())
            limit = int(self.limit_spinbox.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return

        # 清空之前的搜索结果
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        # 更新按钮状态
        self.search_btn.config(text="搜索中...", state=tk.DISABLED)
        self.update()

        try:
            # 执行搜索
            results = self.crawler.search_products(keyword, page, limit)

            if not results:
                messagebox.showinfo("提示", "未找到相关商品")
                return

            # 显示结果
            for item in results:
                self.result_tree.insert("", "end", values=(
                    item['goods_id'],
                    item['name'],
                    item['price'],
                    item['sales']
                ))

            messagebox.showinfo("成功", f"找到 {len(results)} 个商品")

        except Exception as e:
            messagebox.showerror("错误", f"搜索过程中出错: {str(e)}")
        finally:
            self.search_btn.config(text="开始搜索", state=tk.NORMAL)

    def query_product_details(self):
        goods_id = self.id_entry.get().strip()
        if not goods_id:
            messagebox.showerror("错误", "请输入商品ID")
            return

        # 更新按钮状态
        self.query_btn.config(text="查询中...", state=tk.DISABLED)
        self.update()

        try:
            # 获取商品详情
            details = self.crawler.get_product_details(goods_id)

            if not details:
                messagebox.showinfo("提示", "未找到商品详情")
                return

            # 显示详情
            self.detail_text.config(state=tk.NORMAL)
            self.detail_text.delete(1.0, tk.END)

            info = f"商品ID: {details['goods_id']}\n"
            info += f"商品名称: {details['name']}\n"
            info += f"价格: {details['price']}\n"
            info += f"销量: {details['sales']}\n"
            info += f"店铺: {details['shop']}\n"
            info += "=" * 50 + "\n"
            info += f"商品描述:\n{details['description']}\n"

            self.detail_text.insert(tk.END, info)
            self.detail_text.config(state=tk.DISABLED)

            messagebox.showinfo("成功", "商品详情获取成功")

        except Exception as e:
            messagebox.showerror("错误", f"查询过程中出错: {str(e)}")
        finally:
            self.query_btn.config(text="查询详情", state=tk.NORMAL)

    def export_search_results(self):
        # 获取所有结果
        items = self.result_tree.get_children()
        if not items:
            messagebox.showinfo("提示", "没有可导出的数据")
            return

        # 准备数据
        data = []
        for item in items:
            values = self.result_tree.item(item, 'values')
            data.append({
                '商品ID': values[0],
                '商品名称': values[1],
                '价格(元)': values[2],
                '销量': values[3]
            })

        # 创建DataFrame
        df = pd.DataFrame(data)

        # 选择保存路径
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")],
            title="保存搜索结果"
        )

        if not file_path:
            return

        try:
            df.to_csv(file_path, index=False, encoding='utf_8_sig')
            messagebox.showinfo("成功", f"结果已保存到: {file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"导出过程中出错: {str(e)}")

    def save_product_details(self):
        if not self.detail_text.get(1.0, tk.END).strip():
            messagebox.showinfo("提示", "没有可保存的内容")
            return

        # 获取文本内容
        content = self.detail_text.get(1.0, tk.END)

        # 选择保存路径
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            title="保存商品详情"
        )

        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("成功", f"详情已保存到: {file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"保存过程中出错: {str(e)}")

    def clear_search_results(self):
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

    def clear_product_details(self):
        self.detail_text.config(state=tk.NORMAL)
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    app = Application()
    app.mainloop()