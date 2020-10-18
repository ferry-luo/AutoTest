# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
import unittest
import requests
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
        cls.parametric_data_file_path = "../parametric_data/参数化.xlsx"
        cls.parametric_data_sheet_name = "查询发布会"
        cls.parametric_data = ExcelOperate(cls.parametric_data_file_path, cls.parametric_data_sheet_name)
        # 拿到event_name列的数据
        cls.event_name_list = cls.parametric_data.get_col_values(
            cls.parametric_data.get_col_index("event_name") + 1)
        my_log.info("********************接口'%s'的自动化测试用例执行开始********************" % cls.api_name)

    # 存在的发布会名称
    def test_1_query_event_reasonable(cls):
        case_title = "存在的发布会名称"
        try:
            headers = {"Content-Type": "application/json"}
            datas = {"event_id": "", "event_name": cls.event_name_list[1]}
            response = requests.post(url=cls.url, json=datas, headers=headers, timeout=float(cls.timeout))
            result = response.json()
            cls.assertEqual(result["meta"]["message"], "查询成功")
            cls.assertEqual(result["correct"], True)
            cls.assertEqual(result["data"][0]["get_event_name"], "小米10")
            my_log.info("用例'%s'的执行状态为:pass" % case_title)
        except AssertionError as e:
            my_log.info("用例'%s'的执行状态为:fail" % case_title)
            my_log.error("用例不通过的说明：%s" % e)
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            raise Exception(e)

    # 不存在的发布会名称
    def test_2_query_event_no_exist(cls):
        case_title = "不存在的发布会名称"
        try:
            datas = {"event_id": "", "event_name": cls.event_name_list[2]}
            response = requests.post(url=cls.url, json=datas, timeout=float(cls.timeout))
            result = response.json()
            cls.assertEqual(result["meta"]["message"], "查询结果为空")
            cls.assertEqual(result["correct"], False)
            my_log.info("用例'%s'的执行状态为:pass" % case_title)
        except AssertionError as e:
            my_log.info("用例'%s'的执行状态为:fail" % case_title)
            my_log.error("用例不通过的说明：%s" % e)
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            raise Exception(e)

    # 发布会名称为null
    def test_3_query_event_null(cls):
        case_title = "发布会名称为null"
        try:
            datas = {"event_id": "", "event_name": cls.event_name_list[3]}
            response = requests.post(url=cls.url, json=datas, timeout=float(cls.timeout))
            result = response.json()
            cls.assertEqual(result["meta"]["message"], "查询结果为空")
            cls.assertEqual(result["correct"], False)
            my_log.info("用例'%s'的执行状态为:pass" % case_title)
        except AssertionError as e:
            my_log.info("用例'%s'的执行状态为:fail" % case_title)
            my_log.error("用例不通过的说明：%s" % e)
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            raise Exception(e)

    # 发布会名称为其他字符
    def test_4_query_event_other_character(cls):
        case_title = "发布会名称为其他字符"
        try:
            datas = {"event_id": "", "event_name": cls.event_name_list[4]}
            response = requests.post(url=cls.url, json=datas, timeout=float(cls.timeout))
            result = response.json()
            cls.assertEqual(result["meta"]["message"], "查询结果为空")
            cls.assertEqual(result["correct"], False)
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
