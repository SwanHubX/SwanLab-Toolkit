#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/15 13:23
@File: __init__.py
@IDE: pycharm
@Description:
    核心解析模块工具
"""
from .data import BaseType, MediaType, DataSuite, MediaBuffer, ParseResult, ParseErrorInfo, ChartReference
from .settings import SwanLabSharedSettings

ChartType = BaseType.Chart

__all__ = [
    "BaseType",
    "MediaType",
    "ChartType",
    "DataSuite",
    "MediaBuffer",
    "ParseResult",
    "ParseErrorInfo",
    "SwanLabSharedSettings",
    "ChartReference",
]
