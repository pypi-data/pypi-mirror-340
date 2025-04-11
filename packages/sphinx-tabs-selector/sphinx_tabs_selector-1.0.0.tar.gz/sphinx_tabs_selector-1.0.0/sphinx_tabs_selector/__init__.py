#!/rtkoss/python/3.6.7/rhel7/x86_64/bin/python3
# coding=utf-8
"""
@Project : sphinx_tabs_selector
@File    : __init__.py.py
@Time    : 2025/4/11 17:14
@Author  : terra_cai
@Email   : terra_cai@realsil.com.cn
@Software: PyCharm
"""

import os
import sys
from pathlib import Path

my_real_path = Path(__file__).resolve()
libs = [
    str((my_real_path / '../../../../venv/Lib/site-packages').resolve())
]
for lib in libs:
    if lib not in sys.path:
        sys.path.insert(0, lib)
