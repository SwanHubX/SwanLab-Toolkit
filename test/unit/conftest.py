#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/4/3 16:52
@File: conftest.py.py
@IDE: pycharm
@Description:
    配置pytest
"""
import pytest
from tutils import TEMP_DIR
from swankit.env import SwanLabSharedEnv
import shutil
import os


@pytest.fixture(scope="function", autouse=True)
def setup_before_each():
    # ---------------------------------- 在每一个函数执行前，删除临时文件夹 ----------------------------------
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.mkdir(TEMP_DIR)
    # ---------------------------------- 每个函数执行前，清空环境变量 ----------------------------------
    for key in SwanLabSharedEnv.list():
        if key in os.environ:
            del os.environ[key]
    yield
