# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from twisted.internet.protocol import Factory

from communication.receiver import NLaunchReceiver
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class NLaunchFactory(Factory):
    """Factory used by the twisted reactor to handle clients.

    Create a new :class:`NLaunchReceiver` for every client.
    """
    def __init__(self, pwd_path):
        super(NLaunchFactory, self).__init__()
        self.pwd_path = pwd_path

    def buildProtocol(self, addr):
        return NLaunchReceiver(self.pwd_path)
