# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
import os
import configparser

# os.path.realpath(__file__):  #返回当前文件的绝对路径
# os.path.dirname():  #返回（）所在目录
# cur_path = os.path.dirname(os.path.realpath(__file__))  #获取当前文件所在的目录绝对路径。
config_path = "../config/"
email_config_path = os.path.join(config_path, "email_config.ini")  # 路径拼接
conf = configparser.ConfigParser()  # configparser模块中的ConfigParser类中read方法用来读取配置文件（.ini类型文件）
conf.read(email_config_path, encoding="UTF-8")

# get(section,option)  #得到section中option的值，返回为string类型  section就是邮箱配置文件方括号中的email,option就是smtp_server这些
smtp_server = conf.get("email", "smtp_server")
port = conf.get("email", "port")
sender = conf.get("email", "sender")
psw = conf.get("email", "psw")
receiver = conf.get("email", "receiver")
