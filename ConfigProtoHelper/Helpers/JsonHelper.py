# _*_coding:utf-8_*_

import json
from SwapDatas.JsonSwapData import JsonSwapData


class JsonHelper:
    __IS_INIT__ = False
    MESSAGES = dict()

    @staticmethod
    def initialize(desc_path):
        if JsonHelper.__IS_INIT__:
            return
        JsonHelper.__IS_INIT__ = True

        # 根据描述文件创建对应的消息类
        json_desc = json.loads(JsonHelper.load_json(desc_path))
        for desc_name in json_desc:
            message_desc = json_desc[desc_name]
            types = list()
            fields = list()
            notes = list()
            for property_desc in message_desc:
                types.append(property_desc['Type'])
                fields.append(property_desc['Field'])
                notes.append(property_desc['Note'])
            JsonHelper.MESSAGES[desc_name] = JsonSwapData(desc_name, types, notes, fields)

    @staticmethod
    def load_json_config(path):
        json_data = json.loads(JsonHelper.load_json(path))

        # 取出文件名
        name = path[path.rfind('/') + 1: path.rfind('.')]

        # 根据文件名来确定对应哪一张表
        table_type = name
        if -1 != name.find('_'):
            table_type = name[:name.find('_')]
        message_data = JsonHelper.MESSAGES.get(table_type, None)
        if None is message_data:
            print("无效的JSON文件 " + path)
            return
        message_data.insert(json_data)

    @staticmethod
    def load_json(path):
        result = ""
        with open(path, encoding="utf-8") as f:
            config_text = f.readlines()
            f.close()
            for line in config_text:
                result += line
        return result
