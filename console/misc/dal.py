# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from logging import getLogger as get_logger
import json
import typing
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class DAL(object):
    """Data access layer."""

    def __init__(self, pwd_path: str):
        """Create a new :class:`.DAL` object."""
        super(DAL, self).__init__()
        self.logger = get_logger("nlaunch.dal")
        with open(pwd_path, "r") as f:
            self.passwords = json.loads(f.read())
            self.logger.info("Loaded passwords from '{path}'".format(
                path=pwd_path))

    def get_lvl_pwd(self, level: typing.TypeVar("L", str, int)) -> str:
        """Get password for a specific level.

        :param level: The level for which the password should be retrieved
        """
        if isinstance(level, int):
            level = "level-{level:0>3}%03d".format(level=level)
        return self.passwords[level]
