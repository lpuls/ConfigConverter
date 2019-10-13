# _*_coding:utf-8_*_

import sys
import struct
from Tools.ModuleHelper import *
from Temp.Config_pb2 import Box, Studen

__CONFIG__ = dict()


def init(path):
    binary_data_list = bytes()
    with open(path, 'rb') as f:
        temp = f.readlines()
        for item in temp:
            binary_data_list += item

    module_inst = load_module('Config_pb2')

    config_count = struct.unpack('i', binary_data_list[:4])[0]
    binary_data_list = binary_data_list[4:]
    for index in range(0, config_count):
        binary_length, inst_count, class_name_length = struct.unpack('iii', binary_data_list[:12])
        binary_data_list = binary_data_list[12:]

        class_name = struct.unpack('%ds' % (class_name_length,),
                                   binary_data_list[:class_name_length])[0].decode('utf-8')
        binary_data_list = binary_data_list[class_name_length:]

        config_dict = dict()
        cls = getattr(module_inst, class_name)
        for i in range(0, inst_count):
            inst_binary_length = struct.unpack('i', binary_data_list[:4])[0]
            binary_data_list = binary_data_list[4:]
            inst_binary_data = binary_data_list[:inst_binary_length]
            binary_data_list = binary_data_list[inst_binary_length:]
            inst = cls()
            inst.ParseFromString(inst_binary_data)

            config_dict[getattr(inst, 'ID')] = inst
        __CONFIG__[cls.__name__] = config_dict


def get(cls, config_id):
    config = __CONFIG__.get(cls.__name__, None)
    if config:
        return config.get(config_id, None)
    return None


if __name__ == '__main__':
    sys.path.append('../Temp')
    init('../Temp/Config.bytes')
    s = get(Box, 1)
    print(s)
    s = get(Studen, 1)
    print(s)

