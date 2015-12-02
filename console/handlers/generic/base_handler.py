"""Definition of :class:`.BaseHandler`."""
# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from logging import getLogger as get_logger
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class BaseHandler(object):
    """Root handler, parent of every handler."""

    def __init__(self, dal, com):
        """Initialize a new :class:`.BaseHandler`.

        :param dal: The data-access-layer used by the handler.
        :type  dal: misc.DAL
        :param com: The object used to communicate with the client.
        :type  com: communication.NLaunchCommFacade
        """
        super(BaseHandler, self).__init__()
        self.logger = get_logger("nlaunch.handler")
        self.dal = dal
        self.com = com
