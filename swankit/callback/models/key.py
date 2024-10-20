#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/5 16:32
@File: key.py
@IDE: pycharm
@Description:
    与Key相关的回调函数触发时的模型
"""
from typing import Union, Optional, Dict, List, Literal
from swankit.core import ChartType, ParseErrorInfo, MediaBuffer
from urllib.parse import quote
import os


class ColumnInfo:
    """
    列信息，当创建列时，会生成这个对象
    """

    def __init__(
        self,
        key: str,
        key_id: str,
        key_name: str,
        key_class: Literal["CUSTOM", "SYSTEM"],
        section_name: str,
        section_sort: int,
        chart_type: ChartType,
        chart_reference: Literal["step", "time"],
        error: Optional[ParseErrorInfo] = None,
        config: Optional[Dict] = None,
    ):
        """
        生成的列信息对象
        :param key: 生成的列名称
        :param key_id: 当前实验下，列的唯一id，与保存路径等信息有关
        :param key_name: key的别名
        :param key_class: 列的类型，CUSTOM为自定义列，SYSTEM为系统生成列
        :param section_name: 列的组名
        :param section_sort: 列在section中的参考排序，不代表实际排序
        :param chart_type: 列对应的图表类型
        :param chart_reference: 这个列对应图表的参考系，step为步数，time为时间
        :param error: 列的类型错误信息
        :param config: 列的额外配置信息
        """
        self.key = key
        self.key_id = key_id
        self.key_name = key_name
        self.key_class = key_class

        self.section_name = section_name
        self.section_sort = section_sort

        self.chart_type = chart_type
        self.chart_reference = chart_reference

        self.error = error
        self.config = config if config is not None else {}

    @property
    def got(self):
        """
        传入的错误类型，如果列出错，返回错误类型，如果没出错，`暂时`返回None
        """
        if self.error is None:
            return None
        return self.error.got

    @property
    def expected(self):
        """
        期望的类型，如果列出错，返回期望的类型，如果没出错，`暂时`返回None
        """
        if self.error is None:
            return None
        return self.error.expected

    @property
    def key_encode(self):
        """
        对key进行url编码
        """
        return quote(self.key, safe="")


class MetricInfo:
    """
    指标信息，当新的指标数据被log时，会生成这个对象
    """

    __SUMMARY_NAME = "_summary.json"

    def __init__(
        self,
        column_info: ColumnInfo,
        metric: Optional[Dict],
        metric_buffers: Optional[List[MediaBuffer]],
        metric_summary: Optional[Dict],
        metric_step: Optional[int],
        metric_epoch: Optional[int],
        metric_file_name: Optional[str],
        swanlab_logdir: Optional[str],
        swanlab_media_dir: Optional[str],
        error: Optional[ParseErrorInfo] = None,
    ):
        """
        生成的指标信息对象
        :param column_info: 此指标对应的列信息
        :param metric: 此指标的数据
        :param metric_buffers: 此指标的媒体数据，如果为None，表示没有媒体数据
        :param metric_summary: 此指标的摘要信息
        :param metric_step: 此指标的步数
        :param metric_epoch: 此指标对应本地的行数
        :param metric_file_name: 此指标的文件名
        :param swanlab_logdir: swanlab在本次实验的log文件夹路径
        :param swanlab_media_dir: swanlab在本次实验的media文件夹路径
        :param error: 创建此指标时的错误信息
        """
        self.error = error
        self.column_info = column_info
        self.metric = metric
        self.metric_buffers = metric_buffers
        self.metric_summary = metric_summary
        self.metric_step = metric_step
        self.metric_epoch = metric_epoch
        _id = self.column_info.key_id
        self.metric_file_path = None if self.is_error else os.path.join(swanlab_logdir, _id, metric_file_name)
        self.summary_file_path = None if self.is_error else os.path.join(swanlab_logdir, _id, self.__SUMMARY_NAME)
        self.swanlab_media_dir = swanlab_media_dir
        # 写入文件名称，对应上传时的文件名称：{key}/{文件名称}，文件夹名称为key
        if self.metric_buffers is not None:
            for i, buffer in enumerate(self.metric_buffers):
                buffer.file_name = "{}/{}".format(self.column_info.key_encode, metric["data"][i])

    @property
    def is_error(self) -> bool:
        """
        这条指标信息是否有错误，错误分几种：
            1. 列错误，列一开始就出现问题
            2. 重复错误
            3. 指标错误
        """
        return self.error is not None or self.column_error is not None

    @property
    def column_error(self) -> Optional[ParseErrorInfo]:
        """
        列错误信息
        """
        return self.column_info.error

    @property
    def data(self) -> Union[Dict, None]:
        """
        指标数据的data字段
        """
        if self.is_error:
            return None
        return self.metric["data"]


class MetricErrorInfo(MetricInfo):
    def __init__(self, column_info: ColumnInfo, error: ParseErrorInfo):
        """
        错误的指标信息，简化输入参数
        :param column_info: 此指标对应的列信息
        :param error: 创建此指标时的错误信息
        """
        super().__init__(
            column_info,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            error,
        )
