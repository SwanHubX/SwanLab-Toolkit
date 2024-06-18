#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/14 23:19
@File: log.py
@IDE: pycharm
@Description:
    日志模块，封装logging模块，提供swanlab标准日志记录功能
"""
from .utils import FONT
from typing import Literal, Union
import sys

# ---------------------------------- 日志打印等级 ----------------------------------
Levels = Union[Literal["debug", "info", "warning", "error", "critical"], str]
"""
SwanKitLog 预先定义好的日志等级字符串
"""
CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10


# ---------------------------------- 日志类 ----------------------------------


class SwanLabSharedLog:

    def __init__(self, name=__name__.lower(), level: Levels = "info", file=None):
        self.__file = file if file else sys.stdout
        self.__level: int = 0
        # 粗体
        self.__prefix_dict = {
            "debug": FONT.bold(FONT.grey(name)) + ":",
            "info": FONT.bold(FONT.blue(name)) + ":",
            "warning": FONT.bold(FONT.yellow(name)) + ":",
            "error": FONT.bold(FONT.red(name)) + ":",
            "critical": FONT.bold(FONT.bold(FONT.red(name))) + ":",
        }
        self.__levels_dict = {
            "debug": DEBUG,
            "info": INFO,
            "warning": WARNING,
            "error": ERROR,
            "critical": CRITICAL,
        }
        self.level = level
        self.__can_log = True

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, level: Levels):
        """
        设置日志等级
        :param level: 日志等级，可选值为 debug, info, warning, error, critical，如果传入的值不在可选值中，则默认为 info
        """
        self.__level = self.__levels_dict.get(level.lower(), 20)

    def disable_log(self):
        """
        关闭日志输出，实例化时默认开启
        """
        self.__can_log = False

    def enable_log(self):
        """
        开启日志输出
        """
        self.__can_log = True

    def __print(self, log_level: str, *args, **kwargs):
        """
        打印日志
        """
        if not self.__can_log:
            return
        level = self.__levels_dict[log_level]
        if level < self.__level:
            return
        print(self.__prefix_dict[log_level], *args, **kwargs, file=self.__file)

    # 发送调试消息
    def debug(self, *args, **kwargs):
        return self.__print("debug", *args, **kwargs)

    # 发送通知
    def info(self, *args, **kwargs):
        return self.__print("info", *args, **kwargs)

    # 发生警告
    def warning(self, *args, **kwargs):
        return self.__print("warning", *args, **kwargs)

    # 发生错误
    def error(self, *args, **kwargs):
        return self.__print("error", *args, **kwargs)

    # 致命错误
    def critical(self, *args, **kwargs):
        return self.__print("critical", *args, **kwargs)
