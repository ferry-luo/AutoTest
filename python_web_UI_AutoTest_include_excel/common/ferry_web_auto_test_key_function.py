# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import os
import time
from PIL import Image
import math
from functools import reduce
import operator
import logging
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from common.ferry_log_operation import my_logging

my_log = my_logging(level=logging.INFO,
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')


# 将关键字函数封装
class FerryAutoTestKeyFunction(unittest.TestCase):
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

    # def setUp(self):
    #     # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
    #     # a是追加模式，默认如果不写的话，就是追加模式
    #     file_handler = logging.FileHandler(filename="..\\log\\" + "AutoTest.log", encoding='utf-8', mode='a')  # 输出到文件
    #     console_handler = logging.StreamHandler()  # 输出到控制台
    #     logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
    #                         format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',  # 日志格式
    #                         handlers=[file_handler, console_handler]
    #                         )

    # 选择浏览器
    def ferry_choice_browser(cls, browser):
        if (browser.lower() == "chrome"):
            cls.dr = webdriver.Chrome()
        if (browser.lower() == "firefox"):
            cls.dr = webdriver.Firefox()
        if (browser.lower() == "ie"):
            cls.dr = webdriver.Ie()
        return cls.dr

    # 访问网址
    def ferry_open_url(cls, url):
        try:
            cls.dr.get(url)
            operate_result = {"status": "pass", "cell_color": "00FF00"}
        except Exception as e:
            my_log.error("发生异常或错误:%s" % e)
            raise Exception(e)
        return operate_result

    # 保存截图
    def ferry_save_screenshot(cls, filename):
        current_file_path = os.path.dirname(__file__)
        screenshot_path = os.path.join(os.path.dirname(current_file_path), "screenshot")
        current_day = time.strftime("%Y%m%d", time.localtime(time.time()))
        screenshot_day_path = os.path.join(screenshot_path, current_day)
        if not os.path.exists(screenshot_day_path):
            os.mkdir(screenshot_day_path)
        current_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        file_path = os.path.join(screenshot_day_path, filename + "_" + current_time + ".png")
        try:
            # cls.dr.save_screenshot(file_path)
            cls.dr.get_screenshot_as_file(file_path)
            my_log.info("截图成功：%s" % file_path)
        except NameError as e:
            my_log.error("对象未声明或未初始化：%s" % e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
        return file_path

    # 人为主观截图
    def ferry_save_screenshot_by_human_subjectivity(cls, filename):
        current_file_path = os.path.dirname(__file__)
        screenshot_path = os.path.join(os.path.dirname(current_file_path), "screenshot_by_human_subjectivity")
        current_day = time.strftime("%Y%m%d", time.localtime(time.time()))
        screenshot_day_path = os.path.join(screenshot_path, current_day)
        if not os.path.exists(screenshot_day_path):
            os.mkdir(screenshot_day_path)
        current_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        file_path = os.path.join(screenshot_day_path, filename + "_" + current_time + ".png")
        operate_result = {"status": "", "cell_color": "000000", "img_path": "", "path_color": "000000"}
        try:
            # cls.dr.save_screenshot(file_path)
            cls.dr.get_screenshot_as_file(file_path)
            my_log.info("截图成功：%s" % file_path)
            operate_result = {"status": "pass", "cell_color": "00FF00", "img_path": file_path, "path_color": "00BFFF"}
        except NameError as e:
            my_log.error("对象未声明或未初始化：%s" % e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
        return operate_result

    # 通过对比度判断两个图片是否一致   备注：当图片一致，返回浮点型0.0
    def ferry_image_contrast(cls, img1, img2):
        image1 = Image.open(img1)
        image2 = Image.open(img2)

        h1 = image1.histogram()
        h2 = image2.histogram()

        contrast_result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
        return contrast_result

    # 点击元素操作
    def ferry_click(cls, way, element):
        operate_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                cls.dr.find_element_by_id(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "name":
                cls.dr.find_element_by_name(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "class_name":
                cls.dr.find_element_by_class_name(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "tag_name":
                cls.dr.find_element_by_tag_name(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "link_text":
                cls.dr.find_element_by_link_text(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "partial_link_text":
                cls.dr.find_element_by_partial_link_text(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "xpath":
                cls.dr.find_element_by_xpath(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "css_selector":
                cls.dr.find_element_by_css_selector(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
        except NoSuchElementException as e:
            my_log.error("没找到元素或页面元素未加载完全：%s" % e)
            raise NoSuchElementException(e)
        except ElementNotVisibleException as e:
            my_log.error("元素不可见：%s" % e)
            raise ElementNotVisibleException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 输入数据操作
    def ferry_send_keys(cls, way, element, data):
        operate_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                cls.dr.find_element_by_id(element).send_keys(data)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "name":
                cls.dr.find_element_by_name(element).send_keys(data)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "class_name":
                cls.dr.find_element_by_class_name(element).send_keys(data)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "tag_name":
                cls.dr.find_element_by_tag_name(element).send_keys(data)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "link_text":
                cls.dr.find_element_by_link_text(element).send_keys(data)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "partial_link_text":
                cls.dr.find_element_by_partial_link_text(element).send_keys(data)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "xpath":
                cls.dr.find_element_by_xpath(element).send_keys(data)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "css_selector":
                cls.dr.find_element_by_css_selector(element).send_keys(data)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
        except NoSuchElementException as e:
            my_log.error("没找到元素或页面元素未加载完全：%s" % e)
            raise NoSuchElementException(e)
        except ElementNotVisibleException as e:
            my_log.error("元素不可见：%s" % e)
            raise ElementNotVisibleException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 光标悬停
    def ferry_cursor_hover(cls, way, element):
        operate_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                loc = cls.dr.find_element_by_id(element)
                ActionChains(cls.dr).move_to_element(loc).perform()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "name":
                loc = cls.dr.find_element_by_name(element)
                ActionChains(cls.dr).move_to_element(loc).perform()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "class_name":
                loc = cls.dr.find_element_by_class_name(element)
                ActionChains(cls.dr).move_to_element(loc).perform()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "tag_name":
                loc = cls.dr.find_element_by_tag_name(element)
                ActionChains(cls.dr).move_to_element(loc).perform()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "link_text":
                loc = cls.dr.find_element_by_link_text(element)
                ActionChains(cls.dr).move_to_element(loc).perform()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "partial_link_text":
                loc = cls.dr.find_element_by_partial_link_text(element)
                ActionChains(cls.dr).move_to_element(loc).perform()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "xpath":
                loc = cls.dr.find_element_by_xpath(element)
                ActionChains(cls.dr).move_to_element(loc).perform()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "css_selector":
                loc = cls.dr.find_element_by_css_selector(element)
                ActionChains(cls.dr).move_to_element(loc).perform()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
        except NoSuchElementException as e:
            my_log.error("没找到元素或页面元素未加载完全：%s" % e)
            raise NoSuchElementException(e)
        except ElementNotVisibleException as e:
            my_log.error("元素不可见：%s" % e)
            raise ElementNotVisibleException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 通过索引选择选项
    def ferry_select_by_index(cls, way, element, index):
        operate_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                options = cls.dr.find_element_by_id(element)
                Select(options).select_by_index(index)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "name":
                options = cls.dr.find_element_by_name(element)
                Select(options).select_by_index(index)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "class_name":
                options = cls.dr.find_element_by_class_name(element)
                Select(options).select_by_index(index)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "tag_name":
                options = cls.dr.find_element_by_tag_name(element)
                Select(options).select_by_index(index)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "link_text":
                options = cls.dr.find_element_by_link_text(element)
                Select(options).select_by_index(index)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "partial_link_text":
                options = cls.dr.find_element_by_partial_link_text(element)
                Select(options).select_by_index(index)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "xpath":
                options = cls.dr.find_element_by_xpath(element)
                Select(options).select_by_index(index)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "css_selector":
                options = cls.dr.find_element_by_css_selector(element)
                Select(options).select_by_index(index)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
        except NoSuchElementException as e:
            my_log.error("没找到元素或页面元素未加载完全：%s" % e)
            raise NoSuchElementException(e)
        except ElementNotVisibleException as e:
            my_log.error("元素不可见：%s" % e)
            raise ElementNotVisibleException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 通过值选择选项
    def ferry_select_by_value(cls, way, element, value):
        operate_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                options = cls.dr.find_element_by_id(element)
                Select(options).select_by_value(value)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "name":
                options = cls.dr.find_element_by_name(element)
                Select(options).select_by_value(value)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "class_name":
                options = cls.dr.find_element_by_class_name(element)
                Select(options).select_by_value(value)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "tag_name":
                options = cls.dr.find_element_by_tag_name(element)
                Select(options).select_by_value(value)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "link_text":
                options = cls.dr.find_element_by_link_text(element)
                Select(options).select_by_value(value)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "partial_link_text":
                options = cls.dr.find_element_by_partial_link_text(element)
                Select(options).select_by_value(value)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "xpath":
                options = cls.dr.find_element_by_xpath(element)
                Select(options).select_by_value(value)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "css_selector":
                options = cls.dr.find_element_by_css_selector(element)
                Select(options).select_by_value(value)
                operate_result = {"status": "pass", "cell_color": "00FF00"}
        except NoSuchElementException as e:
            my_log.error("没找到元素或页面元素未加载完全：%s" % e)
            raise NoSuchElementException(e)
        except ElementNotVisibleException as e:
            my_log.error("元素不可见：%s" % e)
            raise ElementNotVisibleException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 直接点击选项进行选择
    def ferry_select_direct(cls, way, element):
        operate_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                cls.dr.find_element_by_id(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "name":
                cls.dr.find_element_by_name(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "class_name":
                cls.dr.find_element_by_class_name(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "tag_name":
                cls.dr.find_element_by_tag_name(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "link_text":
                cls.dr.find_element_by_link_text(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "partial_link_text":
                cls.dr.find_element_by_partial_link_text(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "xpath":
                cls.dr.find_element_by_xpath(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "css_selector":
                cls.dr.find_element_by_css_selector(element).click()
                operate_result = {"status": "pass", "cell_color": "00FF00"}
        except NoSuchElementException as e:
            my_log.error("没找到元素或页面元素未加载完全：%s" % e)
            raise NoSuchElementException(e)
        except ElementNotVisibleException as e:
            my_log.error("元素不可见：%s" % e)
            raise ElementNotVisibleException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 切换窗口句柄
    def ferry_switch_window_by_index(cls, index):
        try:
            all_handles = cls.dr.window_handles
            cls.dr.switch_to.window(all_handles[index])
            operate_result = {"status": "pass", "cell_color": "00FF00"}
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 切换frame
    def ferry_switch_frame(cls, way, element):
        operate_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                cls.dr.switch_to.frame(cls.dr.find_element_by_id(element))
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "name":
                cls.dr.switch_to.frame(cls.dr.find_element_by_name(element))
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "class_name":
                cls.dr.switch_to.frame(cls.dr.find_element_by_class_name(element))
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "tag_name":
                cls.dr.switch_to.frame(cls.dr.find_element_by_tag_name(element))
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "link_text":
                cls.dr.switch_to.frame(cls.dr.find_element_by_link_text(element))
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "partial_link_text":
                cls.dr.switch_to.frame(cls.dr.find_element_by_partial_link_text(element))
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "xpath":
                cls.dr.switch_to.frame(cls.dr.find_element_by_xpath(element))
                operate_result = {"status": "pass", "cell_color": "00FF00"}
            if way == "css_selector":
                cls.dr.switch_to.frame(cls.dr.find_element_by_css_selector(element))
                operate_result = {"status": "pass", "cell_color": "00FF00"}
        except NoSuchElementException as e:
            my_log.error("frame not found：%s" % e)
            raise NoSuchElementException(e)
        except ElementNotVisibleException as e:
            my_log.error("frame is not visible:%s" % e)
            raise ElementNotVisibleException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            raise Exception(e)
        return operate_result

    # 断言方法之assertTrue_is_displayed  断言通过了的，status为pass；断言不通过的，status为fail
    def ferry_assertTrue_is_displayed(cls, way, element):
        assert_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                cls.assertTrue(cls.dr.find_element_by_id(element).is_displayed())
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "name":
                cls.assertTrue(cls.dr.find_element_by_name(element).is_displayed())
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "class_name":
                cls.assertTrue(cls.dr.find_element_by_class_name(element).is_dispalyed())
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "tag_name":
                cls.assertTrue(cls.dr.find_element_by_tag_name(element).is_displayed())
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "link_text":
                cls.assertTrue(cls.dr.find_element_by_link_text(element).is_displayed())
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "partial_link_text":
                cls.assertTrue(cls.dr.find_element_by_partial_link_text(element).is_displayed())
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "xpath":
                cls.assertTrue(cls.dr.find_element_by_xpath(element).is_displayed())
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "css_selector":
                cls.assertTrue(cls.dr.find_element_by_css_selector(element).is_displayed())
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
        except NoSuchElementException as e:
            my_log.error("没找到元素或页面元素未加载完全：%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("NoSuchElementException")
            raise NoSuchElementException(e)
        except ElementNotVisibleException as e:
            my_log.error("元素不可见:%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("ElementNotVisibleException")
            raise ElementNotVisibleException(e)
        except AssertionError as e:
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("assertTrue_is_displayed_fail")
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("happen_error")
            raise Exception(e)
        return assert_result

    # 断言方法之assertTrue_is_not_displayed
    def assertTrue_is_not_displayed(cls, way, element):
        assert_result = {"status": "", "cell_color": "00FF00"}
        try:
            if way == "id":
                if not cls.dr.find_element_by_id(element).is_displayed():
                    my_log.info("断言通过")
                else:
                    print("元素是可见的")
                    my_log.error("断言不通过")
                    raise cls.failureException
            if way == "name":
                if not cls.dr.find_element_by_name(element).is_displayed():
                    my_log.info("断言通过")
                else:
                    print("元素是可见的")
                    my_log.error("断言不通过")
                    raise cls.failureException
            if way == "class_name":
                if not cls.dr.find_element_by_class_name(element).is_displayed():
                    my_log.info("断言通过")
                else:
                    print("元素是可见的")
                    my_log.error("断言不通过")
                    raise cls.failureException
            if way == "tag_name":
                if not cls.dr.find_element_by_tag_name(element).is_displayed():
                    my_log.info("断言通过")
                else:
                    print("元素是可见的")
                    my_log.error("断言不通过")
                    raise cls.failureException
            if way == "link_text":
                if not cls.dr.find_element_by_link_text(element).is_displayed():
                    my_log.info("断言通过")
                else:
                    print("元素是可见的")
                    my_log.error("断言不通过")
                    raise cls.failureException
            if way == "partial_link_text":
                if not cls.dr.find_element_by_partial_link_text(element).is_displayed():
                    my_log.info("断言通过")
                else:
                    print("元素是可见的")
                    my_log.error("断言不通过")
                    raise cls.failureException
            if way == "xpath":
                if not cls.dr.find_element_by_xpath(element).is_displayed():
                    my_log.info("断言通过")
                else:
                    print("元素是可见的")
                    my_log.error("断言不通过")
                    raise cls.failureException
            if way == "css_selector":
                if not cls.dr.find_element_by_css_selector(element).is_displayed():
                    my_log.info("断言通过")
                else:
                    print("元素是可见的")
                    my_log.error("断言不通过")
                    raise cls.failureException
        except NoSuchElementException:
            assert_result = {"status": "pass", "cell_color": "00FF00"}
        return assert_result

    # 断言方法之assertTrue_compare
    def ferry_assertTrue_compare(cls, way, element, compare_operator, compare_num):
        # 断言通过了的，status为pass；断言不通过的，status为fail；其他情况（如断言前没找到元素）的，status为uncertain
        assert_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                if compare_operator == ">":
                    cls.assertTrue(int(cls.dr.find_element_by_id(element).text) > compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if compare_operator == "<":
                    cls.assertTrue(int(cls.dr.find_element_by_id(element).text) < compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
            if way == "name":
                if compare_operator == ">":
                    cls.assertTrue(int(cls.dr.find_element_by_name(element).text) > compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if compare_operator == "<":
                    cls.assertTrue(int(cls.dr.find_element_by_name(element).text) < compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
            if way == "class_name":
                if compare_operator == ">":
                    cls.assertTrue(int(cls.dr.find_element_by_class_name(element).text) > compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if compare_operator == "<":
                    cls.assertTrue(int(cls.dr.find_element_by_class_name(element).text) < compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
            if way == "tag_name":
                if compare_operator == ">":
                    cls.assertTrue(int(cls.dr.find_element_by_tag_name(element).text) > compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if compare_operator == "<":
                    cls.assertTrue(int(cls.dr.find_element_by_tag_name(element).text) < compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
            if way == "link_text":
                if compare_operator == ">":
                    cls.assertTrue(int(cls.dr.find_element_by_link_text(element).text) > compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if compare_operator == "<":
                    cls.assertTrue(int(cls.dr.find_element_by_link_text(element).text) < compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
            if way == "partial_link_text":
                if compare_operator == ">":
                    cls.assertTrue(int(cls.dr.find_element_by_partial_link_text(element).text) > compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if compare_operator == "<":
                    cls.assertTrue(int(cls.dr.find_element_by_partial_link_text(element).text) < compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
            if way == "xpath":
                if compare_operator == ">":
                    cls.assertTrue(int(cls.dr.find_element_by_xpath(element).text) > compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if compare_operator == "<":
                    cls.assertTrue(int(cls.dr.find_element_by_xpath(element).text) < compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
            if way == "css_selector":
                if compare_operator == ">":
                    cls.assertTrue(int(cls.dr.find_element_by_css_selector(element).text) > compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
                if compare_operator == "<":
                    cls.assertTrue(int(cls.dr.find_element_by_css_selector(element).text) < compare_num)
                    assert_result = {"status": "pass", "cell_color": "00FF00"}
                    my_log.info("断言通过")
        except NoSuchElementException as e:
            my_log.error("没找到元素或页面元素未加载完全：%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("NoSuchElementException")
            raise NoSuchElementException(e)
        except ElementNotVisibleException as e:
            my_log.error("元素不可见:%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("ElementNotVisibleException")
            raise ElementNotVisibleException(e)
        except AssertionError as e:
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("assertTrue_compare_fail")
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("happen_error")
            raise Exception(e)
        return assert_result

    # 断言方法之assertEqual
    def ferry_assertEqual(cls, way, element, expect_content):
        assert_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                cls.assertEqual(cls.dr.find_element_by_id(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "name":
                cls.assertEqual(cls.dr.find_element_by_name(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "class_name":
                cls.assertEqual(cls.dr.find_element_by_class_name(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "tag_name":
                cls.assertEqual(cls.dr.find_element_by_tag_name(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "link_text":
                cls.assertEqual(cls.dr.find_element_by_link_text(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "partial_link_text":
                cls.assertEqual(cls.dr.find_element_by_partial_link_text(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "xpath":
                cls.assertEqual(cls.dr.find_element_by_xpath(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "css_selector":
                cls.assertEqual(cls.dr.find_element_by_css_selector(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
        except NoSuchElementException as e:
            my_log.error("没找到元素或页面元素未加载完全：%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("NoSuchElementException")
            raise NoSuchElementException(e)
        except ElementNotVisibleException as e:
            my_log.error("元素不可见:%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("ElementNotVisibleException")
            raise ElementNotVisibleException(e)
        except AssertionError as e:
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("assertEqual_fail")
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("happen_error")
            raise Exception(e)
        return assert_result

    # 断言方法之assertEqual_alert
    def ferry_assertEqual_alert(cls, expect_content):
        try:
            alert_text = cls.dr.switch_to.alert.text
            cls.assertEqual(alert_text, expect_content)
            assert_result = {"status": "pass", "cell_color": "00FF00"}
            my_log.info("断言通过")
            cls.dr.switch_to.alert.accept()
        except AssertionError as e:
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("assertEqual_alert_fail")
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("happen_error")
            raise Exception(e)
        return assert_result

    # 断言方法之assertNotEqual
    def ferry_assertNotEqual(cls, way, element, expect_content):
        assert_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                cls.assertNotEqual(cls.dr.find_element_by_id(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "name":
                cls.assertNotEqual(cls.dr.find_element_by_name(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "class_name":
                cls.assertNotEqual(cls.dr.find_element_by_class_name(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "tag_name":
                cls.assertNotEqual(cls.dr.find_element_by_tag_name(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "link_text":
                cls.assertNotEqual(cls.dr.find_element_by_link_text(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "partial_link_text":
                cls.assertNotEqual(cls.dr.find_element_by_partial_link_text(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "xpath":
                cls.assertNotEqual(cls.dr.find_element_by_xpath(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "css_selector":
                cls.assertNotEqual(cls.dr.find_element_by_css_selector(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
        except NoSuchElementException as e:
            my_log.error("没找到元素或页面元素未加载完全：%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("NoSuchElementException")
            raise NoSuchElementException(e)
        except ElementNotVisibleException as e:
            my_log.error("元素不可见:%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("ElementNotVisibleException")
            raise ElementNotVisibleException(e)
        except AssertionError as e:
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("assertNotEqual_fail")
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("happen_error")
            raise Exception(e)
        return assert_result

    # 断言方法之assertIn 预期结果为实际结果的子串
    def ferry_assertIn(cls, way, element, expect_content):
        assert_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                cls.assertIn(expect_content, cls.dr.find_element_by_id(element).text)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "name":
                cls.assertIn(expect_content, cls.dr.find_element_by_name(element).text)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "class_name":
                cls.assertIn(expect_content, cls.dr.find_element_by_class_name(element).text)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "tag_name":
                cls.assertIn(expect_content, cls.dr.find_element_by_tag_name(element).text)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "link_text":
                cls.assertIn(expect_content, cls.dr.find_element_by_link_text(element).text)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "partial_link_text":
                cls.assertIn(expect_content, cls.dr.find_element_by_partial_link_text(element).text)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "xpath":
                cls.assertIn(expect_content, cls.dr.find_element_by_xpath(element).text)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "css_selector":
                cls.assertIn(expect_content, cls.dr.find_element_by_css_selector(element).text)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
        except NoSuchElementException as e:
            my_log.error("没找到元素或页面元素未加载完全：%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("NoSuchElementException")
            raise NoSuchElementException(e)
        except ElementNotVisibleException as e:
            my_log.error("元素不可见:%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("ElementNotVisibleException")
            raise ElementNotVisibleException(e)
        except AssertionError as e:
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("assertIn_fail")
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("happen_error")
            raise Exception(e)
        return assert_result

    # 断言方法之actual_assertIn_expect 实际结果为预期结果的子串
    def ferry_actual_assertIn_expect(cls, way, element, expect_content):
        assert_result = {"status": "", "cell_color": "000000"}
        try:
            if way == "id":
                cls.assertIn(cls.dr.find_element_by_id(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "name":
                cls.assertIn(cls.dr.find_element_by_name(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "class_name":
                cls.assertIn(cls.dr.find_element_by_class_name(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "tag_name":
                cls.assertIn(cls.dr.find_element_by_tag_name(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "link_text":
                cls.assertIn(cls.dr.find_element_by_link_text(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "partial_link_text":
                cls.assertIn(cls.dr.find_element_by_partial_link_text(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "xpath":
                cls.assertIn(cls.dr.find_element_by_xpath(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
            if way == "css_selector":
                cls.assertIn(cls.dr.find_element_by_css_selector(element).text, expect_content)
                assert_result = {"status": "pass", "cell_color": "00FF00"}
                my_log.info("断言通过")
        except NoSuchElementException as e:
            my_log.error("没找到元素或页面元素未加载完全：%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("NoSuchElementException")
            raise NoSuchElementException(e)
        except ElementNotVisibleException as e:
            my_log.error("元素不可见:%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("ElementNotVisibleException")
            raise ElementNotVisibleException(e)
        except AssertionError as e:
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("assertIn_fail")
            raise cls.failureException(e)
        except Exception as e:
            my_log.error("发生异常或错误：%s" % e)
            my_log.error("断言不通过")
            cls.ferry_save_screenshot("happen_error")
            raise Exception(e)
        return assert_result

    # 停留
    def ferry_sleep(cls, seconds):
        time.sleep(seconds)

    # def tearDown(self):
    #     self.dr.quit()
    @classmethod
    def tearDownClass(cls):
        cls.dr.quit()
