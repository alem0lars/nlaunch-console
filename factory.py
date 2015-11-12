from twisted.internet.protocol import Factory
from receiver import ManagementConsoleReceiver


class ManagementConsoleFactory(Factory):
    def __init__(self):
        super(ManagementConsoleFactory, self).__init__()

    def buildProtocol(self, addr):
        return ManagementConsoleReceiver()
