# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
import os
import unittest
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from tools.HTMLTestRunner_cn import HTMLTestRunner
# from common import read_email_config
from common.ferry_email_manager import EmailManager
from common.ferry_log import my_logging
import logging

my_log = my_logging(level=logging.INFO,
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def add_case():
    """第一步：加载所有测试用例 也就是把所有用例放到一个容器中"""
    # 第1种，用相对路径
    # case_path = './test_cases/'

    # 第2种，用绝对路径（备注：当你搭建了jenkins，通过jenkins跑脚本，则一定要用绝对路径，因为jenkins处理不了相对路径）
    # 当前文件所在的目录
    current_file_path = os.path.dirname(
        __file__)  # 返回示例：'Y:\python_接口自动化_通过编写多个函数进行参数化\common'   如果current_file_path在多个函数中用到，可直接在本文件的前面定义（在import下方），避免重复写这代码
    case_path = os.path.join(os.path.dirname(current_file_path),
                             "test_cases")  # 返回示例：'Y:\python_接口自动化_通过编写多个函数进行参数化\test_cases'
    # 若文件夹不存在就创建一个文件夹(其实这是冗余的，我注释掉代码。你写好了你的用例，肯定是已经创建好用例目录并把用例文件放进去了)
    # if not os.path.exists(case_path):
    #     os.mkdir(case_path)
    discover = unittest.defaultTestLoader.discover(case_path, 'test_*.py')  # case目录下的所有test_开头的文件都会被执行，*号表示匹配任意字符
    return discover  # 这个add_case函数返回的是discover这个容器，这个容器装的是所有的用例


def run_case(all_case):
    """第二步：执行所有的用例，并把结果写入到html测试报告中"""
    my_log.info("********************自动化测试开始********************")
    try:
        now = time.strftime("%Y-%m-%d-%H%M%S")  # 返回示例：'2019-08-01-07:10:22'
        report_file_name = "XX项目_接口自动化测试报告_" + now + '.html'
        current_file_path = os.path.dirname(__file__)

        report_path = os.path.join(os.path.dirname(current_file_path), "report")
        # report_path = "Y:\\python_接口自动化_通过编写多个函数进行参数化\\report\\"    # 这个写法有个缺陷，这个自动化测试套给到别人，别人的电脑不一定是这个路径
        # report_path = r"Y:\python_接口自动化_通过编写多个函数进行参数化\report\"  # 复制windows上路径时，要么将'\'写为'\\'（因为在Python中，一个'\'表示转义的意思），要么就在前面加个字母r

        report_abspath = os.path.join(report_path, report_file_name)
        # report_abspath = report_path + report_file_name  # 如果你不想用os.path.join()，而是用'+'号拼接字符串，则一定要注意report_path表示的字符串最后要有'/'或'\\'

        fp = open(report_abspath, "wb")  # wb表示以二进制格式打开报告文件，进行写入（w就是write写入的意思，b就是binary二进制的意思）
        runner = HTMLTestRunner(stream=fp, title="接口自动化测试报告，测试结果如下：", description="用例执行情况")
        # 调用add_case函数。实际上就是执行add_case函数返回的discover，而discover就是所有的test开头的.py用例文件
        runner.run(all_case)
        fp.close()
    except Exception as e:
        my_log.error("出现异常或错误：%s" % e)
    finally:
        my_log.info("*********************自动化测试结束*********************")


def get_report_file(report_path):
    """第三步：获取最新的测试报告"""
    lists = os.listdir(report_path)  # 返回的是一个列表，列表中元素是目录下所有文件或文件夹的名字
    lists.sort(reverse=False)  # 利用sort()函数对原列表排序。reverse=True是降序。排序规则为升序，括号中不填等价于reverse=False,sort()函数默认就是升序
    my_log.info("最新测试生成的报告：" + lists[-1])  # 由于是升序，根据对报告文件的命名规则可知，最新的那个报告的名称当然就是最后一个元素
    report_file = os.path.join(report_path, lists[-1])  # 找到生成最新的报告文件
    return report_file  # 返回最新的那个报告文件的路径


if __name__ == '__main__':
    # 初始化接口测试数据
    # test_data.init_data()
    # 加载用例
    all_the_cases = add_case()
    # 执行所有的用例
    run_case(all_the_cases)
    # 当前文件所在的目录
    current_file_path = os.path.dirname(__file__)  # 返回示例：'Y:\python_接口自动化_通过编写多个函数进行参数化\common'
    # 测试报告目录
    report_path = os.path.join(os.path.dirname(current_file_path), "report")
    report_file = get_report_file(report_path)  # 调用 获取最新测试报告 方法

    # 邮箱配置，邮箱信息获取
    # smtp_server = read_email_config.smtp_server
    # port = read_email_config.port
    # sender = read_email_config.sender
    # psw = read_email_config.psw
    # receiver = read_email_config.receiver

    # 邮箱信息，直接赋值的方式
    smtp_server = 'xx.xx.xx'
    port = 25
    sender = 'x@x.x'
    psw = 'xx'
    receiver = 'x@x.x'

    # 在config目录下的email_config.ini文件填写好smtp服务器、端口、发件人的邮箱号、发件人的密码（不是邮箱密码，是开启了smtp服务后的密码，自行百度）、收件人邮箱号
    # 如果出现configparser.NoSectionError: No section: 'email' ，则说明你的ini文件有问题，请在pycharm安装ini插件。实在解决不了就直接赋值（直接赋值的方式在上面已给出），不通过ini文件获取，并且注释掉from common import read_email_config
    # 在本文件的send_mail函数中，修改为你想写的内容（例如：落款填你自己的名字）
    # 当需要把测试报告发送邮件，把下面这行代码的注释放开
    # EmailManager(smtp_server, port, sender, psw, receiver).ferry_send_email(report_file)  # 调用发送邮件方法

    # schedule.every().day.at("17:20").do(m.send_mail,smtp_server, port, sender, psw, receiver, report_file)    #本行代码可不使用，如需要定时运行自动化测试，可搭建jenkins，自行百度学习
