import os
import main
from Tools.FileHelper import load_json, get_all_file
from Helpers.CSVHelper import CSVHelper

main.load_config("Config.json")
file_list = get_all_file(main.CSV_PATH, is_deep=True, end_witch=".xlsx")
file_list += get_all_file(main.CSV_PATH, is_deep=True, end_witch=".xls")
print(file_list)
for path in file_list:
    csv_helper = CSVHelper(path)
    csv_helper.to_csv("../Out/temp/")
os.system("call ../0__Gen_lua_config.bat")