# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from pwd import getpwnam

from twisted.internet import reactor

from handlers.generic.base_handler import BaseHandler
from misc.subprocess_protocol import SubProcessProtocol
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class ProcessHandler(BaseHandler):
    """Handler for process-based commands."""
    def __init__(self, dal, manager, args, user, welcomeMsg=None):
        super(ProcessHandler, self).__init__(dal, manager)
        if welcomeMsg:
            self.manager.sendLine(welcomeMsg)
        self.process = SubProcessProtocol(self.manager)
        self.finished = False
        user_info = getpwnam(user)
        reactor.spawnProcess(self.process,
            args[0], args=args,
            path=user_info.pw_dir,
            uid=user_info.pw_uid, gid=user_info.pw_gid,
            usePTY=True)
        self.logger.info("Started process (program='{program}', args='{args}', uid='{uid}', gid='{gid}')".format(
            program=args[0], args=args[1:],
            uid=user_info.pw_uid, gid=user_info.pw_gid))

    def handle(self, line):
        if self._shouldTerminateProcess(line):
            self.finished = True

        if self.finished:
            self.logger.info("Terminating current process")
            self.process.transport.signalProcess("KILL")
            self._onProcessQuit()
        elif self._shouldSendToSubprocess(line):
            self.process.sendToSubprocess(line)

        return True

    def _shouldTerminateProcess(self, line):
        False

    def _onProcessQuit(self, line):
        !self._shouldTerminateProcess(line)
