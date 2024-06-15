#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/14 23:19
@File: log.py
@IDE: pycharm
@Description:
    日志模块，封装logging模块，提供swanlab标准日志记录功能
"""
import logging
from .utils import FONT
from typing import Literal, Union
import sys


class ColoredFormatter(logging.Formatter, FONT):
    def __init__(self, fmt=None, datefmt=None, style="%", handle=None):
        super().__init__(fmt, datefmt, style)
        self.__handle = handle
        # 打印等级对应的颜色装载器
        self.__color_map = {
            logging.DEBUG: self.grey,
            logging.INFO: self.bold_blue,
            logging.WARNING: self.yellow,
            logging.ERROR: self.red,
            logging.CRITICAL: self.bold_red,
        }

    def bold_red(self, s: str) -> str:
        """在终端中加粗的红色字符串

        Parameters
        ----------
        s : str
            需要加粗的字符串

        Returns
        -------
        str
            加粗后的字符串
        """
        # ANSI 转义码用于在终端中改变文本样式
        return self.bold(self.red(s))

    def bold_blue(self, s: str) -> str:
        """在终端中加粗的蓝色字符串

        Parameters
        ----------
        s : str
            需要加粗的字符串

        Returns
        -------
        str
            加粗后的字符串
        """
        return self.bold(self.blue(s))

    def __get_colored_str(self, levelno, message):
        """获取使用打印等级对应的颜色装载的字符串

        Parameters
        ----------
        levelno : logging.levelno
            logging 等级对象
        message : string
            需要装载的颜色
        """

        return self.__color_map.get(levelno)(message)

    def format(self, record):
        """格式化打印字符串
            1. 分割消息头和消息体
            2. 消息头根据 logging 等级装载颜色
            3. 使用空格填充，统一消息头长度为 20 个字符
            4.. 拼接消息头和消息体

        Parameters
        ----------
        record : logging.record
            logging 信息实例

        Returns
        -------
        string
            格式化后的字符串
        """
        log_message = super().format(record)
        self.__handle(log_message + "\n") if self.__handle else None
        # 分割消息，分别处理头尾
        messages: list = log_message.split(":", 1)
        # 填充空格，统一消息头的长度
        message_header = messages[0]
        return f"{self.__get_colored_str(record.levelno, message_header)}:{messages[1]}"


Levels = Union[Literal["debug", "info", "warning", "error", "critical"], str]
"""
SwanKitLog 预先定义好的日志等级
"""


class SwanLabSharedLog:
    # 日志系统支持的输出等级
    levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    def __init__(self, name=__name__.lower(), level: Levels = "info"):
        """

        :param name:
        :param level:
        """
        super().__init__()
        self.prefix = name + ':'
        self.__logger = logging.getLogger(name)
        self.__original_level = self.__get_level(level)
        self.__installed = False
        self.__logger.setLevel(self.__original_level)
        # 初始化控制台日志处理器，输出到标准输出流
        self.__handler = logging.StreamHandler(sys.stdout)
        # 添加颜色格式化，并在此处设置格式化后的输出流是否可以被其他处理器处理
        colored_formatter = ColoredFormatter("%(name)s: %(message)s")
        self.__handler.setFormatter(colored_formatter)
        self.enable_log()

    def disable_log(self):
        """
        是否开启日志输出，实例化时默认开启
        """
        self.__logger.removeHandler(self.__handler)

    def enable_log(self):
        self.__logger.addHandler(self.__handler)

    def set_level(self, level: Levels):
        """
        Set the logging level of the logger.

        :param level: The level to set the logger to. This should be one of the following:
            - "debug"
            - "info"
            - "warning"
            - "error"
            - "critical"

        :raises: KeyError: If an invalid level is passed.
        """
        self.__logger.setLevel(self.__get_level(level))

    def __get_level(self, level: Levels):
        """私有属性，获取等级对应的 logging 对象

        Parameters
        ----------
        level : string
            日志级别，可以是 "debug", "info", "warning", "error", 或 "critical"

        Returns
        -------
        logging.level : object
            logging 模块中的日志等级

        Raises
        ------
        KeyError
            无效的日志级别
        """
        if level.lower() in self.levels:
            return self.levels.get(level.lower())
        else:
            raise KeyError("log_level must be one of ['debug', 'info', 'warning', 'error', 'critical']: %s" % level)

    def debug(self, message: str):
        self.__logger.debug(message)
        return

    def info(self, message: str):
        self.__logger.info(message)
        return

    def warning(self, message: str):
        self.__logger.warning(message)
        return

    def error(self, message: str):
        self.__logger.error(message)
        return

    def critical(self, message: str):
        self.__logger.critical(message)
        return
