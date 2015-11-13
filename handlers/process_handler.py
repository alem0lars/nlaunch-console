from pwd import getpwnam

from twisted.internet import reactor

from handlers.base_handler import BaseHandler
from subprocess_protocol import SubProcessProtocol


class ProcessHandler(BaseHandler):
    """Handler for process-based commands."""
    def __init__(self, manager, args, user, welcome_msg=None):
        super(ProcessHandler, self).__init__(manager)
        if welcome_msg:
            self.manager.sendLine(welcome_msg)
        self.process = SubProcessProtocol(self.manager)
        user_info = getpwnam(user)
        reactor.spawnProcess(self.process,
            args[0], args=args,
            path=user_info.pw_dir,
            uid=user_info.pw_uid, gid=user_info.pw_gid,
            usePTY=True)

    def handle(self, line):
        if quit_cond(line):
            # TODO: quit process and swap handler.
        else:
            self.process.sendToSubprocess(line)
        return True

    def _quit_cond(self, line):
        False
