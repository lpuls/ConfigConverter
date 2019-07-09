# _*_coding:utf-8_*_

import sys
from Reader.ExcelReader import *
from Writer.ProtoWriter import *
from Tools.ModuleHelper import load_module


class Config:
    def __init__(self):
        self.python_proto = 'Config_pb2'
        self.binary_path = './Temp/Config.bytes'

if __name__ == '__main__':
    sys.path.append('./Temp')

    data_list = list()
    reader('../Config/Excel/e_FloatingType.xlsx')
    data_list.append(reader('../Config/Excel/Spawn.xlsx'))

    # config = Config()
    # write(config, data_list)
