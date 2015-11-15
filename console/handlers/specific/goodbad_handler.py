# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from re import match, escape
from textwrap import dedent

from handlers.generic.process_handler import ProcessHandler
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class GoodBadHandler(ProcessHandler):

    WELCOME_MSG = dedent("""
        Now you can disarm missiles, but you need to find the missile password..

        Then, to disarm the missile, run:

            !disarm-missile <ID> <PASSWORD>
    """)

    WIN_MSG = dedent("""
        Congratulations, the nuclear missile has been successfully disarmed!!

        You've saved the world today.. not so easy eh!?
    """)

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
        if match("^!disarm-missile\s+%s\s+%s\s*" % (escape(self.ID), escape(self.dal.getpwd(4)),), line):
            self.logger.info("Reached win")
            self.manager.sendLine(self.WIN_MSG)
            self.manager.closeConnection()
            return True
        return False
