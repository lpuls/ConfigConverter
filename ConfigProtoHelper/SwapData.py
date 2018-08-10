# _*_coding:utf-8_*_ 

from ProtoHelper import *


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

        type_names = type_name.split(':')
        type_name_count = len(type_names)

        if type_name_count <= 0:
            print("[DataType] 无效的数据类型:", type_name)
            return
        self.main_type = type_names[0]
        self.main_type_proto = DataType.__type_to_proto_type(self.main_type)

        if type_name_count >= 2:
            self.key_type = type_names[1]
            self.value_type = type_names[2]

    @staticmethod
    def __type_to_proto_type(type_name):
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


class SwapData:
    def __init__(self, file_name, types, notes, field):
        self.types = types
        self.notes = notes
        self.fields = field
        self.datas = list()

        # 根据名称前缀确定要生成什么类型的proto代码
        self.is_message = True
        self.file_name = file_name
        if -1 != self.file_name.find("e_"):
            self.is_message = False
            self.file_name = file_name.replace('e_', '')

    def insert(self, data):
        self.datas.append(data)

    def get(self, index):
        if index >= 0 and index < len(self.datas):
            return self.datas[index]

    def analyze(self):
        """
        将记录下来的数据根据类型翻译成python数据
        """
        for index in range(0, len(self.types)):
            # 先分析所有的类型
            type_name = self.types[index]
            data_type = DataType(self.types[index])
            self.types[index] = data_type
            if None is data_type.main_type:
                return False

            # 根据输入类型分析类据，将其转换为proto数据
            #field_name = self.fields[index]
            #for data in self.datas:
            #    new_data = SwapData.__analyze_data_by_type(data[field_name], data_type)
            #    data[field_name] = new_data
        return True
    
    def to_proto(self):
        if self.is_message:
            return self.to_proto_message()
        else:
            return self.to_proto_enum()

    def to_proto_enum(self):
        enum_field = ""
        for data_value in self.datas:
            name = data_value.get("name", None)
            value = data_value.get("value", None)
            annotation = data_value.get("annotation", None)
            if None is name or None is value or None is annotation:
                print("[SwapData]无效的枚举数值定义")
                return None
            enum_field += "\t%(file_name)s_%(enum_name)s = %(enum_value)d;  // %(annotation)s\n" % {
                    "file_name": self.file_name,
                    "enum_name": name,
                    "enum_value": value,
                    "annotation": annotation 
                }
        return enum_field

    def to_proto_message(self):
        message_field = ""
        for index in range(0, len(self.fields)):
            data_type = self.types[index]
            field_name = self.fields[index]
            if None is data_type:
                print("[SwapData] 无法找到%s对应的类型" % field_name)
                return None
            message_field = message_field + "\t%(type_name)s %(field_name)s = %(index)d;\n" % {
                    "type_name": data_type.main_type_proto,
                    "field_name": field_name,
                    "index": index + 1
                }
        # return write_message(self.file_name, message_field)
        return message_field

    @staticmethod
    def __convert_data__(data, data_type):
        if DataType.STR_TYPE == data_type:
            return data
        elif DataType.INT_TYPE == data_type:
            return int(data)
        elif DataType.BOOL_TYPE == data_type:
            return bool(data)

    @staticmethod
    def __check_data_type__(data):
        temp = data.upper()
        if temp.isdigit():
            return DataType.INT_TYPE
        elif "TRUE" == temp or "FALSE" == temp:
            return DataType.BOOL_TYPE
        else:
            return DataType.STR_TYPE

    @staticmethod
    def __analyze_data_by_type(data, data_type):
        main_type = data_type.main_type
        if DataType.STR_TYPE == main_type:
            return data
        elif DataType.INT_TYPE == main_type:
            if None is not data_type.key_type:
                # todo 之后再处理
                return int(data)
            else:
                return int(data)
        elif DataType.ARRAY_TYPE == main_type:
            if None is not data_type.key_type:
                # todo 之后再处理
                return data
            else:
                return data
            pass
        elif DataType.MAP_TYPE == main_type:
            pass
        elif DataType.BOOL_TYPE == main_type:
            pass

    @staticmethod
    def __analyze_array_data__(data, data_type):
        data_length = len(data)
        if data_length <= 0:
            return None

        # 兼容旧类型写法
        temp = data
        if data[0] == '[':
            temp = data[1:]
        if data[data_length - 1] == ']':
            temp = data[:len(temp) - 1]
        
        # 数据以逗号做为分隔
        result = list()
        list_data = data.split(',')
        if len(list_data) > 0:
            if None is not data_type.key_type:
                data_type.key_type = SwapData.__check_data_type__(list_data[0])
            for item in list_data:
                result.append(SwapData.__convert_data__(item))

        return result