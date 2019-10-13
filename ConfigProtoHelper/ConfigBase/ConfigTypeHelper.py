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
    if isinstance(type_str, str):
        return type_str.replace(':', '_')
    else:
        return '_'.join(type_str)


def add_enum_type(name, desc, note):
    if None is not __TYPE_TABLE__.get(name, None):
        print('重定义枚举类型 ' + name)
        return

    enum_inst = EnumType(name, desc, note)
    __TYPE_TABLE__[name] = enum_inst
    __TYPE_ENUM__[name] = enum_inst


def add_type(name, type_inst, is_structure=True):
    if None is not __TYPE_TABLE__.get(name, None):
        print('重定义类型 ' + name)
        return

    __TYPE_TABLE__[name] = type_inst
    if is_structure:
        __TYPE_STRUCTURE__[name] = type_inst


def add_structure_type(name, desc):
    if None is not __TYPE_TABLE__.get(name, None):
        print('重定义结构类型 ' + name)
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


def get_enum_type_dict():
    return __TYPE_ENUM__


def get_structure_type_dict():
    return __TYPE_STRUCTURE__


if __name__ == '__main__':
    init_type()
    temp = spawn_custom_type('ARRAY:MAP:INT:STR')
    pass

