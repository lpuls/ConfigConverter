# _*_coding:utf-8_*_

import json


class ConfigType:
    def __init__(self, name):
        self.name = name
        pass


class IntType(ConfigType):
    DEF = 'INT'

    def __init__(self):
        ConfigType.__init__(self, IntType.DEF)

    @staticmethod
    def to_data(v):
        return int(v)


class LongType(ConfigType):
    DEF = 'LONG'

    def __init__(self):
        ConfigType.__init__(self, LongType.DEF)

    def to_data(self, v):
        return int(v)


class FloatType(ConfigType):
    DEF = 'FLOAT'

    def __init__(self):
        ConfigType.__init__(self, FloatType.DEF)

    def to_data(self, v):
        return float(v)


class BoolType(ConfigType):
    DEF = 'BOOL'

    def __init__(self):
        ConfigType.__init__(self, BoolType.DEF)

    def to_data(self, v):
        return bool(v)


class StringType(ConfigType):
    DEF = 'STR'

    def __init__(self):
        ConfigType.__init__(self, StringType.DEF)

    def to_data(self, v):
        return str(v)


class ArrayType(ConfigType):
    DEF = 'ARRAY'

    def __init__(self, name):
        ConfigType.__init__(self, name)
        self.element_type = None

    def to_data(self, v):
        new_list = list()
        if isinstance(v, str):
            temp = json.loads(v)
        else:
            temp = v
        for index, item in enumerate(temp):
            new_list.append(self.element_type.to_data(item))
        return new_list


class MapType(ConfigType):
    DEF = 'MAP'

    def __init__(self, name):
        ConfigType.__init__(self, name)
        self.key_type = None
        self.value_type = None

    def to_data(self, v):
        new_dict = dict()
        temp = json.loads(v)
        for key, value in temp.items():
            key = self.key_type.to_data(key)
            value = self.value_type.to_data(value)
            new_dict[key] = value
        return new_dict


class EnumType(ConfigType):
    def __init__(self, name, desc, note):
        ConfigType.__init__(self, name)
        self.desc = desc
        self.note = note

    def to_data(self, v):
        return self.desc.get(v, 0)


class StructureType(ConfigType):
    class StructureElement:
        def __init__(self, field, note, type_inst):
            self.field = field
            self.note = note
            self.type = type_inst

    def __init__(self, name, desc):
        ConfigType.__init__(self, name)
        self.desc = desc
        self.data = list()

    def to_data(self, v):
        data = dict()
        for element in self.desc:
            value = v[element.field]
            data[element.field] = element.type.to_data(value)
        return data

