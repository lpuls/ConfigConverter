# _*_coding:utf-8_*_

import os
from ProtoHelper import *
from ExcelHelper import Excel

EXCEL_NAME = [
    "XX/e_cast_type.xlsx",
    "XX/e_effect_type.xlsx",
    "XX/e_item_detail_type.xlsx",
    "XX/e_race.xlsx",
    "XX/e_target_select_type.xlsx",
    "XX/e_target_camp_type.xlsx",
    "XX/e_range_type.xlsx",
    "XX/skill.xlsx"
    ]


if __name__ == "__main__":
    sheets = dict()
    for execl_name in EXCEL_NAME:
        excel = Excel(execl_name)
        for sheet_name in excel.sheets:
            sheets[sheet_name] = excel.sheets[sheet_name]

    for sheet_name in sheets:
        print("Sheet Name: ", sheet_name)
        sheet = sheets[sheet_name]
        sheet.analyze()
        # print(sheet)

    # 尝试生成Proto文件
    process_data_to_proto("XX/Data.proto", sheets)
    
    # 尝试生成cs和py两份proto代码
    os.system("protoc --csharp_out=./XX ./XX/Data.proto")
    os.system("protoc --python_out=./ ./XX/Data.proto")

    # 将表格中的内容生成proto文件
    binary_context = data_to_binary("XX.Data_pb2", sheets)
    write_to_binary("XX/Data.byte", binary_context)
    data = read_binary("XX/Data.byte")
    #print(data)

