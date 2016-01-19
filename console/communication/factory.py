# -*- coding: utf-8 -*-
"""Definition of :class:`.NLaunchFactory`."""
# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import twisted.internet.protocol

import communication.receiver
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class NLaunchFactory(twisted.internet.protocol.Factory):
    u"""Factory used by the twisted reactor to handle clients.

    Create a new :class:`.NLaunchReceiver` for every client.
    """

    def __init__(self, pwd_path):
        u"""Create a new :class:`.NLaunchFactory`."""
        super(NLaunchFactory, self).__init__()
        self.pwd_path = pwd_path

    def buildProtocol(self, addr):
        return communication.receiver.NLaunchReceiver(self.pwd_path)
