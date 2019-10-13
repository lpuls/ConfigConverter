# _*_coding:utf-8_*_

import json
import sys

from ConfigBase.ConfigHelper import init_type
from Reader.ExtendType import init_extend_type
from Reader.ExcelReader import process as excel_processor
from Reader.JsonReader import process_type as json_type_processor, process_data as json_data_processor
from Writer.ProtoWriter import spawn_proto_file
from Tools.FileHelper import load_file_to_string, get_all_file


class Config:
    def __init__(self):
        self.excel_path = list()
        self.package_name = 'Config'
        self.python_name = 'Config_pb2'
        self.binary_path = './Temp/Config.bytes'
        self.cs_path = ''
        self.py_path = ''
        self.proto_path = ''
        self.python_name = ''
        self.json_path = list()
        self.json_desc_path = list()
        self.csv_path = ''


if __name__ == '__main__':

    config = Config()
    config.__dict__ = json.loads(load_file_to_string('./Temp/Config.json'))

    sys.path.append(config.cs_path)

    # 预处理类型
    init_type()
    init_extend_type()
    json_type_processor(config.json_desc_path)

    path_list = list()
    for item in config.excel_path:
        path_list += get_all_file(path=item, is_deep=True, end_witch='xlsx', with_name=True)
    excel_processor(path_list)

    path_list.clear()
    for item in config.json_path:
        path_list += get_all_file(path=item, is_deep=True, end_witch='json', with_name=True)
    json_data_processor(path_list)

    spawn_proto_file(config.package_name, config.proto_path)

    # path_list.clear()
    # temp_path = list()
    # for item in config.json_path:
    #     temp_path += get_all_file(path=item, is_deep=False, end_witch='json', with_name=True)
    #     for path, name in temp_path:
    #         path_list.append((path, name))
    # data_dict = json_reader(config.json_desc_path, path_list)

    # data_list += list(data_dict.values())

    # proto_writer(config, data_list)

