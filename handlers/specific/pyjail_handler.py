from handlers.generic.process_handler import ProcessHandler
from handler.specific.hellobof_handler import HelloBOFHandler

from re import match, escape


class PyJailHandler(ProcessHandler):

    WELCOME_MSG = """
        To prevent unauthorized access you are now inside a restricted shell..

        If you are the right person, you already know how to bypass the
        restrictions..

        To get real access to the backdoor, you need to use the hidden password,
        found inside the file '002-password'.

        Once you've found the password, you can *unlock the console*, using
        the following command:

            !unlock-console <PASSWORD>
    """

    # Keep the following data in sync with the virtual machine containing the
    # challenge.
    PASSWORD   = "6yfa7iRfqCQpHj5U" # Password (stored in the virtual machine)
    VM_FILE    = "pyjail.py"        # Path to the challenge, relative to ~
    VM_LEVEL   = "level-001"        # Associated level in the virtual machine
    VM_PY_VERS = 3                  # Python version to be used

    """Handler for the challenge PyJail."""
    def __init__(self, manager):
        super(PyJailHandler, self).__init__(manager,
            ["python%d" % (self.VM_PY_VERS,), self.VM_FILE], self.VM_LEVEL,
            welcome_msg=self.WELCOME_MSG)

    def _quit_cond(self, line):
        match("^!unlock-console\s+%s\s*" % (escape(self.PASSWORD),), line)

    def _onProcessQuit(self):
        self.manager.changeHandler(HelloBOFHandler(self.manager))
