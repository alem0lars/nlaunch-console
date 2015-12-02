# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from re import match, escape
from textwrap import dedent

from handlers.generic.gdb_handler import GDBHandler
from handlers.specific.goodbad_handler import GoodBadHandler
from misc.text import color_info, color_token, color_error
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class HelloBOFHandler(GDBHandler):

    WELCOME_MSG = dedent("""
        ------------------------------------------------------------------------
        3.
        For security reasons, the disarm functionality is, by default, disabled.

        Before going ahead, {enableDisarm}.

        You just need to solve a simple challenge to find a password
        (found inside the file '{passwordFile}') to enable disarm:

            {enableDisarmCommand}
    """).format(
        enableDisarm=color_info("enable the disarm functionality"),
        passwordFile=color_token("003-password"),
        enableDisarmCommand=color_token("!enable-disarm <PASSWORD>"))

    # Keep the following data in sync with the virtual machine containing the
    # challenge.
    VM_FILE    = "hellobof.elf"     # Path to the challenge, relative to ~
    VM_LEVEL   = "level-002"        # Associated level in the virtual machine

    """Handler for the challenge HelloBOF."""
    def __init__(self, dal, manager):
        super(HelloBOFHandler, self).__init__(dal, manager,
            self.VM_FILE, self.VM_LEVEL, self.WELCOME_MSG)
        self.win = False

    def onProcessEnded(self, status):
        self.logger.debug("HelloBOFHandler.onProcessEnded")
        if self.win:
            self.com.change_handler(GoodBadHandler(self.dal, self.com))
        else:
            self.com.change_handler(HelloBOFHandler(self.dal, self.com))

    def _should_term_proc(self, line):
        if match("\s*!enable-disarm\s+%s\s*" % (escape(self.dal.get_lvl_pwd(3)),), line):
            self.win = True
            return True
        return super(HelloBOFHandler, self)._should_term_proc(line)

    def _should_send_to_subproc(self, line):
        if match("\s*!enable-disarm", line):
            self.com.send_line(dedent("""
                {failed}

                Please check the entered password..
            """).format(failed=color_error("Failed to enable the disarm command!")))
            return False
        return super(HelloBOFHandler, self)._should_send_to_subproc(line)
