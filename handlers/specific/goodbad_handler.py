from handlers.generic.process_handler import ProcessHandler

from re import match, escape


class GoodBadHandler(GDBHandler):

    WELCOME_MSG = """
        Now you can disarm missiles, but you need to find the missile password..

        Then, to disarm the missile, run:

            !disarm-missile <ID> <PASSWORD>
    """

    WIN_MSG = """
        Congratulations, the nuclear missile has been successfully disarmed!!

        You've saved the world today.. not so easy eh!?
    """

    # Keep the following data in sync with the virtual machine containing the
    # challenge.
    PASSWORD   = "5a6Kw1WURKClBeZI" # Password (stored in the virtual machine)
    VM_FILE    = "goodbad.elf"      # Path to the challenge, relative to ~
    VM_LEVEL   = "level-003"        # Associated level in the virtual machine

    """Handler for the challenge HelloBOF."""
    def __init__(self, manager):
        super(HelloBOFHandler, self).__init__(manager,
            ["gdb", self.VM_FILE], self.VM_LEVEL,
            welcome_msg=self.WELCOME_MSG)

    def _quit_cond(self, line):
        if match("^!disarm-missile\s+%s\s+%s\s*" % (escape(self.ID), escape(self.PASSWORD),), line):
            self.manager.sendLine(WIN_MSG)
            self.manager.closeConnection()
            return True
        return False
