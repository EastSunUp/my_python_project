
# TODO 本部分内待完善,代码欠缺 2025/07/11

import mysql.connector
from mysql.connector import Error
import datetime


class MySQLDatabase:
    def __init__(self, host, user, password, database=None):
        """
        初始化数据库连接参数
        :param host: 数据库主机地址
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名（可选）
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        连接到MySQL数据库
        """
        try:
            connection_params = {
                'host': self.host,
                'user': self.user,
                'password': self.password,
            }

            # 如果指定了数据库，添加到连接参数
            if self.database:
                connection_params['database'] = self.database

            self.connection = mysql.connector.connect(**connection_params)

            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print(f"成功连接到MySQL服务器，版本: {db_info}")

                # 创建游标对象
                self.cursor = self.connection.cursor()
                self.cursor.execute("SELECT DATABASE()")
                database_name = self.cursor.fetchone()[0]
                print(f"当前数据库: {database_name if database_name else '未选择特定数据库'}")

                return True

        except Error as e:
            print(f"连接数据库时发生错误: {e}")
            return False

    def create_database(self, database_name):
        """
        创建数据库
        """
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            print(f"数据库 '{database_name}' 创建成功或已存在")
            return True
        except Error as e:
            print(f"创建数据库时发生错误: {e}")
            return False

    def use_database(self, database_name):
        """
        选择使用的数据库
        """
        try:
            self.connection.database = database_name
            self.database = database_name
            print(f"已切换到数据库: {database_name}")
            return True
        except Error as e:
            print(f"切换数据库时发生错误: {e}")
            return False

    def create_sample_table(self):
        """
        创建示例表
        """
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                age INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            print("用户表创建成功或已存在")
            return True
        except Error as e:
            print(f"创建表时发生错误: {e}")
            return False

    def insert_sample_data(self):
        """
        插入示例数据
        """
        try:
            # 插入多条数据
            insert_query = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"

            sample_data = [
                ("张三", "zhangsan@example.com", 25),
                ("李四", "lisi@example.com", 30),
                ("王五", "wangwu@example.com", 28),
                ("赵六", "zhaoliu@example.com", 35)
            ]

            self.cursor.executemany(insert_query, sample_data)
            self.connection.commit()
            print(f"成功插入 {self.cursor.rowcount} 条示例数据")
            return True
        except Error as e:
            print(f"插入数据时发生错误: {e}")
            return False

    def query_data(self, query, params=None):
        """
        执行查询并返回结果
        """
        try:
            self.cursor.execute(query, params or ())
            results = self.cursor.fetchall()

            # 获取列名
            column_names = [desc[0] for desc in self.cursor.description]
            print("\n查询结果:")
            print("-" * 50)

            # 打印列名
            print(" | ".join(column_names))
            print("-" * 50)

            # 打印数据
            for row in results:
                print(" | ".join(str(item) for item in row))

            return results
        except Error as e:
            print(f"查询数据时发生错误: {e}")
            return None

    def execute_query(self, query, params=None):
        """
        执行SQL语句（用于INSERT, UPDATE, DELETE等）
        """
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            print(f"查询执行成功，影响行数: {self.cursor.rowcount}")
            return True
        except Error as e:
            print(f"执行查询时发生错误: {e}")
            return False

    def get_table_info(self):
        """
        获取当前数据库中的所有表信息
        """
        try:
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()

            print("\n数据库中的表:")
            for table in tables:
                print(f" - {table[0]}")

            return tables
        except Error as e:
            print(f"获取表信息时发生错误: {e}")
            return None

    def close_connection(self):
        """
        关闭数据库连接
        """
        try:
            if self.connection and self.connection.is_connected():
                if self.cursor:
                    self.cursor.close()
                self.connection.close()
                print("数据库连接已关闭")
        except Error as e:
            print(f"关闭连接时发生错误: {e}")


def main():
    """
    主函数：演示完整的数据库操作
    """
    # 数据库连接配置 - 请根据你的环境修改这些参数
    DB_CONFIG = {
        'host': 'localhost',  # MySQL服务器地址
        'user': 'root',  # MySQL用户名
        'password': '123456',  # MySQL密码
        'database': 'test_db'  # 数据库名称
    }

    # 创建数据库实例
    db = MySQLDatabase(**DB_CONFIG)

    try:
        # 1. 连接到数据库
        if not db.connect():
            return

        # 2. 创建数据库（如果不存在）
        db.create_database(DB_CONFIG['database'])
        # 3. 使用指定数据库
        db.use_database(DB_CONFIG['database'])
        # 4. 创建示例表
        db.create_sample_table()
        # 5. 获取表信息
        db.get_table_info()
        # 6. 插入示例数据
        db.insert_sample_data()
        # 7. 查询所有数据
        db.query_data("SELECT * FROM users")
        # 8. 条件查询
        print("\n=== 条件查询示例 ===")
        db.query_data("SELECT name, email, age FROM users WHERE age > %s", (27,))
        # 9. 更新数据示例
        print("\n=== 更新数据示例 ===")
        db.execute_query("UPDATE users SET age = %s WHERE name = %s", (26, "张三"))
        # 10. 验证更新结果
        db.query_data("SELECT * FROM users WHERE name = %s", ("张三",))

        # 11. 删除数据示例（可选，取消注释以测试）
        # print("\n=== 删除数据示例 ===")
        # db.execute_query("DELETE FROM users WHERE name = %s", ("赵六",))
        # db.query_data("SELECT * FROM users")

    except Exception as e:
        print(f"程序执行过程中发生错误: {e}")
    finally:
        # 确保关闭数据库连接
        db.close_connection()


# 简单的连接测试函数
def simple_connection_test():
    """
    简单的连接测试
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456'
        )

        if connection.is_connected():
            print("简单连接测试成功!")
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"MySQL版本: {version[0]}")

            cursor.close()
            connection.close()

    except Error as e:
        print(f"简单连接测试失败: {e}")


if __name__ == "__main__":
    print("=== MySQL数据库连接演示 ===\n")

    # 运行简单连接测试
    print("1. 运行简单连接测试:")
    simple_connection_test()

    print("\n2. 运行完整功能演示:")
    # 运行完整演示
    main()
