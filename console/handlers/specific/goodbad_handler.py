# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from re import match, escape
from textwrap import dedent

from handlers.generic.gdb_handler import GDBHandler
from misc.text import color_info, color_token, color_success, color_error
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class GoodBadHandler(GDBHandler):

    WELCOME_MSG = dedent("""
        ------------------------------------------------------------------------
        4.
        Now you can disarm missiles, but {findPassword}..
        It can be found inside the file '{passwordFile}'.

        Then, to disarm the missile, run:

            {disarmCommand}
    """).format(
        findPassword=color_info("you need to find the missile password"),
        passwordFile=color_token("004-password"),
        disarmCommand=color_token("!disarm-missile <ID> <PASSWORD>"))

    WIN_MSG = dedent("""
        {congrats}

        You've saved the world today.. it's not so easy eh!?
    """).format(
        congrats=color_success("Congratulations, the nuclear missile has been successfully disarmed!!"))

    # Keep the following data in sync with the virtual machine containing the
    # challenge.
    VM_FILE    = "goodbad.elf"      # Path to the challenge, relative to ~
    VM_LEVEL   = "level-003"        # Associated level in the virtual machine

    ID = "K0R34N-B00B135"

    """Handler for the challenge HelloBOF."""
    def __init__(self, dal, manager):
        super(GoodBadHandler, self).__init__(dal, manager,
            self.VM_FILE, self.VM_LEVEL, self.WELCOME_MSG)
        self.win = False

    def onProcessEnded(self, status):
        if self.win:
            self.com.close_conn()
        else:
            self.com.change_handler(GoodBadHandler(self.dal, self.com))

    def _should_term_proc(self, line):
        if match("\s*!disarm-missile\s+%s\s+%s\s*" % (escape(self.ID), escape(self.dal.get_lvl_pwd(4)),), line):
            self.logger.info("R E A C H E D   W I N")
            self.com.send_line(self.WIN_MSG)
            self.win = True
            return True
        return super(GoodBadHandler, self)._should_term_proc(line)

    def _should_send_to_subproc(self, line):
        if match("\s*!disarm-missile", line):
            self.com.send_line(dedent("""
                {failed}

                Please check the entered ID and/or password..
            """).format(failed=color_error("Failed to disarm missile!")))
            return False
        return super(GoodBadHandler, self)._should_send_to_subproc(line)
