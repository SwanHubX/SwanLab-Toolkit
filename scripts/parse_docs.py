#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024/6/17 16:18
@File: parse-docs.py
@IDE: pycharm
@Description:
    主要是为了与wiki的路径保持一致，创建此解析脚本
"""
import re
import os
import argparse


def parse(raw):
    # 定义正则表达式来匹配以 /docs 开头的链接
    pattern = re.compile(r'\[(.*?)]\((/docs/wiki/.*?\.md)\)')

    # 使用正则表达式替换匹配的链接
    def replace_link(match):
        text = match.group(1)
        link = match.group(2)
        # 删除 /docs 和 .md 后缀
        new_link = link.replace('/docs/wiki', '.').replace('.md', '')
        return f'[{text}]({new_link})'

    # 替换所有匹配的链接
    result = pattern.sub(replace_link, raw)
    return result


def main():
    # 创建一个解析器对象
    parser = argparse.ArgumentParser(description='Parse links in a markdown file.')

    # 添加一个位置参数
    parser.add_argument('path', type=str, help='The path to the folder')

    # 解析命令行参数
    args = parser.parse_args()

    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(args.path):
        for file in files:
            if not file.endswith('.md'):
                continue
            # 拼接文件的完整路径
            file_path = os.path.join(root, file)

            # 读取文件内容
            with open(file_path, 'r') as f:
                raw = f.read()

            # 解析文件内容
            parsed = parse(raw)

            # 写入解析后的内容
            with open(file_path, 'w') as f:
                f.write(parsed)


if __name__ == '__main__':
    main()
