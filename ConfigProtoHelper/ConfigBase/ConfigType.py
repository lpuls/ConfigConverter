# _*_coding:utf-8_*_


STR_TYPE = "STR"
INT_TYPE = "INT"
LONG_TYPE = "LONG"
BOOL_TYPE = "BOOL"
ARRAY_TYPE = "ARRAY"
MAP_TYPE = "MAP"
JSON_TYPE = "JSON"
FLOAT_TYPE = "FLOAT"

__TYPE_TABLE__ = dict()
__TYPE_AUTHORITY__ = dict()


class ConfigType:
    def __init__(self):
        pass


class IntType(ConfigType):
    def __init__(self):
        ConfigType.__init__(self)
        self.sub_type = None


class LongType(ConfigType):
    def __init__(self):
        ConfigType.__init__(self)


class FloatType(ConfigType):
    def __init__(self):
        ConfigType.__init__(self)


class BoolType(ConfigType):
    def __init__(self):
        ConfigType.__init__(self)


class StringType(ConfigType):
    def __init__(self):
        ConfigType.__init__(self)


class ArrayType(IntType):
    def __init__(self):
        IntType.__init__(self)


class JsonType(IntType):
    def __init__(self):
        IntType.__init__(self)


class MapType(ConfigType):
    def __init__(self):
        ConfigType.__init__(self)
        self.key_type = None
        self.value_type = None


class CustomType(ConfigType):
    """
    自定义类型
    custom_type: 表示该类型的名称
    custom_desc:
        该类型的描述，这是一个字典
        字段名: 类型
    """
    def __init__(self):
        ConfigType.__init__(self)
        self.type_name = None
        self.custom_desc = dict()


class EnumType(CustomType):
    """
    自定义类型
    custom_type: 表示该类型的名称
    custom_desc:
        该类型的描述，这是一个字典
        字段名: 值
    """
    def __init__(self):
        CustomType.__init__(self)


def __init_type__():
    __TYPE_TABLE__[STR_TYPE] = StringType()
    __TYPE_TABLE__[INT_TYPE] = IntType()
    __TYPE_TABLE__[LONG_TYPE] = LongType()
    __TYPE_TABLE__[BOOL_TYPE] = BoolType()
    __TYPE_TABLE__[FLOAT_TYPE] = FloatType()
    __TYPE_TABLE__[MAP_TYPE] = MapType()
    __TYPE_TABLE__[ARRAY_TYPE] = ArrayType()
    __TYPE_TABLE__[JSON_TYPE] = JsonType()

    # 权限，用于确定类型转换的时候,以值大的类型为主，若相等，说明冲突，以STR为主
    __TYPE_AUTHORITY__[BOOL_TYPE] = {
        BOOL_TYPE: BOOL_TYPE,
        INT_TYPE: INT_TYPE,
        LONG_TYPE: LONG_TYPE,
        FLOAT_TYPE: FLOAT_TYPE,
        JSON_TYPE: STR_TYPE,
        ARRAY_TYPE: STR_TYPE,
        MAP_TYPE: STR_TYPE,
        STR_TYPE: STR_TYPE
    }
    __TYPE_AUTHORITY__[INT_TYPE] = {
        BOOL_TYPE: INT_TYPE,
        INT_TYPE: INT_TYPE,
        LONG_TYPE: LONG_TYPE,
        FLOAT_TYPE: FLOAT_TYPE,
        JSON_TYPE: STR_TYPE,
        ARRAY_TYPE: STR_TYPE,
        MAP_TYPE: STR_TYPE,
        STR_TYPE: STR_TYPE
    }
    __TYPE_AUTHORITY__[LONG_TYPE] = {
        BOOL_TYPE: LONG_TYPE,
        INT_TYPE: LONG_TYPE,
        LONG_TYPE: LONG_TYPE,
        FLOAT_TYPE: FLOAT_TYPE,
        JSON_TYPE: STR_TYPE,
        ARRAY_TYPE: STR_TYPE,
        MAP_TYPE: STR_TYPE,
        STR_TYPE: STR_TYPE
    }
    __TYPE_AUTHORITY__[FLOAT_TYPE] = {
        BOOL_TYPE: FLOAT_TYPE,
        INT_TYPE: FLOAT_TYPE,
        LONG_TYPE: FLOAT_TYPE,
        FLOAT_TYPE: FLOAT_TYPE,
        JSON_TYPE: STR_TYPE,
        ARRAY_TYPE: STR_TYPE,
        MAP_TYPE: STR_TYPE,
        STR_TYPE: STR_TYPE
    }
    __TYPE_AUTHORITY__[JSON_TYPE] = {
        BOOL_TYPE: STR_TYPE,
        INT_TYPE: STR_TYPE,
        LONG_TYPE: STR_TYPE,
        FLOAT_TYPE: STR_TYPE,
        JSON_TYPE: STR_TYPE,
        ARRAY_TYPE: STR_TYPE,
        MAP_TYPE: STR_TYPE,
        STR_TYPE: STR_TYPE
    }
    __TYPE_AUTHORITY__[ARRAY_TYPE] = {
        BOOL_TYPE: STR_TYPE,
        INT_TYPE: STR_TYPE,
        LONG_TYPE: STR_TYPE,
        FLOAT_TYPE: STR_TYPE,
        JSON_TYPE: STR_TYPE,
        ARRAY_TYPE: STR_TYPE,
        MAP_TYPE: STR_TYPE,
        STR_TYPE: STR_TYPE
    }
    __TYPE_AUTHORITY__[MAP_TYPE] = {
        BOOL_TYPE: STR_TYPE,
        INT_TYPE: STR_TYPE,
        LONG_TYPE: STR_TYPE,
        FLOAT_TYPE: STR_TYPE,
        JSON_TYPE: STR_TYPE,
        ARRAY_TYPE: STR_TYPE,
        MAP_TYPE: STR_TYPE,
        STR_TYPE: STR_TYPE
    }
    __TYPE_AUTHORITY__[STR_TYPE] = {
        BOOL_TYPE: STR_TYPE,
        INT_TYPE: STR_TYPE,
        LONG_TYPE: STR_TYPE,
        FLOAT_TYPE: STR_TYPE,
        JSON_TYPE: STR_TYPE,
        ARRAY_TYPE: STR_TYPE,
        MAP_TYPE: STR_TYPE,
        STR_TYPE: STR_TYPE
    }


def get_all_type():
    return __TYPE_TABLE__


def get_type(type_str):
    if len(__TYPE_TABLE__) <= 0:
        __init_type__()

    # 尝试根据类型的字符串找出对应的类型
    return __TYPE_TABLE__.get(type_str, None)


def get_authority(type_str, other_type):
    if len(__TYPE_TABLE__) <= 0:
        __init_type__()
    sub_authority = __TYPE_AUTHORITY__.get(type_str, None)
    if None is not sub_authority:
        return sub_authority.get(other_type, STR_TYPE)
    return STR_TYPE


def __new_type__(type_str):
    index = type_str.find(':')
    if -1 != index:
        pre_type_name = type_str[:index]
        sub_type_str = type_str[index + 1:]
        if MAP_TYPE == pre_type_name:
            # todo 关于多层map循环嵌套……再说吧
            main_type_inst = MapType()
            key_type_str = sub_type_str[:sub_type_str.find(',')]
            value_type_str = sub_type_str[sub_type_str.find(',') + 1:]
            main_type_inst.key_type = __new_type__(key_type_str)
            main_type_inst.value_type = __new_type__(value_type_str)
        elif ARRAY_TYPE == pre_type_name or JSON_TYPE == pre_type_name or MAP_TYPE == pre_type_name:
            main_type_inst = ArrayType()
            main_type_inst.sub_type = __new_type__(sub_type_str)
        return main_type_inst
    return get_type(type_str)


def new_type(name, desc):
    if len(__TYPE_TABLE__) <= 0:
        __init_type__()

    type_inst = __TYPE_TABLE__.get(name, None)
    if None is not type_inst:
        raise Exception('重定义类型 ' + name)
    type_inst = CustomType()
    type_inst.type_name = name.replace(':', '_')

    # 没有描述，说明要从名称直接推导出类型
    if None is not desc:
        type_inst.custom_desc = desc
    else:
        type_inst = __new_type__(name)
    __TYPE_TABLE__[name] = type_inst
    return type_inst


def new_enum(name, value):
    if len(__TYPE_TABLE__) <= 0:
        __init_type__()

    type_inst = __TYPE_TABLE__.get(name, None)
    if None is not type_inst:
        raise Exception('重定义枚举 ' + name)
    type_inst = EnumType()
    type_inst.type_name = name
    type_inst.custom_desc = value
    __TYPE_TABLE__[name] = type_inst
    return type_inst


if __name__ == '__main__':
    new_type('ARRAY:ARRAY:FLOAT')
    # new_type('AbilityType', {
    #     'ID': get_type(INT_TYPE),
    #     'Name': get_type(STR_TYPE)
    # })
    # print(type(get_type('INT')))
    # print(type(get_type('FLOAT')))
    # print(type(get_type('LONG')))
    # print(type(get_type('BOOL')))
    # print(type(get_type('STR')))
    # print(type(get_type('MAP:INT,STR')))
    # print(type(get_type('ARRAY:INT')))
    # print(type(get_type('INT:AbilityType')))
    # print(type(get_type('STR')))
