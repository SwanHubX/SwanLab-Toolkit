"""
@author: cunyue
@file: test_settings.py
@time: 2025/5/15 18:15
@description: 测试 settings
"""


def test_lazy_settings():
    from swankit.core.settings import LazySettings

    settings = LazySettings()
    settings.exp_name = "test"
    settings.exp_colors = ("red", "blue")
    settings.description = "test description"

    assert settings.exp_name == "test"
    assert settings.exp_colors == ("red", "blue")
    assert settings.description == "test description"

    try:
        settings.exp_name = "test2"
    except ValueError as e:
        assert str(e) == "exp_name can only be set once"

    try:
        settings.exp_colors = ("green", "yellow")
    except ValueError as e:
        assert str(e) == "exp_colors can only be set once"

    try:
        settings.description = "test description 2"
    except ValueError as e:
        assert str(e) == "description can only be set once"
