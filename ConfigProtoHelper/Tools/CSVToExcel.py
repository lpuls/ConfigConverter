# _*_coding:utf-8_*_

import os
from Tools.FileHelper import load_json, get_all_file
from Helpers.CSVHelper import CSVHelper


class CSVToErl:
    def __init__(self, helper):
        self.csv_helper = helper

    def to_erl(self, record_name):
        pass


if __name__ == "__main__":
    config = load_json(r"../CSVConfig.json")

    file_list = get_all_file(r"F:/p08_2018_2/csv/", is_deep=True, end_witch=".csv")
    for path in file_list:
        print("To Excel " + path)
        csv_helper = CSVHelper(path, config)
        csv_helper.to_excel(r"../../Function/")
        csv_helper.to_csv("../../Out/temp/")
