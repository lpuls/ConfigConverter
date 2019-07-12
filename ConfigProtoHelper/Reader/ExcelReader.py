# _*_coding:utf-8_*_

import os
import xlrd
from ConfigBase.ConfigType import *
from ConfigBase.TypeHelper import *
from ConfigBase.CommonIntermediateFormat import CommonIntermediateFormat as CIFormat


__TYPE_ROW_ID__ = 0
__NOTE_ROW_ID__ = 1
__FIELD_ROW_ID__ = 2


def __add_new_enum_type__(name, data):
    desc = list()
    for index, _ in enumerate(data.data_list):
        field = data.data_list[index][0]
        value = int(data.data_list[index][1])
        desc.append((field, value))
    new_enum(name, desc)


def __add_new_class_type__(name, data):
    desc = list()
    for index, type_inst in enumerate(data.types):
        field = data.fields[index]
        desc.append((field, type_inst))
    new_type(name, desc)


def __analyze_sheet__(name, sheet):
    # 字段不够就没有继续的必要了
    if sheet.nrows < 3:
        print("无效的表置表格式")
        return None

    # 获取基本属性
    types = sheet.row_values(__TYPE_ROW_ID__)
    notes = sheet.row_values(__NOTE_ROW_ID__)
    fields = sheet.row_values(__FIELD_ROW_ID__)
    data_list = list()

    # 读取表格并生成中间文件
    for row_index in range(__FIELD_ROW_ID__ + 1, sheet.nrows):
        data = list()
        for col_index in range(0, sheet.ncols):
            # todo: 之后再加入过滤和缺省
            data.append(sheet.cell(row_index, col_index).value)
        data_list.append(data)

    for index, type_str in enumerate(types):
        type_inst = get_type(type_str)
        if None is type_inst:
            type_inst = new_type(type_str, None)
        types[index] = type_inst

    # 根据数据类型的字符串得到数据类型实例，若无法判断，则读取数据的第一行
    for row_data in data_list:
        for index, data in enumerate(row_data):
            type_inst = types[index]
            row_data[index], types[index] = pre_process_and_check_type(data, type_inst)
    ci_data = CIFormat(name, types, notes, fields, data_list)

    # 判断是枚举还是表格，若是枚举则需要加入一种新的类型
    if 'e_' == name[:2]:
        __add_new_enum_type__(name[2:], ci_data)
    else:
        __add_new_class_type__(name, ci_data)

    return ci_data


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


if __name__ == '__main__':
    reader('../../Config/Excel/AbilityConfig.xlsx')
    # reader('../../Config/Excel/Spawn.xlsx')
    # print(get_type('FloatingType'))
