# _*_coding:utf-8_*_

import sys
from Reader.ExcelReader import *
from Writer.Proto.ProtoWriter import *
from Tools.FileHelper import load_file_to_string, get_all_file


class Config:
    def __init__(self):
        self.excel_path = list()
        self.python_name = 'Config_pb2'
        self.binary_path = './Temp/Config.bytes'
        self.cs_path = ''
        self.py_path = ''
        self.proto_path = ''
        self.python_name = ''


if __name__ == '__main__':
    sys.path.append('./Temp')

    config = Config()
    config.__dict__ = json.loads(load_file_to_string('./Temp/Config.json'))

    data_list = list()
    path_list = list()

    for item in config.excel_path:
        path_list += get_all_file(path=item, is_deep=True, end_witch='xlsx')
        for path in path_list:
            print(path)
            data_list.append(reader(path))

    write(config, data_list)
