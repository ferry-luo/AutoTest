# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import logging
from common import ferry_log

my_log = ferry_log.my_logging(level=logging.INFO,
                              format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class EmailManager:
    # 发送最新的测试报告内容
    def __init__(self, server, port, sender, psw, receiver):
        self.server = server
        self.port = port
        self.sender = sender
        self.psw = psw
        self.receiver = receiver

    def ferry_send_email(self, report_file):
        # ①定义邮件正文内容
        msg = MIMEMultipart()  # 创建一个读取器
        content_text = '''
                    <p style="font-family:Times New Roman;font-size:20px">Dear Ferry:</p>
                    <p style="text-indent:2em;font-family:新宋体;font-size:18px">附件为XXX项目_接口自动化测试报告，请查阅，谢谢！</p>
                    <p style="font-family:新宋体;font_size:20px" align="right">姓名：机器人</p>
                    '''
        # MIMEText有3个参数：第一个为文本内容（可以用引号括起来一段内容或者为一个变量，变量指向的是某个内容；第二个为设置的文本格式；第三个为编码
        body = MIMEText(content_text, "html", "utf-8")
        msg["Subject"] = "XXX项目_接口自动化测试报告"
        msg["from"] = self.sender
        msg["to"] = self.receiver
        '''另一种写法
        msg['Subject'] = "XXX项目_接口自动化测试报告"
        msg['from'] = Header('Fanlin Luo','utf-8')
        msg['to'] = Header('Ferry','utf-8')
        '''
        msg.attach(body)  # 可以形象地理解为把body所指向的内容（正文内容）附加进邮件

        # ②添加附件
        att_file = MIMEApplication(open(report_file, "rb").read())  # 构造附件，附件为测试报告文件，权限为二进制只读
        att_file.add_header('Content-Disposition', 'attachment',
                            filename='XXX_API_AutoTest_report.html')  # 设定收件人下载这个附件的时候默认文件名，这个随便你怎么定
        msg.attach(att_file)  # 可以形象地理解为把att_file所指向的内容（某个文件、多个文件等附件）附加进邮件
        try:
            # python的smtplib提供了一种很方便的途径发送电子邮件
            smtp = smtplib.SMTP(self.server, self.port)
            # 通过connect方法连接smtp主机
            smtp.connect(self.server, self.port)
            smtp.login(self.sender, self.psw)
            smtp.sendmail(self.sender, self.receiver, msg.as_string())
            my_log.info("邮件已发送成功")
            # 断开与smtp服务器的连接
            smtp.quit()
        except Exception as e:  # 不写出任何一种异常类型，那么只要有异常就会执行
            my_log.error("发生异常：%s" % e)
