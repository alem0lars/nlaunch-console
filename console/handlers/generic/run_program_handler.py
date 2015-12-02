# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from pwd import getpwnam

from twisted.internet import reactor

from handlers.generic.process_handler import ProcessHandler
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class RunProgramHandler(ProcessHandler):
    """Handler for run-program command."""
    def __init__(self, dal, manager, args, user, nextHandler, welcomeMsg=None):
        super(RunProgramHandler, self).__init__(dal, manager, args, user, welcomeMsg)
        self.nextHandler = nextHandler

    def onProcessEnded(self, status):
        self.com.change_handler(self.nextHandler)
