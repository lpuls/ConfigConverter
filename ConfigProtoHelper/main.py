# _*_coding:utf-8_*_

from ProtoHelper import *
from ExcelHelper import Excel

EXCEL_NAME = [
    "XX/e_cast_type.xlsx",
    "XX/e_effect_type.xlsx",
    "XX/e_item_detail_type.xlsx",
    "XX/e_race.xlsx",
    "XX/e_target_select_type.xlsx",
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
        if not sheet.analyze():
            exit()

        # 打印一下测试数据
        #print(sheet.types)
        #print(sheet.notes)
        #print(sheet.fields)
        #for row_data in sheet.datas:
        #    for field_name in row_data:
        #        print(field_name, row_data[field_name], type(row_data[field_name]))
        #    print("==============================")

        # 尝试生成Proto文件
    process_data_to_proto("XX/Data.proto", sheets)

