# encoding:utf-8
# @Time:2020/10/17

# @Author:Ferry

# @colleges_class:湖南理工学院_电子14-2BF
import xlrd
import xlwt
from xlutils.copy import copy

#Excel数据的读取、获取单元格内容、获取一行数据和数据写入等基础操作
class ExcelOperate(object):
    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.excel = self.get_all_excel()
        self.sheet_data = self.get_sheet_data(sheet_name)

    #获取整个excel数据
    def get_all_excel(self):
        """
        :return:
        """
        excel = xlrd.open_workbook(self.file_path)
        return excel

    #获取excel中的某个表数据
    def get_sheet_data(self, sheet_name=0):
        """
        :param sheet_name: 表名，可以是下标也可以是名称
        :return:
        """
        if isinstance(sheet_name, int):
            sheet = self.excel.sheet_by_index(sheet_name)
        else:
            sheet = self.excel.sheet_by_name(sheet_name)
        return sheet

    #获取excel行数
    def get_rows(self):
        """
        :return:
        """

        return self.sheet_data.nrows

    #获取excel列数
    def get_cols(self):
        return self.sheet_data.ncols

    #获取单元格内容
    def get_cell_value(self, row, column):
        """
        :param row:  行号
        :param column: 列号
        :return:
        """
        data = self.sheet_data.cell(row, column).value
        return data

    #获取某列头的索引
    def get_col_index(self,col_name):
        col_index = None
        for i in range(self.sheet_data.ncols):
            if self.sheet_data.cell(0,i).value == col_name:
                col_index = i
                break
        return col_index

    #获取一行的数据
    def get_row_values(self, row):
        """
        :param row:
        """
        return self.sheet_data.row_values(row)

    #获取一列的数据
    def get_col_values(self, col):
        """
        :param col:
        """
        return self.sheet_data.col_values(col)

    #数据写入
    def write_value(self, row, column, value):
        """
        :param row: 行
        :param column: 列
        :param value: 数据
        :return:
        """
        read_value = self.excel
        write_data = copy(read_value)
        write_save = write_data.get_sheet(self.sheet_name)
        write_save.write(row, column, value)
        write_data.save(self.file_path)