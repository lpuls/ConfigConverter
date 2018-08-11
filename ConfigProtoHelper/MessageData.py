# _*_coding:utf-8_*_ 

from SwapData import SwapData


def __str_to_array__(value, type):
    value_length = len(value)
    assert value_length > 0, "无法将%s转换为数组" % value

    # 兼容旧格式
    value_data = value
    value_data.replace('[', '')
    value_data.replace(']', '')
    value_length = len(value_data)

    # 在正式转换前先确认类型
    convert_type = type
    
    # 数据字符串根据逗号进行分隔
    result = list()
    value_list = value_data.split(',')
    for item in value_list:
        if None is convert_type:
            convert_type = __check_data_type__(item)
        __convert_str__(item, convert_type) 


def __process_data_by_type__(value, type_data):
    main_type = type_data.main_type
    if DataType.ARRAY_TYPE == main_type:
        return value
    elif DataType.MAP_TYPE == main_type:
        pass
    else:
        return value


class MessageData(SwapData):
    def __init__(self, file_name, types, notes, field):
        SwapData.__init__(self, file_name, types, notes, field)

    def analyze(self):
        # 先分析所有的类型
        SwapData.analyze(self)

        # 分析所有的数据
        #for data in self.datas:
        #    data_value = data.values()
        #    for index in range(0, len(data_value)):
        #        type_data = self.types[index]
        #        value = data_value[index]
        #        data_value[index] = __process_data_by_type__(value, type_data)
        #        type_data.check_proto_type(value)

    def to_proto(self):
        message_field = ""
        for index in range(0, len(self.fields)):
            data_type = self.types[index]
            field_name = self.fields[index]
            if None is data_type:
                print("[SwapData] 无法找到%s对应的类型" % field_name)
                return None

            message_field = message_field + "\t%(type_name)s %(field_name)s = %(index)d;\n" % {
                    "type_name": self.__to_proto_type__(data_type),
                    "field_name": field_name,
                    "index": index + 1
                }
        return message_field
    
    def __to_proto_type__(self, type_data):
        """
        data_value: 该字段的某个值，为了某些类型中能确认到具体的类型
        """
        if DataType.INT_TYPE == type_data.main_type:  # int类型要判断一下是否为枚举
            if None is not type_data.key_type:
                return type_data.key_type
            else:
                return type_data.main_type_proto
        elif DataType.ARRAY_TYPE == type_data.main_type:  # 数据类型要判断一下存储类型
            return "%s %s" % (type_data.main_type_proto, type_data.key_type_proto)
        else:
            return type_data.main_type_proto

