

user = {'name': 'Bob', 'age': 30}

# 方法1: in 关键字（最佳实践）
if 'name' in user:
    print(f"用户名: {user['name']}")

# 方法2: get()方法
email = user.get('email')
if email:
    print(f"邮箱: {email}")

# 方法3: 同时检查多个键
required_keys = ['name', 'age', 'email']
missing_keys = [key for key in required_keys if key not in user]
if missing_keys:
    print(f"缺少以下键: {missing_keys}")

# 方法4: 使用字典视图的交集
keys_to_check = {'name', 'email'}
existing_keys = keys_to_check & user.keys()
print(f"存在的键: {existing_keys}")


