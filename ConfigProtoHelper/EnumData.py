# _*_coding:utf-8_*_ 

from SwapData import SwapData


class EnumData(SwapData):
    def __init__(self, file_name, types, notes, field):
        SwapData.__init__(self, file_name, types, notes, field)

    def to_proto(self):
        has_zero = False
        enum_field = ""
        for data_value in self.datas:
            name = data_value.get("name", None)
            value = data_value.get("value", None)

            # protobuf的枚举首值必然要为0，因此这里必需检查如果在没有设置值为零的情况下，要添加一个为零的值
            if 0 == value:
                has_zero = True

            # 合成字符
            annotation = data_value.get("annotation", None)
            if None is name or None is value or None is annotation:
                print("[SwapData]无效的枚举数值定义")
                return None
            enum_field += "\t%(file_name)s_%(enum_name)s = %(enum_value)d;  // %(annotation)s\n" % {
                    "file_name": self.file_name,
                    "enum_name": name,
                    "enum_value": int(value),
                    "annotation": annotation 
                }
        if not has_zero:
            enum_field = "\t%(file_name)s_%(enum_name)s = %(enum_value)d;  // %(annotation)s\n" % {
                    "file_name": self.file_name,
                    "enum_name": "AutoSetZero",
                    "enum_value": int(0),
                    "annotation": "// protobuf的枚举首值必然要为0，因此这里必需检查如果在没有设置值为零的情况下，要添加一个为零的值" 
                } + enum_field
        return enum_field
