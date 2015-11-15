# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import json
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class DAL(object):
    """Data access layer."""
    def __init__(self, pass_file):
        super(DAL, self).__init__()
        with open(pass_file, "r") as f:
            self.passwords = json.loads(f.read(f))

    def getpwd(level):
        return self.passwords["level-%03d" % (int(level),)]
