# _*_coding:utf-8_*_

from ConfigBase.ConfigType import *
from ConfigBase.ConfigHelper import get_type, add_type


class Array2D(StructureType):
    def __init__(self):
        self.element_type = None
        self.desc = None

    def to_data(self, v):
        if isinstance(v, str):
            temp = json.loads(v)
        else:
            temp = v
        data = dict()
        for index, item in enumerate(temp):
            element_list = list()
            for value in item:
                element_list.append(self.element_type.to_data(value))
            data[index] = element_list
        return data


class IntArray2D(Array2D):
    def __init__(self):
        ConfigType.__init__(self, "IntArray2D")
        self.element_type = get_type(IntType.DEF)
        self.desc = [StructureType.StructureElement("Data", "数组数据", self.element_type)]


class LongArray2D(Array2D):
    def __init__(self):
        ConfigType.__init__(self, "LongArray2D")
        self.element_type = get_type(LongType.DEF)
        self.desc = [StructureType.StructureElement("Data", "数组数据", self.element_type)]


class FloatArray2D(Array2D):
    def __init__(self):
        ConfigType.__init__(self, ArrayType.DEF)
        self.element_type = get_type(FloatType.DEF)
        self.desc = [StructureType.StructureElement("Data", "数组数据", self.element_type)]


class BoolArray2D(Array2D):
    def __init__(self):
        ConfigType.__init__(self, "BoolArray2D")
        self.element_type = get_type(BoolType.DEF)
        self.desc = [StructureType.StructureElement("Data", "数组数据", self.element_type)]


class StringArray2D(Array2D):
    def __init__(self):
        ConfigType.__init__(self, "StringArray2D")
        self.element_type = get_type(StringType.DEF)
        self.desc = [StructureType.StructureElement("Data", "数组数据", self.element_type)]


def init_extend_type():
    add_type("IntArray2D", IntArray2D(), True)
    add_type("LongArray2D", LongArray2D(), True)
    add_type("FloatArray2D", FloatArray2D(), True)
    add_type("BoolArray2D", BoolArray2D(), True)
    add_type("StringArray2D", StringArray2D(), True)


if __name__ == '__main__':
    a = Array2D()
    a.element_type = IntType()
    print(a.to_data('[[1, 2, 3, 4], [5, 6, 7, 8]]'))

