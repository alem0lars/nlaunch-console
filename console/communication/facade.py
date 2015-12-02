# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from logging import getLogger as get_logger
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class NLaunchCommFacade(object):
    """Facade exposing operations to communicate with the current client.

    It can be seen as the *client-communicator*.
    """

    def __init__(self, receiver):
        super(NLaunchCommFacade, self).__init__()
        self.logger = get_logger("nlaunch.manager")
        self.receiver = receiver

    def send(self, s):
        self.receiver.transport.write(s.encode("utf8"))

    def send_line(self, s):
        """Send the provided line to the client.

        :param s: The line to be sent.
        :type s: str
        """
        self.receiver.send_line(s.encode("utf8"))

    def close_conn(self):
        """Close the connection with the current client."""
        self.receiver.transport.loseConnection()

    def get_current_handler(self):
        """Get the current handler.

        :returns: BaseHandler
        """
        return self.receiver.handler

    def change_handler(self, handler):
        self.logger.info("Changing handler from '{prev}' to '{next}'".format(
            prev=self.receiver.handler.__class__.__name__,
            next=handler.__class__.__name__))
        self.receiver.handler = handler
