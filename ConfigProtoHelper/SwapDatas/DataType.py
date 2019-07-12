# _*_coding:utf-8_*_ 

import re


class DataType:
    STR_TYPE = "STR"
    INT_TYPE = "INT"
    LONG_TYPE = "LONG"
    BOOL_TYPE = "BOOL"
    ARRAY_TYPE = "ARRAY"
    MAP_TYPE = "MAP"
    JSON_TYPE = "JSON"
    FLOAT_TYPE = "FLOAT"

    PROTO_INT_TYPE = "int32"
    PROTO_LONG_TYPE = "int64"
    PROTO_STR_TYPE = "string"
    PROTO_BOOL_TYPE = "bool"
    PROTO_ARRAY_TYPE = "repeated %s"
    PROTO_MAP_TYPE = "map<%s, %s>"
    PROTO_JSON_TYPE = ""
    PROTO_FLOAT_TYPE = "float"

    INVALID_TYPE_OK = 1
    INVALID_TYPE_SKIP = 2
    INVALID_TYPE_ERROR = 3

    def __init__(self, type_name):
        self.is_valid = DataType.INVALID_TYPE_OK
        self.main_type = None
        self.key_type = None
        self.value_type = None
        self.main_type_proto = None

        # 检查
        type_name_list = type_name
        if isinstance(type_name, str):
            if '' == type_name:
                self.is_valid = DataType.INVALID_TYPE_SKIP
                return
            type_name_list = DataType.__split_type_name__(type_name)

        # 分析转放类型
        analyze_result = type_name_list
        if not isinstance(type_name_list, tuple):
            _, analyze_result = DataType.__analyze_sub_type__(type_name_list, 0)
        self.__process_type_name__(analyze_result)

        # 先尝试生成proto类型
        self.main_type_proto = DataType.type_to_proto(self.main_type)

    def __process_type_name__(self, type_name):
        type_name_count = len(type_name)
        assert type_name_count > 0, "无效的数据类型:" + type_name

        self.main_type = type_name[0]
        if DataType.ARRAY_TYPE == self.main_type or DataType.JSON_TYPE == self.main_type:
            if len(type_name) >= 2:
                self.key_type = DataType(type_name[1])
        elif DataType.MAP_TYPE == self.main_type:
            if len(type_name) >= 2:
                self.key_type = DataType(type_name[1])
                self.value_type = DataType(type_name[2])
        elif DataType.INT_TYPE == self.main_type:
            if (len(type_name)) >= 2:
                self.key_type = DataType(type_name[1])

    @staticmethod
    def __analyze_sub_type__(types, index):
        type_name = types[index]
        if DataType.ARRAY_TYPE == type_name or DataType.JSON_TYPE == type_name:
            if len(types[index:]) >= 2:
                new_index, result = DataType.__analyze_sub_type__(types, index + 1)
                return new_index, (type_name, result, )
            return index + 1, (type_name, )
        elif DataType.MAP_TYPE == type_name:
            if len(types[index:]) >= 3:
                new_index, key = DataType.__analyze_sub_type__(types, index + 1)
                new_index, value = DataType.__analyze_sub_type__(types, new_index)
                return new_index, (type_name, key, value, )
            return index + 1, (type_name, )
        elif DataType.INT_TYPE == type_name:
            if len(types[index:]) >= 2 and not DataType.__check_type_valid__(types[index + 1]):
                return index + 2, (type_name, types[index + 1], )
            return index + 1, (type_name,)
        else:
            return index + 1, (type_name, )

    def set_key_type(self, key_type):
        self.key_type = key_type

    def set_value_type(self, value_type):
        self.value_type = value_type

    def to_proto_type(self):
        if DataType.INT_TYPE == self.main_type:  # int类型要判断一下是否为枚举
            if None is not self.key_type:
                return self.key_type.to_proto_type()
            else:
                return self.main_type_proto
        elif DataType.ARRAY_TYPE == self.main_type:  # 数据类型要判断一下存储类型
            return DataType.PROTO_ARRAY_TYPE % self.key_type.to_proto_type()
        elif DataType.MAP_TYPE == self.main_type:
            return DataType.PROTO_MAP_TYPE % (self.key_type.to_proto_type(), self.value_type.to_proto_type())
        elif DataType.JSON_TYPE == self.main_type:
            assert None is not self.key_type, "无法确定Json文件的类型"
            return self.key_type.to_proto_type()
        else:
            return self.main_type_proto

    @staticmethod
    def __check_type_valid__(type_name):
        return type_name in (DataType.STR_TYPE, DataType.INT_TYPE, 
                             DataType.BOOL_TYPE, DataType.ARRAY_TYPE, 
                             DataType.MAP_TYPE, DataType.JSON_TYPE, DataType.LONG_TYPE)

    @staticmethod
    def check_data_type(data):
        """
        todo: 之后可以尝试将检查会都换成正则
        :param data: 检查的对像
        :return: 类型名称
        """
        temp = data.upper()
        if temp.isdigit():
            return DataType.INT_TYPE
        elif None is not re.match(r'^(-?\d+)(\.\d+)?$', data.replace(' ', '')):
            return DataType.FLOAT_TYPE
        elif "TRUE" == temp or "FALSE" == temp:
            return DataType.BOOL_TYPE
        elif len(data) > 0 and '[' == data[0] and ']' == data[-1]:
            return DataType.ARRAY_TYPE
        elif len(data) > 0 and '{' == data[0] and '}' == data[-1]:
            return DataType.MAP_TYPE
        else:
            return DataType.STR_TYPE

    @staticmethod
    def __split_type_name__(type_name):
        type_name_list = list()
        type_name = type_name.split(':')
        for type_name_item in type_name:
            if -1 != type_name_item.find(','):
                sub_type_name_list = type_name_item.split(',')
                for sub_type_name_tiem in sub_type_name_list:
                    type_name_list.append(sub_type_name_tiem)
            else:
                type_name_list.append(type_name_item)
        return type_name_list

    @staticmethod
    def type_to_proto(type_name):
        if DataType.INT_TYPE == type_name:
            return DataType.PROTO_INT_TYPE
        elif DataType.BOOL_TYPE == type_name:
            return DataType.PROTO_BOOL_TYPE
        elif DataType.STR_TYPE == type_name:
            return DataType.PROTO_STR_TYPE
        elif DataType.ARRAY_TYPE == type_name:
            return DataType.PROTO_ARRAY_TYPE
        elif DataType.MAP_TYPE == type_name:
            return DataType.PROTO_MAP_TYPE
        elif DataType.JSON_TYPE == type_name:
            return DataType.PROTO_JSON_TYPE
        elif DataType.LONG_TYPE == type_name:
            return DataType.PROTO_LONG_TYPE
        elif DataType.FLOAT_TYPE == type_name:
            return DataType.PROTO_FLOAT_TYPE
        else:
            return type_name


if __name__ == "__main__":
    data_type = DataType("MAP:ARRAY:JSON:INT,INT:AbilityEffectType")

