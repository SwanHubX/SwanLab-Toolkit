"""
@author: cunyue
@file: test_settings.py
@time: 2025/5/15 18:15
@description: 测试 settings
"""

import os.path
import time
from datetime import datetime

import pytest


def test_lazy_settings():
    from swankit.core.settings import LazySettings

    settings = LazySettings()
    settings.exp_name = "test"
    settings.exp_colors = ("red", "blue")
    settings.description = "test description"

    assert settings.exp_name == "test"
    assert settings.exp_colors == ("red", "blue")
    assert settings.description == "test description"

    with pytest.raises(ValueError, match="exp_name can only be set once"):
        settings.exp_name = "test2"
    with pytest.raises(ValueError, match="exp_colors can only be set once"):
        settings.exp_colors = ("green", "yellow")
    with pytest.raises(ValueError, match="description can only be set once"):
        settings.description = "test description 2"


def test_settings():
    """
    主要测试 settings 初始化时遇见相同文件夹自动创建新文件夹的功能
    """
    from swankit.core.settings import SwanLabSharedSettings
    from tutils import TEMP_DIR

    # 测试创建文件夹
    # 尽量保持代码运行在一秒的开始
    time.sleep(1 - (time.time() % 1))  # 确保时间戳在整秒
    start = time.time()
    run_id = "111111"
    run_dir = os.path.join(TEMP_DIR, "run-{}-{}".format(datetime.now().strftime("%Y%m%d_%H%M%S"), run_id))
    settings = SwanLabSharedSettings(logdir=TEMP_DIR, run_id=run_id, version="develop", should_save=True)
    assert time.time() - start < 1  # 此时不应该等待一秒
    assert settings.run_dir == run_dir
    assert settings.run_id == run_id

    # 测试创建同名文件夹
    # 尽量保持代码运行在一秒的开始
    time.sleep(1 - (time.time() % 1))  # 确保时间戳在整秒
    start = time.time()
    # 测试创建一个存在的文件夹
    run_id = "123456"
    run_dir = os.path.join(TEMP_DIR, "run-{}-{}".format(datetime.now().strftime("%Y%m%d_%H%M%S"), run_id))
    os.mkdir(run_dir)
    settings = SwanLabSharedSettings(logdir=TEMP_DIR, run_id=run_id, version="develop", should_save=True)
    assert 2 > time.time() - start >= 1  # 确保至少等待了一秒
    assert settings.run_dir != run_dir  # 确保没有使用原来的文件夹
    assert settings.run_id == run_id  # 确保run_id正确


def test_settings_no_save():
    """
    测试不保存的情况，此时不会检查文件夹唯一性
    """
    from swankit.core.settings import SwanLabSharedSettings
    from tutils import TEMP_DIR

    # 测试创建文件夹
    # 尽量保持代码运行在一秒的开始
    time.sleep(1 - (time.time() % 1))  # 确保时间戳在整秒
    start = time.time()
    run_id = "111111"
    run_dir = os.path.join(TEMP_DIR, "run-{}-{}".format(datetime.now().strftime("%Y%m%d_%H%M%S"), run_id))
    settings = SwanLabSharedSettings(logdir=TEMP_DIR, run_id=run_id, version="develop", should_save=False)
    assert time.time() - start < 1  # 此时不应该等待一秒
    assert settings.run_dir == run_dir
    assert settings.run_id == run_id

    # 测试创建同名文件夹
    # 尽量保持代码运行在一秒的开始
    time.sleep(1 - (time.time() % 1))  # 确保时间戳在整秒
    start = time.time()
    # 测试创建一个存在的文件夹
    run_id = "123456"
    run_dir = os.path.join(TEMP_DIR, "run-{}-{}".format(datetime.now().strftime("%Y%m%d_%H%M%S"), run_id))
    os.mkdir(run_dir)
    settings = SwanLabSharedSettings(logdir=TEMP_DIR, run_id=run_id, version="develop", should_save=False)
    assert time.time() - start < 1  # 此时不应该等待一秒
    assert settings.run_dir == run_dir
    assert settings.run_id == run_id
