# -*- coding: utf-8 -*-
u"""Definition of :class:`.NLaunchCommFacade`."""
# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from logging import getLogger as get_logger
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class NLaunchCommFacade(object):
    u"""Facade exposing operations to communicate with the current client.

    It can be seen as the *client-communicator*.
    """

    def __init__(self, receiver):
        u"""Create a new :class:`.NLaunchCommFacade`."""
        super(NLaunchCommFacade, self).__init__()
        self.logger = get_logger("nlaunch.manager")
        self.receiver = receiver

    def send(self, s):
        u"""Send the provided string to the client.

        :param s: The string to be sent.
        :type s: str
        """
        self.receiver.transport.write(s.encode("utf8"))

    def send_line(self, s):
        u"""Send the provided line to the client.

        :param s: The line to be sent.
        :type s: str
        """
        self.receiver.send_line(s.encode("utf8"))

    def close_conn(self):
        u"""Close the connection with the current client."""
        self.receiver.transport.loseConnection()

    def get_current_handler(self):
        u"""Get the current handler.

        :returns: handlers.generic.base_handler.BaseHandler
        """
        return self.receiver.handler

    def change_handler(self, handler):
        u"""Change the current handler to the provided one.

        :param handler: The new handler.
        :type handler: handlers.generic.base_handler.BaseHandler
        """
        self.logger.info("Changing handler from '%s' to '%s'",
                         self.receiver.handler.__class__.__name__,
                         handler.__class__.__name__)
        self.receiver.handler = handler
