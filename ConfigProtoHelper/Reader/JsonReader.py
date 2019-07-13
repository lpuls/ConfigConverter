# _*_coding:utf-8_*_

import json
from ConfigBase.ConfigType import new_type
from Tools.FileHelper import load_file_to_string
from ConfigBase.TypeHelper import pre_process_and_check_type, get_type_from_type_list
from ConfigBase.CommonIntermediateFormat import CommonIntermediateFormat as CIF


def __read_desc__(path_list):
    cif_dict = dict()
    for json_desc_path in path_list:
        desc_context = load_file_to_string(json_desc_path)
        json_data = json.loads(desc_context)

        # 加载描述以生成对应的类型
        for class_name, desc in json_data.items():
            class_desc = list()

            # 同时生成cif数据
            fields = list()
            types = list()
            notes = list()

            for field_context in desc:
                class_desc.append((field_context['Field'], field_context['Type']))
                fields.append(field_context['Field'])
                types.append(field_context['Type'])
                notes.append(field_context['Note'])
            new_type(class_name, class_desc)

            # 处理一下类型和数据
            types = get_type_from_type_list(types)
            cif_dict[class_name] = CIF(class_name, types, types, fields, list())

    return cif_dict


def __read_json_data__(cif_dict, path, name):
    index = name.find('_')
    if -1 == index:
        raise Exception('无效的Json文件' + name)

    class_name = name[:index]
    cif = cif_dict.get(class_name, None)
    if not cif:
        raise Exception('无法找到有效的类型 ' + name)

    context = load_file_to_string(path)
    json_data = json.loads(context)
    data_list = [None] * len(cif.fields)
    for field, data in json_data.items():
        index = cif.fields.index(field)
        if -1 != index:
            data_list[index], _ = pre_process_and_check_type(data, cif.types[index])

    cif.data_list.append(data_list)


def reader(desc_path_list, path_with_name_list):
    cif_dict = __read_desc__(desc_path_list)
    for data_path, name in path_with_name_list:
        try:
            __read_json_data__(cif_dict, data_path, name)
        except Exception as error:
            print(error)
    return cif_dict


if __name__ == '__main__':
    cif_map = __read_desc__(['../../Config/Json/JsonDesc.json'])
    __read_json_data__(cif_map, '../../Config/Json/', 'NewConfigHelperTest_1011.json')
