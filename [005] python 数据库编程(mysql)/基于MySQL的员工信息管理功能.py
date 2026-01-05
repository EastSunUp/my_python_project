

import mysql.connector
from mysql.connector import Error


def create_connection():
    """
    创建MySQL数据库连接
    请修改以下连接参数以匹配你的MySQL环境
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",  # 数据库主机地址
            user="root",  # 数据库用户名
            password="123456",  # 数据库密码
            database="company_db"  # 数据库名称,如果不存在会自动创建
        )
        if connection.is_connected():
            print("成功连接到MySQL数据库")
            return connection
    except Error as e:
        print(f"连接数据库时发生错误: '{e}'")
        return None


def create_database_and_table(connection):
    """
    创建数据库和员工表（如果不存在）
    """
    try:
        cursor = connection.cursor()

        # 创建数据库 (如果不存在)
        cursor.execute("CREATE DATABASE IF NOT EXISTS company_db")
        cursor.execute("USE company_db")

        # 创建员工表
        create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            position VARCHAR(100),
            department VARCHAR(100),
            salary DECIMAL(10, 2),
            hire_date DATE
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("数据库和表准备就绪")

    except Error as e:
        print(f"创建数据库和表时发生错误: '{e}'")
    finally:
        if cursor:
            cursor.close()


def insert_employee(connection, name, position, department, salary, hire_date):
    """
    向员工表插入新员工记录
    """
    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO employees (name, position, department, salary, hire_date)
        VALUES (%s, %s, %s, %s, %s)
        """
        record = (name, position, department, salary, hire_date)
        cursor.execute(insert_query, record)
        connection.commit()
        print(f"员工 {name} 的记录插入成功")

    except Error as e:
        print(f"插入员工记录时发生错误: '{e}'")
    finally:
        if cursor:
            cursor.close()


def query_employees(connection):
    """
    查询并显示所有员工记录
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employees")
        records = cursor.fetchall()

        print("\n=== 员工列表 ===")
        for row in records:
            print(f"ID: {row[0]}, 姓名: {row[1]}, 职位: {row[2]}, 部门: {row[3]}, 薪资: {row[4]}, 入职日期: {row[5]}")
        print(f"总共查询到 {len(records)} 条记录")

    except Error as e:
        print(f"查询员工记录时发生错误: '{e}'")
    finally:
        if cursor:
            cursor.close()


def update_employee_salary(connection, employee_id, new_salary):
    """
    更新员工薪资
    """
    try:
        cursor = connection.cursor()
        update_query = "UPDATE employees SET salary = %s WHERE id = %s"
        cursor.execute(update_query, (new_salary, employee_id))
        connection.commit()
        print(f"员工ID {employee_id} 的薪资已更新为 {new_salary}")

    except Error as e:
        print(f"更新员工薪资时发生错误: '{e}'")
    finally:
        if cursor:
            cursor.close()


def delete_employee(connection, employee_id):
    """
    根据ID删除员工记录
    """
    try:
        cursor = connection.cursor()
        delete_query = "DELETE FROM employees WHERE id = %s"
        cursor.execute(delete_query, (employee_id,))
        connection.commit()
        print(f"员工ID {employee_id} 的记录已删除")

    except Error as e:
        print(f"删除员工记录时发生错误: '{e}'")
    finally:
        if cursor:
            cursor.close()


def main():
    """
    主函数：演示完整的数据库操作流程
    """
    connection = None
    try:
        # 1. 建立数据库连接
        connection = create_connection()
        if connection is None:
            return

        # 2. 创建数据库和表
        create_database_and_table(connection)

        # 3. 插入示例员工数据
        print("\n--- 插入员工数据 ---")
        insert_employee(connection, "张三", "软件工程师", "技术部", 15000.00, "2023-01-15")
        insert_employee(connection, "李四", "产品经理", "产品部", 18000.00, "2022-08-20")
        insert_employee(connection, "王五", "UI设计师", "设计部", 12000.00, "2023-03-10")

        # 4. 查询显示所有员工
        query_employees(connection)

        # 5. 更新员工薪资
        print("\n--- 更新员工薪资 ---")
        update_employee_salary(connection, 1, 16000.00)  # 更新张三的薪资

        # 6. 再次查询显示更新后的数据
        query_employees(connection)

        # 7. 删除一个员工（可选，取消注释以测试）
        # print("\n--- 删除员工 ---")
        # delete_employee(connection, 3)  # 删除王五
        # query_employees(connection)

    except Error as e:
        print(f"主程序执行过程中发生错误: '{e}'")
    finally:
        # 8. 关闭数据库连接
        if connection and connection.is_connected():
            connection.close()
            print("\n数据库连接已关闭")


if __name__ == "__main__":
    main()
