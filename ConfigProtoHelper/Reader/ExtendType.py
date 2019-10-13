# _*_coding:utf-8_*_

from ConfigBase.ConfigType import *
from ConfigBase.ConfigTypeParser import parser, add_parser, to_type_name


class Array2D(StructureType):
    def __init__(self, name, desc):
        StructureType.__init__(self, name, desc)
        self.element_type = None

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


def __parser_array_2d__(type_list):
    if len(type_list) < 1:
        raise Exception("无效的Array2D类型定义长度")

    index = 1
    element_type_inst, offset = parser(type_list[index:])
    if None is element_type_inst:
        raise Exception("无效的Array2D的成员类型定义")

    array_inst = ArrayType(to_type_name(type_list))
    array_inst.element_type = element_type_inst
    inst = Array2D(element_type_inst.name + "Array2D",
                   [StructureType.StructureElement("Data", "数组数据", array_inst)])
    inst.element_type = element_type_inst
    return inst, offset


def init_extend_parser():
    add_parser('ARRAY2D', __parser_array_2d__)
