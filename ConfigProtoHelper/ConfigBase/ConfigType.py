# _*_coding:utf-8_*_


__STR_TYPE__ = "STR"
__INT_TYPE__ = "INT"
__LONG_TYPE__ = "LONG"
__BOOL_TYPE__ = "BOOL"
__ARRAY_TYPE__ = "ARRAY"
__MAP_TYPE__ = "MAP"
__JSON_TYPE__ = "JSON"
__FLOAT_TYPE__ = "FLOAT"

__TYPE_TABLE__ = dict()


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
    __TYPE_TABLE__[__STR_TYPE__] = StringType()
    __TYPE_TABLE__[__INT_TYPE__] = IntType()
    __TYPE_TABLE__[__LONG_TYPE__] = LongType()
    __TYPE_TABLE__[__BOOL_TYPE__] = BoolType()
    __TYPE_TABLE__[__FLOAT_TYPE__] = FloatType()
    __TYPE_TABLE__[__MAP_TYPE__] = MapType()
    __TYPE_TABLE__[__ARRAY_TYPE__] = ArrayType()
    __TYPE_TABLE__[__JSON_TYPE__] = JsonType()


def get_all_type():
    return __TYPE_TABLE__


def new_type(name, desc):
    if len(__TYPE_TABLE__) <= 0:
        __init_type__()

    type_inst = __TYPE_TABLE__.get(name, None)
    if None is not type_inst:
        raise Exception('重定义类型 ' + name)
    type_inst = CustomType()
    type_inst.type_name = name
    type_inst.custom_desc = desc
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


def get_type(type_str):
    if len(__TYPE_TABLE__) <= 0:
        __init_type__()

    # 尝试根据类型的字符串找出对应的类型
    type_inst = __TYPE_TABLE__.get(type_str, None)
    if None is type_inst:
        index = type_str.find(':')
        if -1 == index:
            raise Exception('无效类型声明' + type_str)
        main_type_str = type_str[:index]
        type_inst = get_type(main_type_str)
        if -1 != type_str.find(__MAP_TYPE__):
            sub_type_str = type_str[index + 1:]
            index = sub_type_str.find(',')
            key_type_str = sub_type_str[:index]
            value_type_str = sub_type_str[index + 1:]
            type_inst.key_type = get_type(key_type_str)
            type_inst.value_type = get_type(value_type_str)
        elif -1 != index and (-1 != type_str.find(__ARRAY_TYPE__) or
                              -1 != type_str.find(__JSON_TYPE__) or -1 != type_str.find(__INT_TYPE__)):
            type_inst.sub_type = get_type(type_str[index + 1:])
        else:
            raise Exception('未知类型' + type_str)
    return type_inst


if __name__ == '__main__':
    new_type('AbilityType', {
        'ID': get_type(__INT_TYPE__),
        'Name': get_type(__STR_TYPE__)
    })
    print(type(get_type('INT')))
    print(type(get_type('FLOAT')))
    print(type(get_type('LONG')))
    print(type(get_type('BOOL')))
    print(type(get_type('STR')))
    print(type(get_type('MAP:INT,STR')))
    print(type(get_type('ARRAY:AbilityType')))
    print(type(get_type('INT:AbilityType')))
    # print(type(get_type('STR')))
