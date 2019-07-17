# _*_coding:utf-8_*_

import re
import os
import shutil
import csv
from ConfigBase.ConfigType import *


def __process_cif_to_csv__(cif, save_path):
    if len(cif.data_list) <= 0:
        return

    out = csv.writer(open(save_path + cif.name + ".csv", 'w', encoding='utf-8', newline=''), dialect='excel')
    # 处理类型
    csv_types = list()
    for type_inst in cif.types:
        if isinstance(type_inst, ArrayType) or isinstance(type_inst, StringType):
            csv_types.append('varchar')
        elif isinstance(type_inst, IntType) or isinstance(type_inst, LongType):
            csv_types.append('int')
        elif isinstance(type_inst, BoolType):
            csv_types.append('bool')
        elif isinstance(type_inst, FloatType):
            csv_types.append('float')
    out.writerow(csv_types)

    # 处理平台
    csv_notes = list()
    for note_context in cif.notes:
        search_result = re.search(r'\((CS|SC|C|S)\)', note_context.upper())
        if None is not search_result:
            csv_notes.append(search_result.group()[0])
        else:
            csv_notes.append('C')
    out.writerow(csv_notes)

    # 写入注释
    out.writerow(cif.notes)

    # 写入数据
    for data in cif.data_list:
        temp = list()
        for index, type_inst in enumerate(cif.types):
            if '' != data[index]:
                if isinstance(type_inst, ArrayType):
                    temp.append(str(data[index]).replace('[', '{').replace(']', '}'))
                elif isinstance(type_inst, StringType):
                    temp.append(str(data[index]))
                elif isinstance(type_inst, IntType):
                    temp.append(str(int(data[index])))
                elif isinstance(type_inst, BoolType):
                    temp.append(str(data[index]))
                elif isinstance(type_inst, FloatType):
                    temp.append(str(float(data[index])))
            else:
                temp.append(data[index])
        out.writerow(temp)


def writer(config, cif_list):
    if os.path.exists(config.csv_path):
        shutil.rmtree(config.csv_path)
    os.mkdir(config.csv_path)

    for cif in cif_list:
        __process_cif_to_csv__(cif, config.csv_path)
