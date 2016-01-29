#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
from functools import wraps


def dec(func):
    @wraps(func)
    def deal(ctxl):
        """
        特殊处理appfolderauth部分的内容
        """
        startm = re.compile("\[AppFolderAuth\]")
        endm = re.compile("\[")
        ctxm = re.compile("^(?P<header>[^\s]+) [^\s]")
        # ctxl = []
        # fr = file("test.txt", "r")
        # _raw = fr.readline()
        # while _raw:
        #     ctxl.append(_raw)
        #     _raw = fr.readline()

        coxl = []
        tag = 0
        i = 0
        head = None
        while i < len(ctxl):
            line = ctxl[i]
            if tag == 0:
                if not startm.search(line) is None:
                    tag = 1
            elif tag == 1:
                if endm.search(line) is None:
                    if line.startswith("已成功") or line.startswith("Success") \
                            or line.startswith("N/A") or line == "\n":
                        i += 1
                        continue
                    else:
                        if not ctxm.search(line) is None:
                            head = ctxm.search(line).group("header")
                        else:
                            line = head + " " + line.lstrip()
                        # print line
                else:
                    tag = 2
            coxl.append(line)
            i += 1
        return func(coxl)
    return deal
