# _*_coding:utf-8_*_

import os
from ProtoHelper import *
from ExcelHelper import Excel

EXCEL_NAME = [
    "XX/Test.xlsx"
    ]

EXCEL_PATH = "XX/"
OUT_PATH = "./Out"
PROTO_SAVE_PATH = "./Out/Data.proto"
PROTO_MODULE = "Out.Data_pb2"
BINARY_SAVE_PATH = "Out/Data.byte"
LOG_PATH = "Out/log.txt"
SPWAN_CS_PROTO = "protoc --csharp_out=%s %s" % (OUT_PATH, PROTO_SAVE_PATH) 
SPWAN_PY_PROTO = "protoc --python_out=%s %s" % ("./", PROTO_SAVE_PATH)


def write_log(context):
    log = open(LOG_PATH, 'w+')
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
            if not sheet.analyze():
                print('%s不是有效的配置表' % (sheet_name,))
                write_log('%s.%s' % (sheet_name, execl_name))
            else:
                print("Process %s [COMPLETE]\n" % (sheet_name,))
                sheets[sheet_name] = sheet
    return sheets


def to_binary(in_path, out_path, sheets):
   # 尝试生成cs和py两份proto代码
   os.system(SPWAN_CS_PROTO)
   os.system(SPWAN_PY_PROTO)

   # 将表格中的内容生成proto文件
   binary_context = data_to_binary(PROTO_MODULE, sheets)
   write_to_binary(BINARY_SAVE_PATH, binary_context)


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
    file_paths = search_file('XX/')
    
    # 分析二进制表格
    sheets = process_config(file_paths)

    # 尝试生成Proto文件
    process_data_to_proto(PROTO_SAVE_PATH, sheets)
    
    # 将excel表格生成二进制文件
    to_binary("./Out/Data.proto", "Out/Data.byte", sheets)

    # 测试写成二进制文件的结果
    #from Out.Data_pb2 import DataHelper
    #result = read_binary('Out/Data.byte', DataHelper())
    #test_dict = result.Test_list[0].TEST
    #for k in test_dict:
    #    print(k)
    #    print(test_dict[k])
