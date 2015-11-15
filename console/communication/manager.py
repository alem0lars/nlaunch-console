class NLaunchManager(object):
    """Manage common operations."""
    def __init__(self, receiver):
        super(Manager, self).__init__()
        self.receiver = receiver

    def send(self, s):
        self.receiver.transport.write(s.encode("utf8"))

    def sendLine(self, s):
        self.receiver.sendLine(s.encode("utf8"))

    def closeConnection(self):
        self.receiver.transport.loseConnection()

    def changeHandler(self, handler):
        self.receiver.handler = handler
