# _*_coding:utf-8_*_

import os
import struct
from pbjson import *
from Data_pb2 import *


class BinaryReader:
    def __init__(self, binary):
        self.__peek = 0
        self.__binary = binary

    def read_int(self):
        result = struct.unpack('i', self.__binary[self.__peek:self.__peek + 4])
        self.__peek += 4
        return result[0]

    def read_str(self):
        str_length = self.read_int() 
        result = struct.unpack('%ds' % (str_length), self.__binary[self.__peek:self.__peek + str_length])
        self.__peek += str_length
        result = result[0]
        return result.decode('gbk')

    def read_bytes(self):
       length = self.read_int()
       result = self.__binary[self.__peek:self.__peek + length]
       self.__peek += length
       return result


def read_binary(path):
    binary_file = open(path, 'rb')
    binary_context = binary_file.readlines()
    binary_file.close()

    binary = bytes()
    for context in binary_context:
        binary += context
    return binary


def __load_module__(path):
    paths = path.split('.')
    if len(paths) <= 0:
        return None

    module = __import__(path)
    for index in range(1, len(paths)):
        module = getattr(module, paths[index])
    return module


if __name__ == "__main__":
    model_module = __load_module__('Data_pb2')

    binary =  read_binary("../Config/Data.byte")
    reader = BinaryReader(binary)
    binary_class_count = reader.read_int()
    for index in range(0, binary_class_count):
        class_data = reader.read_bytes()
        class_reader = BinaryReader(class_data)
        
        class_inst_count = class_reader.read_int()

        class_name = class_reader.read_str()  # .decode('gbk')
        inst_func = getattr(model_module, class_name)

        if 'Timeline' == class_name:
            for inst_index in range(0, class_inst_count):
                class_inst = class_reader.read_bytes()
                prefab = Timeline()
                prefab.ParseFromString(class_inst)
                print(prefab)
            


