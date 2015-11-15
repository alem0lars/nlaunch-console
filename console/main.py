#!/usr/bin/env python3
#
# State machine:
#
# ┌────┐      enter       ┌──────────┐               ┌───────────┐               ┌───────────┐
# │INIT│──────pyjail ────▶│  PyJail  │────solved────▶│ HelloBOF  │────solved────▶│  GoodBad  │
# └────┘     command      └──────────┘               └───────────┘               └───────────┘
#                                                                                      │
#                                        ┌────────────────────solved───────────────────┘
#                                        │
#                                        ▼
#                                   ┌─────────┐
#                                   │ Victory │
#                                   └─────────┘

from os import environ
from twisted.internet import reactor
from communication.factory import NLaunchFactory


reactor.listenTCP(int(environ["PORT"]), NLaunchFactory())
reactor.run()
