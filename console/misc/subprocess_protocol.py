# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from logging import getLogger

from twisted.internet.protocol import ProcessProtocol
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class SubProcessProtocol(ProcessProtocol):
    """Protocol managing interaction with a subprocess."""
    def __init__(self, manager):
        super(SubProcessProtocol, self).__init__()
        self.logger = getLogger(self.__class__.__name__)
        self.manager = manager

    def errReceived(self, data):
        self.logger.debug(data.decode("utf8"))

    def outReceived(self, data):
        self.logger.info("Received '%s' from subprocess" % (data,))
        self.manager.send(data.decode("utf8"))

    def sendToSubprocess(self, s):
        self.logger.info("Sending '%s' to subprocess" % (s,))
        self.transport.write(("%s\n" % (s,)).encode("utf8"))
