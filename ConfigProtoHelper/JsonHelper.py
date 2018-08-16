# _*_coding:utf-8_*_

import json
from pbjson import *
from DataType import *
from SwapData import *
from MessageData import MessageData


class TimelineSwapData(MessageData):
    ID_INDEX = 0

    def __init__(self, file_name, types, notes, field):
        MessageData.__init__(self, file_name, types, notes, field)
        self.key = SwapData.DEFAULT_KEY
        self.key_type = DataType(DataType.INT_TYPE)

    def to_proto(self):
        # TODO 我先简单粗暴的这么写好了
        message_field  = "\tint32 ID = 1;\n"
        message_field += "\tint32 duration = 2;\n"
        message_field += "\tmessage ClipInfo {\n\t\tint32 Start = 1;\n\t\tint32 End = 1;\n}"
        message_field += "\tmap<string, int32> Recover = 3;\n"
        message_field += "\tmap<string, int32> PreInput = 4;\n"
        message_field += "\trepeated int32 AnimationClips = 5;\n"
        message_field += "\trepeated int32 hitTimes = 6;"
        return message_field

    def analyze(self):
        return True


class JsonHelper:
    __IS_INIT__ = False
    MESSAGES = None
    CLIP_INFO_MESSAGE = None
    TIME_LINE_MESSAGE = None  # MessageData()

    @staticmethod
    def initialize():
        JsonHelper.__IS_INIT__ = True
        JsonHelper.TIME_LINE_MESSAGE = TimelineSwapData("TimelineInfo", [], [], [])

        JsonHelper.MESSAGES = {
                "TimelineInfo": JsonHelper.TIME_LINE_MESSAGE
            }

    @staticmethod
    def load_json_config(path):
        if not JsonHelper.__IS_INIT__:
            JsonHelper.initialize()

        json_data = json.loads(JsonHelper.load_json(path))
        json_data[SwapData.DEFAULT_KEY] = TimelineSwapData.ID_INDEX;
        TimelineSwapData.ID_INDEX += 1;
        JsonHelper.TIME_LINE_MESSAGE.insert(json_data)


    @staticmethod
    def load_json(path):
        result = ""
        with open(path) as f:
            config_text = f.readlines()
            f.close()
            for line in config_text:
                result += line
        return result
