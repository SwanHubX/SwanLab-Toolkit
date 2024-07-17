#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/14 23:07
@File: env.py
@IDE: pycharm
@Description:
    规定可以被复用的、全局的环境变量，原则上，这里的环境变量和工具应该影响到所有基于 SwanLab-Toolkit 开发的项目
"""
import os
import sys
from enum import Enum
from typing import List
import datetime


class SwanLabMode(Enum):
    """
    swanlab的解析模式，枚举类
    """

    DISABLED = "disabled"
    CLOUD = "cloud"
    CLOUD_ONLY = "cloud-only"
    LOCAL = "local"

    @classmethod
    def list(cls) -> List[str]:
        """
        获取所有的枚举值
        :return: 所有的枚举值
        """
        return [item.value for item in cls]


class SwanLabSharedEnv(Enum):
    """
    环境变量Key，枚举类，这些环境变量是swanlab全局共用的环境变量
    """

    SWANLAB_FOLDER = "SWANLAB_SAVE_DIR"
    """
    swanlab全局文件夹保存的路径，默认为用户主目录下的.swanlab文件夹
    """
    SWANLOG_FOLDER = "SWANLAB_LOG_DIR"
    """
    swanlab解析日志文件保存的路径，默认为当前运行目录的swanlog文件夹
    """
    SWANLAB_MODE = "SWANLAB_MODE"
    """
    swanlab的解析模式，涉及操作员注册的回调，目前有三种：local、cloud、disabled，默认为cloud
    大小写不敏感
    """

    @classmethod
    def list(cls) -> List[str]:
        """
        获取所有的枚举值
        :return: 所有的枚举值
        """
        return [item.value for item in cls]


# ---------------------------------- 获取环境变量/配置的值 ----------------------------------


def is_windows() -> bool:
    """判断当前操作系统是否是windows还是类unix系统，主要是路径分隔上的差别
    此外的系统会报错为 UnKnownSystemError
    :raise OSError: 未知系统错误，此时swanlab运行在未知系统上，这个系统不是windows或者类unix系统
    :return: True表示是windows系统，False表示是类unix系统
    """
    if sys.platform.startswith("win"):
        return True
    elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        return False
    raise OSError("Unknown system, not windows or unix-like system")


def create_time() -> str:
    """获取当前时间(UTC时区)"""
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def get_save_dir() -> str:
    """
    获取存放swanlab全局文件的文件夹路径，如果不存在就创建
    此函数对应为SWANLAB_SAVE_FOLDER全局变量，如果没有设置，默认为用户主目录下的.swanlab文件夹
    执行此函数时，如果文件夹不存在，自动创建，但是出于安全考虑，不会自动创建父文件夹
    :raises
        :raise FileNotFoundError: folder的父目录不存在
        :raise NotADirectoryError: folder不是一个文件夹
    :return: swanlab全局文件夹保存的路径，返回处理后的绝对路径
    """
    folder = os.getenv(SwanLabSharedEnv.SWANLAB_FOLDER.value)
    if folder is None:
        folder = os.path.join(os.path.expanduser("~"), ".swanlab")
    folder = os.path.abspath(folder)
    if not os.path.exists(os.path.dirname(folder)):
        raise FileNotFoundError(f"{os.path.dirname(folder)} not found")
    if not os.path.exists(folder):
        # 只创建当前文件夹，不创建父文件夹
        os.mkdir(folder)
    if not os.path.isdir(folder):
        raise NotADirectoryError(f"{folder} is not a directory")
    return folder


def get_swanlog_dir() -> str:
    """
    获取存放swanlog日志文件的文件夹路径
    此函数对应为SWANLAB_LOG_FOLDER全局变量，如果没有设置，默认为当前运行目录下的swanlog文件夹
    需要注意，此函数并不会保证文件夹的存在，但是会检查父文件夹是否存在以及folder是否是一个文件夹
    :raises
        :raise FileNotFoundError: folder的父目录不存在
        :raise NotADirectoryError: folder不是一个文件夹
    :return: swanlog日志文件保存的路径，返回处理后的绝对路径
    """
    folder = os.getenv(SwanLabSharedEnv.SWANLOG_FOLDER.value)
    if folder is None:
        folder = os.path.join(os.getcwd(), "swanlog")
    folder = os.path.abspath(folder)
    if not os.path.exists(os.path.dirname(folder)):
        raise FileNotFoundError(f"{os.path.dirname(folder)} not found")
    if not os.path.exists(folder):
        return folder
    if not os.path.isdir(folder):
        raise NotADirectoryError(f"{folder} is not a directory")
    return folder


def get_mode() -> str:
    """
    获取当前的swanlab解析模式，如果没有设置，默认为cloud
    :raise ValueError: 未知的swanlab模式
    :return: swanlab的解析模式
    """
    mode = os.getenv(SwanLabSharedEnv.SWANLAB_MODE.value)
    if mode is None:
        mode = SwanLabMode.CLOUD.value
    mode = mode.lower()
    if mode not in SwanLabMode.list():
        raise ValueError(f"Unknown swanlab mode: {mode}")
    return mode
