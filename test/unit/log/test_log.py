#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/14 23:41
@File: test_log.py
@IDE: pycharm
@Description:
    测试日志模块
"""
from swankit.log import SwanLabSharedLog
import nanoid


class TestSwanKitLog:
    """
    测试日志模块
    """

    def test_enable_default(self, capsys):
        """
        测试开启日志
        """
        levels = ["debug", "info", "warning", "error", "critical"]
        for level in levels:
            name = nanoid.generate()
            text = nanoid.generate()
            t = SwanLabSharedLog(name, level=level)
            for le in levels:
                getattr(t, le)(text)
                out, err = capsys.readouterr()
                if levels.index(le) >= levels.index(level):
                    assert text in out
                    assert name in out
                    assert err == ""
                else:
                    assert out == ""
                    assert err == ""

    def test_disable(self, capsys):
        """
        测试关闭日志
        """
        levels = ["debug", "info", "warning", "error", "critical"]
        for level in levels:
            name = nanoid.generate()
            text = nanoid.generate()
            t = SwanLabSharedLog(name, level=level)
            t.disable_log()
            for le in levels:
                getattr(t, le)(text)
                out, err = capsys.readouterr()
                assert out == ""
                assert err == ""

    def test_set_level(self, capsys):
        """
        测试设置日志等级
        """
        levels = ["debug", "info", "warning", "error", "critical"]
        for le in levels:
            name = nanoid.generate()
            text = nanoid.generate()
            t = SwanLabSharedLog(name, level="debug")
            t.level = le
            getattr(t, le)(text)
            out, err = capsys.readouterr()
            assert text in out
            assert name in out
            assert err == ""
