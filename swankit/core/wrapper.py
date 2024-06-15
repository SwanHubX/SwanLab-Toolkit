#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/15 13:08
@File: wrapper.py
@IDE: pycharm
@Description:
    包装器相关模型
"""
from typing import Optional


class WrapperErrorInfo:
    """
    DataWrapper转换时的错误信息
    """

    def __init__(
            self,
            expected: Optional[str],
            got: Optional[str],
            chart: Optional[BaseType.Chart],
            duplicated: bool = False
    ):
        """
        :param expected: 期望的数据类型
        :param got: 实际的数据类型
        :param chart: 当前错误数据对应的图表类型
        :param duplicated: 是否是重复错误,如果为是，expected和got和chart都为None
        """
        self.expected = expected if not duplicated else None
        self.got = got if not duplicated else None
        self.chart = chart if not duplicated else None
        self.__duplicated = duplicated

    def dict(self):
        return {"expected": self.expected, "got": self.got}

    @property
    def duplicated(self) -> bool:
        """
        是否是重复错误，重复错误时，got和expected为None
        """
        return self.__duplicated
