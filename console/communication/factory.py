from twisted.internet.protocol import Factory
from communication.receiver import NLaunchReceiver


class NLaunchFactory(Factory):
    def __init__(self):
        super(NLaunchFactory, self).__init__()

    def buildProtocol(self, addr):
        return NLaunchReceiver()
