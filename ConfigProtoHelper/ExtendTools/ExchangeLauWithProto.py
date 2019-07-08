# _*_coding:utf-8_*_
"""
将lua用的excel中，array的格式转换为proto用的格式
"""

import re
import xlwt
from Helpers.CSVHelper import CSVHelper
from SwapDatas.MessageData import str_to_array
from SwapDatas.DataType import DataType
from Helpers.ExcelHelper import ExcelHelper
from Tools.FileHelper import get_all_file


def save_to_excel(path, sheet):
    file = xlwt.Workbook()
    table = file.add_sheet('sheet 1')
    for index, value in enumerate(sheet.types):
        table.write(0, index, value)
    for index, value in enumerate(sheet.notes):
        table.write(1, index, value)
    for index, value in enumerate(sheet.fields):
        table.write(2, index, value)
    for index, value in enumerate(sheet.data_list):
        for field, data in value.items():
            data_index = sheet.fields.index(field)
            table.write(3 + index, data_index, data)
    file.save(path)


def process_sheet(name, sheet):
    data_types = sheet.types
    for index, type_name in enumerate(data_types):
        if DataType.ARRAY_TYPE == type_name:
            for data in sheet.data_list:
                field_name = sheet.fields[index]
                temp = data[field_name].replace('{', '[').replace('}', ']')
                _, t = str_to_array(temp)
                if None is t:
                    sheet.types[index] = DataType.STR_TYPE
                else:
                    data[field_name] = temp
                    result = re.search(r'\[*', data[field_name])
                    sheet.types[index] = len(result.group()) * 'ARRAY:' + t.main_type
    save_to_excel("../../Config/CSV2Excel/" + name + ".xls", sheet)


if __name__ == '__main__':
    # e = ExcelHelper("../../Config/CSV2Excel/hero.xls")
    # for excel_name, excel_sheet in e.sheets.items():
    #     process_sheet(excel_name, excel_sheet)
    # c = CSVHelper("../../Config/CSV2Excel/activity_template.xls")
    # c.to_csv("../../Config/CSV/")

    file_list = get_all_file("../../Config/CSV2Excel/", is_deep=True, end_witch=".xlsx")
    file_list += get_all_file("../../Config/CSV2Excel/", is_deep=True, end_witch=".xls")
    for file_name in file_list:
        e = ExcelHelper(file_name)
        for excel_name, excel_sheet in e.sheets.items():
            try:
                process_sheet(excel_name, excel_sheet)
            except Exception as error:
                print(excel_name, error)
        c = CSVHelper(file_name)
        c.to_csv("../../Config/CSV/")
