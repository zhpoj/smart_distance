import os
from dotenv import load_dotenv
load_dotenv()
import logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
import mysql.connector

class DataBaseConnection:
    def __init__(self):
        self.host=os.getenv("MYSQL_HOST","localhost")
        self.port=os.getenv("MYSQL_PORT","3306")
        self.user=os.getenv("MYSQL_USER_NAME","root")
        self.password=os.getenv("MYSQL_USER_PASSWORD","root")
        self.db_name=os.getenv("MYSQL_DB_NAME","ai_distance")
        
        # 调试信息：打印实际读取的配置
        logger.info(f"数据库配置 - 主机:{self.host}, 端口:{self.port}, 用户:{self.user}, 数据库:{self.db_name}")

        self.connection=None
        self.cursor=None

    def initialize_connection(self)->bool:

        try:
            self.connection=mysql.connector.connect(user=self.user,
                                                    password=self.password,
                                                    host=self.host,
                                                    port=self.port,
                                                    database=self.db_name,
                                                    charset="utf8")

            self.cursor=self.connection.cursor(dictionary=True)
            logger.info(f"数据库{self.db_name}链接初始化成功")
            return True


        except mysql.connector.Error as e:
            logger.error(f"数据库{self.db_name}链接初始化失败:{e}")
            return False


    def disconnect_disconnection(self)->bool:
        if self.cursor:
            self.cursor.close()
            self.cursor=None

        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection=None

    def __enter__(self):

        if self.initialize_connection():
            logger.info("数据库初始化成功")
            return self
        else:
            raise Exception("数据库连接初始化失败")

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.disconnect_disconnection()


def test_connection():
    with DataBaseConnection() as db:
        db.cursor.execute("select 1")
        test_res=db.cursor.fetchall()
        if test_res:
            print(f"测试数据库连接成功，查询结果是：{test_res}")
        else:
            print("测试数据库连接失败")
if __name__=="__main__":
    print("测试数据库连接可用性：")
    test_connection()






