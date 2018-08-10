# _*_coding:utf-8_*_

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


def write_to_file(path, context):
    f = open(path, 'w')
    f.write(context)
    f.close()


def process_data_to_proto(path, datas):
    enum_list = list()
    message_list = list()
    for data_name in datas:
        data = datas[data_name]
        result = data.to_proto()
        if data.is_message:
            message_list.append(write_message(data.file_name, result))
        else:
            enum_list.append(write_enum(data.file_name, result))
    context = write_proto(enum_list, message_list)
    print(context)
    write_to_file(path, context)
