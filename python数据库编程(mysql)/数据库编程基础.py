
import mysql.connector

# 创建数据库连接
mydb = mysql.connector.connect(
    host="localhost",  # 数据库主机地址
    user="yourusername",  # 数据库用户名
    passwd="yourpassword"  # 数据库密码
)

print(mydb)

# 创建数据库
mydb2 = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456"
)

mycursor = mydb2.cursor()

mycursor.execute("CREATE DATABASE runoob_db")


