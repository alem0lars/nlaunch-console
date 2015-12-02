# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from json import loads
from logging import getLogger as get_logger
from typing import TypeVar
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class DAL(object):
    """Data access layer."""

    def __init__(self, pwd_path: str):
        super(DAL, self).__init__()
        self.logger = get_logger("nlaunch.dal")
        with open(pwd_path, "r") as f:
            self.passwords = loads(f.read())
            self.logger.info("Loaded passwords from '{path}'".format(
                path=pwd_path))

    def get_lvl_pwd(self, level: TypeVar("L", str, int)) -> str:
        if isinstance(level, int):
            level = "level-{level:0>3}%03d".format(level=level)
        return self.passwords[level]
