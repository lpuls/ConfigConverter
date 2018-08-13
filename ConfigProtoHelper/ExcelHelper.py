# _*_coding:utf-8_*_

import os
import xlrd
from SwapData import *
from EnumData import *
from MessageData import *


def get_swap_data(file_name, types, notes, field):
    if 'e_' != file_name[:2]:
        return MessageData(file_name, types, notes, field)
    else:
        return EnumData(file_name[2:], types, notes, field)

class Excel:
    TYPE_ROW_ID = 0
    NOTE_ROW_ID = 1
    FIELD_ROW_ID = 2

    def __init__(self, path):
        self.sheets = dict()

        # 检查可读与否
        if not os.access(path, os.R_OK):
            print("文件%s不可读" % path)
            return

        # 分析每张工作表的内容
        data = xlrd.open_workbook(path)
        sheets = data.sheets()
        assert len(sheets) > 0, "无可用的工作表"

        # 如果有多个工作表则分别处理每个工作表，否则则以当前文件名做为读入工作表名
        if 1 == len(sheets):
            name = path[path.rfind('/') + 1: path.rfind('.')]
            sheet_obj = self.__analyze_sheet__(name, sheets[0])
            if None is not sheet_obj:
                self.sheets[name] = sheet_obj
        else:
            for sheet in data.sheets():
                sheet_obj = self.__analyze_sheet__(sheet.name, sheet)
                if None is not sheet_obj:
                    self.sheets[sheet.name] = sheet_obj
    
    @staticmethod
    def __analyze_sheet__(name, sheet):
        if sheet.nrows < 3: 
            print("无效的表置表格式")
            return None

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