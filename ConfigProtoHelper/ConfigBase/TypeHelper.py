# _*_coding:utf-8_*_

import json
from ConfigBase.ConfigType import *


def __check_base_type__(data):
    if isinstance(data, int):
        return get_type(IntType)
    elif isinstance(data, float):
        return get_type(FloatType)
    elif isinstance(data, bool):
        return get_type(BoolType)
    elif isinstance(data, str):
        return get_type(StringType)
    else:
        None


def __process_array__(array_str, element_type):
    result = json.loads(array_str)

    if None is element_type:
        temp_type = get_type(IntType)
        for item in result:
            pass

    return result, element_type


def __process_map__(map_str, key_type, value_type):
    pass


def process(data_str, data_type):
    if isinstance(data_type, IntType):
        # todo: 之后再处理枚举的问题
        return int(data_str)
    elif isinstance(data_type, LongType):
        return int(data_str)
    elif isinstance(data_type, FloatType):
        return float(data_str)
    elif isinstance(data_type, BoolType):
        return True if 'TRUE' == data_str.upper() else False
    elif isinstance(data_type, StringType):
        return data_str
    elif isinstance(data_type, MapType):
        return __process_map__(data_str, data_type.key_type, data_type.value_type)
    elif isinstance(data_type):
        return __process_array__(data_str, data_type.sub_type)


if __name__ == '__main__':
    v, _ = process_array('[1, 2, 3]', None)
    print(type(v[0]))
