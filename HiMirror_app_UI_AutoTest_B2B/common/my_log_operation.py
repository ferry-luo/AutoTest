# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
import time
import logging
import os
from logging import handlers


# 生成日志
def my_logging(**kwargs):
    # 在字典中寻找pop方法：删除字典给定键 key 及对应的值，返回值为被删除的值。
    level = kwargs.pop("level", None)
    filename = kwargs.pop("filename", None)
    date_format = kwargs.pop("date_format", None)
    format = kwargs.pop("format", None)
    if level is None:
        level = logging.DEBUG
    if filename is None:
        current_day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        filename = "..\\log\\" + "AutoTest.log" + "." + current_day
    if date_format is None:
        date_format = "%Y-%m-%d %H:%M:%S"
    if format is None:
        format = "%(asctime)s [%(module)s] %(levelname)s [%(lineno)d] %(message)s"

    log = logging.getLogger(filename)
    log.handlers = []
    format_str = logging.Formatter(format, date_format)
    # backupCount 保存日志的数量，过期自动删除
    # when 按什么日期格式切分
    time_handler = handlers.TimedRotatingFileHandler(filename="..\\log\\" + "AutoTest.log", when="D",
                                                     backupCount=7,
                                                     encoding="utf-8")
    time_handler.setFormatter(format_str)
    time_handler.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(format_str)
    console_handler.setLevel(logging.INFO)
    log.addHandler(time_handler)
    log.addHandler(console_handler)
    log.setLevel(level)
    return log
