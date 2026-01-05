


# TODO 该代码不可用,需要后续调试.
import requests
# 广州天气信息网址: http://www.tqyb.com.cn/
response = requests.get("https://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q=广州")
print(response.json()["current"]["temp_c"])  # 输出广州当前温度

