# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from re import match, escape
from textwrap import dedent

from handlers.generic.process_handler import ProcessHandler
from handlers.specific.hellobof_handler import HelloBOFHandler
from misc.text import color_info, color_token, color_error
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class PyJailHandler(ProcessHandler):

    WELCOME_MSG = dedent("""
        ------------------------------------------------------------------------
        2.
        To prevent unauthorized access you are now inside a restricted shell..

        If you are the right person, you already know how to bypass the
        restrictions..

        To get real access to the backdoor, you need to use the hidden password,
        found inside the file '{pwd_name}'.

        Once you've found the password, you can {unlock}, using the following
        command:

            {cmd_unlock}
    """).format(
        pwd_name=color_token("002-password"),
        unlock=color_info("unlock the console"),
        cmd_unlock=color_token("!unlock-console <PASSWORD>"))

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
        self.win = False

    def onProcessEnded(self, status):
        if self.win:
            self.com.change_handler(HelloBOFHandler(self.dal, self.com))
        else:
            self.com.change_handler(PyJailHandler(self.dal, self.com))

    def _should_term_proc(self, line):
        if match("\s*!unlock-console\s+%s\s*" % (escape(self.dal.get_lvl_pwd(2)),), line):
            self.win = True
            return True
        return super(PyJailHandler, self)._should_term_proc(line)

    def _should_send_to_subproc(self, line):
        if match("\s*!unlock-console", line):
            self.com.send_line(dedent("""
                {failed}

                Please check the entered password..
            """).format(failed=color_error("Failed to unlock the console!")))
            return False
        return super(PyJailHandler, self)._should_send_to_subproc(line)
