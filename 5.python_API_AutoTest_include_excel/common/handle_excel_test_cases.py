# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
from common.ferry_API_auto_test_key_function import FerryAutoTestKeyFunction
from common.excel_xlsx_operation import ExcelOperate
import logging
import unittest
import ddt
import time
import warnings
import hashlib
from cx_Oracle import connect
from common import ferry_log_operation

# 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
# a是追加模式，默认如果不写的话，就是追加模式
# file_handler = logging.FileHandler(filename="..\\log\\" + "AutoTest.log", encoding='utf-8', mode='a')  # 输出到文件
# console_handler = logging.StreamHandler()  # 输出到控制台
# logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
#                     format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',  # 日志格式
#                     handlers=[file_handler, console_handler]
#                     )
my_log = ferry_log_operation.my_logging(level=logging.INFO,
                                        format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
excel_test_cases_path = "../test_cases/AutoTestCases_XXX.xlsx"
# 用例文件中各sheet的名称
cases_sheet_name = "cases"
steps_sheet_name = "steps"
# 获取cases sheet的行数
cases_sheet_rows = ExcelOperate(excel_test_cases_path, cases_sheet_name).get_rows()

case_id_list = []
# 遍历sheet中第2行到第最后一行
# 备注：与xlrd不同，openpyxl 读写单元格时，单元格的坐标位置起始值是（1,1），即下标最小值为1，否则报错！
for i in range(2, cases_sheet_rows + 1):
    # cases表格的第i行的case_id数据
    cases_sheet_case_id_data = ExcelOperate(excel_test_cases_path, cases_sheet_name).get_cell_value(i, 1)
    # cases表格的第i行的case_title数据
    cases_sheet_case_title_data = ExcelOperate(excel_test_cases_path, cases_sheet_name).get_cell_value(i, 2)
    # cases表格的第i行的whether_execute数据
    cases_sheet_whether_execute_data = ExcelOperate(excel_test_cases_path, cases_sheet_name).get_cell_value(i, 3)

    # 先判断是否有空值
    # 如果至少存在一项为空
    if (
            cases_sheet_case_id_data == "" or cases_sheet_case_title_data == "" or cases_sheet_whether_execute_data == ""):
        my_log.error("cases表格的第" + str(i) + "行的case_id或case_title或whether_execute为空，请检查")
        continue
    # 都有值，再看看此条用例是否需要执行
    else:
        # 如果需要执行
        if (cases_sheet_whether_execute_data == "Y"):
            case_id_list.append(cases_sheet_case_id_data)
        # 如果不需要，则进入下一次for循环：看下一条用例
        elif (cases_sheet_whether_execute_data == "N"):
            continue
        # whether_execute既不是Y，也不是N
        else:
            my_log.error("cases表格的第" + str(i) + "行的whether_execute既不是Y也不是N，请检查")
            continue


# 处理Excel用例文件
@ddt.ddt
class HandleExcelTestCases(unittest.TestCase):

    def setUp(self):
        # self.connection = connect('dealer_plat', 'bst+dealer_plat', '10.50.115.8:1521/mama100')
        #
        # self.username = "ADM0603"
        # self.password = "888888"
        # self.md5_password = hashlib.md5(self.password.encode(encoding="utf-8")).hexdigest()
        # self.local_time = time.localtime()
        # self.current_time = time.strftime("%Y%m%d%H", self.local_time)
        # self.s = self.username + self.md5_password + self.current_time
        # self.sign = hashlib.md5(self.s.encode(encoding="utf-8")).hexdigest()
        self.key_func = FerryAutoTestKeyFunction()

    # 执行用例
    # 利用ddt数据驱动，将需要执行的用例编号作为test_cases_run函数的参数，生成的HTML测试报告就会有每条用例的执行结果
    # 如果不这么做，生成的HTML测试报告就会处理成只有一条用例，以这里的函数名test_cases_run作为用例编号或名称
    @ddt.data(*case_id_list)
    def test_cases_run(self, case_id):
        # 为避免代码字符很长，对类实例化
        steps_excel_operate = ExcelOperate(excel_test_cases_path, steps_sheet_name)

        # steps表格的第1列数据
        # 备注：get_col_values()函数返回了列表类型，这里就不用再处理成列表了
        steps_sheet_case_id_data_list = ExcelOperate(excel_test_cases_path,
                                                     steps_sheet_name).get_col_values(1)

        # 列表中，除了第一个（因为第一个是表头的值），其余的全部拿来遍历，看能否找到此条用例
        for j in range(1, len(steps_sheet_case_id_data_list)):
            # 如果找到了
            if (steps_sheet_case_id_data_list[j] == case_id):
                my_log.info("当前用例为：" + case_id)
                # 把steps_sheet中第i+1行的数据放到一个列表，然后按照列表依次执行对应的操作（也就是调用已封装好的关键字函数）
                # 传参i+1，是因为用的openpyxl库处理xlsx，从1开始。列表list索引是从0开始
                # 备注：get_row_values()函数返回了列表类型，这里就不用再处理成列表了
                steps_sheet_j_list = steps_excel_operate.get_row_values(
                    j + 1)

                # 根据各列中不同的数据，调用不同的关键字函数
                if (steps_sheet_j_list[steps_excel_operate.get_col_index("keyword")] == "ferry_assertEqual_complete"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    operate_result = self.key_func.ferry_assertEqual_complete(
                        steps_sheet_j_list[steps_excel_operate.get_col_index(
                            "request_type")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("request_url")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("headers")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("parameters")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("body")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("expect_result")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("need_token")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("need_cookie")]
                    )
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    operate_result["status"],
                                                    operate_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[steps_excel_operate.get_col_index("keyword")] == "ferry_assertEqual"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    operate_result = self.key_func.ferry_assertEqual(
                        steps_sheet_j_list[steps_excel_operate.get_col_index(
                            "request_type")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("request_url")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("headers")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("parameters")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("body")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("hierarchy_1")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("hierarchy_2")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("hierarchy_3")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("hierarchy_4")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("at_number_of_hierarchy")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("expect_result")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("expect_result_type")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("need_token")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("need_cookie")]
                    )
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    operate_result["status"],
                                                    operate_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[steps_excel_operate.get_col_index("keyword")] == "ferry_assertIn"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    operate_result = self.key_func.ferry_assertIn(
                        steps_sheet_j_list[steps_excel_operate.get_col_index(
                            "request_type")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("request_url")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("headers")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("parameters")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("body")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("expect_result")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("need_token")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("need_cookie")]
                    )
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    operate_result["status"],
                                                    operate_result["cell_color"]
                                                    )

            # 如果没找到
            else:
                continue

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
