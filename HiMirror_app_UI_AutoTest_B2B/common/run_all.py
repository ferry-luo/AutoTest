# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
import time
import unittest
from tools.HTMLTestRunner_cn import HTMLTestRunner
import logging
from common import my_log_operation

my_log = my_log_operation.my_logging(level=logging.INFO,
                                     format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')


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
        t = time.localtime()
        current_time = time.strftime("%Y-%m-%d%H%M%S", t)
        # 定义测试报告名字
        report_name = current_time + "_" + "HiMirror_B2B_UI_AutoTest" + ".html"
        # 测试报告的路径
        report_relative_path = report_path + report_name
        fp = open(report_relative_path, "wb")
        runner = HTMLTestRunner(stream=fp, title="HiMirror_B2B_UI自动化测试报告", description="用例执行情况")
        common_path = "./"
        discover = unittest.TestLoader().discover(common_path, "handle_excel_test_cases.py")
        runner.run(discover)
        fp.close()
    except Exception as e:
        my_log.error("出现异常或错误：%s" % e)
    finally:
        my_log.info("*********************自动化测试结束*********************")


if __name__ == "__main__":
    run_all_cases()
