# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from re import match, escape
from textwrap import dedent

from handlers.generic.run_program_handler import RunProgramHandler
from handlers.generic.process_handler import ProcessHandler
from misc.text import colorInfo, colorToken, colorError
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class GDBHandler(ProcessHandler):

    WELCOME_MSG_SUFFIX = dedent("""
        To run the program in standalone mode (i.e. without gdb), run:

            {runCommand}
    """).format(
        runCommand=colorToken("!run-program <ARGS>"))

    """Handler for a GDB-based challenge."""
    def __init__(self, dal, manager, binary, user, welcomeMsg=None):
        super(GDBHandler, self).__init__(dal, manager,
            ["gdb",
             "-q",
             "-iex",
             "set auto-load safe-path /home/{level}".format(level=user),
             binary],
            user,
            welcomeMsg="{welcome}\n{suffix}".format(
                welcome=welcomeMsg,
                suffix=self.WELCOME_MSG_SUFFIX))
        self.binary = binary
        self.user = user

    def _shouldSendToSubprocess(self, line):
        if match("\s*!run-program\s*", line):
            m = re.findall("\s*!run-program(?:\s+(.+))?", line)
            suffix = m[0]
            self.logger.debug("Suffix: %s" % suffix)
            args = " ".split(suffix).unshift(self.binary)
            self.manager.changeHandler(
                RunProgramHandler(dal, manager, args, self.user,
                    self)) # Return to this handler after program termination.
            return False
        return super(GDBHandler, self)._shouldSendToSubprocess(line)
