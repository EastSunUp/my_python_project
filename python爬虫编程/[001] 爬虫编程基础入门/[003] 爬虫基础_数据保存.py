import csv

# 接单时客户最常要的CSV格式
with open('movies.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['排名', '电影名称', '评分'])  # 写表头

    # 示例数据（实际替换为爬取数据）
    writer.writerow([1, '肖申克的救赎', 9.7])
    writer.writerow([2, '霸王别姬', 9.6])

print("数据已保存到movies.csv")

