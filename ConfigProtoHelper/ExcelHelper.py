# _*_coding:utf-8_*_

import xlrd
from SwapData import *

class Excel:
    TYPE_ROW_ID = 0
    NOTE_ROW_ID = 1
    FIELD_ROW_ID = 2

    def __init__(self, path):
        self.sheets = dict()

        # 分析每张工作表的内容
        data = xlrd.open_workbook(path)
        for sheet in data.sheets():
            self.sheets[sheet.name] = self.__analyze_sheet__(sheet.name, sheet)
    
    @staticmethod
    def __analyze_sheet__(name, sheet):
        # 获取基本属性
        types = sheet.row_values(Excel.TYPE_ROW_ID)
        notes = sheet.row_values(Excel.NOTE_ROW_ID)
        fields = sheet.row_values(Excel.FIELD_ROW_ID)

        # 生成数据类
        sheetData = get_swap_data(name, types, notes, fields)

        # 获需所有字段
        for row_index in range(Excel.FIELD_ROW_ID + 1, sheet.nrows):
            data = dict()
            for col_index in range(0, sheet.ncols):
                field_name = fields[col_index]
                data[field_name] = sheet.cell(row_index, col_index).value
            sheetData.insert(data)
        
        return sheetData