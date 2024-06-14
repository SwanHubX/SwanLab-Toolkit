#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/15 01:49
@File: path.py
@IDE: pycharm
@Description:
    路径操作
"""

import os

_ = os.path.dirname(os.path.dirname(__file__))

TEMP_DIR = os.path.join(_, 'test', 'temp')
