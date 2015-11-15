# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from twisted.internet.protocol import ProcessProtocol
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class SubProcessProtocol(ProcessProtocol):
    """Protocol managing interaction with a subprocess."""
    def __init__(self, manager):
        super(SubProcessProtocol, self).__init__()
        self.manager = manager

    def errReceived(self, data):
        print(">> %s" % (data.decode("utf8"),))

    def outReceived(self, data):
        print(">> received from subprocess: %s" % (data,))
        self.manager.send(data.decode("utf8"))

    def sendToSubprocess(self, s):
        print(">> sending to subprocess: %s" % (s,))
        self.transport.write(("%s\n" % (s,)).encode("utf8"))
