# _*_coding:utf-8_*_

import json


def to_object(class_type, context):
    json_data = json.loads(context)
    inst = class_type()
    for k, v in json_data.items():
        if isinstance(v, dict):
            pass
        elif isinstance(v, list):
            pass
        else:
            inst.__dict__[k] = v
    return inst


def to_json(inst):
    json_data = inst.__dict__
    return json.dumps(json_data)


class Ability:
    def __init__(self):
        self.id = 0
        self.power = 0


class Player:
    def __init__(self):
        self.name = ''
        self.age = ''
        self.abilities = list()


if __name__ == '__main__':
    p = to_object(Player, '{"name": "xp", "age": 10, "abilities": [{"id": 1, "power": 100}, {"id": 2, "power": 200}]}')
    print(p.name)
    print(p.age)
    print(p.abilities)
