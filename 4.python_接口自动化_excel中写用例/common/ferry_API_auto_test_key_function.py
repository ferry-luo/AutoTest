# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
import os
import unittest
import math
import logging
import requests
import json
from common import ferry_log

# 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
# a是追加模式，默认如果不写的话，就是追加模式
# file_handler = logging.FileHandler(filename="..\\log\\" + "AutoTest.log", encoding='utf-8', mode='a')  # 输出到文件
# console_handler = logging.StreamHandler()  # 输出到控制台
# logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
#                     format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',  # 日志格式
#                     handlers=[file_handler, console_handler]
#                     )
my_log = ferry_log.my_logging(level=logging.INFO,
                              format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')


# 将关键字函数封装
class FerryAutoTestKeyFunction(unittest.TestCase):
    def setUp(self):
        self.host = "http://test-01.biostime.us"
        self.port = 80
        self.timeout = 10.0

    # 获取token
    def obtain_token(self):
        headers = {"Content-Type": "application/json", "AccessKeyId": "SVNodVZlQnpmdWFP",
                   "Signature": "94d24144b3e34c80fd579496a345e595cd919f49", "Timestamp": "1569374123550"}
        datas = {"functionId": 0,
                 "interceptParam": None,
                 "intervalTime": 5000,
                 "needIntercept": False,
                 "request": {
                     "device":
                         {"appVer": 141, "appVerName": "8.4.2.1", "brand": "OnePlus", "devToken": None,
                          "deviceId": "869897031963639", "dpi": None, "height": 2074, "model": "ONEPLUS A6000",
                          "os": "android", "osVer": "9", "width": 1080},
                     "isMixPassword": True, "operator": "13964293010", "password": "6e0fc086c40cebeedf45c0dbc4c2a81d",
                     "passwordLength": 6},
                 "seqNo": "1569374123541",
                 "sourceSystem": "MKT_ANDROID",
                 "url": "https://test-01.biostime.us/merchant-server/merchant/system/login/login",
                 "version": None
                 }
        d = json.dumps(datas, separators=(",", ":"))
        print(d)

        url = self.host + "/merchant-server/merchant/system/login/login"
        response = requests.post(url=url, headers=headers, data=d, timeout=float(self.timeout))
        result = response.json()
        # print(self.result)
        # self.assertEqual(self.result['code'], 100)
        # self.assertEqual(self.result['desc'], '成功')
        return result['response']['token']

    # 获取cookies
    def obtain_cookies(self):
        # 在通过requests.post()进行POST请求时，传入报文的参数有两个，一个是data，一个是json
        # data与json既可以是str类型，也可以是dict类型
        # data为dict时，如果不指定Content-Type，默认为application/x-www-form-urlencoded，相当于普通form表单提交的形式
        # data为str时，如果不指定Content-Type，默认为text/plain
        # json为dict时，如果不指定Content-Type，默认为application/json
        # json为str时，如果不指定Content-Type，默认为application/json
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        url = "http://127.0.0.1:8000/users/user_login/"
        data = {"username": "lfl19961119@163.com", "password": "123456789"}
        response = requests.post(url=url, headers=headers, data=data)
        cookies_dict = requests.utils.dict_from_cookiejar(response.cookies)
        return cookies_dict

    # 断言方法之ferry_assertEqual_complete
    def ferry_assertEqual_complete(self, request_type, url, headers, parameters, body, expect_result, need_token,
                                   need_cookie):
        '''

        :param request_type: 请求类型
        :param url: 请求的接口地址
        :param headers: 请求头
        :param parameters: get请求的参数
        :param body: post请求的参数
        :param expect_result: 预期结果
        :param need_token: 是否需要token
        :param need_cookie: 是否需要cookie
        :return:
        '''
        assert_result = {"status": "", "cell_color": "000000"}
        try:
            # 如果单元格填了内容，要提取内容需要用eval()。
            # 但当单元格没填内容，也就是None,eval()处理时会报错，eval()的参数需是str类型，所以需将None转为"{}"
            headers = eval(self.ferry_None_to_dict(headers))
            parameters = eval(self.ferry_None_to_dict(parameters))
            cookies = None
            if need_token == "Y":
                headers["token"] = self.obtain_token()
            if need_cookie == "Y":
                cookies = self.obtain_cookies()
            if request_type == "get":
                response = requests.get(url=url, headers=headers, params=parameters, cookies=cookies)
                response_json = response.json()
                self.assertEqual(response_json, eval(expect_result))
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if request_type == "post":
                response = requests.post(url=url, headers=headers,
                                         json=eval(self.ferry_None_to_dict(body)), cookies=cookies)
                response_json = response.json()
                self.assertEqual(response_json, eval(expect_result))
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
        except AssertionError as e:
            my_log.error("断言不通过：%s" % e)
            raise self.failureException(e)
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            raise Exception(e)
        return assert_result

    # 断言方法之ferry_assertEqual
    def ferry_assertEqual(self, request_type, url, headers, parameters, body, hierarchy_1,
                          hierarchy_2, hierarchy_3, hierarchy_4, at_number_of_hierarchy, expect_result,
                          expect_result_type, need_token, need_cookie):
        '''

        :param request_type:请求类型
        :param url:请求的接口地址
        :param headers:请求头
        :param parameters:get请求的参数
        :param body:post请求的参数
        :param at_number_of_hierarchy:要断言的字段所在层级数
        :param hierarchy_1:第1层字段
        :param hierarchy_2:第2层字段
        :param hierarchy_3:第3层字段
        :param hierarchy_4:第4层字段
        :param expect_result:预期结果
        :param expect_result_type:预期结果的数据类型
        :param need_token:是否需要token
        :param need_cookie:是否需要cookie
        :return:
        '''
        assert_result = {"status": "", "cell_color": "000000"}
        try:
            # 如果单元格填了内容，要提取内容需要用eval()。
            # 但当单元格没填内容，也就是None,eval()处理时会报错，eval()的参数需是str类型，所以需将None转为"{}"
            headers = eval(self.ferry_None_to_dict(headers))
            parameters = eval(self.ferry_None_to_dict(parameters))
            cookies = None
            if need_token == "Y":
                headers["token"] = self.obtain_token()
            if need_cookie == "Y":
                cookies = self.obtain_cookies()
            if expect_result_type == "str":
                expect_result = str(expect_result)
            if expect_result_type == "int":
                expect_result = int(expect_result)
            if expect_result_type == "float":
                expect_result = float(expect_result)
            if expect_result == "bool":
                expect_result = self.ferry_str_to_bool(expect_result)
            if request_type == "get":
                response = requests.get(url=url, headers=headers, params=parameters, cookies=cookies)
                response_json = response.json()
                if int(at_number_of_hierarchy) == 1:
                    self.assertEqual(response_json[hierarchy_1], expect_result)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if int(at_number_of_hierarchy) == 2:
                    self.assertEqual(response_json[hierarchy_1][hierarchy_2], expect_result)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if int(at_number_of_hierarchy) == 3:
                    self.assertEqual(response_json[hierarchy_1][hierarchy_2][hierarchy_3], expect_result)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if int(at_number_of_hierarchy) == 4:
                    self.assertEqual(response_json[hierarchy_1][hierarchy_2][hierarchy_3][hierarchy_4], expect_result)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
            if request_type == "post":
                response = requests.post(url=url, headers=headers,
                                         json=eval(self.ferry_None_to_dict(body)), cookies=cookies)
                response_json = response.json()
                if int(at_number_of_hierarchy) == 1:
                    self.assertEqual(response_json[hierarchy_1], expect_result)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if int(at_number_of_hierarchy) == 2:
                    self.assertEqual(response_json[hierarchy_1][hierarchy_2], expect_result)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if int(at_number_of_hierarchy) == 3:
                    self.assertEqual(response_json[hierarchy_1][hierarchy_2][hierarchy_3], expect_result)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if int(at_number_of_hierarchy) == 4:
                    self.assertEqual(response_json[hierarchy_1][hierarchy_2][hierarchy_3][hierarchy_4], expect_result)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
        except AssertionError as e:
            my_log.error("断言不通过：%s" % e)
            raise self.failureException(e)
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            raise Exception(e)
        return assert_result

    # 断言方法之assertIn
    def ferry_assertIn(self, request_type, url, headers, parameters, body,
                       expect_result, need_token, need_cookie):
        '''

        :param request_type:请求类型
        :param url:请求的接口地址
        :param headers:请求头
        :param parameters:get请求的参数
        :param body:post请求的参数
        :param expect_result:预期结果
        :param need_token:是否需要token
        :param need_cookie:是否需要cookie
        :return:
        '''
        assert_result = {"status": "", "cell_color": "000000"}
        try:
            # 如果单元格填了内容，要提取内容需要用eval()。
            # 但当单元格没填内容，也就是None,eval()处理时会报错，eval()的参数需是str类型，所以需将None转为"{}"
            headers = eval(self.ferry_None_to_dict(headers))
            parameters = eval(self.ferry_None_to_dict(parameters))
            cookies = None
            if need_token == "Y":
                headers["token"] = self.obtain_token()
            if need_cookie == "Y":
                cookies = self.obtain_cookies()
            if request_type == "get":
                response = requests.get(url=url, headers=headers, params=parameters, cookies=cookies)
                response_json = response.json()
                self.assertIn(expect_result.replace("\"", "\'"), str(response_json))
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if request_type == "post":
                response = requests.post(url=url, headers=headers,
                                         json=eval(self.ferry_None_to_dict(body)), cookies=cookies)
                response_json = response.json()
                self.assertIn(expect_result.replace("\"", "\'"), str(response_json))
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
        except AssertionError as e:
            my_log.error("断言不通过：%s" % e)
            raise self.failureException(e)
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            raise Exception(e)
        return assert_result

    # 将None转为空字符串
    def ferry_None_to_str(self, value):
        if value == None:
            return ""
        return value

    # 将None转为"{}"
    def ferry_None_to_dict(self, value):
        if value == None:
            return "{}"
        return value

    # 将字符串转布尔值
    def ferry_str_to_bool(self, value):
        if value == "true" or value == "True":
            return True
        if value == "false" or value == "False":
            return False

    def tearDown(self):
        pass
