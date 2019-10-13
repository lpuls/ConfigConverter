# _*_coding:utf-8_*_

import os
import struct
from ConfigBase.ConfigType import *
from ConfigBase.ConfigTypeHelper import get_enum_type_dict, get_structure_type_dict
from Tools.ModuleHelper import load_module
from Writer.pbjson import *


__ENUM_ELEMENT_TEMPLATE__ = """\t{name} = {value};\n"""

__ENUM_TEMPLATE__ = """enum {enum_name} {{
{enum_context}
}}

"""

__STRUCTURE_ELEMENT_TEMPLATE__ = """\t{type} {name} = {value};\n"""

__STRUCTURE_TEMPLATE__ = """message {structure_name} {{
{structure_context}
}}

"""

__PROTO_TEMPLATE__ = """syntax = "proto3";

option csharp_namespace = "{package_name}";

{enums}

{structures}

"""

__PROTO_NAME_TABLE__ = {
    IntType.DEF: "int32",
    LongType.DEF: "int64",
    FloatType.DEF: "float",
    StringType.DEF: "string",
    BoolType.DEF: "bool",
}


def __get_proto_type_name__(type_inst):
    if isinstance(type_inst, ArrayType):
        return "repeated {type}".format(type=__get_proto_type_name__(type_inst.element_type))
    elif isinstance(type_inst, MapType):
        return "map<{key}, {value}>".format(key=__get_proto_type_name__(type_inst.key_type),
                                            value=__get_proto_type_name__(type_inst.value_type))
    elif isinstance(type_inst, StructureType) or isinstance(type_inst, EnumType):
        return type_inst.name
    else:
        return __PROTO_NAME_TABLE__.get(type_inst.name, None)


def spawn_proto_file(package_name, proto_save_path):
    enums = ''
    enum_dict = get_enum_type_dict()
    for enum_type_name, item in enum_dict.items():
        context = ""
        temp = [None] * len(item.desc)
        for enum_name, enum_value in item.desc.items():
            temp[enum_value] = enum_name
        for enum_value, enum_name in enumerate(temp):
            enum_result_name = enum_type_name + "_" + enum_name
            context += __ENUM_ELEMENT_TEMPLATE__.format(name=enum_result_name, value=enum_value)
        context = __ENUM_TEMPLATE__.format(enum_name=enum_type_name, enum_context=context)
        enums += context

    structures = ''
    structure_dict = get_structure_type_dict()
    for structure_name, item in structure_dict.items():
        context = ""
        for index, element in enumerate(item.desc):
            context += __STRUCTURE_ELEMENT_TEMPLATE__.format(type=__get_proto_type_name__(element.type),
                                                             name=element.field, value=index + 1)
        structures += __STRUCTURE_TEMPLATE__.format(structure_name=structure_name, structure_context=context)

    context = __PROTO_TEMPLATE__.format(package_name=package_name, enums=enums, structures=structures)

    with open(proto_save_path, 'w') as f:
        f.write(context)


def call_proto_executor(cs_path, python_path, proto_path):
    os.system("protoc --python_out=%s %s" % (python_path, proto_path))
    os.system("protoc --csharp_out=%s %s" % (cs_path, proto_path))


def to_binary(proto_module, save_path):
    module_inst = load_module(proto_module)
    binary_list = list()

    # 将数据写进DataHelper
    type_inst_list = get_structure_type_dict()
    for type_name, type_inst in type_inst_list.items():

        if isinstance(type_inst, EnumType) or (isinstance(type_inst, StructureType) and len(type_inst.data) <= 0):
            continue

        # 检查是否存在id,没有的话生成一个并以当前行做为ID号，所有的ID字段都为大写的ID
        for element_inst in type_inst.desc:
            if 'ID' == element_inst.field.upper():
                break
        else:
            print("[Warning] 没有找到有效的ID字磁，将跳过 " + type_inst.name)
            continue

        # 将dict转为proto类
        pb_dict = list()
        cls = getattr(module_inst, type_inst.name)
        for config_data in type_inst.data:
            pb_dict.append(dict2pb(cls, config_data))
        binary_list.append(__merge_single_binary__(type_inst.name, pb_dict))
    binary_data = __merge_all_binary__(binary_list)

    with open(save_path, 'wb') as f:
        f.write(binary_data)


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


