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
from os.path import realpath, dirname, join
from twisted.internet import reactor
from communication.factory import NLaunchFactory


def main(port, data_dir):
    reactor.listenTCP(port, NLaunchFactory(data_dir))
    reactor.run()


if __name__ == "__main__":
    port     = int(environ["PORT"])
    data_dir = join(dirname(dirname(realpath(__file__))), "data")
    main()
