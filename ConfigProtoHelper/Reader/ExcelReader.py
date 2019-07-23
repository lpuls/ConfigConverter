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


def __conversion_list_to_n_array__(list_data):
    if isinstance(list_data, list):
        data = {"data": list()}
        for item in list_data:
            data["data"].append(__conversion_list_to_n_array__(item))
        return data
    return list_data


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
            value = sheet.cell(row_index, col_index).value
            if 0 == col_index and (isinstance(value, str)
                                   and ((len(value) > 0 and '#' == value[0]) or len(value) <= 0)):
                print("Skip ", row_index)
                break
            data.append(value)
        else:
            data_list.append(data)

    # 判断是枚举还是表格，若是枚举则需要加入一种新的类型
    if 'e_' == name[:2]:
        ci_data = CIFormat(name[2:], types, notes, fields, data_list)
        __add_new_enum_type__(name[2:], ci_data)
    else:

        for index, type_str in enumerate(types):
            type_inst = get_type(type_str)
            if None is type_inst:
                type_inst = new_type(type_str, None)
            types[index] = type_inst

        # 根据数据类型的字符串得到数据类型实例，若无法判断，则读取数据的第一行
        for row_index, row_data in enumerate(data_list):
            for index, data in enumerate(row_data):
                type_inst = types[index]

                # 若是有空值，则根据类型填写默认值
                if isinstance(data, str) and len(data) <= 0:
                    if isinstance(type_inst, ArrayType):
                        row_data[index] = []
                    elif isinstance(type_inst, MapType):
                        row_data[index] = {}
                    elif isinstance(type_inst, BoolType):
                        row_data[index] = False
                    elif isinstance(type_inst, FloatType):
                        row_data[index] = 0.0
                    elif isinstance(type_inst, IntType) or isinstance(type_inst, LongType):
                        row_data[index] = 0
                    else:
                        row_data[index] = ""
                else:
                    row_data[index], types[index] = pre_process_and_check_type(data, type_inst)

        # 检查多维数组，将多维数组合并成新的数据类型，交替换掉当前类型
        for type_index, type_inst in enumerate(types):
            if isinstance(type_inst, ArrayType) and isinstance(type_inst.sub_type, ArrayType):
                sub_type_inst = type_inst.sub_type
                sub_type_inst_list = list()
                while isinstance(sub_type_inst, ArrayType):
                    sub_type_inst_list.append(sub_type_inst)
                    sub_type_inst = sub_type_inst.sub_type

                    # 分析多维数组
                    for index, item in enumerate(sub_type_inst_list[::-1]):
                        if 0 == index:
                            new_type('_%dDArray' % (index + 2), [
                                ('data', item)
                            ])
                        else:
                            new_type('_%dDArray' % (index + 2), [
                                ('data', get_type('_%dDArray' % (index + 2)))
                            ])
                    type_inst.sub_type = get_type('_%dDArray' % (len(sub_type_inst_list) + 1))

                # 转换数据
                for item in data_list:
                    temp = list()
                    for item_value in item[type_index]:
                        temp.append(__conversion_list_to_n_array__(item_value))
                    item[type_index] = temp

        ci_data = CIFormat(name, types, notes, fields, data_list)
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
    r = __conversion_list_to_n_array__([[[1, 2, 3], [2, 3, 4], [5, 6, 7]], [[1, 2, 3], [2, 3, 4], [5, 6, 7]]])
    print(r)
