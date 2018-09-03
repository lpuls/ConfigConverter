# _*_coding:utf-8_*_

from pbjson import *
from Data_pb2 import *


def read_binary(path, pb_obj):
    binary_file = open(path, 'rb')
    binary_context = binary_file.readlines()
    binary_file.close()

    binary = bytearray()
    for context in binary_context:
        binary += context

    pb_obj.ParseFromString(binary)
    return pb_obj


if __name__ == "__main__":
    obj =  read_binary("../Config/Data.byte", DataHelper())
    test_dict = obj.Test_dict
    test_value = test_dict[1]
    print(test_value.TEST)
    print(test_value.ARRAY_TEST)
    print(test_value.ObjectTest)
    print(test_value.ARRAY_NORMAL)    
    print(test_value.MAP_NORMAL)