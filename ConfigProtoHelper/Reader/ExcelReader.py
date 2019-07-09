# _*_coding:utf-8_*_

import os
import xlrd
from ConfigBase.ConfigType import *
from ConfigBase.CommonIntermediateFormat import CommonIntermediateFormat as CIFormat


__TYPE_ROW_ID__ = 0
__NOTE_ROW_ID__ = 1
__FIELD_ROW_ID__ = 2


def __analyze_sheet__(name, sheet):
    # 判断是枚举还是表格，若是枚举则需要加入一种新的类型
    if 'e_' == name[:2]:
        new_type(name[2:])

    # 字段不够就没有继续的必要了
    if sheet.nrows < 3:
        print("无效的表置表格式")
        return None

    # 获取基本属性
    types = sheet.row_values(__TYPE_ROW_ID__)
    notes = sheet.row_values(__NOTE_ROW_ID__)
    fields = sheet.row_values(__FIELD_ROW_ID__)
    data_list = list()

    for row_index in range(__FIELD_ROW_ID__ + 1, sheet.nrows):
        data = list()
        for col_index in range(0, sheet.ncols):
            # todo: 之后再加入过滤和缺省
            data.append(fields[col_index])
        data_list.append(data)

    return CIFormat(name, types, notes, fields, data_list)


def reader(path):
    if not os.access(path, os.R_OK):
        print("文件%s不可读" % path)
        return

    # 分析每张工作表的内容
    data = xlrd.open_workbook(path)
    sheets = data.sheets()
    assert len(sheets) > 0, "无可用的工作表"

    # 暂时不支持多张sheet表了
    name = path[path.rfind('/') + 1: path.rfind('.')]
    return __analyze_sheet__(name, sheets[0])
