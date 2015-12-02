# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from logging import getLogger as get_logger
from textwrap import dedent

from twisted.protocols.basic import LineReceiver

from communication.facade import NLaunchCommFacade
from handlers.specific.initial_handler import InitialHandler
from misc.dal import DAL
from misc.text import color_info, color_error, color_token
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class NLaunchReceiver(LineReceiver):

    WELCOME_MSG = dedent("""
        ------------------------------------------------------------------------

        {welcome}..

        To get started on available commands run: '{helpCommand}'

    """).format(
        welcome=color_info("Welcome to the (hidden) NSA missile launcher console"),
        helpCommand=color_token("!help"))

    UNRECOGNIZED_CMD_MSG = dedent("""
        {commandNotRecognized}
        The incident will be reported!
    """).format(commandNotRecognized=color_error("Command not recognized."))

    GOODBYE_MSG = dedent("""
        {goodbye}
    """).format(goodbye=color_info("Goodbye..."))

    delimiter = "\n".encode("utf8")

    def __init__(self, pwd_path):
        super(NLaunchReceiver, self).__init__()
        self.logger = get_logger("nlaunch.receiver")
        self.dal = DAL(pwd_path)
        self.facade = NLaunchCommFacade(self)
        self.handler = InitialHandler(self.dal, self.facade)

    def connectionMade(self):
        self.logger.info("Made new connection with a client")
        self.facade.send_line(self.WELCOME_MSG)

    def connectionLost(self, reason):
        self.logger.info("Lost connection with a client")
        self.facade.send_line(self.GOODBYE_MSG)

    def lineReceived(self, line):
        line = line.decode("utf8").rstrip("\r")
        self.logger.info("A new line has been received: '{line}'".format(
            line=line))
        handled = self.handler.handle(line)
        if not handled:
            self.facade.send_line(self.UNRECOGNIZED_CMD_MSG)
