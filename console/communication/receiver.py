from twisted.protocols.basic import LineReceiver
from handlers.specific.initial_handler import InitialHandler
from communication.manager import NLaunchManager


WELCOME_MSG = """
Welcome to the (hidden) NSA missile launcher console..
To get started on available commands type '!help'
"""

GOODBYE_MSG = """
Goodbye...
"""


class NLaunchReceiver(LineReceiver):

    delimiter = "\n".encode("utf8")

    def __init__(self):
        super(NLaunchReceiver, self).__init__()
        self.manager = NLaunchManager(self)
        self.handler = InitialHandler(self.manager)

    def connectionMade(self):
        print(">> made connection with client..")
        self.manager.sendLine(WELCOME_MSG)

    def connectionLost(self, reason):
        print(">> lost connection with client..")
        self.manager.sendLine(GOODBYE_MSG)

    def lineReceived(self, line):
        line = line.decode("utf8").rstrip("\r")
        print(">> a line has been received (%s).." % (line,))
        handled = self.handler.handle(line)
        if not handled:
            self.manager.sendLine("Command not recognized. The incident will be reported!")
