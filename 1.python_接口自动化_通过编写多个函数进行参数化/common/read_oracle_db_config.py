# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
# 我在config目录下写了两个读取数据库配置文件（read_mysql_dbconfig和read_oracle_dbconfig），当公司中具体项目是用的什么数据库服务器，就对应用写哪一种文件。
from cx_Oracle import connect  # cx_Oracle是要安装了才有，不是写这句代码就意味着导入进来了
import os  # os库提供很多方法，用来处理文件和目录
import configparser  # 在Python中，configparser模块中的ConfigParser类用来读取配置文件（也就是.ini类型文件）

# 封装数据库操作的大致步骤：建立连接、获取游标、执行SQL语句、提交（有几种语句需要commit)、关闭游标、断开与数据库的连接


dbconfig_path = "../config/oracle_db_config.ini"
cf = configparser.ConfigParser()  # 给ConfigParser类创建对象，初始化
# 读取配置文件，第一个参数就是配置文件所在的绝对路径，第二个参数是设定编码
cf.read(dbconfig_path, encoding='UTF-8')

ho = cf.get("oracleconf", "ho")
port = cf.get("oracleconf", "port")
db = cf.get("oracleconf", "db")
user = cf.get("oracleconf", "user")
password = cf.get("oracleconf", "password")


# 封装ORACLE数据库基本操作
class DB:
    def __init__(self):
        try:
            # 连接数据库
            self.connection = connect(host=ho,
                                      port=port,
                                      user=user,
                                      password=password,
                                      db=db,
                                      charset="utf8")
        except Exception as e:  # 抛出带参数的异常，我这里设的参数是e，这个随意，各个单词、字母都行
            print("oracle error:%s" % e)

    # 定义 清除表中数据 的函数
    def clear(self, table_name):
        # 如果是要删表中所有数据还可以使用truncate
        # real_sql="truncate "+table+";"
        real_sql = "delete " + table_name + ";"  # 这句代码表示的SQL语句就是 delete 某个表名; ①写死的关键词就直接双引号括起来,有空格就一定要打上空格符②变动的东西就用一个对象表示，用C或C++解释就是用一个变量表示，在某个地方赋值给这个变量就行。③用+号进行连接
        with self.connection.cursor() as x:
            # cursor方法是操作游标execute方法执行SQL语句
            # 如果表和表之间建立了外键约束，则无法删除表及修改表结构。在Mysql中取消外键约束:  SET FOREIGN_KEY_CHECKS=0;
            x.execute("SET FOREIGN_KEY_CHECKS = 0;")
            x.execute(real_sql)
        # 还有一种写法--创建对象
        # c = self.conn.cursor()
        # c.execute(real_sql)
        self.connection.commit()

    # 定义 向表中插入初始数据 的函数。比如我之后一个测试数据是要测重复的shop_id，要数据库表中先有个初始数据shop_id才可能重复，不然怎么会重复。所以要定义这么一个函数，并在创建数据库表数据那里（db_fixture下的test_data）调用它
    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) + "'"  # 先将字段（列名）强制类型转换成字符串，再打上引号则成为键
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = "INSERT INTO " + table_name + "(" + key + ") values(" + value + ")" + ";"
        # 第一种写法
        with self.connection.cursor() as cursor:
            cursor.execute(real_sql)
        self.connection.commit()

        # 第二种写法，直接创建一个对象
        '''
        a = self.conn.cursor()
        a.execute(real_sql)
        '''

    # 定义 关闭数据库连接 的函数
    def close(self):
        self.connection.close()  # conn指向connect类，connect()类中有个close方法或者叫函数是用来关闭数据库连接的

    def init_data(self, datas):
        for table, data in datas.items():
            for d in data:
                self.insert(table, d)  # for循环嵌套。打个比方有两个表，那么先对第一个表调用clear函数，然后把对数据调用insert函数。再到外面那个循环，对第二个表操作。
        self.close()


if __name__ == "__main__":
    database = DB()
    table_name = "dl_barcode_info"
    data = {"serial_code": "34343434343434", "midcode": "0", "big_code": "555555555555555555555555", "product_id": 857,
            "serial_type": 3, "dealer_id": 100603, "batch": "6142201808142", "storehouse_code": 1000,
            "upload_time": "to_date('2018-08-15 09:30:20','yyyy-mm-dd hh24:mi:ss')", "position": 2, "status": 2,
            "split_type": 0, "delivery_Type": 1, "destination_id": 100603, "destination_name": "杭州黄浦贸易有限公司",
            "destination_type": 3, "destination_time": "to_date('2019-01-24 09:16:10','yyyy-mm-dd hh24:mi:ss')"}
    database.insert(table_name, data)
