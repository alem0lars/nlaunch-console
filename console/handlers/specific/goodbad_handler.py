# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from re import match, escape
from textwrap import dedent

from handlers.generic.process_handler import ProcessHandler
from misc.text import colorInfo, colorToken, colorSuccess
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class GoodBadHandler(ProcessHandler):

    WELCOME_MSG = dedent("""
        ------------------------------------------------------------------------

        Now you can disarm missiles, but {findPassword}..
        It can be found inside the file '{passwordFile}'.

        Then, to disarm the missile, run:

            {disarmCommand}
    """).format(
        findPassword=colorInfo("you need to find the missile password"),
        passwordFile=colorToken("004-password"),
        disarmCommand=colorToken("!disarm-missile <ID> <PASSWORD>"))

    WIN_MSG = dedent("""
        {congrats}

        You've saved the world today.. not so easy eh!?
    """).format(
        congrats=colorSuccess("Congratulations, the nuclear missile has been successfully disarmed!!"))

    # Keep the following data in sync with the virtual machine containing the
    # challenge.
    VM_FILE    = "goodbad.elf"      # Path to the challenge, relative to ~
    VM_LEVEL   = "level-003"        # Associated level in the virtual machine

    """Handler for the challenge HelloBOF."""
    def __init__(self, dal, manager):
        super(HelloBOFHandler, self).__init__(dal, manager,
            ["gdb", self.VM_FILE], self.VM_LEVEL,
            welcomeMsg=self.WELCOME_MSG)

    def _shouldTerminateProcess(self, line):
        if match("\s*!disarm-missile\s+%s\s+%s\s*" % (escape(self.ID), escape(self.dal.getpwd(4)),), line):
            self.logger.info("R E A C H E D      W I N")
            self.manager.sendLine(self.WIN_MSG)
            self.manager.closeConnection()
            return True
        return False
