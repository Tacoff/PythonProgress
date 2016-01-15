#!/usr/bin/env python27
# -*- coding: utf8 -*-

from appblog import app

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=80)
