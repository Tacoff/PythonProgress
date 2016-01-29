#!/usr/bin/env python
# -*- coding: utf8 -*-

from dealraw import dec


@dec
def write(c):
    '''
    记录文本的内容
    '''
    with file("test2.txt", "w") as f:
        for line in c:
            f.write(line)
    return "ok"


def main():
    fr = file("test.txt", "r")
    cx = []
    _raw = fr.readline()
    while _raw:
        cx.append(_raw)
        _raw = fr.readline()

    st = write(cx)
    print st
    print write.__doc__
    print write.__name__


if __name__ == '__main__':
    main()
