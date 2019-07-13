# _*_coding:utf-8_*_

import os
import tqdm
import struct

from ConfigBase.ConfigType import *
from Tools.ModuleHelper import load_module
from Writer.pbjson import *

PROTO_TEMPLATE = """
syntax = "proto3";
option csharp_namespace = "Config";
%(enums)s
%(messages)s
"""

MESSAGE_TEMPLATE = """
message %(message_name)s
{
%(message_fields)s
}
"""

ENUM_TEMPLATE = """
enum %(enum_name)s {
%(enum_fields)s
}
"""


__TYPE_TO_PROTO__ = {
    StringType: "string",
    IntType: "int32",
    LongType: "int64",
    BoolType: "bool",
    ArrayType: "repeated",
    MapType: "map",
    JsonType: "",
    FloatType: "float",
}


def __get_proto_type__(type_inst):
    if isinstance(type_inst, MapType):
        return 'map<%(k)s, %(v)s>' % {
            "k": __get_proto_type__(type_inst.key_type),
            "v": __get_proto_type__(type_inst.value_type)
        }
    elif isinstance(type_inst, ArrayType):


        return 'repeated %(t)s' % {
            "t": __get_proto_type__(type_inst.sub_type),
        }
    elif isinstance(type_inst, IntType):
        if None is type_inst.sub_type:
            return 'int32'
        else:
            return __get_proto_type__(type_inst.sub_type)
    elif isinstance(type_inst, JsonType):
        return __get_proto_type__(type_inst.sub_type)
    elif isinstance(type_inst, EnumType) or isinstance(type_inst, CustomType):
        return type_inst.type_name
    else:
        return __TYPE_TO_PROTO__.get(type_inst, 'int32')


def __spawn_enum_def__(enum_inst):
    enum_fields = ""
    for item in enum_inst.custom_desc:
        field = item[0]
        value = item[1]
        if 'NONE' == field.upper():
            field = enum_inst.type_name + '_' + field.upper()
        enum_fields += '    %(field)s = %(value)d;\n' % {
            "field": field,
            "value": value
        }
    return ENUM_TEMPLATE % {
        "enum_name": enum_inst.type_name,
        "enum_fields": enum_fields
    }


def __spawn_class_def__(class_inst):
    class_fields = ""
    index = 1
    for item in class_inst.custom_desc:
        field = item[0]
        value = item[1]
        class_fields += '    %(type_name)s %(field)s = %(value)d;\n' % {
            "type_name": __get_proto_type__(value),
            "field": field,
            "value": index
        }
        index += 1
    return MESSAGE_TEMPLATE % {
        "message_name": class_inst.type_name,
        "message_fields": class_fields
    }


def __check_id__(data_list):
    for data in data_list:

        type_inst = get_type(data.name)
        if isinstance(type_inst, EnumType) or len(data.data_list) <= 0:
            continue

        # 检查是否存在id,没有的话生成一个并以当前行做为ID号，所有的ID字段都为大写的ID
        for index, field in enumerate(data.fields):
            if 'ID' == field.upper():
                data.fields[index] = 'ID'
                break
        else:
            type_inst.custom_desc.insert(0, ('ID', get_type(INT_TYPE)))
            data.fields.insert(0, 'ID')
            data.types.insert(0, get_type(INT_TYPE))
            data.notes.insert(0, 'Automatic generated ID')
            for index, config_data in enumerate(data.data_list):
                config_data.insert(0, index)


def __data_to_binary__(proto_module, data_list):
    module_inst = load_module(proto_module)
    binary_list = list()

    # 将数据写进DataHelper
    for data in data_list:

        type_inst = get_type(data.name)
        if isinstance(type_inst, EnumType):
            continue

        # 检查是否存在id,没有的话生成一个并以当前行做为ID号，所有的ID字段都为大写的ID
        for index, field in enumerate(data.fields):
            if 'ID' == field.upper():
                data.fields[index] = 'ID'
                break
        else:
            data.fields.insert(0, 'ID')
            data.types.insert(0, get_type(INT_TYPE))
            for index, config_data in enumerate(data.data_list):
                config_data.insert(0, index)

        # 将dict转为proto类
        pb_dict = list()
        cls = getattr(module_inst, data.name)
        for config_data in data.data_list:
            data_dict = dict(zip(data.fields, config_data))
            pb_dict.append(dict2pb(cls, data_dict))
        binary_list.append(__merge_single_binary__(data.name, pb_dict))
    return __merge_all_binary__(binary_list)


def __merge_single_binary__(type_name, binary_data):
    b_type_name = type_name.encode()
    type_name_length = len(type_name)
    binary_head = struct.pack('ii%ds' % (type_name_length,), len(binary_data), type_name_length, b_type_name)
    for inst in binary_data:
        inst_binary = inst.SerializeToString()
        binary_body = struct.pack('i', len(inst_binary)) + inst_binary
        binary_head += binary_body
    return binary_head


def __merge_all_binary__(binary_list):
    binary_head = struct.pack('i', len(binary_list))
    for binary in binary_list:
        binary_head = binary_head + struct.pack('i', len(binary)) + binary
    return binary_head


def spawn_proto_file():
    enum_def = ""
    message_def = ""
    type_tables = get_all_type()
    table_list = list(type_tables.values())

    # 主要用于记录多组数组所产生的额外的类型
    temp = list()

    # 将现有的类型分析成对应的proto数据
    for type_inst in table_list:
        if isinstance(type_inst, EnumType):
            enum_def += __spawn_enum_def__(type_inst)
        elif isinstance(type_inst, CustomType):
            message_def += __spawn_class_def__(type_inst)

    # 将生成过程中额外产生的多组数组类形生成成proto数据
    for type_inst in temp:
        if isinstance(type_inst, EnumType):
            enum_def += __spawn_enum_def__(type_inst)
        elif isinstance(type_inst, CustomType):
            message_def += __spawn_class_def__(type_inst)

    # 合成proto数据
    return PROTO_TEMPLATE % {
        "enums": enum_def,
        "messages": message_def
    }


def write(config, cif_list):
    # 先检查一下ID
    __check_id__(cif_list)

    # 写入proto
    proto_context = spawn_proto_file()
    with open(config.proto_path, 'w') as f:
        f.write(proto_context)

    # 调用Protoc生成proto代码
    os.system("protoc --python_out=%s %s" % (config.py_path, config.proto_path))
    os.system("protoc --csharp_out=%s %s" % (config.cs_path, config.proto_path))

    # 加载proto.py模块
    binary_data = __data_to_binary__(config.python_name, cif_list)
    with open(config.binary_path, 'wb+') as f:
        f.write(binary_data)


if __name__ == '__main__':
    print(__get_proto_type__(new_type('ARRAY:ARRAY:ARRAY:ARRAY:INT', None)))




