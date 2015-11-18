# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from ast import literal_eval
from re import match, escape, findall
from os import seteuid, setegid
from textwrap import dedent

from handlers.generic.run_program_handler import RunProgramHandler
from handlers.generic.process_handler import ProcessHandler
from misc.text import colorInfo, colorToken, colorError
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class GDBHandler(ProcessHandler):

    WELCOME_MSG_SUFFIX = dedent("""
        You can pass plain arguments or a python literal string to be evaluated.
        To do that, encapsulate the literal between curly brackets.
        For example:

            {argCmdExample}

        To run the program in standalone mode (i.e. without GDB), run:

            {runCommand}
    """).format(
        argCmdExample=colorInfo('{"AAAAAAAAAAAA\\xef\\xbe\\xad\\xde"}'),
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
            m = findall("\s*!run-program(?:\s+(.+))?", line)
            suffix = m[0]
            self.logger.debug("Suffix: '%s'" % suffix)
            args = self._buildArgs(suffix)
            args.insert(0, self.binary)
            self.manager.changeHandler(
                RunProgramHandler(self.dal, self.manager, args, self.user,
                    self)) # Return to this handler after program termination.
            return False
        return super(GDBHandler, self)._shouldSendToSubprocess(line)

    def _buildArgs(self, argsStr):
        args = None

        matches = findall(r'\{([^\}]+)\}', argsStr)
        if len(matches) > 0:
            # THIS FUCKING LINE WASTED 8 OF MY HOURS!!!
            # IF YOU FUCKING DELETE IT, I WILL FUCKING BURN YOU IN THE HELL
            args = [literal_eval(matches[0]).encode("latin1")]
        else:
            args = argsStr.split(" ")

        return args
