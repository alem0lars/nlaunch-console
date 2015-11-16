# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from re import match, escape
from textwrap import dedent

from handlers.generic.process_handler import ProcessHandler
from handlers.specific.hellobof_handler import HelloBOFHandler
from misc.text import colorInfo, colorToken
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class PyJailHandler(ProcessHandler):

    WELCOME_MSG = dedent("""
        To prevent unauthorized access you are now inside a restricted shell..

        If you are the right person, you already know how to bypass the
        restrictions..

        To get real access to the backdoor, you need to use the hidden password,
        found inside the file '{passwordFile}'.

        Once you've found the password, you can {unlock}, using
        the following command:

            {unlockCommand}
    """).format(
        passwordFile=colorToken("002-password"),
        unlock=colorInfo("unlock the console"),
        unlockCommand=colorToken("!unlock-console <PASSWORD>"))

    # Keep the following data in sync with the virtual machine containing the
    # challenge.
    VM_FILE    = "pyjail.py"     # Path to the challenge, relative to ~
    VM_LEVEL   = "level-001"     # Associated level in the virtual machine
    VM_PY_VERS = 3               # Python version to be used

    """Handler for the challenge PyJail."""
    def __init__(self, dal, manager):
        super(PyJailHandler, self).__init__(dal, manager,
            ["python%d" % (self.VM_PY_VERS,), self.VM_FILE], self.VM_LEVEL,
            welcomeMsg=self.WELCOME_MSG)

    def _shouldTerminateProcess(self, line):
        match("^!unlock-console\s+%s\s*" % (escape(self.dal.getpwd(2)),), line)

    def _onProcessQuit(self):
        self.manager.changeHandler(HelloBOFHandler(self.dal, self.manager))
