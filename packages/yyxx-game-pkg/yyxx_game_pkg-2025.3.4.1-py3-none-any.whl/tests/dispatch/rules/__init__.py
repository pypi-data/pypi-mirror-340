# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/14

import os
import importlib
from os.path import dirname
from yyxx_game_pkg.stat.log import local_log


def rules_auto_import():
    pkg_dir = dirname(__file__)
    files = os.listdir(pkg_dir)
    for idx, filepath in enumerate(files):
        if filepath.startswith("__init__"):
            continue
        if not filepath.endswith(".py"):
            continue
        module_name = filepath[:-3]
        import_path = "tests.dispatch.rules.{}".format(module_name)
        module = importlib.import_module(import_path)
        local_log("********[dispatch] auto import {}".format(module))
