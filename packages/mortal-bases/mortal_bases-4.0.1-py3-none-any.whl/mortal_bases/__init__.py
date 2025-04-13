#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2025/4/10 22:07
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
__all__ = ["MortalBases"]
from .base_main import MortalBasesMain


class MortalBases(MortalBasesMain):
    def __init__(self):
        super().__init__()
