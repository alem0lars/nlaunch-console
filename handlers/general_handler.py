from handlers.base_handler import BaseHandler
from handlers.pyjail_handler import PyJailHandler
from re import match, escape


HELP_MSG = """
The following commands are available:

    !history
    !launch-missile <ID> <TARGET> <PASSWORD>
    !disarm-missile <ID> <PASSWORD>
"""

WIN_MSG = """
Congratulations, the nuclear missile has been successfully disarmed!!

You've saved the world today.. not so easy eh!?
"""

MISSILE_ID       = "K00R34N-B00B1ES"
MISSILE_TARGET   = "39°02'24.1\"N 125°45'50.7\"E - Rungna People's Pleasure Ground, Pyongyang (평양시), North Korea"
MISSILE_PASSWORD = "D(2wQIq-f@"

COMMAND_ENTER_PYJAIL = "dqwjoi"


class GeneralHandler(BaseHandler):
    """Handler for generic commands."""
    def __init__(self, manager):
        super(GeneralHandler, self).__init__(manager)
        self.history = []
        self._add_command_to_history("launch-missile", {
            "id": MISSILE_ID,
            "target": MISSILE_TARGET
        })

    def handle(self, line):
        if match("\s*!help\s*", line):
            return self._handleHelp()
        elif match("\s*!history\s*", line):
            return self._handleHistory()
        elif match("\s*!launch-missile\s*", line):
            return self._handleLaunchMissile()
        elif match("\s*!disarm-missile\s*", line):
            return self._handleDisarmMissile(line)
        elif line == COMMAND_ENTER_PYJAIL:
            return self._handleEnterPyJail()
        else:
            return False

    # Handlers ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _handleHelp(self):
        print(">> handling help..")
        self.manager.sendLine(HELP_MSG)
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

    def _handleDisarmMissile(self, line):
        print(">> handling disarm missile..")
        if match("\s*!disarm-missile\s+%s\s+%s\s*" % (escape(MISSILE_ID), escape(MISSILE_PASSWORD)), line):
            self.manager.sendLine(WIN_MSG)
            self.manager.closeConnection()
        return True

    def _handleEnterPyJail(self):
        print(">> entering in PyJail..")
        self.manager.changeHandler(PyJailHandler(self.manager))
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
