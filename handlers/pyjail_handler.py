from handlers.base_handler import BaseHandler
from twisted.internet import reactor
from subprocess_protocol import SubProcessProtocol


class PyJailHandler(BaseHandler):
    """Handler for PyJail commands."""
    def __init__(self, manager):
        super(PyJailHandler, self).__init__(manager)
        self.process = SubProcessProtocol(self.manager)
        reactor.spawnProcess(self.process, "python", ["python", "challenges/pyjail.py"], {}, usePTY=True)

    def handle(self, line):
        self.process.sendToSubprocess(line)
        return True
