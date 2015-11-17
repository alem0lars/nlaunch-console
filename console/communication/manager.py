# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from logging import getLogger
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class NLaunchManager(object):
    """Manage common operations."""
    def __init__(self, receiver):
        super(NLaunchManager, self).__init__()
        self.logger = getLogger("nlaunch.manager")
        self.receiver = receiver

    def send(self, s):
        self.receiver.transport.write(s.encode("utf8"))

    def sendLine(self, s):
        self.receiver.sendLine(s.encode("utf8"))

    def closeConnection(self):
        self.receiver.transport.loseConnection()

    def getCurrentHandler(self):
        return self.receiver.handler

    def changeHandler(self, handler):
        self.logger.info("Changing handler from '{prev}' to '{next}'".format(
            prev=self.receiver.handler.__class__.__name__,
            next=handler.__class__.__name__))
        self.receiver.handler = handler
