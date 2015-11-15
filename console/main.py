# State machine:
#
# ┌────┐      enter       ┌──────────┐    pyjail     ┌───────────┐     bin1      ┌───────────┐
# │INIT│──────pyjail ────▶│  PyJail  │────solved────▶│   Bin1    │────solved────▶│   Bin2    │
# └────┘     command      └──────────┘               └───────────┘               └───────────┘
#    ▲                                                                                 │
#    │                                  bin2                                           │
#    └──────────────────────────────── solved ─────────────────────────────────────────┘


from os import environ
from twisted.internet import reactor
from communication.factory import NLaunchFactory


reactor.listenTCP(int(environ["PORT"]), NLaunchFactory())
reactor.run()
