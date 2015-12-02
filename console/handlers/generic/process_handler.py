# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from logging import getLogger
from pwd import getpwnam

from twisted.internet import reactor
from twisted.internet.protocol import ProcessProtocol

from handlers.generic.base_handler import BaseHandler
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class ProcessHandler(BaseHandler):
    """Handler for process-based commands."""
    def __init__(self, dal, manager, args, user, welcomeMsg=None):
        super(ProcessHandler, self).__init__(dal, manager)
        if welcomeMsg:
            self.com.send_line(welcomeMsg)
        self.process = SubProcessProtocol(self.com)
        user_info = getpwnam(user)
        self.uid = user_info.pw_uid
        self.gid = user_info.pw_gid
        self.current_dir = user_info.pw_dir
        self.finished = False
        reactor.spawnProcess(self.process,
            args[0], args=args,
            path=self.current_dir,
            uid=self.uid, gid=self.gid,
            usePTY=True)
        self.logger.info("Started process (program='{program}', args='{args}', uid='{uid}', gid='{gid}')".format(
            program=args[0], args=args[1:],
            uid=user_info.pw_uid, gid=user_info.pw_gid))

    def handle(self, line):
        if not self.finished and self._should_term_proc(line):
            self.logger.info("Terminating current process")
            self.finished = True

        if self.finished:
            self.process.transport.signalProcess("KILL")
        elif self._should_send_to_subproc(line):
            self.process.sendToSubprocess(line)

        return True

    def _should_send_to_subproc(self, line):
        return True

    def _should_term_proc(self, line):
        return False

    def onProcessEnded(self, status):
        pass

class SubProcessProtocol(ProcessProtocol):
    """Protocol managing interaction with a sub-process."""
    def __init__(self, manager):
        super(SubProcessProtocol, self).__init__()
        self.logger = getLogger("nlaunch.subprocess")
        self.com = manager

    def errReceived(self, data):
        self.logger.debug(data.decode("utf8"))

    def outReceived(self, data):
        self.logger.debug("Received '%s' from subprocess" % (data,))
        self.com.send(data.decode("utf8"))

    def processEnded(self, status):
        self._notifyProcessEnded(status)

    def sendToSubprocess(self, s):
        self.logger.debug("Sending '%s' to subprocess" % (s,))
        self.transport.write(("%s\n" % (s,)).encode("utf8"))

    def _notifyProcessEnded(self, status):
        try:
            if callable(self.com.get_current_handler().onProcessEnded):
                self.logger.debug("Process ended. Notifying the handler")
                self.com.get_current_handler().onProcessEnded(status)
        except AttributeError as e:
            self.logger.debug(
                "Handler '{handler}' doesn't respond to event 'process ended'".format(
                    handler=self.com.get_current_handler().__class__.__name__))
