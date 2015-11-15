# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from json import loads
from logging import getLogger
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class DAL(object):
    """Data access layer."""
    def __init__(self, pwdFile):
        super(DAL, self).__init__()
        self.logger = getLogger(self.__class__.__name__)
        with open(pwdFile, "r") as f:
            self.passwords = loads(f.read())
            self.logger.debug("Loaded passwords from '%s'" % (pwdFile,))

    def getpwd(self, level):
        return self.passwords["level-%03d" % (int(level),)]
