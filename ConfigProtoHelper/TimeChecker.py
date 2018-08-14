from time import clock


def init_time():
    log = open("../Config/Time.txt", 'w')
    log.close()


def __write_time__(context):
    log = open("../Config/Time.txt", 'a')
    log.write(context)
    log.write('\n')
    log.close()


def return_cal_run_time(func, info, *args):
    start = clock()
    result = func(*args)
    time = clock() - start
    __write_time__('"Func": "%s", "Time": %f, "Info": "%s"' % (func.__name__, time, info, ))
    print('"Func": "%s", "Time": %f, "Info": "%s"' % (func.__name__, time, info, ))
    return time, result


def cal_run_time_no_args(func, info):
    start = clock()
    result = func()
    time = clock() - start
    __write_time__('"Func": "%s", "Time": %f, "Info": "%s"' % (func.__name__, time, info, ))
    print('"Func": "%s", "Time": %f, "Info": "%s"' % (func.__name__, time, info, ))
    return result


def cal_run_time(func, info, *args):
    start = clock()
    result = func(*args)
    time = clock() - start
    # __write_time__('"Func": "%s", "Time": %f, "Info": "%s"' % (func.__name__, time, info, ))
    print('"Func": "%s", "Time": %f, "Info": "%s"' % (func.__name__, time, info, ))
    return result

def cal_run_time_deco(func):
    def wrapper(*args, **kwargs):
        start = clock()
        result = func(*args, **kwargs)
        time = clock() - start
        # __write_time__('Execute Func: %s, Time: %f' % (func.__name__, time, ))
        print("%s: %f" % (func.__name__, time, ))
        return result
    return wrapper
