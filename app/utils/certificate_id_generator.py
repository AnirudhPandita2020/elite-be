from time import time


def certificate_id():
    value = str(int(time() * 1000))
    return "ETC" + value[0:(len(value) - 1 // 2)]
