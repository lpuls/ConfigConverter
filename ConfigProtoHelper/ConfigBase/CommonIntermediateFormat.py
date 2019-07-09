# _*_coding:utf-8_*_


class CommonIntermediateFormat:
    """
    通用中间格式
    任意源->中间格式->目标格式
    types 每个字段的类型
    notes 每个字段的说明
    fields 每个字段的名称
    data_list list<> 记录每一组数据的列表
    """
    def __init__(self, name, types, notes, fields, data_list):
        self.name = name
        self.types = types
        self.notes = notes
        self.fields = fields
        self.data_list = data_list
