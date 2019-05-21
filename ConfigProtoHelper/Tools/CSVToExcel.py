# _*_coding:utf-8_*_

from Tools.FileHelper import load_json, get_all_file
from Helpers.CSVHelper import CSVHelper

if __name__ == "__main__":
    config = load_json(r"D:/Self/Python/dev/ConfigProtoHelper/ConfigProtoHelper/CSVConfig.json")

    file_list = get_all_file(r"D:\Self\Python\dev\ConfigProtoHelper\Config\CSV/", is_deep=True, end_witch=".csv")
    for path in file_list:
        csv_helper = CSVHelper(path, config)
        csv_helper.to_excel(r"D:\Self\Python\dev\ConfigProtoHelper\Config\CSV2Excel/")
        # csv_helper.to_lua(r"D:\Self\Python\dev\ConfigProtoHelper\Config\CSV2Excel/")

    file_list = get_all_file(r"D:\Self\Python\dev\ConfigProtoHelper\Config\CSV2Excel/", is_deep=True, end_witch=".xlsx")
    for path in file_list:
        csv_helper = CSVHelper(path)
        csv_helper.to_lua(r"D:\Self\Python\dev\ConfigProtoHelper\Config\Excel2Lua/")
