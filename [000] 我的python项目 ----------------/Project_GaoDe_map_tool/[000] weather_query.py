

import requests
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# 天气 URL
Weather_URL = "https://restapi.amap.com/v3/weather/weatherInfo?"
API_URL = "https://restapi.amap.com/v3/place/text"
API_KEY = "your_api_key_here"  # 替换为实际API Key

# params = {
#         "key": API_KEY,
#         "keywords": keyword,    # 搜索关键词
#         "city": district,   # 目标城市
#         "offset": "25",  # 每页记录数
#         "page": page,
#         "extensions": "all",  # 获取详细信息
#         "output": "json"
#     }

provence_map={
    "广东省": "440000",
    "湖南省": "430000"
}

city_map={
    "广州市":{
        "ad_code": "440100",
        "city_code": "020",
        "荔湾区": "440303",    "越秀区": "440304",    "海珠区": "440305",
        "天河区": "440306",    "白云区": "440307",    "黄浦区": "440308",
        "番禺区": "440309",    "花都区": "440310",    "南沙区": "440311",
        "从化区": "440309",    "增城区": "440310"
    },
    "深圳市":{
        "city_code": "0755",
        "ad_code": "440300",
        "罗湖区": "440303",    "福田区": "440304",    "南山区": "440305",
        "宝安区": "440306",    "龙岗区": "440307",    "盐田区": "440308",
        "龙华区": "440309",    "坪山区": "440310",    "光明区": "440311"
    },
    "珠海市":{
    },
}

# district 需要确认
def fetch_weather_data(API_KEY="e68bc4ec6a494544e80acae8a9839fd4",
                       weather_type = "all", district=None, page=1):
    if district is None:
        district = {"城市": "深圳市", "城区": "龙华区"}
    """从高德API获取POI数据"""
    # city_key ={
    #     "city_code":city_map[district["城市"]]["city_code"],
    #     "ad_code":city_map[district["城市"]][district["城区"]]
    # }
    # print(f"city_key:{city_key}")
    ad_code = city_map[district["城市"]][district["城区"]]
    print(f'city_name:{district["城市"]}, ad_code:{ad_code}')

    weather_params ={
        "key": API_KEY,
        "city": ad_code,  # 目标城市,目标城区的 ad_code
        "extensions": weather_type,  # 气象类型,base 返回实况天气, all 返回预报天气
        "output": "json"    # 返回的数据类型的格式
    }
    response = requests.get(url=Weather_URL, params=weather_params, timeout=10)
    if response.status_code == 200:
        print(f"data:{response.json()}")
        return response.json()

# 从高德地图API获取天气数据
weather_data = fetch_weather_data()
print(f"status:{weather_data["status"]}")

# -------------------------------------------------------------------------------------------------
# 创建Tk root,以显示.
root = tk.Tk()
root.title("Tool: 从高德地图获取天气状况")
root.geometry("1250x600")
root.configure(bg="#f0f0f0")    # 基础背景色:  #f0f0f0/white
# # 设置窗口整体透明度（0.0=完全透明，1.0=完全不透明）
# root.attributes("-alpha", 0.9)  # 90%不透明，10%透明
# 设置主题
style = ttk.Style()
style.theme_use("clam")
# # 配置一个白色背景的Frame样式
# style.configure("White.TFrame", background="white")
# 创建主框架
main_frame = ttk.Frame(root, padding=20, style="White.TFrame")
main_frame.pack(fill=tk.BOTH, expand=True)

# 基础信息面板
city_frame = ttk.LabelFrame(main_frame, text="城市基础信息", padding=10)
city_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
# 数据面板
weather_frame = ttk.LabelFrame(main_frame, text="天气预测数据", padding=10)
weather_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
# 数据面板
mode_frame = ttk.LabelFrame(main_frame, text="模式选项&设置", padding=10)
mode_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

# 城市信息
ttk.Label(city_frame, text="城市名称:").grid(row=0, column=0, sticky="w", pady=5)
# 文本框填写
date_entry = ttk.Entry(city_frame, width=7, justify="center")
date_entry.delete(0, tk.END)
date_entry.insert(0, "深圳")    # 设置文本框内容
date_entry.grid(row=0, column=1, padx=5, pady=5)    # 设置放置文本框的位置

# 城区信息
ttk.Label(city_frame, text="所属城区:").grid(row=0, column=2, sticky="w", pady=5)
# 文本框填写
date_entry = ttk.Entry(city_frame, width=7, justify="center")
date_entry.delete(0, tk.END)
date_entry.insert(0, "龙华区")    # 设置文本框内容
date_entry.grid(row=0, column=3, padx=5, pady=5)    # 设置放置文本框的位置

# 刷新模式信息
ttk.Label(city_frame, text="当前模式").grid(row=0, column=4, sticky="w", pady=5)
# 文本框填写
date_entry = ttk.Entry(city_frame, width=18, justify="center")
date_entry.delete(0, tk.END)
date_entry.insert(0, "手动模式")    # 设置文本框内容
date_entry.grid(row=0, column=5, padx=5, pady=5)    # 设置放置文本框的位置

# 状态: 刷新成功/刷新失败
ttk.Label(city_frame, text="刷新状态").grid(row=0, column=6, sticky="w", pady=5)
# 文本框填写
date_entry = ttk.Entry(city_frame, width=18, justify="center")
date_entry.delete(0, tk.END)
date_entry.insert(0, "刷新成功/刷新失败")    # 设置文本框内容
date_entry.grid(row=0, column=7, padx=5, pady=5)    # 设置放置文本框的位置

weather_map={
    "日期":{"para_name": "date", "entry_width":12},
    "星期":{"para_name": "week", "entry_width":4},
    "白天天气":{"para_name": "dayweather", "entry_width":7},
    "夜间天气":{"para_name": "nightweather", "entry_width":7},
    "白天风向":{"para_name": "daywind", "entry_width":7},
    "白天风力级别":{"para_name": "daypower", "entry_width":7},
    "夜间风向":{"para_name": "nightwind", "entry_width":7},
    "夜间风力级别":{"para_name": "nightpower", "entry_width":7},
    "白天温度":{"para_name": "daytemp", "entry_width":7},
    "夜间温度":{"para_name": "nighttemp", "entry_width":7}
}

base_info_map={
    "省份名称": {"para_name":"province", "entry_width":7},
    "adcode":  {"para_name":"adcode", "entry_width": 7},
    "当前日期":{"para_name":"reporttime", "entry_width":18},
    "刷新时间":{"para_name":"reporttime", "entry_width":18}
}

# "城市":{"para_name":"date", "entry_width":7},
# "获取状态是否成功":{"para_name":"nightweather", "entry_width":7}
week_map={
    "1":"一", "2":"二", "3":"三",
    "4":"四", "5":"五", "6":"六",
    "7":"日"}

def set_label_entry(frame, row, context_info, label_map):
    '''
        函数功能:每次显示指定frame 中 一行的所有label_map中的内容
        参数说明:
            frame: 指定框架     row:当前布置的行号
            context_info: 布置当前行的内容字典,这是一个一维字典
            label_map: 这一行的所有标签映射谱
        返回值: 无
        附加说明:
            1.context_info数据类型必须为字典类型的数据,并且其键值对需要与label_map   相匹配
            2.每调用一次该函数只布置一行内容,其中row为行号
    '''
    for col_cnt, label_str in enumerate(label_map):
        # 设置标签内容(考虑天气信息中的特殊内容)
        # if row_cnt == 0 and index ==0:
        #     # 日期信息
        #     ttk.Label(control_frame, text="今天:").grid(row=0, column=0, sticky="w", pady=5)
        # else:
        #     ttk.Label(control_frame, text=label_name).grid(row=row_cnt, column=index*2, sticky="w", pady=5)
        # 设置标签及其名称
        ttk.Label(frame, text=label_str).grid(row=row, column=col_cnt * 2, sticky="w", pady=5)

        # 设置信息框内容
        entry_str = f"{context_info[label_map[label_str]["para_name"]]}"
        # 特殊项添加额外单位/变更显示
        if "温度" in label_str and "℃" not in entry_str:
            entry_str = entry_str + "℃"
        elif label_str == "星期":
            entry_str = week_map[context_info[label_map[label_str]["para_name"]]]
        entry = ttk.Entry(frame, width=label_map[label_str]["entry_width"], justify="center")
        entry.delete(0, tk.END)  # 清空文本框内容
        entry.insert(0, entry_str)  # 填写文本框中内容
        entry.grid(row=row, column=col_cnt * 2 + 1, padx=5, pady=5)  # 设置放置文本框位置
        # entry_str = ""

 # 解析天气数据信息(来自高德地图API获取)
forecasts = weather_data["forecasts"]   # ["casts"]
for forecast in forecasts:
    # for key in data.keys():
    #     print(f"{key}:{data[key]}")
    #print(f"print_casts:{data["casts"]}")
    # for cast in data["casts"]:
    #     print(f"print_cast:{cast}")
    base_info = forecast.copy()
    del base_info["casts"]
    print(f"base info: {base_info}")
    set_label_entry(frame=city_frame, row=1, context_info=base_info, label_map=base_info_map)
    # 布置天气信息
    for row_cnt, entry_info in enumerate(forecast["casts"]):
        set_label_entry(frame=weather_frame, row=row_cnt, context_info=entry_info, label_map=weather_map)

# -------------------------------------------------------------------------------------------------
# # 日期信息_1
# ttk.Label(control_frame, text="今天日期:").grid(row=0, column=0, sticky="w", pady=5)
# # 设置日期信息框 1
# date_entry = ttk.Entry(control_frame, width=12, justify="center")
# date_entry.delete(0, tk.END)
# date_entry.insert(0, "2022/11/09")    # 设置文本框内容
# date_entry.grid(row=0, column=1, padx=5, pady=5)    # 设置放置文本框的位置

# 绑定按钮对应动作的槽函数操作
ttk.Button(mode_frame, text="刷新", command=None).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(mode_frame, text="自动/手动", command=None).grid(row=0, column=1, padx=5, pady=5)

# 区域选择读取/信息读取
ttk.Label(mode_frame, text="区域选择:").grid(row=0, column=2, sticky="w", pady=5)
# 文本框填写
date_entry = ttk.Entry(mode_frame, width=18, justify="center")
date_entry.delete(0, tk.END)
date_entry.insert(0, "广东省/深圳/龙华区")    # 设置文本框内容
date_entry.grid(row=0, column=3, padx=5, pady=5)    # 设置放置文本框的位置
# 自动刷新频率
ttk.Label(mode_frame, text="自动刷新频率:").grid(row=0, column=4, sticky="w", pady=5)
# 文本框填写
date_entry = ttk.Entry(mode_frame, width=10, justify="center")
date_entry.delete(0, tk.END)
date_entry.insert(0, "5次/分钟")    # 设置文本框内容
date_entry.grid(row=0, column=5, padx=5, pady=5)    # 设置放置文本框的位置

# 天气模式
ttk.Label(mode_frame, text="天气模式:").grid(row=0, column=6, sticky="w", pady=5)
color_var = tk.StringVar(value="预测模式")
color_options = ["预测模式", "实时模式", "自定义..."]
ttk.Combobox(
    mode_frame, textvariable=color_var, values=color_options, width=15
).grid(row=0,column=7,sticky="w",pady=5)


# 启动页面显示主循环
root.mainloop()

