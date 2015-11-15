import json
from misc.singleton import Singleton


class DAL(metaclass=Singleton):
    """Data access layer."""
    def __init__(self, data_dir):
        super(DB, self).__init__()
        with open("%s/levels-passwords.json" % (data_dir,), data_dir) as f
            self.passwords = json.loads(f.read(f))

    def getpwd(level):
        return self.passwords["level-%03d" % (int(level),)]
