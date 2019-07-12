# _*_coding:utf-8_*_

import os
import struct
from Writer.Proto.pbjson import *
from ConfigBase.ConfigType import *
from Tools.ModuleHelper import load_module

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


def __data_to_binary__(proto_module, data_list):
    module_inst = load_module(proto_module)
    binary_list = list()

    # 将数据写进DataHelper
    for data in data_list:

        type_inst = get_type(data.name)
        if isinstance(type_inst, EnumType):
            continue

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
    for _, type_inst in type_tables.items():
        if isinstance(type_inst, EnumType):
            enum_def += __spawn_enum_def__(type_inst)
        elif isinstance(type_inst, CustomType):
            message_def += __spawn_class_def__(type_inst)
    return PROTO_TEMPLATE % {
        "enums": enum_def,
        "messages": message_def
    }


def write(config, cif_list):
    # 写入proto
    proto_context = spawn_proto_file()
    # with open('./Temp/Config.proto', 'w') as f:
    with open(config.proto_path, 'w') as f:
        f.write(proto_context)

    # 调用Protoc生成proto代码
    # os.system("protoc --python_out=./ ./Temp/Config.proto")
    # os.system("protoc --csharp_out=./Temp ./Temp/Config.proto")
    os.system("protoc --python_out=%s %s" % (config.py_path, config.proto_path))
    os.system("protoc --csharp_out=%s %s" % (config.cs_path, config.proto_path))

    # 加载proto.py模块
    binary_data = __data_to_binary__(config.python_name, cif_list)
    with open(config.binary_path, 'wb+') as f:
        f.write(binary_data)




