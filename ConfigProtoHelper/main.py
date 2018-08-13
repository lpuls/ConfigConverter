# _*_coding:utf-8_*_

import os
from ProtoHelper import *
from ExcelHelper import Excel
from TimeChecker import init_time, cal_run_time, cal_run_time_no_args


EXCEL_NAME = [
    "../Config/Excel/level_npc.xlsx",
    ]

EXCEL_PATH = "../Config/Excel/"             # excel所在路径
OUT_PATH = "../Config/"                     # 结果输出路径
PROTO_SAVE_PATH = "../Config/Data.proto"    # proto文件保存位置
BINARY_SAVE_PATH = "../Config/Data.byte"    # 二进制文件保存位置
LOG_PATH = "../Config/log.txt"              # 日志结果保存位置
PYTHON_PROTO_MODULE_PATH = "Data_pb2"       # 生成二进制文件时，所需要的python proto类所在模块


def write_log(context):
    log = open(LOG_PATH, 'a')
    log.write(context)
    log.write('\n')
    log.close()


def process_config(path):
    sheets = dict()
    for execl_name in path:
        print(execl_name)
        excel = Excel(execl_name)
        for sheet_name in excel.sheets:
            print("Process %s" % sheet_name)
            sheet = excel.sheets[sheet_name]
            if not cal_run_time_no_args(sheet.analyze, "Analyze "):
                print("Process %s [ERROR]\n" % (sheet_name,))
                write_log('%s' % execl_name)
                #os.system('pause')
                continue
            print("Process %s [COMPLETE]\n" % (sheet_name,))
            sheets[sheet_name] = sheet
    return sheets


def to_binary(in_path, out_path, sheets):
   # 生成proto文件
   os.system("run.bat")

   # 将表格中的内容生成proto文件
   binary_context = data_to_binary(in_path, sheets)
   write_to_binary(out_path, binary_context)


def end_with(s, *end):
    array = map(s.endswith, end)
    if True in array:
        return True
    else:
        return False


def search_file(file_path):
    files = list()
    path_dir =  os.listdir(file_path)
    for all_dir in path_dir:
        path = os.path.join('%s%s' % (file_path, all_dir))
        if os.path.isfile(path) and end_with(path, '.xlsx', '.XLSX') and -1 == path.find('~$'):
            files.append(path)
    return files


if __name__ == "__main__":
    init_time()

    # 找出所有的excel文件
    file_paths = search_file(EXCEL_PATH)
    
    # 分析二进制表格
    # sheets = process_config(file_paths)
    sheets = process_config(EXCEL_NAME)

    # 尝试生成Proto文件
    process_data_to_proto(PROTO_SAVE_PATH, sheets)
    
    # 将excel表格生成二进制文件
    to_binary(PYTHON_PROTO_MODULE_PATH, BINARY_SAVE_PATH, sheets)
