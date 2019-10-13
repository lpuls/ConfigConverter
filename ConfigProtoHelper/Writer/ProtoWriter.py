# _*_coding:utf-8_*_

from ConfigBase.ConfigType import *
from ConfigBase.ConfigHelper import get_enum_type_dict, get_structure_type_dict


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



