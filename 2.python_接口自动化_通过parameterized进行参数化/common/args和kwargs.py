# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF

# 在 python 中，*args 和 **kwargs 都代表 1个 或 多个 参数的意思。
# *args 传入tuple 类型的无名参数，而 **kwargs 传入的参数是 dict 类型。
def test_1(**kwargs):
    print(kwargs)
    keys = kwargs.keys()
    values = kwargs.values()
    print(keys)
    print(values)


test_1(a=1, b=2, c="hh")


def test_2(*args):
    print(args)
    for i in args:
        print(i)


test_2(8, 9, "yu")
