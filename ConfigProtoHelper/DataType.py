# _*_coding:utf-8_*_ 

class DataType:
    STR_TYPE = "STR"
    INT_TYPE = "INT"
    BOOL_TYPE = "BOOL"
    ARRAY_TYPE = "ARRAY"
    MAP_TYPE = "MAP"

    PROTO_INT_TYPE = "int32"
    PROTO_STR_TYPE = "string"
    PROTO_BOOL_TYPE = "bool"
    PROTO_ARRAY_TYPE = "repeated"

    def __init__(self, type_name):
        self.main_type = None
        self.key_type = None
        self.value_type = None
        self.main_type_proto = None
        self.key_type_proto = None
        self.value_type_proto = None

        type_names = type_name.split(':')
        type_name_count = len(type_names)

        assert type_name_count > 0, "无效的数据类型:" + type_name 
        self.main_type = type_names[0]

        # 尝试直接从传放类型字符取出
        if type_name_count >= 2:
            self.key_type = type_names[1]
        if type_name_count >= 3:
            self.value_type = type_names[2]

        # 先尝试生成proto类型
        self.main_type_proto = DataType.type_to_proto(self.main_type) 
        self.key_type_proto = DataType.type_to_proto(self.key_type) 
        self.value_type_proto = DataType.type_to_proto(self.value_type) 

    def set_key_type(self, key_type):
        self.key_type = key_type
        self.key_type_proto = DataType.type_to_proto(self.key_type) 

    def set_value_type(self, value_type):
        self.value_type = value_type
        self.value_type_proto = DataType.type_to_proto(self.value_type)

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
                return DataType.PROTO_INT_TYPE
          elif DataType.BOOL_TYPE == type_name:
                return DataType.PROTO_BOOL_TYPE
          elif DataType.STR_TYPE == type_name:
                return DataType.PROTO_STR_TYPE
          elif DataType.ARRAY_TYPE == type_name:
                return DataType.PROTO_ARRAY_TYPE
          elif DataType.MAP_TYPE == type_name:
                return DataType.ARRAY_TYPE
