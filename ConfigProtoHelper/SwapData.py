# _*_coding:utf-8_*_ 


class DataType:
    STR_TYPE = "STR"
    INT_TYPE = "INT"
    BOOL_TYPE = "BOOL"
    ARRAY_TYPE = "ARRAY"
    MAP_TYPE = "MAP"

    def __init__(self, type_name):
        self.main_type = None
        self.key_type = None
        self.value_type = None

        type_names = type_name.split(':')
        type_name_count = len(type_names)

        if type_name_count <= 0:
            print("[DataType] 无效的数据类型:", type_name)
            return
        self.main_type = type_names[0]

        if type_name_count >= 2:
            self.key_type = type_names[1]
            self.value_type = type_names[2]


class SwapData:
    def __init__(self, types, notes, field):
        self.types = types
        self.notes = notes
        self.fields = field
        self.datas = list()

    def insert(self, data):
        self.datas.append(data)

    def get(self, index):
        if index >= 0 and index < len(self.datas):
            return self.datas[index]

    def analyze(self):
        """
        将记录下来的数据根据类型翻译成python数据
        """
        for index in range(0, len(self.types)):
            # 先分析所有的类型
            type_name = self.types[index]
            data_type = DataType(self.types[index])
            self.types[index] = data_type
            if None is data_type.main_type:
                return

            # 根据输入类型分析类据，将其转换为proto数据
            field_name = self.fields[index]
            for data in self.datas:
                new_data = SwapData.__analyze_data_by_type(data[field_name], data_type)
                data[field_name] = new_data
    
    @staticmethod
    def __convert_data__(data, data_type):
        if DataType.STR_TYPE == data_type:
            return data
        elif DataType.INT_TYPE == data_type:
            return int(data)
        elif DataType.BOOL_TYPE == data_type:
            return bool(data)

    @staticmethod
    def __check_data_type__(data):
        temp = data.upper()
        if temp.isdigit():
            return DataType.INT_TYPE
        elif "TRUE" == temp or "FALSE" == temp:
            return DataType.BOOL_TYPE
        else:
            return DataType.STR_TYPE

    @staticmethod
    def __analyze_data_by_type(data, data_type):
        main_type = data_type.main_type
        if DataType.STR_TYPE == main_type:
            return data
        elif DataType.INT_TYPE == main_type:
            if None is not data_type.key_type:
                # todo 之后再处理
                return int(data)
            else:
                return int(data)
        elif DataType.ARRAY_TYPE == main_type:
            if None is not data_type.key_type:
                # todo 之后再处理
                return data
            else:
                return data
            pass
        elif DataType.MAP_TYPE == main_type:
            pass
        elif DataType.BOOL_TYPE == main_type:
            pass

    @staticmethod
    def __analyze_array_data__(data, data_type):
        data_length = len(data)
        if data_length <= 0:
            return None

        # 兼容旧类型写法
        temp = data
        if data[0] == '[':
            temp = data[1:]
        if data[data_length - 1] == ']':
            temp = data[:len(temp) - 1]
        
        # 数据以逗号做为分隔
        result = list()
        list_data = data.split(',')
        if len(list_data) > 0:
            if None is not data_type.key_type:
                data_type.key_type = SwapData.__check_data_type__(list_data[0])
            for item in list_data:
                result.append(SwapData.__convert_data__(item))

        return result