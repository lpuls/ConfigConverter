# _*_coding:utf-8_*_

import struct
from pbjson import *
from SwapData import *
from EnumData import *
from MessageData import *
from ProtoTemplate import *

def write_message(message_name, message_fields):
    return MESSAGE_TEMPLATE % {
                "message_name": message_name,
                "message_fields": message_fields
            }


def write_enum(enum_name, enum_fields):
    return ENUM_TEMPLATE % {
                "enum_name": enum_name,
                "enum_fields": enum_fields
            }


def write_proto(enum_list, message_helper, message_list):
    enum_str = ""
    for enum in enum_list:
        enum_str += enum

    message_str = ""
    for message in message_list:
        message_str += message
    return PROTO_TEMPLATE % { 
            "enums": enum_str, 
            "messages": message_str,
            "message_list": message_helper 
        }


def write_to_file(path, context, modle='w'):
    f = open(path, modle)
    f.write(context)
    f.close()


def process_data_to_proto(path, datas):
    enum_list = list()
    message_list = list()
    message_helper_list = list()
    field_index = 1
    message_helper = ""
    for data_name in datas:
        data = datas[data_name]
        result = data.to_proto()
        if isinstance(data, MessageData):
            message_list.append(write_message(data.file_name, result))
            message_helper = message_helper + ("\trepeated %(message_name)s %(message_name)s_list = %(field_index)d;\n" % {
                    "message_name": data.file_name,
                    "field_index": field_index
                })
            field_index += 1
        else:
            enum_list.append(write_enum(data.file_name, result))
    context = write_proto(enum_list, message_helper, message_list)
    print(context)
    write_to_file(path, context)


def __load_module__(path):
    paths = path.split('.')
    if len(paths) <= 0:
        return None

    module = __import__(path)
    for index in range(1, len(paths)):
        module = getattr(module, paths[index])
    return module


def data_to_binary(proto_module, datas):
    module = __load_module__(proto_module)

    # 生成DataHelper
    dataHelper = getattr(module, "DataHelper")
    dataHelper = dataHelper()

    # 将数据写进DataHelper
    for data_key in datas:
        data = datas[data_key]
        print(data_key)
        if isinstance(data, MessageData):
            # 获取DataHelper中对应类的列表
            data_list = getattr(dataHelper, data.file_name + "_list")
            
            # 将dict转为proto类
            pb_list = list()
            cls = getattr(module, data.file_name)
            for config_data in data.datas:
                pb_obj = dict2pb(cls, config_data)
                pb_list.append(pb_obj)
            data_list.extend(pb_list)
    return dataHelper


def write_to_binary(path, context):
    binary_file = open(path, 'wb')
    binary_file.write(context.SerializeToString())
    binary_file.close()


def read_binary(path, pb_obj):
    binary_file = open(path, 'rb')
    binary_context = binary_file.readlines()
    binary_file.close()

    binary = bytearray()
    for context in binary_context:
        binary += context

    pb_obj.ParseFromString(binary)
    return pb_obj