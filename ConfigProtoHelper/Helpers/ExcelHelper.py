# _*_coding:utf-8_*_

import os
import xlrd
from SwapDatas.EnumData import *
from SwapDatas.MessageData import *


class ExcelHelper:
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

        # 暂时不支持多张sheet表了
        name = path[path.rfind('/') + 1: path.rfind('.')]
        sheet_obj = self.__analyze_sheet__(name, sheets[0])
        if None is not sheet_obj:
            self.sheets[name] = sheet_obj

    @staticmethod
    def __get_swap_data__(file_name, types, notes, field):
        if 'e_' != file_name[:2]:
            return MessageData(file_name, types, notes, field)
        else:
            return EnumData(file_name[2:], types, notes, field)
    
    @staticmethod
    def __analyze_sheet__(name, sheet):
        if sheet.nrows < 3:
            print("无效的表置表格式")
            return None

        # 获取基本属性
        types = sheet.row_values(ExcelHelper.TYPE_ROW_ID)
        notes = sheet.row_values(ExcelHelper.NOTE_ROW_ID)
        fields = sheet.row_values(ExcelHelper.FIELD_ROW_ID)

        # 生成数据类
        sheet_data = ExcelHelper.__get_swap_data__(name, types, notes, fields)

        # 获需所有字段
        for row_index in range(ExcelHelper.FIELD_ROW_ID + 1, sheet.nrows):
            data = dict()
            for col_index in range(0, sheet.ncols):
                field_name = fields[col_index]
                cell_value = sheet.cell(row_index, col_index).value
                # data[field_name] = cell_value
                # 过滤掉注释和空行
                if 0 == col_index and (isinstance(cell_value, str)
                                       and (('' != cell_value and '#' == cell_value[0]) or '' == cell_value)):
                    print(name, row_index, col_index)
                    continue

                # 检查数值是否为空
                if (DataType.INT_TYPE == types[col_index] or DataType.FLOAT_TYPE == types[col_index]
                    or DataType.LONG_TYPE == types[col_index]) \
                        and '' == cell_value:
                    cell_value = '0'
                elif (DataType.MAP_TYPE == types[col_index] or DataType.JSON_TYPE == types[col_index]) \
                        and '' == cell_value:
                    cell_value = '{}'
                elif DataType.ARRAY_TYPE == types[col_index] and '' == cell_value:
                    cell_value = '[]'
                elif DataType.BOOL_TYPE == types[col_index] and '' == cell_value:
                    cell_value == 'False'
                data[field_name] = cell_value
            else:
                # continue
                sheet_data.insert(data)

        return sheet_data
