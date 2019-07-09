# _*_coding:utf-8_*_


def process_array(array_str, element_type):
    array_context = array_str[1: -1]

    stack = list()
    result = list()
    is_nesting = False
    for index, item in enumerate(array_context):
        if '[' == item:
            is_nesting = True
            stack.append(index)
        elif ']' == item:
            temp = stack.pop()
            element, element_type = process_array(array_context[temp: index + 1])
            result.append()

    if None is element_type:
        pass

    if not is_nesting:
        pass

    return result, element_type

if __name__ == '__main__':
    pass
