# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
import requests
import json

data = {
    "name": "bob",
    "age": 100,
}
print(data)
print(type(data))
# dumps()将dict转为str
json_str = json.dumps(data)
print(json_str)
print(type(json_str))
# loads()将str转为dict
d = json.loads(json_str)
print(d)
print(type(d))

# dump()用来编码JSON数据
with open("my_json.json", "w") as f:
    json.dump(data, f)

# load()用来解码JSON数据
with open("my_json.json", "r") as f:
    load_result = json.load(f)
    print(load_result)
    print(type(load_result))
