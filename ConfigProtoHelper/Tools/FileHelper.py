# _*_coding:utf-8_*_

import os
import json
import xlrd


def load_file_to_string(path):
    result = ""
    with open(path, encoding="utf-8") as f:
        config_text = f.readlines()
        f.close()
        for line in config_text:
            result += line
    return result


def load_file_to_list(path):
    with open(path, encoding="utf-8") as f:
        config_text = f.readlines()
        f.close()
        return config_text


def load_json(path):
    context = load_file_to_string(path)
    return json.loads(context)


def get_all_file(path, is_deep=True, end_witch=None, with_name=False):
    file_list = list()
    path_dir = os.listdir(path)
    for all_dir in path_dir:
        file_path = os.path.join('%s%s' % (path, all_dir))
        if os.path.isfile(file_path):
            if end_witch and not file_path.endswith(end_witch):
                continue
            if with_name:
                file_list.append((file_path, all_dir))
            else:
                file_list.append(file_path)
        elif is_deep:
            file_list += get_all_file(file_path, is_deep, end_witch)
    return file_list


def load_excel(path, analyze_sheet):
    assert os.access(path, os.R_OK), print("文件%s不可读" % path)

    # 分析每张工作表的内容
    data = xlrd.open_workbook(path)
    sheets = data.sheets()
    assert len(sheets) > 0, "无可用的工作表"

    # 暂时不支持多张sheet表了
    name = path[path.rfind('/') + 1: path.rfind('.')]
    analyze_sheet(name, sheets[0])
