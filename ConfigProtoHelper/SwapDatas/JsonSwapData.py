# _*_coding:utf-8_*_

from SwapDatas.MessageData import *
from SwapDatas.SwapData import SwapData


class JsonSwapData(SwapData):
    def __init__(self, file_name, types, notes, field):
        SwapData.__init__(self, file_name, types, notes, field)


