#!/usr/bin/env python3
#
# State machine ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ┌────────┐           ┌──────────┐              ┌─────┐
# │Decrypt │  enter    │  Unlock  │   shell      │Basic│   Enabled     ┌───────────┐
# │ Email  │──hidden ─▶│Restricted│──unlocked───▶│ BOF │───`disarm` ──▶│  GoodBad  │
# └────────┘   code    │  Shell   │              └─────┘   command     └───────────┘
#                      └──────────┘                                          │
#                                       ┌───────────────solved───────────────┘
#                                       │
#                                       ▼
#                                  ┌─────────┐
#                                  │ Victory │
#                                  └─────────┘
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import logging
from os import environ
from os.path import realpath, dirname, join, isfile
from twisted.internet import reactor
from communication.factory import NLaunchFactory
from sys import exit
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def main(port, pass_file):
    logging.basicConfig(format="%(asctime)-15s %(message)s")
    if not isfile(pass_file):
        exit(-1)
    reactor.listenTCP(int(port), NLaunchFactory(pass_file))
    reactor.run()


if __name__ == "__main__": # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    port      = environ["PORT"]
    pass_file = environ["LEVELS_PWDS"]
    main(port, pass_file)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
