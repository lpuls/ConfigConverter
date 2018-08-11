# _*_coding:utf-8_*_ 

from ProtoHelper import *
from DataType import DataType


class SwapData:
    def __init__(self, file_name, types, notes, field):
        self.types = types
        self.notes = notes
        self.fields = field
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
            self.types[index] = data_type
