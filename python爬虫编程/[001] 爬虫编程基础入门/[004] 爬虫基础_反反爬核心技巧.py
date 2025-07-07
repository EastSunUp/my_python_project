

import random
import time

# 技巧1：随机延迟（避免被封）
delay = random.uniform(1, 3)  # 1~3秒随机延迟
time.sleep(delay)

# 技巧2：轮换User-Agent
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15'
]
headers = {'User-Agent': random.choice(user_agents)}

