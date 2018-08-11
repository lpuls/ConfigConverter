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

    # 尝试生成Proto文件
    process_data_to_proto("XX/Data.proto", sheets)

