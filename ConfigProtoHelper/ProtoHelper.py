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


def write_message_helper(message_name):
    return 


def write_enum(enum_name, enum_fields):
    return ENUM_TEMPLATE % {
                "enum_name": enum_name,
                "enum_fields": enum_fields
            }


def write_proto(enum_list, message_list):
    enum_str = ""
    for enum in enum_list:
        enum_str += enum

    message_str = ""
    for message in message_list:
        message_str += message
    return PROTO_TEMPLATE % { 
            "enums": enum_str, 
            "messages": message_str 
        }


def write_to_file(path, context, modle='w'):
    f = open(path, modle)
    f.write(context)
    f.close()


def process_data_to_proto(path, datas):
    enum_list = list()
    message_list = list()
    for data_name in datas:
        data = datas[data_name]
        result = data.to_proto()
        if isinstance(data, MessageData):
            message_list.append(write_message(data.file_name, result))
        else:
            enum_list.append(write_enum(data.file_name, result))
    context = write_proto(enum_list, message_list)
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
    result = dict()
    for data_key in datas:
        data = datas[data_key]
        if isinstance(data, MessageData):
            pb_list = list()
            cls = getattr(module, data.file_name)
            for config_data in data.datas:
                pb_obj = dict2pb(cls, config_data)
                pb_list.append(pb_obj.SerializeToString())
            result[data.file_name] = pb_list
    return result


def write_to_binary(path, context):
    binary_file = open(path, 'wb')
    result = bytes()
    binary_file.write(struct.pack('i', len(context)))
    for binary_name in context:
        binary_context = context[binary_name]
        name_length = len(binary_name)
        result += struct.pack('i%ssi' % name_length, name_length, binary_name.encode(), len(binary_context))
        for item in binary_context:
            item_length = len(item)
            item_binary = struct.pack('i%ss' % item_length, item_length, item)
            result += item_binary
    binary_file.write(result)
    binary_file.close()


def read_binary(path):
    binary_file = open(path, 'rb')
    binary_context = binary_file.readlines()
    binary_file.close()

    binary = bytearray()
    for context in binary_context:
        binary += context

    file_count = struct.unpack('i', binary[:4])[0]
    file_name_length = struct.unpack('i', binary[4:8])[0]
    file_name = struct.unpack('%ss' % file_name_length, binary[8: 8 + file_name_length])[0]
    print(file_count, file_name_length, file_name, file_context_count)
    return binary