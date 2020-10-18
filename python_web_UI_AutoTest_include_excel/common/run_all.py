# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
import time
import unittest
from tools.HTMLTestRunner_cn import HTMLTestRunner
import logging
from common.ferry_log_operation import my_logging
import os
# from common import read_email_config
from common.ferry_email_manager import EmailManager

my_log = my_logging(level=logging.INFO,
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')


# 获取最新的测试报告
def get_newest_report_file(report_path):
    lists = os.listdir(report_path)  # 返回的是一个列表，列表中元素是目录下所有文件或文件夹的名字
    lists.sort(reverse=False)  # 利用sort()函数对原列表排序。reverse=True是降序。排序规则为升序，括号中不填等价于reverse=False,默认就是升序
    report_file = os.path.join(report_path, lists[-1])  # 找到生成最新的报告文件并返回
    # report_file = report_path+lists[-1]
    return report_file  # 也就是这个get_report_file函数返回的是最新的那个报告文件的路径


def run_all_cases():
    # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
    # a是追加模式，默认如果不写的话，就是追加模式
    # file_handler = logging.FileHandler(filename="..\\log\\" + "AutoTest.log", encoding='utf-8', mode='a')  # 输出到文件
    # console_handler = logging.StreamHandler()  # 输出到控制台
    # logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
    #                     format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',  # 日志格式
    #                     handlers=[file_handler, console_handler]
    #                     )
    my_log.info("********************自动化测试开始********************")
    try:
        # 测试报告所在文件夹
        report_path = "../report/"
        current_time = time.strftime("%Y-%m-%d%H%M%S", time.localtime())
        # 定义测试报告名字
        report_name = "XXX项目_web自动化测试报告_" + current_time + ".html"
        # 测试报告的路径
        report_relative_path = report_path + report_name
        fp = open(report_relative_path, "wb")
        runner = HTMLTestRunner(stream=fp, title="XXX项目_接口自动化测试报告", description="用例执行情况")
        common_path = "./"
        discover = unittest.defaultTestLoader.discover(common_path, "handle_excel_test_cases.py")
        runner.run(discover)
        fp.close()

    except Exception as e:
        my_log.error("出现异常或错误：%s" % e)
    finally:
        my_log.info("*********************自动化测试结束*********************")


if __name__ == "__main__":
    run_all_cases()
    # 当前文件所在目录
    current_file_path = os.path.dirname(__file__)
    # 测试报告的目录   #os.path.dirname(current_file_path)可得到当前文件所在目录的上一层目录
    report_path = os.path.join(os.path.dirname(current_file_path), "report")
    # 调用 获取最新测试报告 方法
    report_file = get_newest_report_file(report_path)

    # 邮箱配置，邮箱信息获取
    # smtp_server = read_email_config.smtp_server
    # port = read_email_config.port
    # sender = read_email_config.sender
    # psw = read_email_config.psw
    # receiver = read_email_config.receiver

    smtp_server = "xx.xx.xx"
    port = "25"
    sender = "xx@xx.xx"
    psw = "xxx"
    receiver = "xx@xx.xx"
    # EmailManager(smtp_server, port, sender, psw, receiver).ferry_send_email(report_file)  # 调用发送邮件方法
