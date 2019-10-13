# _*_coding:utf-8_*_

from ConfigBase.ConfigTypeHelper import *
from ConfigBase.ConfigTypeParser import process_structure_element_type
from Tools.FileHelper import load_excel, get_all_file


__ENUM_PREFIX__ = 'e_'

__TYPE_ROW_ID__ = 0
__NOTE_ROW_ID__ = 1
__FIELD_ROW_ID__ = 2

__ENUM_NAME_ROW__ = 0
__ENUM_VALUE_ROW__ = 1
__ENUM_NOTE_ROW__ = 2


def __process_enum_excel__(name, sheet):
    desc = dict()
    notes = list()

    row_count = sheet.nrows
    for y in range(__FIELD_ROW_ID__ + 1, row_count):
        enum_name = sheet.cell_value(y, __ENUM_NAME_ROW__)
        value = int(sheet.cell_value(y, __ENUM_VALUE_ROW__))
        note = sheet.cell_value(y, __ENUM_NOTE_ROW__)
        desc[enum_name] = value
        notes.append(note)
    add_enum_type(name.replace(__ENUM_PREFIX__, ''), desc, notes)


def __process_structure_excel__(name, sheet):
    desc = list()
    col_count = sheet.ncols
    for x in range(0, col_count):
        type_str = sheet.cell_value(__TYPE_ROW_ID__, x)
        note = sheet.cell_value(__NOTE_ROW_ID__, x)
        field = sheet.cell_value(__FIELD_ROW_ID__, x)
        element = StructureType.StructureElement(field, note, type_str)
        desc.append(element)
    add_structure_type(name, desc)


def __process_structure_data__(name, sheet):
    inst = get_type(name)
    if None is inst:
        raise Exception("无效的结构 " + name)

    for y in range(__FIELD_ROW_ID__ + 1, sheet.nrows):
        data_dict = dict()
        for x in range(0, sheet.ncols):
            data_dict[inst.desc[x].field] = inst.desc[x].type.to_data(sheet.cell_value(y, x))
            # data_list.append(sheet.cell_value(y, x))
        inst.data.append(data_dict)


def __process_structure_list_type__(structure_list):
    for name in structure_list:
        structure = get_type(name.replace('.xlsx', ''))
        if None is structure:
            raise Exception('存在无法正确识别的类型声时 ' + name)

        process_structure_element_type(structure)


def process(file_list):
    enum_path_list = list()
    structure_name_list = list()
    structure_path_list = list()

    # 将枚举和结构体分离
    for item in file_list:
        path = item[0]
        name = item[1]
        if name[:2] == __ENUM_PREFIX__:
            enum_path_list.append(path)
        else:
            structure_name_list.append(name)
            structure_path_list.append(path)

    # 先将枚举加入类型列表中
    for path in enum_path_list:
        load_excel(path, __process_enum_excel__)

    # 再处理结构体
    for path in structure_path_list:
        load_excel(path, __process_structure_excel__)

    # 确定结构体的类型
    __process_structure_list_type__(structure_name_list)

    # 处理结构体中的数据
    for path in structure_path_list:
        load_excel(path, __process_structure_data__)


def __test__():
    excel_list = get_all_file('../../Config/Test/', is_deep=False, end_witch='.xlsx', with_name=True)
    process(excel_list)
    type_inst = get_type('Box')
    print(type_inst.data)
    pass


if __name__ == '__main__':
    init_type()
    __test__()
    pass
