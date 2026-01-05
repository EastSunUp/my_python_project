
# TODO 代码欠缺,内容未补充完整

import requests
import csv
import time
import json

# 这里的代码是通过高德地图获取对应的劳务中介的相关信息.

# 高德API配置（需自行注册）
API_KEY = "your_api_key_here"  # 替换为实际API Key
API_URL = "https://restapi.amap.com/v3/place/text"

# 爬取参数配置
KEYWORDS = ["劳务中介", "人力资源", "劳务派遣", "人才派遣"]
CITY_DISTRICTS = {
    "顺德区": "440606",
    "三水区": "440607",
    "禅城区": "440604",
    "南海区": "440605"
}
OUTPUT_FILE = "foshan_labor_agencies.csv"


def fetch_poi_data(keyword, district, page=1):
    """从高德API获取POI数据"""
    params = {
        "key": API_KEY,
        "keywords": keyword,
        "city": district,
        "offset": "25",  # 每页记录数
        "page": page,
        "extensions": "all",  # 获取详细信息
        "output": "json"
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    return None


def parse_poi_data(json_data):
    """解析API返回的POI数据"""
    results = []
    if json_data["status"] == "1" and int(json_data["count"]) > 0:
        for poi in json_data["pois"]:
            # 获取电话号码（多个号码用分号分隔）
            phone = poi.get("tel", "")
            phones = phone.split(";") if phone else []

            # 过滤无效号码
            valid_phones = [p.strip() for p in phones
                            if p.strip() and len(p.strip()) >= 7]

            # 构造结果对象
            result = {
                "name": poi.get("name", ""),
                "address": poi.get("address", ""),
                "phones": ";".join(valid_phones),
                "district": poi.get("adname", ""),
                "location": poi.get("location", "")
            }
            results.append(result)
    return results


def save_to_csv(data, filename):
    """保存结果到CSV文件"""
    if not data:
        return

    with open(filename, "w", newline="", encoding="utf-8-sig") as csvfile:
        fieldnames = ["name", "phones", "address", "district", "location"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"已保存 {len(data)} 条数据到 {filename}")


def main():
    all_results = []

    for district, code in CITY_DISTRICTS.items():
        print(f"\n开始爬取 {district} 区...")

        for keyword in KEYWORDS:
            print(f"  搜索关键词: {keyword}")
            page = 1
            total_pages = 1

            while page <= total_pages:
                data = fetch_poi_data(keyword, code, page)
                if not data:
                    break

                # 解析数据
                results = parse_poi_data(data)
                all_results.extend(results)

                # 更新分页信息
                count = int(data.get("count", 0))
                total_pages = min(10, (count + 24) // 25)  # 高德限制最多1000条

                print(f"    第 {page}/{total_pages} 页: 获取 {len(results)} 条记录")

                # 翻页并延迟防止请求过快
                page += 1
                time.sleep(0.5)  # 遵守API请求频率限制

    # 去重处理
    unique_results = {f"{item['name']}{item['address']}": item
                      for item in all_results}.values()

    # 保存结果
    save_to_csv(unique_results, OUTPUT_FILE)

if __name__ == "__main__":
    main()
