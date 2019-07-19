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


def get_type_from_type_list(types):
    new_types = list()
    for index, item in enumerate(types):
        type_inst = get_type(item)
        if None is type_inst:
            type_inst = new_type(item, None)
        new_types.append(type_inst)
    return new_types


def pre_process_and_check_type(data_str, data_type):
    result = None
    if isinstance(data_type, JsonType):
        result = json.loads(data_str)
    elif isinstance(data_type, ArrayType):
        # 根据是否为json字符串先处理数据
        array_data = data_str
        if isinstance(data_str, str):
            array_data = json.loads(data_str)

        # 是否确定的元素类型
        if None is data_type.sub_type:
            type_str = __check_array_element_type__(array_data)
            data_type = get_type(type_str)
            if None is data_type:
                data_type = new_type(type_str, None)
        if None is data_type:
            raise Exception('无法处理的数组对像')

        # 根据确定了的元还给类型将所有子元素处处理一下
        for index in range(0, len(array_data)):
            array_data[index], _ = pre_process_and_check_type(array_data[index], data_type.sub_type)

        # 将处理完的结果及确定了的类型返回
        result = array_data
    elif isinstance(data_type, IntType):
        result = int(data_str)
    elif isinstance(data_type, LongType):
        result = int(data_str)
    elif isinstance(data_type, FloatType):
        result = int(data_str)
    elif isinstance(data_type, BoolType):
        if isinstance(data_str, str):
            result = True if 'TRUE' == data_str.upper() else False
        else:
            result = bool(data_str)
    elif isinstance(data_type, StringType):
        result = data_str
    elif isinstance(data_type, MapType):
        # todo json只支持以str为key，这边也先这先规定，以后再处理
        array_data = data_str
        if isinstance(data_str, str):
            array_data = json.loads(data_str)

        new_dict = dict()
        for key, value in array_data.items():
            key_value, _ = pre_process_and_check_type(key, data_type.key_type)
            value_value, _ = pre_process_and_check_type(value, data_type.value_type)
            new_dict[key_value] = value_value

        result = new_dict
    return result, data_type


if __name__ == '__main__':
    _2d_array = new_type('ARRAY:ARRAY:INT', None)
    _spec_map_ = new_type('MAP:INT,ARRAY:INT', None)
    v, t = pre_process_and_check_type('[[1, 2, 3], [1, 2, 3], [1, 2, 3]]', _2d_array)
    print(v, type(t))
    v, t = pre_process_and_check_type('{"1":[1, 2, 3], "2": [3, 4, 5]}', _spec_map_)
    print(v, type(t))
