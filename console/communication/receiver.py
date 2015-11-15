from twisted.protocols.basic import LineReceiver
from handlers.specific.initial_handler import InitialHandler
from communication.manager import NLaunchManager



class NLaunchReceiver(LineReceiver):

    WELCOME_MSG = """
        Welcome to the (hidden) NSA missile launcher console..
        To get started on available commands type '!help'
    """

    GOODBYE_MSG = "Goodbye..."

    delimiter = "\n".encode("utf8")

    def __init__(self, data_dir):
        super(NLaunchReceiver, self).__init__()
        self.dal     = DAL(data_dir)
        self.manager = NLaunchManager(self)
        self.handler = InitialHandler(self.dal, self.manager)

    def connectionMade(self):
        print(">> made connection with client..")
        self.manager.sendLine(self.WELCOME_MSG)

    def connectionLost(self, reason):
        print(">> lost connection with client..")
        self.manager.sendLine(self.GOODBYE_MSG)

    def lineReceived(self, line):
        line = line.decode("utf8").rstrip("\r")
        print(">> a line has been received (%s).." % (line,))
        handled = self.handler.handle(line)
        if not handled:
            self.manager.sendLine("Command not recognized. The incident will be reported!")
