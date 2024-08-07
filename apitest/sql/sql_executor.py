import random

import mysql.connector
from mysql.connector import Error
import logging

from apitest.api.utils.utils import generate_random_string


# 单例模式，确保程序运行中只有一个mysql链接实例
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


# 数据库操作类
class DBExecutor(metaclass=SingletonMeta):
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None

    # 数据库链接操作
    def connect(self):
        if self.conn is None:
            try:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
            except Exception as e:
                logging.info(f"Error connecting to MySQL Platform: {e}")
        return self.conn

    # 数据库关闭连接操作
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    # 插入sql
    def insert_sql(self, query, data):
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, data)
            self.conn.commit()
            print("Record inserted successfully")
        except Error as e:
            print(f"Failed to insert record into table: {e}")
        finally:
            if cursor:
                cursor.close()

    # 查询sql
    def describe_sql(self, query, data=None):
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(query, data)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Failed to read data from table: {e}")
        finally:
            if cursor:
                cursor.close()

    # 更新sql
    def update_sql(self, query, data):
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, data)
            self.conn.commit()
            print("Record updated successfully")
        except Error as e:
            print(f"Failed to update record in table: {e}")
        finally:
            if cursor:
                cursor.close()

    # 删除SQL
    def delete_sql(self, query, data):
        cursor = None

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, data)
            self.conn.commit()
            print("Record deleted successfully")
        except Error as e:
            print(f"Failed to delete record from table: {e}")
        finally:
            if cursor:
                cursor.close()


if __name__ == "__main__":
    # 使用单例模式的数据库连接
    db = DBExecutor('localhost', 'apitest', 'root', 'test@123456')
    db.connect()

    table = "cluster"
    cluster_id = generate_random_string("cc", 10)
    name = generate_random_string("AutoTest", 20)
    desc = "faf"
    version = "1.24"
    cni_plugin = "flannel"
    delete_protection = 0
    status_phase = "Creating"
    status_condition_type = "Progressing"

    create_query_new = "INSERT INTO cluster (cluster_id, name, description, version, cni_plugin, delete_protection, status_phase, status_condition_type) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    create_data = (cluster_id, name, desc, version, cni_plugin, delete_protection, status_phase, status_condition_type)
    db.insert_sql(create_query_new, create_data)


# Read
# read_query = "SELECT * FROM users WHERE age > %s"
# read_data = (25,)
# users = db.read(read_query, read_data)
# for user in users:
#     print(user)
#
# # Update
# update_query = "UPDATE users SET age = %s WHERE name = %s"
# update_data = (35, "John Doe")
# db.update(update_query, update_data)
#
# # Delete
# delete_query = "DELETE FROM users WHERE name = %s"
# delete_data = ("John Doe",)
# db.delete(delete_query, delete_data)

    db.close()
