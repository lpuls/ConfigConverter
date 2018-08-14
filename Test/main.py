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
    for field in obj.DESCRIPTOR.fields:
        data_list = getattr(obj, field.name)
        print(field.name)
        for item in data_list:
            print(item)
            data_obj = data_list[item]
            print(data_obj.ID)
            for v in data_obj.ARRAY_TEST:
                print(v)
            for k in data_obj.TEST:
                print(k, data_obj.TEST[k])
        print('\n')
        pass
    
