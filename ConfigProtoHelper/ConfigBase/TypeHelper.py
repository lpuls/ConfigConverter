# _*_coding:utf-8_*_

import json
from ConfigBase.ConfigType import *


def __check_str_value_type__(data):
    if isinstance(data, bool):
        return BOOL_TYPE
    elif isinstance(data, int):
        return INT_TYPE
    elif isinstance(data, float):
        return FLOAT_TYPE
    elif isinstance(data, str):
        return STR_TYPE
    elif isinstance(data, list):
        return __check_array_element_type__(data)
    else:
        None


def __check_array_element_type__(array):
    if len(array) > 0:
        temp_type = __check_str_value_type__(array[0])
        for item in array:
            item_type = __check_str_value_type__(item)
            if temp_type != item_type:
                temp_type = get_authority(temp_type, item_type)
    else:
        temp_type = STR_TYPE

    return ARRAY_TYPE + ':' + temp_type


def __check_map_key_value_type__(map_str, key_type, value_type):
    pass


def pre_process_and_check_type(data_str, data_type):
    if isinstance(data_type, ArrayType):
        # 根据是否为json字符串先处理数据
        array_data = data_str
        if isinstance(data_str, str):
            array_data = json.loads(data_str)

        # 是否确定的元素类型
        if None is data_type.sub_type:
            data_type = get_type(__check_array_element_type__(array_data))

        # 根据确定了的元还给类型将所有子元素处处理一下
        for index in range(0, len(array_data)):
            array_data[index], _ = pre_process_and_check_type(array_data[index], data_type)

        # 将处理完的结果及确定了的类型返回
        return array_data,
    elif isinstance(data_type, JsonType):
        return json.loads(data_str), data_type
    elif isinstance(data_type, IntType):
        # todo: 之后再处理枚举的问题
        return int(data_str), data_type
    elif isinstance(data_type, LongType):
        return int(data_str), data_type
    elif isinstance(data_type, FloatType):
        return float(data_str), data_type
    elif isinstance(data_type, BoolType):
        return True if 'TRUE' == data_str.upper() else False, data_type
    elif isinstance(data_type, StringType):
        return data_str, data_type
    elif isinstance(data_type, MapType):
        return None, __check_map_key_value_type__(data_str, data_type.key_type, data_type.value_type)


if __name__ == '__main__':
    new_type('ARRAY:ARRAY:INT', None)
    v, t = pre_process_and_check_type('[[1, 2, 3], [1, 2, 3], [1, 2, 3]]', get_type(ARRAY_TYPE))
    print(v, type(t))
