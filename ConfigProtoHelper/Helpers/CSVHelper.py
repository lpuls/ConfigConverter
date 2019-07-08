# _*_coding:utf-8_*_

import os
import csv
import xlwt
from Tools.FileHelper import load_excel
from SwapDatas.DataType import DataType


__TO_LUA_TEMPLATE__ = """
-- DO NOT MODIFY, This file is generated by tool.
local this = {{
{elements}
{extra}
{all}
}}
return this
"""


class CSVHelper:
    def __init__(self, path, config=None):
        self.__config = None
        self.module = ""
        self.target_name = ""
        self.order_index = None

        if None is not config:
            self.__load_from_csv__(path, config)
        else:
            self.__load_from_excel__(path)

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, config):
        self.__config = config
        module = config["DataTable"].get(self.name, None)
        if None is not module:
            self.target_name = module["TargetName"]
            self.module = module["Module"]
            self.order_index = module.get('order_key', None)
        else:
            self.module = "default_module"
            names = self.name.split('_')
            self.target_name = ""
            for name in names:
                self.target_name += name.capitalize()
            self.target_name += "Cfg"
            self.order_index = None

    def __load_from_csv__(self, path, config):
        """
        通过csv读取
        :param path: csv路径
        :param config: csv相关的配置文件
        """
        self.filed = list()
        self.type = list()
        self.swap_type = list()
        self.platform = list()
        self.note = list()
        self.order_index = None
        self.extra_index = list()
        self.data = list()
        self.has_all = True

        # 从配置表中找出对应的数据
        self.name = os.path.basename(path)
        self.name = self.name.replace('.csv', '')
        module = config["DataTable"].get(self.name, None)
        if None is not module:
            self.target_name = module["TargetName"]
            self.module = module["Module"]
            self.order_index = module.get('order_key', None)
        else:
            self.module = "default_module"
            self.target_name = self.name + "Cfg"
            self.order_index = None

        # 读取csv
        self.__load_csv__(path)

        # 分析数据
        self.__process_origin_data__()
        self.__check_type_from_data__()

        self.has_all = self.target_name not in config['WithOutTotalIndex']
        self.extra_index = config['ExtraIndex'].get(self.name, self.extra_index)
        if "define" in self.filed:
            self.extra_index.append(self.filed.index("define"))
        if None is not self.order_index:
            self.order_index = self.filed.index(self.order_index)

    def __load_from_excel__(self, path):
        """
        通过excel读取
        :param path: excel路径
        """
        self.filed = list()
        self.type = list()
        self.swap_type = list()
        self.platform = list()
        self.note = list()
        self.order_index = None
        self.extra_index = list()
        self.define_index = None
        self.data = list()

        # 分析出文件名
        self.name = os.path.basename(path)
        self.name = self.name.replace(".xlsx", "")
        self.name = self.name.replace(".xls", "")
        self.target_name = self.name
        first_underline_index = self.name.find("_")
        self.has_all = (self.name[:first_underline_index]).upper() == "TRUE"

        self.__load_excel__(path)
        self.__check_type_from_data__()

        # 分析字段
        for item in self.note:
            if -1 != item.upper().find("(EXTRA)"):
                self.extra_index.append(self.note.index(item))

        if "sort_by_field_module" == self.module:
            for item in self.note:
                if -1 != item.upper().find("(ORDER)"):
                    self.order_index = self.note.index(item)
                    break
        elif "unique_module" == self.module:
            if "define" in self.filed:
                self.extra_index.append(self.filed.index("define"))

    def __check_type_from_data__(self):
        """
        根据数据分析对应DataType的类型
        :return:
        """
        data = self.data[0]
        for index in range(0, len(data)):
            if 'int' == self.type[index]:
                self.swap_type.append(DataType(DataType.INT_TYPE))
            elif 'float' == self.type[index]:
                self.swap_type.append(DataType(DataType.FLOAT_TYPE))
            elif 'bool' == self.type[index]:
                self.swap_type.append(DataType(DataType.BOOL_TYPE))
            elif 'varchar' == self.type[index]:
                if len(data[index]) > 0 and '{' == data[index][0]:
                    self.swap_type.append(DataType(DataType.ARRAY_TYPE))
                else:
                    self.swap_type.append(DataType(DataType.STR_TYPE))
            else:
                self.swap_type.append(DataType(self.type[index]))

    def __process_origin_data__(self):
        """
        处理原始数据
        :return:
        """
        for item in self.data[0]:
            self.filed.append(item)
        for item in self.data[1]:
            self.type.append(item)
        for item in self.data[2]:
            self.platform.append(item.upper())
        for item in self.data[3]:
            self.note.append(item)
        del self.data[0]
        del self.data[0]
        del self.data[0]
        del self.data[0]

    def __load_csv__(self, path):
        """
        从csv中加载数据
        :param path: csv路径
        """
        csv_file = csv.reader(open(path, 'r', encoding='utf8'))
        for item in csv_file:
            temp = list()
            self.data.append(temp)
            for data in item:
                temp.append(data)

    def __load_excel__(self, path):
        def analyze_sheet(_, sheet):
            if sheet.nrows < 3:
                print("无效的表置表格式")
                return None

            # 获取基本属性
            self.type = sheet.row_values(0)
            self.note = sheet.row_values(1)
            self.filed = sheet.row_values(2)
            # self.platform = sheet.row_values(3)

            for item in self.note:
                if -1 != item.find("(C)"):
                    self.platform.append('C')
                elif -1 != item.find("(CS)") or -1 != item.find("(SC)"):
                    self.platform.append('CS')
                elif -1 != item.find("(S)"):
                    self.platform.append("S")
                else:
                    self.platform.append("N")

            for row_index in range(3, sheet.nrows):
                self.data.append(sheet.row_values(row_index))

        load_excel(path, analyze_sheet)

    @staticmethod
    def __write_to_execl_by_index__(row, table, data_list):
        for index in range(0, len(data_list)):
            table.write(row, index, data_list[index])

    def __extra_index__(self, id_index):
        """
        根据extral表生成以extral表中记录的字段对应的ID列表
        :param id_index: id的列号
        :return: 对应的lua字符串
        """

        extra_index = self.extra_index
        index_value = dict()
        for data in self.data:
            # 遍历所有需要处理的字段下标
            for index in extra_index:
                extra_index_dict = index_value.get(index, dict())
                index_value[index] = extra_index_dict

                value = data[index]
                extra_list = extra_index_dict.get(value, list())
                extra_index_dict[value] = extra_list
                extra_list.append(data[id_index])

        # 转成列表
        result = ""
        for index, id_to_value_list in index_value.items():
            filed = self.filed[index]
            main_type = self.swap_type[index].main_type
            context = "\tget_id_list_by_{0} = {{\n{1}\n\t}},\n"
            element = ""
            for key, value in id_to_value_list.items():
                if DataType.STR_TYPE == main_type:
                    element += "\t\t{0} = {1},\n".format(key, value[0])
                else:
                    element += "\t\t[{0}] = {{{1}}},\n".format(key, value[1: len(value) - 1])
            result += context.format(filed, element)
        return result

    def __get_value_by_type__(self, data, index):
        if len(data[index]) <= 0:
            if DataType.INT_TYPE == self.swap_type[index].main_type:
                return "0"
            elif DataType.BOOL_TYPE == self.swap_type[index].main_type:
                return "true"
            elif DataType.ARRAY_TYPE == self.swap_type[index].main_type:
                return "{}"
            else:
                return "0"
        else:
            if DataType.STR_TYPE == self.swap_type[index].main_type:
                if '{' == data[index][0]:
                    return data[index]
                elif '@' == data[index][0]:
                    return data[index].replace('@', '')
                else:
                    return "\"{0}\"".format(data[index])
            if DataType.BOOL_TYPE == self.swap_type[index].main_type:
                print(data, index, data[index])
                return data[index]
            else:
                return data[index]

    def __spawn_element_format__(self):
        """
        根据表结构生成格式
        :return: 格式字符串
        """
        index = 0
        element = ""
        for item in self.filed:
            if -1 != self.platform[index].find('C'):
                element += "\t\t{{{0}}} = {{{1}}},\n".format(item, item + "_value")
            index += 1
        return """\t[{{id_index_value}}] = {{{{\n{0}\n\t}}}},\n""".format(element)

    def __process_default__(self, id_index):
        """
        处理默认模版表
        :param id_index: id 的列号
        :return: 导出成lua的内容， all表的内容
        """
        all_id = list()
        element = self.__spawn_element_format__()

        result = ""
        for data in self.data:
            filed_to_value = dict()
            filed_to_value["id_index_value"] = self.__get_value_by_type__(data, id_index)  # data[id_index]
            if self.has_all:
                all_id.append(int(data[id_index]))
            for index in range(0, len(self.filed)):
                if -1 == self.platform[index].find('C'):
                    continue
                filed_to_value[self.filed[index]] = self.filed[index]
                filed_to_value[self.filed[index] + "_value"] = self.__get_value_by_type__(data, index)
            result += element.format_map(filed_to_value)
        if self.has_all:
            str_all = str(all_id)
            str_all = "\tall = {{{0}}},".format(str_all[1: len(str_all) - 1])
        else:
            str_all = ""
        return result, str_all

    def __process_sort__(self, id_index):
        """
        处理排序模版表
        :param id_index: id 的列号
        :return: 导出成lua的内容， all表的内容
        """
        element = self.__spawn_element_format__()

        result = ""
        all_id = [None] * len(self.data)
        for data in self.data:
            filed_to_value = dict()
            filed_to_value["id_index_value"] = self.__get_value_by_type__(data, id_index)  # data[id_index]
            if self.has_all:
                all_id[int(data[self.order_index]) - 1] = int(data[id_index])
            for index in range(0, len(self.filed)):
                if -1 == self.platform[index].find('C'):
                    continue
                filed_to_value[self.filed[index]] = self.filed[index]
                filed_to_value[self.filed[index] + "_value"] = self.__get_value_by_type__(data, index)
            result += element.format_map(filed_to_value)
        if self.has_all:
            str_all = str(all_id)
            str_all = "\tall = {{{0}}},".format(str_all[1: len(str_all) - 1])
        else:
            str_all = ""
        return result, str_all

    def __process_unique__(self, id_index):
        """
        处理唯一ID模版表
        :param id_index: id 的列号
        :return: 导出成lua的内容， all表的内容
        """
        return self.__process_default__(id_index)

    def __process_word__(self):
        """
        处理字词模版表
        :return: 导出成lua的内容，空字符串
        """
        root = dict()

        def build_word_tree(tree, word):
            for w in word:
                leaf = tree.get(w, dict())
                tree[w] = leaf
                tree = leaf
            tree["result"] = "true"

        for data in self.data:
            build_word_tree(root, data[0])

        def tree_to_lua(key, tree, deep):
            space = "\t" * deep
            if not isinstance(tree, dict):
                return "\n{2}{0} = {1},\n".format(key.replace('\\', '\\\\'), tree, space)

            context = "\n{1}[\"{0}\"] = {{".format(key.replace('\\', '\\\\'), space)
            for k, v in tree.items():
                context += tree_to_lua(k, v, deep + 1)
            context += space + "},\n"
            return context

        lua_context = ""
        for leaf_key, leaf_value in root.items():
            lua_context += tree_to_lua(leaf_key, leaf_value, 1)
        return lua_context, ""

    def to_excel(self, path):
        """
        将csv转成excel
        :param path: 导出路径
        :return:
        """
        file = xlwt.Workbook()
        table = file.add_sheet('sheet 1')

        # 将原本各种模版需要的数据以标记的方式写入字段名中
        if "sort_by_field_module" == self.module and None is not self.order_index and -1 != self.order_index:
            self.note[self.order_index] += "(ORDER)"
        for extra_index in self.extra_index:
            self.note[extra_index] += "(EXTRA)"

        # 写入类型
        data_type = list()
        for item in self.swap_type:
            data_type.append(item.main_type)
        CSVHelper.__write_to_execl_by_index__(0, table, data_type)

        # 写入说明
        index = 0
        for item in self.platform:
            self.note[index] += "({0})".format(item.upper())
            index += 1
        CSVHelper.__write_to_execl_by_index__(1, table, self.note)

        # 写入字段名
        CSVHelper.__write_to_execl_by_index__(2, table, self.filed)

        # 写入数据
        for row in range(0, len(self.data)):
            CSVHelper.__write_to_execl_by_index__(3 + row, table, self.data[row])

        file.save(path + self.name + ".xls")

    def to_lua(self, path):
        """
        导出成lua代码
        :param path: 导出路径
        :return:
        """
        # 找到id所在的列
        id_index = 0
        if "unique_module" == self.module:
            assert None is not id_index, "找不到id"
            result, all_id = self.__process_default__(id_index)
        elif "sort_by_field_module" == self.module:
            assert None is not id_index, "找不到id"
            assert None is not self.order_index and -1 != self.order_index, "找不到排序字段"
            result, all_id = self.__process_sort__(id_index)
        elif "word_module" == self.module:
            result, all_id = self.__process_word__()
        else:
            assert None is not id_index, "找不到id"
            result, all_id = self.__process_default__(id_index)

        extra = self.__extra_index__(id_index)
        context = __TO_LUA_TEMPLATE__.format_map({
            "elements": result,
            "extra": extra,
            "all": all_id
        })
        with open(path + self.target_name + ".lua", 'w', encoding='utf8') as f:
            f.write(context)

    def to_csv(self, path):
        out = csv.writer(open(path + self.name + ".csv", 'w', encoding='utf-8', newline=''), dialect='excel')
        
        out.writerow(self.filed)

        csv_types = list()
        for swap_type in self.swap_type:
            if DataType.ARRAY_TYPE == swap_type.main_type or DataType.STR_TYPE == swap_type.main_type:
                csv_types.append('varchar')
            elif DataType.INT_TYPE == swap_type.main_type:
                csv_types.append('int')
            elif DataType.BOOL_TYPE == swap_type.main_type:
                csv_types.append('bool')
            elif DataType.FLOAT_TYPE == swap_type.main_type:
                csv_types.append('float')
        out.writerow(csv_types)

        platform = list()
        for item in self.platform:
            platform.append(item.lower())
        out.writerow(platform)
        
        out.writerow(self.note)

        for data in self.data:
            temp = list()
            for index in range(0, len(self.swap_type)):
                swap_type = self.swap_type[index]
                if '' != data[index]:
                    if DataType.ARRAY_TYPE == swap_type.main_type:
                        temp.append(str(data[index]).replace('[', '{').replace(']', '}'))
                    elif DataType.STR_TYPE == swap_type.main_type:
                        temp.append(str(data[index]))
                    elif DataType.INT_TYPE == swap_type.main_type:
                        temp.append(int(data[index]))
                    elif DataType.BOOL_TYPE == swap_type.main_type:
                        temp.append(str(data[index]))
                    elif DataType.FLOAT_TYPE == swap_type.main_type:
                        temp.append(float(data[index]))
                else:
                    temp.append(data[index])
            out.writerow(temp)
