# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
import requests

# 手动获取：手工登录获取cookie，登录成功后可以不断更新cookie到文件中存储。参考：https://www.jianshu.com/p/5ef0c7bb1ed2.

target_url = "http://127.0.0.1:8000/orgs/org_list/"

# 设置头User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}

# 开启一个session会话
my_session = requests.session()

# 设置请求头信息
my_session.headers = headers

# 声明一个用于存储手动cookies的字典
manual_cookies = {}

##打开手动设置的cookies文件
# 部分网站需要滑动验证，这里通过浏览器登录成功后获取cookies手动存到文本来绕过验证，后续cookies自动更新
with open("manual_cookies.txt", "r", encoding="utf-8") as fr_cookie:
    cookies_txt = fr_cookie.read().strip(";")  # 读取文本内容，移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
    # 手动分割添加cookie
    for item in cookies_txt.split(";"):
        name, value = item.strip().split("=", 1)  # 用=号分割，分割1次
        manual_cookies[name] = value  # 为字典cookies添加内容

print("文件中原来的cookies信息如下")
print(manual_cookies)
# 将字典转为CookieJar：
cookiesJar = requests.utils.cookiejar_from_dict(manual_cookies, cookiejar=None, overwrite=True)

# 将cookiesJar赋值给会话
my_session.cookies = cookiesJar

# 向目标网站发起请求
res = my_session.get(target_url)

# 将CookieJar转为字典：
res_cookies_dic = requests.utils.dict_from_cookiejar(res.cookies)

# 将新的cookies信息更新到手动cookies字典
for k in res_cookies_dic.keys():
    manual_cookies[k] = res_cookies_dic[k]

print("新的cookies信息如下")
print(manual_cookies)

# 重新将新的cookies信息写回文本
res_manual_cookies_txt = ""
# 将更新后的cookies写入到文本
for k in manual_cookies.keys():
    res_manual_cookies_txt += k + "=" + manual_cookies[k] + ";"
for k in manual_cookies.keys():
    res_manual_cookies_txt += k + "=" + manual_cookies[k] + ";"

# 将新的cookies写入到文本中更新原来的cookies
with open("manual_cookies.txt", "w", encoding="utf-8") as fw_cookie:
    fw_cookie.write(res_manual_cookies_txt)
