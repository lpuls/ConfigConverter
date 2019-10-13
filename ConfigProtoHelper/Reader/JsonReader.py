# _*_coding:utf-8_*_

from Tools.FileHelper import load_json
from ConfigBase.ConfigTypeHelper import *
from ConfigBase.ConfigTypeParser import process_structure_element_type


def process_type(file_list):
    for path in file_list:
        context = load_json(path)

        # 从描述表中生成类型
        name_list = list()
        for name, value in context.items():
            desc = list()
            for element in value:
                type_str = element['Type']
                field = element['Field']
                note = element['Note']
                element = StructureType.StructureElement(field, note, type_str)
                desc.append(element)
            add_structure_type(name, desc)
            name_list.append(name)

        # 分析类型中的结构
        for name in name_list:
            type_inst = get_type(name)
            if None is type_inst:
                raise Exception('存在无法正确识别的类型声时 ' + name)

            process_structure_element_type(type_inst)


def process_data(file_list):
    for path, name in file_list:
        structure_name = name[:name.find('_')]
        structure_inst = get_type(structure_name)
        if None is structure_inst:
            print("无对应类型的Json数据 " + path)
            continue

        json_context = load_json(path)
        data_dict = structure_inst.to_data(json_context)
        structure_inst.data.append(data_dict)


def __test__():
    desc_file_list = ['../../Config/Test/JsonDesc.json']
    process_type(desc_file_list)
    process_data([('../../Config/Test/Studen_1.json', 'Studen_1')])


if __name__ == '__main__':
    init_type()
    __test__()
    pass

