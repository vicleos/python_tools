#!/usr/bin/env python
# coding:utf8
# author: vicleo

try:
    import psutil
except ImportError:
    print('Error: psutil module not found!')
    exit()


def getKey():
    keyInfo = psutil.net_io_counters(pernic=True).keys()
    recv = {}
    sent = {}

    for key in keyInfo:
        recv.setdefault(
            key, psutil.net_io_counters(pernic=True).get(key).bytes_recv)
        sent.setdefault(
            key, psutil.net_io_counters(pernic=True).get(key).bytes_sent)

    return keyInfo, recv, sent


def getRate(func):
    import time
    keyInfo, oldRecv, oldSent = func()

    time.sleep(1)
    keyInfo, nowRecv, nowSent = func()
    netIn = {}
    netOut = {}

    for key in keyInfo:
        netIn.setdefault(key, (nowRecv.get(key) - oldRecv.get(key)) / 1024)
        netOut.setdefault(key, (nowSent.get(key) - oldSent.get(key)) / 1024)

    return keyInfo, netIn, netOut


while 1:
    try:
        keyInfo, netIn, netOut = getRate(getKey)

        for key in keyInfo:
            if key == '本地连接':
                print('%s\nInput:\t %-5s KB/s\nOutPut:\t %-5s KB/s\n' % (key, netIn.get(key), netOut.get(key)))
    except KeyboardInterrupt:
        exit()

# End