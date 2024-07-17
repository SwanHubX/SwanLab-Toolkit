#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/14 23:42
@File: env.py
@IDE: pycharm
@Description:
    测试环境变量
"""
from swankit import env as E
from tutils import TEMP_DIR
import pytest
import shutil
import nanoid
import datetime
import os


def test_create_time():
    t = E.create_time()
    assert t.endswith("+00:00")
    d = datetime.datetime.fromisoformat(t)
    assert d.tzinfo == datetime.timezone.utc


def test_list_mode():
    ms = E.SwanLabMode.list()
    assert len(ms) == 4
    assert "disabled" in ms
    assert "cloud" in ms
    assert "cloud-only" in ms
    assert "local" in ms


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
        assert E.get_save_dir() == folder
        assert os.path.exists(folder)

    def test_env_abs(self):
        """
        设置了一个绝对路径的环境变量
        """
        path = os.path.join(TEMP_DIR, nanoid.generate("1234567890abcdef", 10))
        os.environ[E.SwanLabSharedEnv.SWANLAB_FOLDER.value] = path
        assert not os.path.exists(path)
        assert E.get_save_dir() == path
        assert os.path.exists(path)

    def test_env_rel(self):
        """
        设置了一个相对路径的环境变量
        """
        abs_path = os.path.join(TEMP_DIR, nanoid.generate("1234567890abcdef", 10))
        rel_path = os.path.relpath(abs_path.__str__(), os.getcwd())
        os.environ[E.SwanLabSharedEnv.SWANLAB_FOLDER.value] = rel_path
        assert not os.path.exists(abs_path)
        assert E.get_save_dir() == abs_path
        assert os.path.exists(abs_path)

    def test_env_parent_not_exist(self):
        """
        父目录不存在
        """
        path = os.path.join(TEMP_DIR, nanoid.generate("1234567890abcdef", 10), "a")
        os.environ[E.SwanLabSharedEnv.SWANLAB_FOLDER.value] = path
        assert not os.path.exists(path)
        with pytest.raises(FileNotFoundError):
            E.get_save_dir()

    def test_env_not_a_folder(self):
        """
        文件夹不存在，但是文件存在
        """
        path = os.path.join(TEMP_DIR, nanoid.generate("1234567890abcdef", 10))
        with open(path, "w") as f:
            f.write("test")
        os.environ[E.SwanLabSharedEnv.SWANLAB_FOLDER.value] = path
        assert os.path.exists(path)
        with pytest.raises(NotADirectoryError):
            E.get_save_dir()


class TestGetSwanlog:

    def test_default(self):
        """
        默认情况
        """
        pwd = os.getcwd()
        folder = os.path.join(pwd, "swanlog")
        if os.path.exists(folder):
            shutil.rmtree(folder)
        assert E.get_swanlog_dir() == folder
        assert not os.path.exists(folder)

    def test_env_abs(self):
        """
        设置了一个绝对路径的环境变量
        """
        path = os.path.join(TEMP_DIR, nanoid.generate("1234567890abcdef", 10))
        os.environ[E.SwanLabSharedEnv.SWANLOG_FOLDER.value] = path
        if os.path.exists(path):
            shutil.rmtree(path)
        assert E.get_swanlog_dir() == path
        assert not os.path.exists(path)

    def test_env_rel(self):
        """
        设置了一个相对路径的环境变量
        """
        abs_path = os.path.join(TEMP_DIR, nanoid.generate("1234567890abcdef", 10))
        rel_path = os.path.relpath(abs_path.__str__(), os.getcwd())
        os.environ[E.SwanLabSharedEnv.SWANLOG_FOLDER.value] = rel_path
        if os.path.exists(abs_path):
            shutil.rmtree(abs_path)
        assert E.get_swanlog_dir() == abs_path
        assert not os.path.exists(abs_path)

    def test_env_parent_not_exist(self):
        """
        父目录不存在
        """
        path = os.path.join(TEMP_DIR, nanoid.generate("1234567890abcdef", 10), "a")
        os.environ[E.SwanLabSharedEnv.SWANLOG_FOLDER.value] = path
        assert not os.path.exists(path)
        with pytest.raises(FileNotFoundError):
            E.get_swanlog_dir()

    def test_env_not_a_folder(self):
        """
        文件夹不存在，但是文件存在
        """
        path = os.path.join(TEMP_DIR, nanoid.generate("1234567890abcdef", 10))
        with open(path, "w") as f:
            f.write("test")
        os.environ[E.SwanLabSharedEnv.SWANLOG_FOLDER.value] = path
        assert os.path.exists(path)
        with pytest.raises(NotADirectoryError):
            E.get_swanlog_dir()


class TestGetMode:
    """
    测试获取解析模式
    """

    def test_default(self):
        """
        默认情况
        """
        assert E.get_mode() == E.SwanLabMode.CLOUD.value

    def test_env(self):
        """
        设置了环境变量
        """
        os.environ[E.SwanLabSharedEnv.SWANLAB_MODE.value] = E.SwanLabMode.LOCAL.value
        assert E.get_mode() == E.SwanLabMode.LOCAL.value

    def test_unknown(self):
        """
        未知的模式
        """
        os.environ[E.SwanLabSharedEnv.SWANLAB_MODE.value] = "unknown"
        with pytest.raises(ValueError):
            E.get_mode()
