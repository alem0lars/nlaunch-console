# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from twisted.internet.protocol import Factory

from communication.receiver import NLaunchReceiver
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class NLaunchFactory(Factory):
    def __init__(self, pwdFile):
        super(NLaunchFactory, self).__init__()
        self.pwdFile = pwdFile

    def buildProtocol(self, addr):
        return NLaunchReceiver(self.pwdFile)
