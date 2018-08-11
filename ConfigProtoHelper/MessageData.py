# _*_coding:utf-8_*_ 

from DataType import DataType
from SwapData import SwapData


def __convert_str__(str_value, type):
    try:
        if DataType.INT_TYPE == type:
            return int(str_value)
        elif DataType.BOOL_TYPE == type:
            return bool(str_value)
        elif DataType.STR_TYPE == type:
            return str_value
    except TypeError:
        print("无效的类型转换%s, %s", str_value, type)


def __str_to_array__(value, type):
    # 兼容旧格式
    value_data = value
    value_data = value_data.replace('[', '')
    value_data = value_data.replace(']', '')

    # 在正式转换前先确认类型
    convert_type = type
    
    # 数据字符串根据逗号进行分隔
    result = list()
    value_list = value_data.split(',')
    for item in value_list:
        if '' == item:
            continue

        if None is convert_type:
            convert_type = DataType.check_data_type(item)
            assert convert_type, "无法确定类型的数值：" + item
        result.append(__convert_str__(item, convert_type))
    return result, convert_type


def __str_to_map(value, key_type, value_type):
    # 兼容旧格式
    value_data = value
    value_data = value_data.replace('{', '')
    value_data = value_data.replace('}', '')
    
    convert_key_type = key_type
    convert_value_type = value_type

    # 数据字符串根据逗号进行分隔
    result = dict()
    value_list = value_data.split(',')
    for item in value_list:
        if '' == item:
            continue

        item_list = item.split(':')
        assert len(item_list) > 0, "无效的字典内容" + value

        key = item_list[0]
        key = key.replace('"', '')  # 兼容旧格式
        value = item_list[1]

        # 根据内容推存一次类型
        if None is convert_key_type:
            convert_key_type = DataType.check_data_type(key)
            assert convert_key_type, "无法确定类型的字典key：" + key
        if None is convert_value_type:
            convert_value_type = DataType.check_data_type(value)
            assert convert_value_type, "无法确定类型的字典value：" + value

        key = __convert_str__(key, convert_key_type)
        value = __convert_str__(value, convert_value_type)
        result[key] = value

    return result, convert_key_type, convert_value_type


def __process_data_by_type__(value, type_data):
    main_type = type_data.main_type
    if DataType.ARRAY_TYPE == main_type:
        result, convert_type = __str_to_array__(value, type_data.key_type)
        if None is type_data.key_type:
            type_data.set_key_type(convert_type)
        return result
    elif DataType.MAP_TYPE == main_type:
        result, convert_key_type, convert_value_type = __str_to_map(value, type_data.key_type, type_data.value_type)
        if None is type_data.key_type:
            type_data.set_key_type(convert_key_type)
        if None is type_data.value_type:
            type_data.set_value_type(convert_value_type)
        return result
    else:
        return __convert_str__(value, type_data.main_type)


class MessageData(SwapData):
    def __init__(self, file_name, types, notes, field):
        SwapData.__init__(self, file_name, types, notes, field)

    def analyze(self):
        # 先分析所有的类型
        SwapData.analyze(self)

        # 分析所有的数据
        for data in self.datas:
            data_value = data.values()
            for key in data:
               type_data = self.field_to_type.get(key, None)
               assert type_data, "字段%s无对应的数据类型" % key
               data[key] = __process_data_by_type__(data[key], type_data)

    def to_proto(self):
        message_field = ""
        for index in range(0, len(self.fields)):
            data_type = self.types[index]
            field_name = self.fields[index]
            assert data_type, "无法找到%s对应的类型" % field_name

            message_field = message_field + "\t%(type_name)s %(field_name)s = %(index)d;\n" % {
                    "type_name": DataType.to_proto_type(data_type),
                    "field_name": field_name,
                    "index": index + 1
                }
        return message_field

