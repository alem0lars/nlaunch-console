# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from re import match, escape

from handlers.generic.base_handler import BaseHandler
from handlers.specific.pyjail_handler import PyJailHandler
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class InitialHandler(BaseHandler):

    HELP_MSG = """
        The following commands are available:

            !history
            !launch-missile <ID> <TARGET> <PASSWORD>
    """

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
        self._add_command_to_history("launch-missile", {
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
        print(">> handling help..")
        self.manager.sendLine(self.HELP_MSG)
        return True

    def _handleHistory(self):
        print(">> handling history..")
        self.manager.sendLine("The commands already executed are:")
        [self.manager.sendLine(command) for command in self.history]
        return True

    def _handleLaunchMissile(self):
        print(">> handling launch missile..")
        self.manager.sendLine("Error: Another missile has already been launched!")
        return True

    def _handleEnterPyJail(self):
        print(">> entering in PyJail..")
        self.manager.changeHandler(PyJailHandler(self.dal, self.manager))
        return True

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _add_command_to_history(self, name, info):
        elem = "Command: '%s'" % (name,)
        if len(info) > 0:
            elem += " ( "
            for (k,v) in info.items():
                elem += "%s: %s, " % (k, v)
            elem += " )"
        self.history.append(elem)
