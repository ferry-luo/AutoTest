# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
import requests


# 自动获取，先写登录方法，等登录成功后从响应报文中得到cookie。有些登录很简单，只需要用户名，密码就可以。有些登录还有验证码，有验证码的登陆可以验证码自动识别的方式获取。当然，有验证码的登陆，有些也可以直接使用cookie来绕过验证码。这种方式就必须熟悉cookie怎么用。

# 第一步，写登录方法
def obtain_cookies():
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


# 第二步，拿登录接口响应报文中的cookies作为下游接口的入参
# 方法1

url = "下游接口地址"
data = {"xxx1": "aaa", "xxx2": "bbb"}
cookies = obtain_cookies()
response1 = requests.get(url=url, cookies=cookies)
# response2 = requests.post(url, data=data, cookies=cookies)
# response3 = requests.post(url=url, json=data, cookies=cookies)

# 方法2，headers中加cookie。
url = "下游接口地址"
data = {"xxx1": "aaa", "xxx2": "bbb"}
c_dict = obtain_cookies()
c_str = ""
for k in c_dict.keys():
    c_str += k + "=" + c_dict[k] + ";"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Cookie': c_str
}
response1 = requests.get(url=url, headers=headers)
# response2 = requests.post(url=url, data=data, headers=headers)
# response3 = requests.post(url=url, json=data, headers=headers)
