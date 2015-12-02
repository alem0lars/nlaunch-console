# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from re import match, escape

from textwrap import dedent
from termcolor import colored

from handlers.generic.base_handler import BaseHandler
from handlers.specific.pyjail_handler import PyJailHandler
from misc.text import color_info, color_token, color_error
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class InitialHandler(BaseHandler):

    HELP_MSG = dedent("""
        ------------------------------------------------------------------------
        1.
        The following commands are available:

            {cmd_history}
            {cmd_launch}
    """).format(
        cmd_history=color_token("!history"),
        cmd_launch=color_token("!launch-missile <ID> <TARGET> <PASSWORD>"))

    MISSILE_ID       = "K0R34N-B00B135"
    MISSILE_TARGET   = ", ".join([
        "39°02'24.1\"N 125°45'50.7\"E - Rungna People's Pleasure Ground",
        "Pyongyang (평양시)",
        "North Korea"
    ])

    """Handler for the initial commands."""
    def __init__(self, dal, manager):
        super(InitialHandler, self).__init__(dal, manager)
        self.history = []
        self._add_cmd_to_history("launch-missile", {
            "id":     self.MISSILE_ID,
            "target": self.MISSILE_TARGET
        })

    def handle(self, line):
        if match("\s*!help\s*", line):
            return self._handleHelp()
        elif match("\s*!history\s*", line):
            return self._handle_history()
        elif match("\s*!launch-missile\s*", line):
            return self._handle_launch_missile()
        elif line == self.dal.get_lvl_pwd(1):
            return self._handle_enter_pyjail()
        else:
            return False

    # Handlers ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _handleHelp(self):
        self.logger.info("Handling command 'help'")
        self.com.send_line(self.HELP_MSG)
        return True

    def _handle_history(self):
        self.logger.info("Handling command 'history'")
        self.com.send_line(dedent("""
            The commands that have already been carried out are:

            {commands}
        """).format(commands="".join(self.history)))
        return True

    def _handle_launch_missile(self):
        self.logger.info("Handling command 'launch-missile'")
        self.com.send_line(dedent("""
            Error: {launched}
        """).format(
            launched=color_error("Another missile has already been launched!")))
        return True

    def _handle_enter_pyjail(self):
        self.logger.info("Entering in PyJail")
        self.com.change_handler(PyJailHandler(self.dal, self.com))
        return True

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _add_cmd_to_history(self, name, info):
        elem = "Command: '%s'" % (colored(name, "magenta"),)
        if len(info) > 0:
            elem += " ( "
            for (k,v) in info.items():
                elem += "%s: %s, " % (colored(k, "blue"), colored(v, "green"))
            elem += " )"
        self.history.append(elem)
