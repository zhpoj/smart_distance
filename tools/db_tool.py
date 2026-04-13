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

        if exc_type:
            logger.error(f"数据库异常: {exc_val}")
        return False

def get_all_menu_items() -> str: #定义的全局方法
    try :
        with DataBaseConnection() as db:
            query_sql="""
            SELECT
            id,dish_name,description,price,category,spice_level,flavor,main_ingredients,cooking_method,
            is_vegetarian,allergens,is_available
            FROM menu_items
            where is_available=1
            ORDER BY category,dish_name
            """
            db.cursor.execute(query_sql)
            menu_items = db.cursor.fetchall()

            if not menu_items:
                logger.info("当前无可用的商品信息")
                return "当前无可用的菜品信息"

            menu_strings = []
            for item in menu_items:
                # 4.1 处理字符串类型的值
                # 菜品描述处理
                description_text = item.get('description', '') if item.get('description', '').strip() else "未知描述"
                # 过敏原处理
                allergens_text = item.get('allergens', '') if item.get('allergens', '').strip() else "无过敏原"
                # 处理主要食材
                main_ingredients_text = item.get('main_ingredients', '') if item.get('main_ingredients',
                                                                                     '').strip() else "未知食材"

                # 4.2 处理数字类型的值
                # 辣度转换
                spice_level = {"0": "不辣", "1": "微辣", "2": "中辣", "3": "重辣"}
                spice_text = spice_level.get(item["spice_level"], "未知辣度")

                # 4.3 处理布尔类型的值
                #  是否素食转换
                vegetarian_text = "是" if item['is_vegetarian'] else "否"

                # 4.4 拼接每个菜品的完整信息字符串
                menu_string = f"菜品ID:{item['id']}|菜品名称:{item['dish_name']}|价格:¥{item['price']:.2f}|菜品描述:{description_text}|分类:{item['category']}|辣度:{spice_text}|口味:{item['flavor']}|主要食材:{main_ingredients_text}|烹饪方法:{item['cooking_method']}|素食:{vegetarian_text}|过敏原:{allergens_text}"
                menu_strings.append(menu_string)
                # 将所有菜品信息用换行符连接成一个大字符串
            all_menu_info = "\n".join(menu_strings)
            logger.info(f"已成功查询到菜品信息，菜品数量: {len(menu_strings)}个")
            return all_menu_info
    except Exception as e:
        logger.error(f"查询菜品信息失败: {e}")
        return "查询菜品信息失败"
        

def test_connection():
    with DataBaseConnection() as db:
        db.cursor.execute("select 1")
        test_res=db.cursor.fetchall()
        if test_res:
            print(f"测试数据库连接成功，查询结果是：{test_res}")
        else:
            print("测试数据库连接失败")
if __name__=="__main__":
    #print("测试数据库连接可用性：")
    #test_connection()
    print("测试所有菜品信息")
    menu_res=get_all_menu_items()
    print(menu_res)




