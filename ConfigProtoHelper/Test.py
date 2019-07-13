# _*_coding:utf-8_*_

import json
import sys

from Reader.ExcelReader import reader as excel_reader
from Reader.JsonReader import reader as json_reader
from Writer.ProtoWriter import write as proto_writer
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
        self.json_path = list()
        self.json_desc_path = list()


if __name__ == '__main__':

    config = Config()
    config.__dict__ = json.loads(load_file_to_string('./Temp/Config.json'))

    sys.path.append(config.cs_path)

    data_list = list()
    path_list = list()

    for item in config.excel_path:
        path_list += get_all_file(path=item, is_deep=True, end_witch='xlsx')
        for path in path_list:
            print(path)
            data_list.append(excel_reader(path))

    # path_list.clear()
    # temp_path = list()
    # for item in config.json_path:
    #     temp_path += get_all_file(path=item, is_deep=False, end_witch='json', with_name=True)
    #     for path, name in temp_path:
    #         path_list.append((path, name))
    # data_dict = json_reader(config.json_desc_path, path_list)
    #
    # data_list += list(data_dict.values())

    proto_writer(config, data_list)
