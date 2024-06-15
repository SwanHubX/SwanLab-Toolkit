#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/14 23:12
@File: __init__.py
@IDE: pycharm
@Description:
    日志模块，提供swanlab标准日志记录功能
"""
from .utils import FONT
from .log import SwanLabSharedLog, Levels

__all__ = ["FONT", "SwanLabSharedLog", "Levels"]
