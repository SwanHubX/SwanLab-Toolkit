"""
@author: cunyue
@file: test_settings.py
@time: 2025/5/15 18:15
@description: 测试 settings
"""

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
