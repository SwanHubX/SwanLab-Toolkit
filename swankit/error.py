#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/15 01:16
@File: error.py
@IDE: pycharm
@Description:
    swanlab内部错误，方便捕获
"""


class SwanLabError(Exception):
    """SwanLab内部错误基类"""
    pass


class UnKnownSystemError(Exception):
    """未知系统错误，此时swanlab运行在未知系统上，这个系统不是windows或者类unix系统
    """
    pass
