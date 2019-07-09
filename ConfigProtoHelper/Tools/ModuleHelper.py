# _*_coding:utf-8_*_


def load_module(path):
    paths = path.split('.')
    if len(paths) <= 0:
        return None

    module_inst = __import__(path)
    for index in range(1, len(paths)):
        module_inst = getattr(module_inst, paths[index])
    return module_inst
