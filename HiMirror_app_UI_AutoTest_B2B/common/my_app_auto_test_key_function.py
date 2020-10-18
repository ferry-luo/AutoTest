# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
import os
import unittest
from appium import webdriver
import os
import time
from PIL import Image
from functools import reduce
import operator
import logging
from selenium.common.exceptions import NoSuchElementException
import math
from common import my_log_operation

my_log = my_log_operation.my_logging(level=logging.INFO,
                                     format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')


# 将关键字函数封装
class MyAutoTestKeyFunction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
        # a是追加模式，默认如果不写的话，就是追加模式
        # file_handler = logging.FileHandler(filename="..\\log\\" + "AutoTest.log", encoding='utf-8', mode='a')  # 输出到文件
        # console_handler = logging.StreamHandler()  # 输出到控制台
        # logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
        #                     format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',  # 日志格式
        #                     handlers=[file_handler, console_handler]
        #                     )
        pass

    #
    def my_choice_driver(cls, automation_name):
        # 连APP的一些初始化信息
        if automation_name == "UiAutomator1":
            cls.d = {
                "deviceName": "CN42191M00057",
                "platformName": "Android",
                "platformVersion": "5.0",
                "appPackage": "com.himirror.mirrorxsmax",
                "appActivity": "com.himirror.mirrorxsmax.CustomerHome.HomeActivity",
                "unicodeKeyboard": True,  # 使用unicode编码方式发送字符串
                "resetKeyboard": True,  # 屏蔽软键盘
                "automationName": "UiAutomator1"
            }
        else:
            cls.d = {
                "deviceName": "CN42191M00057",
                "platformName": "Android",
                "platformVersion": "5.0",
                "appPackage": "com.himirror.mirrorxsmax",
                "appActivity": "com.himirror.mirrorxsmax.CustomerHome.HomeActivity",
                "unicodeKeyboard": True,  # 使用unicode编码方式发送字符串
                "resetKeyboard": True,  # 屏蔽软键盘
            }
        cls.dr = webdriver.Remote("http://localhost:4723/wd/hub", cls.d)  # 访问服务接口，启动APP
        return cls.dr

    # 保存截图
    def my_save_screenshot(cls, filename):
        '''

        :param filename: 图片名称
        :return:
        '''
        current_file_path = os.path.dirname(__file__)
        screenshot_path = os.path.join(os.path.dirname(current_file_path), "screenshot")
        current_day = time.strftime("%Y%m%d", time.localtime(time.time()))
        screenshot_day_path = os.path.join(screenshot_path, current_day)
        if not os.path.exists(screenshot_day_path):
            os.mkdir(screenshot_day_path)
        current_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        file_path = os.path.join(screenshot_day_path, current_time + "_" + filename + ".png")
        try:
            # cls.dr.save_screenshot(file_path)
            cls.dr.get_screenshot_as_file(file_path)
            my_log.info("截图成功：%s" % file_path)
        except NameError as e:
            my_log.error("对象未声明或未初始化：%s" % e)
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
        return file_path

    # 人为主观截图
    def my_save_screenshot_by_human_subjectivity(cls, filename):
        '''

        :param filename: 图片名称
        :return:
        '''
        current_file_path = os.path.dirname(__file__)
        screenshot_path = os.path.join(os.path.dirname(current_file_path), "screenshot_by_human_subjectivity")
        current_day = time.strftime("%Y%m%d", time.localtime(time.time()))
        screenshot_day_path = os.path.join(screenshot_path, current_day)
        if not os.path.exists(screenshot_day_path):
            os.mkdir(screenshot_day_path)
        current_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        file_path = os.path.join(screenshot_day_path, current_time + "_" + filename + ".png")
        operate_result = {"status": "", "cell_color": "000000", "img_path": "", "path_color": "000000"}
        try:
            # cls.dr.save_screenshot(file_path)
            cls.dr.get_screenshot_as_file(file_path)
            my_log.info("截图成功：%s" % file_path)
            operate_result = {"status": "pass", "cell_color": "00FF00", "img_path": file_path,
                              "path_color": "00BFFF"}
        except NameError as e:
            my_log.error("对象未声明或未初始化：%s" % e)
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
        return operate_result

    # 通过对比度判断两个图片是否一致   备注：当图片一致，返回浮点型0.0
    def my_image_contrast(cls, img1, img2):
        '''

        :param img1: 图1
        :param img2: 图2
        :return:
        '''
        image1 = Image.open(img1)
        image2 = Image.open(img2)

        h1 = image1.histogram()
        h2 = image2.histogram()

        contrast_result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
        return contrast_result

    # 向左滑动
    def my_swipe_left_base_on_window(cls, duration, frequency):
        '''

        :param duration: 滑动时长
        :param frequency: 滑动次数
        :return:
        '''
        try:
            s = cls.dr.get_window_size()
            x1 = int(s["width"] * 0.9)
            y1 = int(s["height"] * 0.5)
            x2 = int(s["width"] * 0.1)
            for i in range(frequency):
                cls.dr.swipe(x1, y1, x2, y1, duration)
            operate_result = {"status": "pass", "cell_color": "00FF00"}
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 向右滑动
    def my_swipe_right_base_on_window(cls, duration, frequency):
        '''

        :param duration: 滑动时长
        :param frequency: 滑动次数
        :return:
        '''
        try:
            s = cls.dr.get_window_size()
            x1 = int(s["width"] * 0.1)
            y1 = int(s["height"] * 0.5)
            x2 = int(s["width"] * 0.9)
            for i in range(frequency):
                cls.dr.swipe(x1, y1, x2, y1, duration)
            operate_result = {"status": "pass", "cell_color": "00FF00"}
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 向上滑动  duration为滑动时长，frequency为滑动次数
    def my_swipe_up_base_on_window(cls, duration, frequency):
        '''

        :param duration: 滑动时长
        :param frequency: 滑动次数
        :return:
        '''
        try:
            s = cls.dr.get_window_size()
            x1 = int(s["width"] * 0.5)
            y1 = int(s["height"] * 0.9)
            y2 = int(s["height"] * 0.1)
            for i in range(frequency):
                cls.dr.swipe(x1, y1, x1, y2, duration)
            operate_result = {"status": "pass", "cell_color": "00FF00"}
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 向下滑动  duration为滑动时长，frequency为滑动次数
    def my_swipe_down_base_on_window(cls, duration, frequency):
        '''

        :param duration: 滑动时长
        :param frequency: 滑动次数
        :return:
        '''
        try:
            s = cls.dr.get_window_size()
            x1 = int(s["width"] * 0.5)
            y1 = int(s["height"] * 0.1)
            y2 = int(s["height"] * 0.9)
            for i in range(frequency):
                cls.dr.swipe(x1, y1, x1, y2, duration)
            operate_result = {"status": "pass", "cell_color": "00FF00"}
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 滑动
    def my_swipe_base_on_coordinate(cls, x1, y1, x2, y2, duration):
        '''

        :param x1: 起点的横坐标
        :param y1: 起点的纵坐标
        :param x2: 终点的横坐标
        :param y2: 终点的纵坐标
        :param duration: 滑动时长
        :return:
        '''
        try:
            cls.dr.swipe(x1, y1, x2, y2, duration)
            operate_result = {"status": "pass", "cell_color": "00FF00"}
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 点击元素操作
    def my_click(cls, way, element, x1, y1, x2, y2):
        '''

        :param way: 定位元素的方式
        :param element: 定位元素方式对应的表达式
        :param x1: 定位元素左上角的横坐标
        :param y1: 定位元素左上角的纵坐标
        :param x2: 定位元素右下角的横坐标
        :param y2: 定位元素右下角的纵坐标
        :return:
        '''
        if way != None:
            way = way.strip()
        if element != None:
            element = element.strip()
        operate_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                cls.dr.find_element_by_id(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "xpath":
                cls.dr.find_element_by_xpath(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "coordinate":
                cls.dr.tap([(int(x1), int(y1)), (int(x2), int(y2))], 100)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "text":
                ele = 'new UiSelector().text("%s")' % element
                cls.dr.find_element_by_android_uiautomator(ele).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "resourceId":
                ele = 'new UiSelector().resourceId("%s")' % element
                cls.dr.find_element_by_android_uiautomator(ele).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
        except NoSuchElementException as e:
            my_log.error("没找到元素或元素尚未加载出来：%s" % e)
            raise NoSuchElementException(e)
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 输入数据操作
    def my_send_keys(cls, way, element, data):
        '''

        :param way: 定位元素的方式
        :param element: 定位元素方式对应的表达式
        :param data: 要输入的数据
        :return:
        '''
        if way != None:
            way = way.strip()
        if element != None:
            element = element.strip()
        operate_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                cls.dr.find_element_by_id(element).send_keys(data)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "xpath":
                cls.dr.find_element_by_xpath(element).send_keys(data)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "text":
                ele = 'new UiSelector().text("%s")' % element
                cls.dr.find_element_by_android_uiautomator(ele).send_keys(data)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "resourceId":
                ele = 'new UiSelector.resourceId("%s")' % element
                cls.dr.find_element_by_android_uiautomator(ele).send_keys(data)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
        except NoSuchElementException as e:
            my_log.error("没找到元素或元素尚未加载出来：%s" % e)
            raise NoSuchElementException(e)
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 操作系统按键
    def my_press_keycode(cls, value):
        '''

        :param value:系统按键对应的数字
        :return:
        '''
        try:
            cls.dr.press_keycode(int(value))
            operate_result = {"status": "pass", "cell_color": "00FF00"}
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 断言方法之assertTrue_is_displayed  断言通过了的，status为pass；断言不通过的，status为fail
    def my_assertTrue_is_displayed(cls, way, element):
        '''

        :param way: 定位元素的方式
        :param element: 定位元素方式对应的表达式
        :return:
        '''
        if way != None:
            way = way.strip()
        if element != None:
            element = element.strip()
        assert_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                cls.assertTrue(cls.dr.find_element_by_id(element).is_displayed())
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "xpath":
                cls.assertTrue(cls.dr.find_element_by_xpath(element).is_displayed())
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "text":
                ele = 'new UiSelector().text("%s")' % element
                cls.assertTrue(cls.dr.find_element_by_android_uiautomator(ele).is_displayed())
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "resourceId":
                ele = 'new UiSelector().resourceId("%s")' % element
                cls.assertTrue(cls.dr.find_element_by_android_uiautomator(ele).is_displayed())
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
        except NoSuchElementException as e:
            my_log.error("没找到元素或元素尚未加载出来：%s" % e)
            cls.my_save_screenshot("NoSuchElementException")
            raise NoSuchElementException(e)
        except AssertionError as e:
            my_log.error("断言不通过")
            cls.my_save_screenshot("assertTrue_is_displayed_fail")
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            cls.my_save_screenshot("happen_error")
            raise Exception(e)
        return assert_result

    # 断言方法之my_assertTrue_is_not_displayed
    def my_assertTrue_is_not_displayed(cls, way, element):
        '''

        :param way: 定位元素的方式
        :param element: 定位元素方式对应的表达式
        :return:
        '''
        if way != None:
            way = way.strip()
        if element != None:
            element = element.strip()
        assert_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                if not cls.dr.find_element_by_id(element).is_displayed():
                    my_log.info("断言通过")
                else:
                    print("元素是可见的")
                    my_log.error("断言不通过")
                    cls.my_save_screenshot("assertTrue_is_not_displayed_fail")
                    raise cls.failureException
            if way == "xpath":
                if not cls.dr.find_element_by_xpath(element).is_displayed():
                    my_log.info("断言通过")
                else:
                    print("元素是可见的")
                    my_log.error("断言不通过")
                    cls.my_save_screenshot("assertTrue_is_not_displayed_fail")
                    raise cls.failureException
            if way == "text":
                ele = 'new UiSelector().text("%s")' % element
                if not cls.dr.find_element_by_android_uiautomator(ele).is_displayed():
                    my_log.info("断言通过")
                else:
                    print("元素是可见的")
                    my_log.error("断言不通过")
                    cls.my_save_screenshot("assertTrue_is_not_displayed_fail")
                    raise cls.failureException
            if way == "resourceId":
                ele = 'new UiSelector().resourceId("%s")' % element
                if not cls.dr.find_element_by_android_uiautomator(ele).is_displayed():
                    my_log.info("断言通过")
                else:
                    print("元素是可见的")
                    my_log.error("断言不通过")
                    cls.my_save_screenshot("assertTrue_is_not_displayed_fail")
                    raise cls.failureException
        except NoSuchElementException:
            assert_result = {"status": "pass", "cell_color": "00FF00"}
        return assert_result

    # 断言方法之assertTrue_compare
    def my_assertTrue_compare(cls, way, element, compare_operator, compare_num):
        '''

        :param way: 定位元素的方式
        :param element: 定位元素方式对应的表达式
        :param compare_operator: 比较运算符，目前涉及的为 < 和 >
        :param compare_num:被比较的数值
        :return:
        '''
        if way != None:
            way = way.strip()
        if element != None:
            element = element.strip()
        # 断言通过了的，status为pass；断言不通过的，status为fail；其他情况（如断言前没找到元素或元素尚未加载出来）的，status为uncertain
        assert_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                if compare_operator == ">":
                    cls.assertTrue(float(cls.dr.find_element_by_id(element).text.strip("%")) > float(compare_num))
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if compare_operator == "<":
                    cls.assertTrue(float(cls.dr.find_element_by_id(element).text.strip("%")) < float(compare_num))
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
            if way == "xpath":
                if compare_operator == ">":
                    cls.assertTrue(
                        float(cls.dr.find_element_by_xpath(element).text.strip("%")) > float(compare_num))
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if compare_operator == "<":
                    cls.assertTrue(
                        float(cls.dr.find_element_by_xpath(element).text.strip("%")) < float(compare_num))
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
            if way == "text":
                if compare_operator == ">":
                    ele = 'new UiSelector().text("%s")' % element
                    cls.assertTrue(
                        float(cls.dr.find_element_by_android_uiautomator(ele).text.strip("%")) > float(compare_num)
                    )
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if compare_operator == "<":
                    ele = 'new UiSelector().text("%s")' % element
                    cls.assertTrue(
                        float(cls.dr.find_element_by_android_uiautomator(ele).text.strip("%")) < float(compare_num)
                    )
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
            if way == "resourceId":
                if compare_operator == ">":
                    ele = 'new UiSelector().resourceId("%s")' % element
                    cls.assertTrue(
                        float(cls.dr.find_element_by_android_uiautomator(ele).text.strip("%")) > float(compare_num)
                    )
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if compare_operator == "<":
                    ele = 'new UiSelector().resourceId("%s")' % element
                    cls.assertTrue(
                        float(cls.dr.find_element_by_android_uiautomator(ele).text.strip("%")) < float(compare_num)
                    )
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
        except NoSuchElementException as e:
            my_log.error("没找到元素或元素尚未加载出来：%s" % e)
            cls.my_save_screenshot("NoSuchElementException")
            raise NoSuchElementException(e)
        except AssertionError as e:
            my_log.error("断言不通过：%s" % e)
            cls.my_save_screenshot("assertTrue_compare_fail")
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            cls.my_save_screenshot("happen_error")
            raise Exception(e)
        return assert_result

    # 断言方法之assertEqual
    def my_assertEqual(cls, way, element, expect_content):
        '''

        :param way: 定位元素的方式
        :param element: 定位元素方式对应的表达式
        :param expect_content: 期望结果
        :return:
        '''
        if way != None:
            way = way.strip()
        if element != None:
            element = element.strip()
        assert_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                cls.assertEqual(cls.dr.find_element_by_id(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "xpath":
                cls.assertEqual(cls.dr.find_element_by_xpath(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "text":
                ele = 'new UiSelector().text("%s")' % element
                cls.assertEqual(cls.dr.find_element_by_android_uiautomator(ele).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "resourceId":
                ele = 'new UiSelector().resourceId("%s")' % element
                cls.assertEqual(cls.dr.find_element_by_android_uiautomator(ele).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
        except NoSuchElementException as e:
            my_log.error("没找到元素或元素尚未加载出来：%s" % e)
            cls.my_save_screenshot("NoSuchElementException")
            raise NoSuchElementException(e)
        except AssertionError as e:
            my_log.error("断言不通过：%s" % e)
            cls.my_save_screenshot("assertEqual_fail")
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            cls.my_save_screenshot("happen_error")
            raise Exception(e)
        return assert_result

    # 断言方法之assertNotEqual
    def my_assertNotEqual(cls, way, element, expect_content):
        '''

        :param way: 定位元素的方式
        :param element: 定位元素方式对应的表达式
        :param expect_content: 期望结果
        :return:
        '''
        if way != None:
            way = way.strip()
        if element != None:
            element = element.strip()
        assert_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                cls.assertNotEqual(cls.dr.find_element_by_id(element).text, cls.my_None_to_str(expect_content))
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "xpath":
                cls.assertNotEqual(cls.dr.find_element_by_xpath(element).text,
                                   cls.my_None_to_str(expect_content))
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "text":
                ele = 'new UiSelector().text("%s")' % element
                cls.assertNotEqual(cls.dr.find_element_by_android_uiautomator(ele).text,
                                   cls.my_None_to_str(expect_content))
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "resourceId":
                ele = 'new UiSelector().resourceId("%s")' % element
                cls.assertNotEqual(cls.dr.find_element_by_android_uiautomator(ele).text,
                                   cls.my_None_to_str(expect_content))
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
        except NoSuchElementException as e:
            my_log.error("没找到元素或元素尚未加载出来：%s" % e)
            cls.my_save_screenshot("NoSuchElementException")
            raise NoSuchElementException(e)
        except AssertionError as e:
            my_log.error("断言不通过：%s" % e)
            cls.my_save_screenshot("assertNotEqual_fail")
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            cls.my_save_screenshot("happen_error")
            raise Exception(e)
        return assert_result

    # 断言方法之assertIn
    def my_assertIn(cls, way, element, expect_content):
        '''

        :param way: 定位元素的方式
        :param element: 定位元素方式对应的表达式
        :param expect_content: 期望结果
        :return:
        '''
        if way != None:
            way = way.strip()
        if element != None:
            element = element.strip()
        assert_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                cls.assertIn(expect_content, cls.dr.find_element_by_id(element).text)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "xpath":
                cls.assertIn(expect_content, cls.dr.find_element_by_xpath(element).text)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "text":
                ele = 'new UiSelector().text("%s")' % element
                cls.assertIn(expect_content, cls.dr.find_element_by_android_uiautomator(ele).text)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "resourceId":
                ele = 'new UiSelector().resourceId("%s")' % element
                cls.assertIn(expect_content, cls.dr.find_element_by_android_uiautomator(ele).text)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
        except NoSuchElementException as e:
            my_log.error("没找到元素或元素尚未加载出来：%s" % e)
            cls.my_save_screenshot("NoSuchElementException")
            raise NoSuchElementException(e)
        except AssertionError as e:
            my_log.error("断言不通过：%s" % e)
            cls.my_save_screenshot("assertIn_fail")
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("出现异常或错误：%s" % e)
            cls.my_save_screenshot("happen_error")
            raise Exception(e)
        return assert_result

    # 停顿/思考时间
    def my_sleep(cls, seconds):
        '''

        :param seconds: 停顿秒数
        :return:
        '''
        time.sleep(seconds)

    # 将None转为空字符串
    def my_None_to_str(cls, value):
        if value == None:
            return ""
        return value

    @classmethod
    def tearDownClass(cls):
        cls.dr.quit()
