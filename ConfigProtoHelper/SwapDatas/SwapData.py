# _*_coding:utf-8_*_ 

from SwapDatas.DataType import DataType


class SwapData:
    DEFAULT_KEY = "ID"
    DEFAULT_STRING_KEY = "KEY"

    def __init__(self, file_name, types, notes, field):
        self.types = types
        self.notes = notes
        self.fields = field
        self.field_to_type = dict()
        self.data_list = list()
        self.key = None
        self.key_type = None

        # 根据名称前缀确定要生成什么类型的proto代码
        self.is_message = True
        self.file_name = file_name

    def insert(self, data):
        self.data_list.append(data)

    def to_proto(self):
        message_field = ""
        for index in range(0, len(self.fields)):
            field_name = self.fields[index]
            data_type = self.field_to_type.get(field_name, None)  # self.types[index]
            assert data_type, "无法找到%s对应的类型" % field_name

            # 所有的ID都转换成大写
            if 'ID' == field_name.upper():
                field_name = field_name.upper()

            message_field = message_field + "\t%(type_name)s %(field_name)s = %(index)d;\n" % {
                    "type_name": DataType.to_proto_type(data_type),
                    "field_name": field_name,
                    "index": index + 1
                }
        return message_field

    def get(self, index):
        if index <= index <= len(self.data_list):
            return self.data_list[index]

    def analyze(self):
        for index in range(0, len(self.types)):
            field_name = self.fields[index]
            data_type = DataType(self.types[index])
            if DataType.INVALID_TYPE_ERROR == data_type.is_valid:
                return False
            self.types[index] = data_type
            self.field_to_type[field_name] = data_type

            # 检查一下是否存在key键
            if SwapData.check_is_key(field_name):
                self.key = field_name
                self.key_type = data_type

        # 无自带key,则自动生成
        if None is self.key:
            self.auto_key()
        return True

    @staticmethod
    def check_is_key(field):
        upper = field.upper()
        return upper == SwapData.DEFAULT_STRING_KEY or upper == SwapData.DEFAULT_KEY

    def auto_key(self):
        key_data_type = DataType(DataType.INT_TYPE)
        self.types.insert(0, key_data_type)
        self.fields.insert(0, SwapData.DEFAULT_KEY)
        self.field_to_type[SwapData.DEFAULT_KEY] = key_data_type
        key_value = 1
        for data in self.data_list:
            data[SwapData.DEFAULT_KEY] = key_value
            key_value += 1
        self.key = SwapData.DEFAULT_KEY
        self.key_type = key_data_type

    def get_key_type(self, key, str_key):
        for field in self.fields:
            upper = field.upper()
            if upper == key:
                field_type = self.field_to_type.get(field, None)
                if None is not field_type:
                    self.key = field
                    return DataType.type_to_proto(field_type.main_type)
            elif upper == str_key:
                field_type = self.field_to_type.get(field, None)
                if None is not field_type:
                    self.key = field
                    return DataType.type_to_proto(field_type.main_type)
        return None

    def __repr__(self):
        result = ""
        for type_value in self.types:
            result += str(type_value)
            result += "\t"
        
        result += "\n"
        for field in self.fields:
            result += field
            result += "\t"

        result += "\n"
        for note in self.notes:
            result += note
            result += "\t"

        result += "\n"
        for data_value in self.data_list:
            for key in data_value:
                data = data_value[key]
                result = result + str(data) + "\t" + str(type(data)) + "\t"
            result += "\n"
        return result
