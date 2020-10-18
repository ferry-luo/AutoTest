# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
from common.ferry_web_auto_test_key_function import FerryAutoTestKeyFunction
from common.excel_xlsx_operation import ExcelOperate
import logging
from common.ferry_log_operation import my_logging
import unittest
import ddt
import time
import warnings

my_log = my_logging(level=logging.INFO,
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

# 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
# a是追加模式，默认如果不写的话，就是追加模式
# file_handler = logging.FileHandler(filename="..\\log\\" + "AutoTest.log", encoding='utf-8', mode='a')  # 输出到文件
# console_handler = logging.StreamHandler()  # 输出到控制台
# logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
#                     format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',  # 日志格式
#                     handlers=[file_handler, console_handler]
#                     )
excel_test_cases_path = "../test_cases/AutoTestCases_web_any.xlsx"
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
    if (cases_sheet_case_id_data == "" or cases_sheet_case_title_data == "" or cases_sheet_whether_execute_data == ""):
        my_log.error("cases表格的第" + str(i) + "行的case_id或case_title或whether_execute为空，请检查")
        continue
    # 都有值
    else:
        # 看此条用例是否需要执行
        # 如果不需要，则进入下一次for循环：看下一条用例
        if (cases_sheet_whether_execute_data == "N"):
            continue
        # 如果需要执行
        else:
            case_id_list.append(cases_sheet_case_id_data)


# 处理Excel用例文件
@ddt.ddt
class HandleExcelTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        cls.key_func = FerryAutoTestKeyFunction()
        cls.dr = cls.key_func.ferry_choice_browser("Chrome")
        cls.dr.maximize_window()
        cls.dr.implicitly_wait(15)

    # 执行用例
    @ddt.data(*case_id_list)
    def test_cases_run(cls, case_id):
        # 为避免代码字符很长，对类实例化
        steps_excel_operate = ExcelOperate(excel_test_cases_path, steps_sheet_name)

        # steps表格的第1列数据
        # 备注：get_col_values()函数返回了列表类型，这里就不用再处理成列表了
        steps_sheet_case_id_data_list = steps_excel_operate.get_col_values(1)

        # 列表中，除了第一个（因为第一个是表头的值），其余的全部拿来遍历，看能否找到此条用例
        for j in range(1, len(steps_sheet_case_id_data_list)):
            # 如果找到了
            if (steps_sheet_case_id_data_list[j] == case_id):
                my_log.info("当前操作步骤所在用例为：" + case_id)

                # 把steps_sheet中第j+1行的数据放到一个列表，然后按照列表依次执行对应的操作（也就是调用已封装好的关键字函数）
                # 传参j+1，是因为用的openpyxl库处理xlsx，从1开始。列表list索引是从0开始
                # 备注：get_row_values()函数返回了列表类型，这里就不用再处理成列表了
                steps_sheet_j_list = steps_excel_operate.get_row_values(j + 1)
                my_log.info("当前操作步骤为：" + steps_sheet_j_list[steps_excel_operate.get_col_index("step_description")])

                # 根据各列中不同的数据，调用不同的关键字函数
                # 先写入fail，再根据调用关键字函数的结果写入最终状态
                if (steps_sheet_j_list[
                    steps_excel_operate.get_col_index("keyword")] == "ferry_save_screenshot_by_human_subjectivity"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    operate_result = cls.key_func.ferry_save_screenshot_by_human_subjectivity(
                        steps_sheet_j_list[steps_excel_operate.get_col_index(
                            "operate_value")])
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "screenshot_by_human_subjectivity"),
                                                    operate_result["img_path"],
                                                    operate_result["path_color"]
                                                    )
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    operate_result["status"],
                                                    operate_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[steps_excel_operate.get_col_index("keyword")] == "ferry_open_url"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    operate_result = cls.key_func.ferry_open_url(steps_sheet_j_list[steps_excel_operate.get_col_index(
                        "operate_value")])
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    operate_result["status"],
                                                    operate_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[steps_excel_operate.get_col_index("keyword")] == "ferry_click"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    operate_result = cls.key_func.ferry_click(steps_sheet_j_list[steps_excel_operate.get_col_index(
                        "operate_element_position_expression")],
                                                              steps_sheet_j_list[
                                                                  steps_excel_operate.get_col_index(
                                                                      "expression_value")])
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    operate_result["status"],
                                                    operate_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[steps_excel_operate.get_col_index("keyword")] == "ferry_send_keys"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    operate_result = cls.key_func.ferry_send_keys(steps_sheet_j_list[steps_excel_operate.get_col_index(
                        "operate_element_position_expression")],
                                                                  steps_sheet_j_list[
                                                                      steps_excel_operate.get_col_index(
                                                                          "expression_value")],
                                                                  steps_sheet_j_list[
                                                                      steps_excel_operate.get_col_index(
                                                                          "input_data_1")])
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    operate_result["status"],
                                                    operate_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[
                    steps_excel_operate.get_col_index("keyword")] == "ferry_cursor_hover"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    operate_result = cls.key_func.ferry_cursor_hover(
                        steps_sheet_j_list[steps_excel_operate.get_col_index("operate_element_position_expression")],
                        steps_sheet_j_list[steps_excel_operate.get_col_index("expression_value")]
                    )
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    operate_result["status"],
                                                    operate_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[
                    steps_excel_operate.get_col_index("keyword")] == "ferry_select_by_index"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    operate_result = cls.key_func.ferry_select_by_index(
                        steps_sheet_j_list[steps_excel_operate.get_col_index("operate_element_position_expression")],
                        steps_sheet_j_list[steps_excel_operate.get_col_index("expression_value")],
                        steps_sheet_j_list[steps_excel_operate.get_col_index("operate_value")]
                    )
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    operate_result["status"],
                                                    operate_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[
                    steps_excel_operate.get_col_index("keyword")] == "ferry_select_by_value"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    operate_result = cls.key_func.ferry_select_by_value(
                        steps_sheet_j_list[steps_excel_operate.get_col_index("operate_element_position_expression")],
                        steps_sheet_j_list[steps_excel_operate.get_col_index("expression_value")],
                        steps_sheet_j_list[steps_excel_operate.get_col_index("operate_value")]
                    )
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    operate_result["status"],
                                                    operate_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[
                    steps_excel_operate.get_col_index("keyword")] == "ferry_select_direct"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    operate_result = cls.key_func.ferry_select_direct(
                        steps_sheet_j_list[steps_excel_operate.get_col_index("operate_element_position_expression")],
                        steps_sheet_j_list[steps_excel_operate.get_col_index("expression_value")]
                    )
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    operate_result["status"],
                                                    operate_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[
                    steps_excel_operate.get_col_index("keyword")] == "ferry_switch_window_by_index"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    operate_result = cls.key_func.ferry_switch_window_by_index(
                        steps_sheet_j_list[steps_excel_operate.get_col_index("operate_value")])
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    operate_result["status"],
                                                    operate_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[
                    steps_excel_operate.get_col_index("keyword")] == "ferry_switch_frame"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    operate_result = cls.key_func.ferry_switch_frame(
                        steps_sheet_j_list[steps_excel_operate.get_col_index(
                            "operate_element_position_expression")],
                        steps_sheet_j_list[
                            steps_excel_operate.get_col_index("expression_value")])
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    operate_result["status"],
                                                    operate_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[
                    steps_excel_operate.get_col_index("keyword")] == "ferry_assertTrue_is_displayed"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    assert_result = cls.key_func.ferry_assertTrue_is_displayed(steps_sheet_j_list[
                                                                                   steps_excel_operate.get_col_index(
                                                                                       "operate_element_position_expression")],
                                                                               steps_sheet_j_list[
                                                                                   steps_excel_operate.get_col_index(
                                                                                       "expression_value")])

                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    assert_result["status"],
                                                    assert_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[
                    steps_excel_operate.get_col_index("keyword")] == "assertTrue_is_not_displayed"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    assert_result = cls.key_func.assertTrue_is_not_displayed(steps_sheet_j_list[
                                                                                 steps_excel_operate.get_col_index(
                                                                                     "operate_element_position_expression")],
                                                                             steps_sheet_j_list[
                                                                                 steps_excel_operate.get_col_index(
                                                                                     "expression_value")])

                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    assert_result["status"],
                                                    assert_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[
                    steps_excel_operate.get_col_index("keyword")] == "ferry_assertTrue_compare"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    assert_result = cls.key_func.ferry_assertTrue_compare(steps_sheet_j_list[
                                                                              steps_excel_operate.get_col_index(
                                                                                  "operate_element_position_expression")],
                                                                          steps_sheet_j_list[
                                                                              steps_excel_operate.get_col_index(
                                                                                  "expression_value")],
                                                                          steps_sheet_j_list[
                                                                              steps_excel_operate.get_col_index(
                                                                                  "comparison_operator")],
                                                                          steps_sheet_j_list[
                                                                              steps_excel_operate.get_col_index(
                                                                                  "comparison_value")])

                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    assert_result[
                                                        "status"],
                                                    assert_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[
                    steps_excel_operate.get_col_index("keyword")] == "ferry_assertEqual"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    assert_result = cls.key_func.ferry_assertEqual(steps_sheet_j_list[
                                                                       steps_excel_operate.get_col_index(
                                                                           "operate_element_position_expression")],
                                                                   steps_sheet_j_list[
                                                                       steps_excel_operate.get_col_index(
                                                                           "expression_value")],
                                                                   steps_sheet_j_list[
                                                                       steps_excel_operate.get_col_index(
                                                                           "expect_result")])

                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    assert_result[
                                                        "status"],
                                                    assert_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[steps_excel_operate.get_col_index("keyword")] == "ferry_assertEqual_alert"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    assert_result = cls.key_func.ferry_assertEqual_alert(steps_sheet_j_list[
                                                                             steps_excel_operate.get_col_index(
                                                                                 "expect_result")])

                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    assert_result[
                                                        "status"],
                                                    assert_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[steps_excel_operate.get_col_index("keyword")] == "ferry_assertIn"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    assert_result = cls.key_func.ferry_assertIn(steps_sheet_j_list[
                                                                    steps_excel_operate.get_col_index(
                                                                        "operate_element_position_expression")],
                                                                steps_sheet_j_list[
                                                                    steps_excel_operate.get_col_index(
                                                                        "expression_value")],
                                                                steps_sheet_j_list[
                                                                    steps_excel_operate.get_col_index(
                                                                        "expect_result")])

                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    assert_result[
                                                        "status"],
                                                    assert_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[steps_excel_operate.get_col_index("keyword")] == "ferry_actual_assertIn_expect"):
                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    "fail",
                                                    "FF0000"
                                                    )
                    assert_result = cls.key_func.ferry_actual_assertIn_expect(steps_sheet_j_list[
                                                                    steps_excel_operate.get_col_index(
                                                                        "operate_element_position_expression")],
                                                                steps_sheet_j_list[
                                                                    steps_excel_operate.get_col_index(
                                                                        "expression_value")],
                                                                steps_sheet_j_list[
                                                                    steps_excel_operate.get_col_index(
                                                                        "expect_result")])

                    steps_excel_operate.write_value(j,
                                                    steps_excel_operate.get_col_index(
                                                        "status"),
                                                    assert_result[
                                                        "status"],
                                                    assert_result["cell_color"]
                                                    )

                if (steps_sheet_j_list[
                    steps_excel_operate.get_col_index("keyword")] == "ferry_sleep"):
                    cls.key_func.ferry_sleep(steps_sheet_j_list[steps_excel_operate.get_col_index("operate_value")])

            # 如果没找到
            else:
                continue

    @classmethod
    def tearDownClass(cls):
        cls.dr.quit()


if __name__ == "__main__":
    unittest.main()
