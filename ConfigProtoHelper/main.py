# _*_coding:utf-8_*_

import os
import json
from ProtoHelper import *
from ExcelHelper import Excel
from JsonHelper import JsonHelper
from TimeChecker import init_time, cal_run_time, cal_run_time_no_args


EXCEL_NAME = [
    "../Config/TestExcel/Test.xlsx",
    "../Config/TestExcel/SubTest.xlsx",
    ]

JSON_PATH = "../Config/JSON/"               # json所在路径
EXCEL_PATH = "../Config/Excel/"             # excel所在路径
OUT_PATH = "../Config/"                     # 结果输出路径
PROTO_SAVE_PATH = "../Config/Data.proto"    # proto文件保存位置
BINARY_SAVE_PATH = "../Config/Data.byte"    # 二进制文件保存位置
LOG_PATH = "../Config/log.txt"              # 日志结果保存位置
PYTHON_PROTO_MODULE_PATH = "Data_pb2"       # 生成二进制文件时，所需要的python proto类所在模块
SPAWN_CSHARP_COMMAND = "protoc -I ../Config/ --csharp_out=../Config/ ../Config/Data.proto"  # 生成csproto指令 
SPAWN_PYTHON_COMMAND = "protoc -I ../Config/ --python_out=./ ../Config/Data.proto"  # 生成python指令


def load_config(path):
    global OUT_PATH
    global LOG_PATH
    global JSON_PATH
    global JSON_DESC
    global EXCEL_PATH
    global PROTO_SAVE_PATH
    global BINARY_SAVE_PATH
    global PYTHON_PROTO_MODULE_PATH
    global SPAWN_CSHARP_COMMAND
    global SPAWN_PYTHON_COMMAND

    result = JsonHelper.load_json(path)
    config = json.loads(result)

    OUT_PATH = config['OUT_PATH']
    LOG_PATH = config['LOG_PATH']
    JSON_PATH = config['JSON_PATH']
    EXCEL_PATH = config['EXCEL_PATH']
    PROTO_SAVE_PATH = config['PROTO_SAVE_PATH']
    BINARY_SAVE_PATH = config['BINARY_SAVE_PATH']
    PYTHON_PROTO_MODULE_PATH = config['PYTHON_PROTO_MODULE_PATH']
    SPAWN_CSHARP_COMMAND = config['SPAWN_CSHARP_COMMAND']
    SPAWN_PYTHON_COMMAND = config['SPAWN_PYTHON_COMMAND']
    print(config)


def write_log(context):
    log = open(LOG_PATH, 'a')
    log.write(context)
    log.write('\n')
    log.close()


def merge_dict(dict1, dict2):
    for key in dict2:
        assert key not in dict1.keys(), "Key重复"
        dict1[key] = dict2[key]


def process_excel_config(path):
    sheets = dict()
    for execl_name in path:
        excel = Excel(execl_name)
        for sheet_name in excel.sheets:
            sheets[sheet_name] = excel.sheets[sheet_name]
    return sheets


def process_json_config(path):
    JsonHelper.initialize(JSON_PATH + "JsonDesc.json")
    for json_name in path:
        JsonHelper.load_json_config(json_name)
    return JsonHelper.MESSAGES


def analyze_config(datas):
    delete_config = list()
    for data_name in datas:
        data = datas[data_name]
        print("Process %s" % data_name)
        if not data.analyze():
           print("Process %s [ERROR]\n" % (data_name,))
           write_log('%s' % data_name)
           delete_config.append(data_name)
           continue
        print("Process %s [SUCCESS]" % data_name)
    for item in delete_config:
        del datas[item]


def to_binary(in_path, out_path, sheets):
   # 生成proto文件
   os.system(SPAWN_PYTHON_COMMAND)
   os.system(SPAWN_CSHARP_COMMAND)

   # 将表格中的内容生成proto文件
   binary_context = data_to_binary(in_path, sheets)
   write_to_binary(out_path, binary_context)


def end_with(s, *end):
    array = map(s.endswith, end)
    if True in array:
        return True
    else:
        return False


def search_file(file_path, ends):
    files = list()
    path_dir =  os.listdir(file_path)
    for all_dir in path_dir:
        path = os.path.join('%s%s' % (file_path, all_dir))
        if os.path.isfile(path) and end_with(path, *ends) and -1 == path.find('~$'):
            files.append(path)
    return files


if __name__ == "__main__":
    load_config("Config.json");

    sheets = dict()

    # 找出所有的excel文件并分析二进制表格
    # file_paths = search_file(EXCEL_PATH, [".xlsx", ".XLSX"])
    # excel_sheets = process_excel_config(file_paths)
    excel_sheets = process_excel_config(EXCEL_NAME)
    merge_dict(sheets, excel_sheets)

    # 找出所有的json文件并分析二进制
    #file_paths = search_file(JSON_PATH, [".json", ".JSON"])
    #json_sheets = process_json_config(file_paths)
    #merge_dict(sheets, json_sheets)

    # 生成proto文件前先分析一下
    analyze_config(sheets)

    # 尝试生成Proto文件
    process_data_to_proto(PROTO_SAVE_PATH, sheets)
    
    # 将excel表格生成二进制文件
    to_binary(PYTHON_PROTO_MODULE_PATH, BINARY_SAVE_PATH, sheets)