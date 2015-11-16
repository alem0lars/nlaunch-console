# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from re import match, escape
from textwrap import dedent

from handlers.generic.process_handler import ProcessHandler
from handlers.specific.goodbad_handler import GoodBadHandler
from misc.text import colorInfo, colorToken
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class HelloBOFHandler(ProcessHandler):

    WELCOME_MSG = dedent("""
        ------------------------------------------------------------------------

        For security reasons, the disarm functionality is, by default, disabled.

        Before going ahead, {enableDisarm}.

        You just need to solve a simple challenge to find a password
        (found inside the file '{passwordFile}') to enable disarm:

            {enableDisarmCommand}
    """).format(
        enableDisarm=colorInfo("enable the disarm functionality"),
        passwordFile=colorToken("003-password"),
        enableDisarmCommand=colorToken("!enable-disarm <PASSWORD>"))

    # Keep the following data in sync with the virtual machine containing the
    # challenge.
    VM_FILE    = "hellobof.elf"     # Path to the challenge, relative to ~
    VM_LEVEL   = "level-002"        # Associated level in the virtual machine

    """Handler for the challenge HelloBOF."""
    def __init__(self, dal, manager):
        super(HelloBOFHandler, self).__init__(dal, manager,
            ["gdb", self.VM_FILE], self.VM_LEVEL,
            welcomeMsg=self.WELCOME_MSG)

    def _shouldTerminateProcess(self, line):
        match("\s*!enable-disarm\s+%s\s*" % (escape(self.dal.getpwd(3)),), line)

    def _onProcessQuit(self):
        self.manager.changeHandler(GoodBadHandler(self.dal, self.manager))
