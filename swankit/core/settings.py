#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/15 13:24
@File: settings.py
@IDE: pycharm
@Description:
    swankit 为 swanlab 定制的配置类
"""
import os
import time
from datetime import datetime
from typing import Tuple, List, Optional


class LazySettings:
    """
    运行时动态设置的信息，只能设置一次，他们并不在一开始就被赋予意义，如果在设置前访问，返回None
    """

    def __init__(self):
        self.__exp_name = None
        self.__exp_colors = None
        self.__description = None
        self.__tags = None

    @property
    def exp_name(self) -> str:
        """实验名称"""
        if self.__exp_name is None:
            raise ValueError("exp_name is None before set")
        return self.__exp_name

    @exp_name.setter
    def exp_name(self, exp_name: str) -> None:
        """实验名称"""
        if self.__exp_name is not None:
            raise ValueError("exp_name can only be set once")
        self.__exp_name = exp_name

    @property
    def exp_colors(self) -> Optional[Tuple[str, str]]:
        """实验颜色"""
        return self.__exp_colors

    @exp_colors.setter
    def exp_colors(self, exp_colors: Tuple[str, str]) -> None:
        """实验颜色"""
        if self.__exp_colors is not None:
            raise ValueError("exp_colors can only be set once")
        self.__exp_colors = exp_colors

    @property
    def description(self) -> Optional[str]:
        """实验描述"""
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        """实验描述"""
        if self.__description is not None:
            raise ValueError("description can only be set once")
        self.__description = description

    @property
    def tags(self) -> Optional[List[str]]:
        """实验标签"""
        return self.__tags

    @tags.setter
    def tags(self, tags: List[str]) -> None:
        """实验标签"""
        if self.__tags is not None:
            raise ValueError("tags can only be set once")
        self.__tags = tags


class SwanLabSharedSettings(LazySettings):
    """
    SwanLabRun的配置信息，包括当前实验路径信息等

    涉及路径的属性都已经自动转换为绝对路径，并且文件夹路径在`should_save=True`时会自动创建

    "几乎"所有属性都为只读属性，只有在初始化时可以设置
    """

    def __init__(self, logdir: str, run_id: str, version: str, should_save: bool) -> None:
        """
        初始化
        :param logdir: 日志目录
        :param run_id: 实验运行id
        :param version: 实验版本
        :param should_save: 是否应该保存实验相关信息，如果保存，相关文件夹将自动创建（文件不会自动创建）
        """
        LazySettings.__init__(self)
        # ---------------------------------- 静态信息 ----------------------------------
        self.__should_save = should_save
        self.__version = version
        self.__run_id = run_id
        # ----------------------- 检测运行文件夹的创建，确保文件夹在当前进程唯一占有 ----------
        run_dir = None
        while True:
            run_dir is not None and time.sleep(1)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            run_name = "run-{}-{}".format(timestamp, run_id)
            run_dir = os.path.join(logdir, run_name)
            if not should_save:
                break
            try:
                os.mkdir(run_dir)
                break
            except FileExistsError:
                pass
        assert run_dir is not None, "run_dir should not be None, please check the logdir and run_id"
        # ---------------------------------- 文件夹信息 ----------------------------------
        self.__root_dir = os.path.dirname(logdir)
        self.__swanlog_dir = logdir
        self.__run_dir = run_dir
        self.__console_dir = os.path.join(self.run_dir, "console")
        self.__log_dir = os.path.join(self.run_dir, "logs")
        self.__files_dir = os.path.join(self.run_dir, "files")
        self.__media_dir = os.path.join(self.run_dir, "media")
        # ---------------------------------- 文件信息 ----------------------------------
        self.__error_path = os.path.join(self.console_dir, "error.log")

    def mkdir(self, path: str) -> None:
        """创建目录
        为了保证安全性，不会递归创建
        """
        try:
            if not os.path.exists(path) and self.should_save:
                os.mkdir(path)
        except FileExistsError:  # https://github.com/SwanHubX/SwanLab/issues/1090
            pass

    # ---------------------------------- 静态属性 ----------------------------------

    @property
    def should_save(self):
        """
        是否应该保存实验信息
        """
        return self.__should_save

    @property
    def version(self) -> str:
        return self.__version

    @property
    def run_id(self) -> str:
        """实验运行id"""
        return self.__run_id

    # ---------------------------------- 文件夹属性 ----------------------------------

    @property
    def root_dir(self) -> str:
        """swanlog保存的根目录"""
        # 必然存在，不需要创建
        return self.__root_dir

    @property
    def swanlog_dir(self) -> str:
        """swanlog目录，存储所有实验的日志目录，也是runs.swanlab数据库的存储目录"""
        self.mkdir(self.__swanlog_dir)
        return self.__swanlog_dir

    @property
    def run_dir(self) -> str:
        """实验日志、信息文件夹路径"""
        self.mkdir(self.__run_dir)
        return self.__run_dir

    @property
    def log_dir(self) -> str:
        """记录用户日志文件夹路径"""
        self.mkdir(self.__log_dir)
        return self.__log_dir

    @property
    def console_dir(self) -> str:
        """记录终端日志路径"""
        self.mkdir(self.__console_dir)
        return self.__console_dir

    @property
    def media_dir(self) -> str:
        """静态资源路径"""
        self.mkdir(self.__media_dir)
        return self.__media_dir

    @property
    def files_dir(self) -> str:
        """实验配置信息路径"""
        self.mkdir(self.__files_dir)
        return self.__files_dir

    # ---------------------------------- 文件属性 ----------------------------------

    @property
    def error_path(self) -> str:
        """错误日志文件路径"""
        return self.__error_path
