# _*_coding:utf-8_*_

from ExcelHelper import Excel

if __name__ == "__main__":
    excel = Excel("XX/e_cast_type.xlsx")
    for sheet_name in excel.sheets:
        print("Sheet Name: ", sheet_name)
        sheet = excel.sheets[sheet_name]
        print(sheet.types)
        print(sheet.notes)
        print(sheet.fields)
        sheet.analyze()
        for row_data in sheet.datas:
            for field_name in row_data:
                print(field_name, row_data[field_name])
            print("==============================")

