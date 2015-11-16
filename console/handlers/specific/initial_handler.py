# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from re import match, escape
from textwrap import dedent

from termcolor import colored

from handlers.generic.base_handler import BaseHandler
from handlers.specific.pyjail_handler import PyJailHandler
from misc.text import colorInfo, colorToken
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class InitialHandler(BaseHandler):

    HELP_MSG = dedent("""
        The following commands are available:

            {historyCommand}
            {launchCommand}
    """).format(
        historyCommand=colorToken("!history"),
        launchCommand=colorToken("!launch-missile <ID> <TARGET> <PASSWORD>"))

    MISSILE_ID       = "K00R34N-B00B1ES"
    MISSILE_TARGET   = ", ".join([
        "39°02'24.1\"N 125°45'50.7\"E - Rungna People's Pleasure Ground",
        "Pyongyang (평양시)",
        "North Korea"
    ])

    """Handler for the initial commands."""
    def __init__(self, dal, manager):
        super(InitialHandler, self).__init__(dal, manager)
        self.history = []
        self._addCommandToHistory("launch-missile", {
            "id":     self.MISSILE_ID,
            "target": self.MISSILE_TARGET
        })

    def handle(self, line):
        if match("\s*!help\s*", line):
            return self._handleHelp()
        elif match("\s*!history\s*", line):
            return self._handleHistory()
        elif match("\s*!launch-missile\s*", line):
            return self._handleLaunchMissile()
        elif line == self.dal.getpwd(1):
            return self._handleEnterPyJail()
        else:
            return False

    # Handlers ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _handleHelp(self):
        self.logger.info("Handling command 'help'")
        self.manager.sendLine(self.HELP_MSG)
        return True

    def _handleHistory(self):
        self.logger.info("Handling command 'history'")
        self.manager.sendLine("The commands that have already been carried out are:")
        for command in self.history:
            self.manager.sendLine("\t- {command}".format(command=command))
        return True

    def _handleLaunchMissile(self):
        self.logger.info("Handling command 'launch-missile'")
        self.manager.sendLine("Error: Another missile has already been launched!")
        return True

    def _handleEnterPyJail(self):
        self.logger.info("Entering in PyJail")
        self.manager.changeHandler(PyJailHandler(self.dal, self.manager))
        return True

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _addCommandToHistory(self, name, info):
        elem = "Command: '%s'" % (colored(name, "magenta"),)
        if len(info) > 0:
            elem += " ( "
            for (k,v) in info.items():
                elem += "%s: %s, " % (colored(k, "blue"), colored(v, "green"))
            elem += " )"
        self.history.append(elem)
