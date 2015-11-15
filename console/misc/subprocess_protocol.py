# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from logging import getLogger

from twisted.internet.protocol import ProcessProtocol
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class SubProcessProtocol(ProcessProtocol):
    """Protocol managing interaction with a sub-process."""
    def __init__(self, manager):
        super(SubProcessProtocol, self).__init__()
        self.logger = getLogger("nlaunch.subprocess")
        self.manager = manager

    def errReceived(self, data):
        self.logger.debug(data.decode("utf8"))

    def outReceived(self, data):
        self.logger.debug("Received '%s' from subprocess" % (data,))
        self.manager.send(data.decode("utf8"))

    def sendToSubprocess(self, s):
        self.logger.debug("Sending '%s' to subprocess" % (s,))
        self.transport.write(("%s\n" % (s,)).encode("utf8"))
