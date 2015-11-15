# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from twisted.internet.protocol import Factory

from communication.receiver import NLaunchReceiver
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class NLaunchFactory(Factory):
    def __init__(self, pass_file):
        super(NLaunchFactory, self).__init__()
        self.pass_file = pass_file

    def buildProtocol(self, addr):
        return NLaunchReceiver(self.pass_file)
