#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/14 23:42
@File: env.py
@IDE: pycharm
@Description:
    测试环境变量
"""
import pytest

from swankit import env as E
from tutils import TEMP_DIR
import shutil
import nanoid
import os


class TestGetFolder:
    """
    测试获取全局保存文件夹
    """

    def test_default(self):
        """
        默认情况
        """
        # 获取当前用户的主目录
        home = os.path.expanduser("~")
        folder = os.path.join(home, ".swanlab")
        if os.path.exists(folder):
            shutil.rmtree(folder)
        assert E.get_swanlab_save_folder() == folder
        assert os.path.exists(folder)

    def test_env_abs(self):
        """
        设置了一个绝对路径的环境变量
        """
        path = os.path.join(TEMP_DIR, nanoid.generate("1234567890abcdef", 10))
        os.environ[E.SwanLabEnv.SAVE_FOLDER.value] = path
        assert not os.path.exists(path)
        assert E.get_swanlab_save_folder() == path
        assert os.path.exists(path)

    def test_env_rel(self):
        """
        设置了一个相对路径的环境变量
        """
        abs_path = os.path.join(TEMP_DIR, nanoid.generate("1234567890abcdef", 10))
        rel_path = os.path.relpath(abs_path.__str__(), os.getcwd())
        os.environ[E.SwanLabEnv.SAVE_FOLDER.value] = rel_path
        assert not os.path.exists(abs_path)
        assert E.get_swanlab_save_folder() == abs_path
        assert os.path.exists(abs_path)

    def test_env_parent_not_exist(self):
        """
        父目录不存在
        """
        path = os.path.join(TEMP_DIR, nanoid.generate("1234567890abcdef", 10), "a")
        os.environ[E.SwanLabEnv.SAVE_FOLDER.value] = path
        assert not os.path.exists(path)
        with pytest.raises(FileNotFoundError):
            E.get_swanlab_save_folder()

    def test_env_not_a_folder(self):
        """
        文件夹不存在，但是文件存在
        """
        path = os.path.join(TEMP_DIR, nanoid.generate("1234567890abcdef", 10))
        with open(path, "w") as f:
            f.write("test")
        os.environ[E.SwanLabEnv.SAVE_FOLDER.value] = path
        assert os.path.exists(path)
        with pytest.raises(NotADirectoryError):
            E.get_swanlab_save_folder()
