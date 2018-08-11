# _*_coding:utf-8_*_ 

class DataType:
    STR_TYPE = "STR"
    INT_TYPE = "INT"
    BOOL_TYPE = "BOOL"
    ARRAY_TYPE = "ARRAY"
    MAP_TYPE = "MAP"

    def __init__(self, type_name):
        self.main_type = None
        self.key_type = None
        self.value_type = None
        self.main_type_proto = None
        self.key_type_proto = None
        self.value_type_proto = None

        type_names = type_name.split(':')
        type_name_count = len(type_names)

        assert type_name_count > 0, "[DataType] 无效的数据类型:" + type_name 
        self.main_type = type_names[0]

        # 尝试直接从传放类型字符取出
        if type_name_count >= 2:
            self.key_type = type_names[1]
        if type_name_count >= 3:
            self.value_type = type_names[2]

    def check_proto_type():
        pass

    @staticmethod
    def __type_to_proto_type(type_name, key_type, value_type, data_value):
        main_type_value = type_to_proto(type_name)
        assert main_type_value, print("[DataType] 无法确定类型 " + type_name)

        key_type_value = None
        value_type_value = None
        # 根据主类型决定子类型的proto类型
        if DataType.ARRAY_TYPE == type_name:
            # 直接转换
            if None is key_type:
               key_type_value = type_to_proto(key_type)
            # 无法直接转换则需要根据数值来确定
            if None is key_type_value:
                key_type_value = check_data_type(data_value)
            # 数据也无法确定，说明有错
            assert key_type_value, "[DataType] 无法确定数组类型 %s, %s, %s, %s" % (type_name, key_type, value_type, data_value,)
        elif DataType.MAP_TYPE == type_name:
            pass
        return main_type_value, key_type_value, value_type_value

    @staticmethod
    def check_data_type(data):
            temp = data.upper()
            if temp.isdigit():
                return DataType.INT_TYPE
            elif "TRUE" == temp or "FALSE" == temp:
                return DataType.BOOL_TYPE
            else:
                return DataType.STR_TYPE

    @staticmethod
    def type_to_proto(type_name):
          if DataType.INT_TYPE == type_name:
                return "int32"
          elif DataType.BOOL_TYPE == type_name:
                return "bool"
          elif DataType.STR_TYPE == type_name:
                return "string"
          elif DataType.ARRAY_TYPE == type_name:
                return "required"
          elif DataType.MAP_TYPE == type_name:
                return "required"
