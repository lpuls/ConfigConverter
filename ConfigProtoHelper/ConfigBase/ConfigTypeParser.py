# _*_coding:utf-8_*_

from ConfigBase.ConfigType import *
from ConfigBase.ConfigTypeHelper import get_type, to_type_name, add_type


__TYPE_PARSER__ = dict()


def __parser_common__(type_list):
    if len(type_list) <= 0:
        raise Exception("无法的类型定义长度")

    head = type_list[0]
    return get_type(head), 1


def __parser_array__(type_list):
    if len(type_list) < 1:
        raise Exception("无效的Array类型定义长度")

    element_inst, new_index = parser(type_list[1:])
    if None is element_inst:
        raise Exception("无效的Array类型定义长度")

    inst = ArrayType(to_type_name(type_list))
    inst.element_type = element_inst
    return inst, new_index + 1


def __parser_dict__(type_list):
    if len(type_list) < 2:
        raise Exception("无效的Map类型定义长度")

    index = 1
    key_inst, new_index = parser(type_list[index:])
    if None is key_inst:
        raise Exception("无效的字典Key类型 " + type_list[index])
    index += new_index

    value_inst, new_index = parser(type_list[index:])
    if None is value_inst:
        raise Exception("无效的数组Value类型 " + type_list[index])
    index += new_index

    inst = MapType(to_type_name(type_list))
    inst.key_type = key_inst
    inst.value_type = value_inst
    return inst, index


def init_parser():
    __TYPE_PARSER__[StringType.DEF] = __parser_common__
    __TYPE_PARSER__[IntType.DEF] = __parser_common__
    __TYPE_PARSER__[LongType.DEF] = __parser_common__
    __TYPE_PARSER__[BoolType.DEF] = __parser_common__
    __TYPE_PARSER__[FloatType.DEF] = __parser_common__
    __TYPE_PARSER__[ArrayType.DEF] = __parser_array__
    __TYPE_PARSER__[MapType.DEF] = __parser_dict__


def add_parser(type_name, parser_func):
    if None is not __TYPE_PARSER__.get(type_name):
        raise Exception("重复定义了解释器 " + type_name)

    __TYPE_PARSER__[type_name] = parser_func


def parser(type_str):
    """
    根据输入的类型字符串列表分析出类型实例
    :param type_str: 要分析的类型字符串
    :return: 解释出来类型，下一个要处理的类型字符串的偏移(所有的解释函数都要返回这个)
    """
    type_list = type_str
    if isinstance(type_str, str):
        type_list = type_str.split(':')

    if None is type_list:
        raise Exception("无䇅的类型定义 " + type_str)

    type_name = type_list[0]
    parser_func = __TYPE_PARSER__.get(type_name, __parser_common__)
    return parser_func(type_list)


def process_structure_element_type(structure):
    for element in structure.desc:
        element_type_str = element.type
        type_name = to_type_name(element_type_str)
        type_inst = get_type(type_name)
        if None is type_inst:
            type_inst, _ = parser(element_type_str)
            if None is type_inst:
                raise Exception("无法正确识别的字段类型 " + element_type_str)
            add_type(type_inst.name, type_inst, isinstance(type_inst, StructureType))
        element.type = type_inst


# if __name__ == '__main__':
#     init_type()
#     init_parser()
#     temp, _ = parser('MAP:INT:ARRAY:FLOAT')
#     print(temp)

