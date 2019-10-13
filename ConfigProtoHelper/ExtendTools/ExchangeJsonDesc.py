# _*_coding:utf-8_*_

import json
from Tools.FileHelper import load_json


result = list()
desc = load_json("../../Config/Timeline/JsonDesc.json")
for key, value in desc.items():
    temp = {"Name": key, "Desc": value}
    result.append(temp)

with open("../../Config/Timeline/JsonDesc2.json", 'w') as f:
    f.write(json.dumps(result))
