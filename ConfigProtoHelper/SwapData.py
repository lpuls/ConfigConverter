# _*_coding:utf-8_*_ 

from ProtoHelper import *
from DataType import DataType


class SwapData:
    def __init__(self, file_name, types, notes, field):
        self.types = types
        self.notes = notes
        self.fields = field
        self.field_to_type = dict()
        self.datas = list()

        # 根据名称前缀确定要生成什么类型的proto代码
        self.is_message = True
        self.file_name = file_name

    def insert(self, data):
        self.datas.append(data)

    def to_proto(self):
        return None

    def get(self, index):
        if index >= 0 and index < len(self.datas):
            return self.datas[index]

    def analyze(self):
        for index in range(0, len(self.types)):
            type_name = self.types[index]
            field_name = self.fields[index]
            data_type = DataType(self.types[index])
            if DataType.INVALD_TYPE_ERROR == data_type.is_valid:
                return False
            self.types[index] = data_type
            self.field_to_type[field_name] = data_type
        return True

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
        for data_value in self.datas:
            for key in data_value:
                data = data_value[key]
                result = result + str(data) + "\t" + str(type(data)) + "\t"
            result += "\n"
        return result