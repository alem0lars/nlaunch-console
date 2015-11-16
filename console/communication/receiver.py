# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from logging import getLogger
from textwrap import dedent

from twisted.protocols.basic import LineReceiver

from communication.manager import NLaunchManager
from handlers.specific.initial_handler import InitialHandler
from misc.dal import DAL
from misc.text import colorInfo, colorError, colorToken
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class NLaunchReceiver(LineReceiver):

    WELCOME_MSG = dedent("""
        {welcome}..

        To get started on available commands run: '{helpCommand}'
    """).format(
        welcome=colorInfo("Welcome to the (hidden) NSA missile launcher console"),
        helpCommand=colorToken("!help"))

    UNRECOGNIZED_CMD_MSG = dedent("""
        {commandNotRecognized}
        The incident will be reported!
    """).format(commandNotRecognized=colorError("Command not recognized."))

    GOODBYE_MSG = dedent("""
        {goodbye}
    """).format(goodbye=colorInfo("Goodbye..."))

    delimiter = "\n".encode("utf8")

    def __init__(self, pwdFile):
        super(NLaunchReceiver, self).__init__()
        self.logger  = getLogger("nlaunch.receiver")
        self.dal     = DAL(pwdFile)
        self.manager = NLaunchManager(self)
        self.handler = InitialHandler(self.dal, self.manager)

    def connectionMade(self):
        self.logger.info("Made new connection with a client")
        self.manager.sendLine(self.WELCOME_MSG)

    def connectionLost(self, reason):
        self.logger.info("Lost connection with a client")
        self.manager.sendLine(self.GOODBYE_MSG)

    def lineReceived(self, line):
        line = line.decode("utf8").rstrip("\r")
        self.logger.info("A new line has been received: '{line}'".format(
            line=line))
        handled = self.handler.handle(line)
        if not handled:
            self.manager.sendLine(self.UNRECOGNIZED_CMD_MSG)
