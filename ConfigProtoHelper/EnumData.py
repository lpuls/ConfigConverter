# _*_coding:utf-8_*_ 

from SwapData import SwapData


class EnumData(SwapData):
    def __init__(self, file_name, types, notes, field):
        SwapData.__init__(self, file_name, types, notes, field)

    def to_proto(self):
        enum_field = ""
        for data_value in self.datas:
            name = data_value.get("name", None)
            value = data_value.get("value", None)
            annotation = data_value.get("annotation", None)
            if None is name or None is value or None is annotation:
                print("[SwapData]无效的枚举数值定义")
                return None
            enum_field += "\t%(file_name)s_%(enum_name)s = %(enum_value)d;  // %(annotation)s\n" % {
                    "file_name": self.file_name,
                    "enum_name": name,
                    "enum_value": value,
                    "annotation": annotation 
                }
        return enum_field
