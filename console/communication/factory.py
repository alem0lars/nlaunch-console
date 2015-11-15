from twisted.internet.protocol import Factory
from communication.receiver import NLaunchReceiver


class NLaunchFactory(Factory):
    def __init__(self, data_dir):
        super(NLaunchFactory, self).__init__()
        self.data_dir = data_dir

    def buildProtocol(self, addr):
        return NLaunchReceiver(self.data_dir)
