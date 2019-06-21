# _*_coding:utf-8_*_

from Tools.FileHelper import load_json, get_all_file
from Helpers.CSVHelper import CSVHelper


class CSVToErl:
    def __init__(self, helper):
        self.csv_helper = helper

    def to_erl(self, record_name):
        pass


if __name__ == "__main__":
    config = load_json(r"D:/Self/Python/dev/ConfigProtoHelper/ConfigProtoHelper/CSVConfig.json")

    file_list = get_all_file(r"D:\Self\Python\dev\ConfigProtoHelper\Config\CSV/", is_deep=True, end_witch=".csv")
    for path in file_list:
        print("To Excel " + path)
        csv_helper = CSVHelper(path, config)
        csv_helper.to_excel(r"D:\Self\Python\dev\ConfigProtoHelper\Config\CSV2Excel/")

    # file_list = get_all_file(r"D:\Self\Python\dev\ConfigProtoHelper\Config\CSV2Excel/",
    #                          is_deep=True, end_witch=".xlsx")
    # for path in file_list:
    #     print("To Lua " + path)
    #     csv_helper = CSVHelper(path)
    #     csv_helper.config = config
    #     csv_helper.to_erl_lua("../lua/", "../0__Gen_lua_config.bat")
        # csv_helper.to_lua(r"D:\Self\Python\dev\ConfigProtoHelper\Config\Excel2Lua/")
        # csv_helper.to_erl(r"D:\Self\Python\dev\ConfigProtoHelper\Config\Excel2Erl/")

