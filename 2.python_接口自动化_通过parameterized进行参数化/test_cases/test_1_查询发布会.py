# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
import unittest
import requests
from parameterized import parameterized
import xlrd
import json
from common.excel_xlsx_operation import ExcelOperate
from common.ferry_log import my_logging
import logging

my_log = my_logging(level=logging.INFO,
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')


# 将查询发布会接口的测试用例封装成一个类
class TestQueryEventInfo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = "https://ferry1119.com:8000"
        cls.url = cls.host + "/query_event_post"
        cls.api_name = "查询发布会('%s')" % cls.url
        cls.timeout = 60.0
        my_log.info("********************接口'%s'的自动化测试用例执行开始********************" % cls.api_name)

    @parameterized.expand([
        ("event_name_reasonable", "存在的发布会名称", "", "小米10", "查询成功"),
        ("event_name_no_exist", "不存在的发布会名称", "", "小米9", "查询结果为空"),
        ("event_name_null", "发布会名称为null", "", None, "查询结果为空"),
        ("event_name_other_character", "发布会名称为其他字符", "", ",,..", "查询结果为空")
    ])
    def test_query_event(cls, case_id, case_title, event_id, event_name, message):
        try:
            headers = {"Content-Type": "application/json"}
            datas = {"event_id": event_id, "event_name": event_name}
            response = requests.post(url=cls.url, json=datas, headers=headers, timeout=float(cls.timeout))
            result = response.json()
            cls.assertEqual(result["meta"]["message"], message)
            my_log.info("用例'%s'的执行状态为:pass" % case_title)
        except AssertionError as e:
            my_log.info("用例'%s'的执行状态为:fail" % case_title)
            my_log.error("用例不通过的说明：%s" % e)
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            raise Exception(e)

    @classmethod
    def tearDownClass(cls):
        my_log.info("*********************接口'%s'的自动化测试用例执行结束*********************" % cls.api_name)


if __name__ == "__main__":
    unittest.main()
