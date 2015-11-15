# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from logging import getLogger

from twisted.protocols.basic import LineReceiver

from communication.manager import NLaunchManager
from handlers.specific.initial_handler import InitialHandler
from misc.dal import DAL
from misc.text import formatMsg
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class NLaunchReceiver(LineReceiver):

    WELCOME_MSG = formatMsg("""
        #{cyan}Welcome to the (hidden) NSA missile launcher console..#{normal}

        To get started on available commands run: '#{bold}#{magenta}!help#{normal}'
    """)

     "\n".join([
        colorInfo(""),
        "" % (colorToken(""),)
    ])

    UNRECOGNIZED_CMD_MSG = "\n".join([
        colorError("Command not recognized."),
        "The incident will be reported!"
    ])

    GOODBYE_MSG = colorInfo("Goodbye...")

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
        self.logger.info("A new line has been received: '%s'" % (line,))
        handled = self.handler.handle(line)
        if not handled:
            self.manager.sendLine(self.UNRECOGNIZED_CMD_MSG)
