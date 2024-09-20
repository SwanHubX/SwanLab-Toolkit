#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/14 23:06
@File: __init__.py.py
@IDE: pycharm
@Description:
    回调类，规定回调函数的接口规范。
"""

from abc import ABC, abstractmethod
from .models import *
from swankit.core import SwanLabSharedSettings
from typing import Tuple


class SwanKitCallback(ABC):
    """
    SwanKitCallback，回调函数注册类，所有以`on_`和`before_`开头的函数都会在对应的时机被调用
    此处只定义会被调用的函数，用于接口规范
    """

    def on_init(self, proj_name: str, workspace: str, logdir: str = None, **kwargs):
        """
        执行`swanlab.init`时调用，此时运行时环境变量没有被设置，此时修改环境变量还是有效的
        :param logdir: str, 用户设置的日志目录
        :param proj_name: str, 项目名称
        :param workspace: str, 工作空间
        :param kwargs: dict, 其他参数，为了增加灵活性，可以在on_init的时候设置一些其他类内参数
        """
        pass

    def before_run(self, settings: SwanLabSharedSettings):
        """
        在运行实验之前调用
        :param settings: SwanLabSharedSettings, 运行时的共享配置
        """
        pass

    def before_init_experiment(
        self,
        run_id: str,
        exp_name: str,
        description: str,
        num: int,
        colors: Tuple[str, str],
    ):
        """
        在初始化实验之前调用，此时SwanLabRun已经初始化完毕
        :param run_id: str, SwanLabRun的运行id
        :param exp_name: str, 实验名称
        :param description: str, 实验描述
        :param num: int, 历史实验数量
        :param colors: Tuple[str, str], 实验颜色，[light, dark]
        """
        pass

    def on_run(self):
        """
        SwanLabRun初始化完毕时调用
        """
        pass

    def on_run_error_from_operator(self, e: OperateErrorInfo):
        """
        执行`on_run`错误时被操作员调用
        """
        pass

    def on_runtime_info_update(self, r: RuntimeInfo):
        """
        运行时信息更新时调用
        :param r: RuntimeInfo, 运行时信息
        """
        pass

    def on_log(self):
        """
        每次执行swanlab.log时调用
        """
        pass

    def on_column_create(self, column_info: ColumnInfo):
        """
        列创建回调函数,新增列信息时调用
        """
        pass

    def on_metric_create(self, metric_info: MetricInfo):
        """
        指标创建回调函数,新增指标信息时调用
        """
        pass

    def on_stop(self, error: str = None):
        """
        训练结束时的回调函数
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        返回当前回调函数的名称，这条应该是一个全局唯一的标识
        在operator中会用到这个名称，必须唯一
        """
        pass


__all__ = ["SwanKitCallback", "MediaBuffer", "MetricInfo", "ColumnInfo", "OperateErrorInfo", "RuntimeInfo"]
