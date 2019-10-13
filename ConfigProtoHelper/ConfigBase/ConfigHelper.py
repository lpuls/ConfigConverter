# _*_coding:utf-8_*_

from ConfigBase.ConfigType import *


__TYPE_TABLE__ = dict()
__TYPE_ENUM__ = dict()
__TYPE_STRUCTURE__ = dict()


def init_type():
    __TYPE_TABLE__[StringType.DEF] = StringType()
    __TYPE_TABLE__[IntType.DEF] = IntType()
    __TYPE_TABLE__[LongType.DEF] = LongType()
    __TYPE_TABLE__[BoolType.DEF] = BoolType()
    __TYPE_TABLE__[FloatType.DEF] = FloatType()


def to_type_name(type_str):
    return type_str.replace(':', '_')


def add_enum_type(name, desc, note):
    if None is not __TYPE_TABLE__.get(name, None):
        print('重定义枚举类型 ' + name)
        return

    enum_inst = EnumType(name, desc, note)
    __TYPE_TABLE__[name] = enum_inst
    __TYPE_ENUM__[name] = enum_inst


def add_type(name, type_inst, is_structure=True):
    if None is not __TYPE_TABLE__.get(name, None):
        print('重定义枚举类型 ' + name)
        return

    __TYPE_TABLE__[name] = type_inst
    if is_structure:
        __TYPE_STRUCTURE__[name] = type_inst


def add_structure_type(name, desc):
    if None is not __TYPE_TABLE__.get(name, None):
        print('重定义枚举类型 ' + name)
        return

    inst = StructureType(name, desc)
    __TYPE_TABLE__[name] = inst
    __TYPE_STRUCTURE__[name] = inst


def add_array_or_map_type(name, inst):
    if None is not __TYPE_TABLE__.get(name, None):
        print('重定义枚举类型 ' + name)
        return

    __TYPE_TABLE__[name] = inst


def get_type(name):
    return __TYPE_TABLE__.get(name, None)


def __spawn_custom_type__(type_context_list):
    if len(type_context_list) <= 0:
        raise Exception("请输入有效类型")
        return

    index = 1
    head = type_context_list[0]
    if 'ARRAY' == head and len(type_context_list) >= 2:
        element_inst, new_index = __spawn_custom_type__(type_context_list[index:])
        if None is element_inst:
            raise Exception("无效的数组类型")
        inst = ArrayType()
        inst.element_type = element_inst
        index += new_index
    elif 'MAP' == head:
        key_inst, new_index = __spawn_custom_type__(type_context_list[index:])
        if None is key_inst:
            raise Exception("无效的字典Key类型 " + type_context_list[index])
        index += new_index

        value_inst, new_index = __spawn_custom_type__(type_context_list[index:])
        if None is value_inst:
            raise Exception("无效的数组Value类型 " + type_context_list[index])
        index += new_index

        inst = MapType()
        inst.key_type = key_inst
        inst.value_type = value_inst
    else:
        inst = get_type(head)
    return inst, index


def spawn_custom_type(type_context_str):
    type_list = type_context_str.split(':')
    type_inst, _ = __spawn_custom_type__(type_list)
    return type_inst


def process_structure_element_type(structure):
    for element in structure.desc:
        element_type_str = element.type
        type_name = to_type_name(element_type_str)
        type_inst = get_type(type_name)
        if None is type_inst:
            type_inst = spawn_custom_type(element_type_str)
            if None is type_inst:
                raise Exception("无法正确识别的字段类型 " + element_type_str)
            add_array_or_map_type(type_name, type_inst)
        element.type = type_inst


def get_enum_type_dict():
    return __TYPE_ENUM__


def get_structure_type_dict():
    return __TYPE_STRUCTURE__


if __name__ == '__main__':
    init_type()
    temp = spawn_custom_type('ARRAY:MAP:INT:STR')
    pass

