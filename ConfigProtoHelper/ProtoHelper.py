# _*_coding:utf-8_*_

from pbjson import *
from EnumData import EnumData
from DataType import DataType
from MessageData import MessageData
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
    field_index = 2
    message_helper = ""
    for data_name in datas:
        data = datas[data_name]
        
        # 找出是否存在默认键
        result = data.to_proto()
        if isinstance(data, MessageData):
            # 获取key的类型
            message_list.append(write_message(data.file_name, result))

            # 获取key来生成最后的DataHelper
            key_type_name = None
            if not data.key_type:
                print("config type neither id type nor key type , this config will be ignored : " + data_name)
                continue
            key_type_name = DataType.type_to_proto(data.key_type.main_type)

            message_helper = message_helper + ("\tmap<%(message_key)s, %(message_name)s> %(message_name)s_dict = %(field_index)d;\n" % {
                    "message_key": key_type_name,
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
    data_helper = getattr(module, "DataHelper")
    data_helper = data_helper()
    message_type_list = list()

    # 将数据写进DataHelper
    for data_key in datas:
        data = datas[data_key]
        print(data_key)
        if isinstance(data, MessageData):
            # 获取DataHelper中对应类的列表
            if not data.key:
                continue
            message_type_list.append(data.file_name);
            data_helper_field_name = data.file_name + "_dict"
            data_dict = getattr(data_helper, data_helper_field_name)

            # 将dict转为proto类
            pb_dict = dict()
            cls = getattr(module, data.file_name)
            for config_data in data.datas:
                key = config_data[data.key]
                dict2pbobj(data_dict[key], config_data)
    message_types = getattr(data_helper, 'messageType')
    message_types.extend(message_type_list)
    return data_helper


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