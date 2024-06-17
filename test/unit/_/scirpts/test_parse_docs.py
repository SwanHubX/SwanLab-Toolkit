#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/17 16:32
@File: test_parse_docs.py
@IDE: pycharm
@Description:
    测试parse_docs.py
"""
import os
from scripts.parse_docs import parse, main
from tutils import TEMP_DIR
from unittest.mock import patch
import argparse
import pytest


@pytest.mark.parametrize("raw, expected", [
    (
            "Here is a link to [some document](/docs/wiki/some/path/to/document.md).",
            "Here is a link to [some document](./some/path/to/document)."
    ),
    (
            "And another link to [another document](/docs/wiki/another/path/to/document.md).",
            "And another link to [another document](./another/path/to/document)."
    ),
    (
            "No change to [normal link](https://example.com).",
            "No change to [normal link](https://example.com)."
    ),
    (
            "Multiple links [doc1](/docs/wiki/doc1.md) and [doc2](/docs/wiki/doc2.md).",
            "Multiple links [doc1](./doc1) and [doc2](./doc2)."
    ),
    (
            "Empty link []().",
            "Empty link []()."
    ),
    (
            "Link with no extension [doc](/docs/wiki/doc).",
            "Link with no extension [doc](/docs/wiki/doc)."
    ),
    (
            "Link with different extension [doc](/docs/wiki/doc.txt).",
            "Link with different extension [doc](/docs/wiki/doc.txt)."
    ),
])
def test_parse(raw, expected):
    """
    测试parse函数
    """
    assert parse(raw) == expected


def test_main():
    """
    测试main函数
    """
    path = os.path.join(TEMP_DIR, "test_parse_docs")
    os.makedirs(path)
    # ---------------------------------- 写入一些文件 ----------------------------------
    with open(os.path.join(path, "test1.md"), "w") as f:
        f.write("Here is a link to [some document](/docs/wiki/some/path/to/document.md).")
    with open(os.path.join(path, "test2.md"), "w") as f:
        f.write("And another link to [another document](/docs/wiki/another/path/to/document.md).")

    with patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(path=path)):
        main()

    with open(os.path.join(path, "test1.md"), "r") as f:
        assert f.read() == "Here is a link to [some document](./some/path/to/document)."
    with open(os.path.join(path, "test2.md"), "r") as f:
        assert f.read() == "And another link to [another document](./another/path/to/document)."
