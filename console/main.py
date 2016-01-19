#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""NLaunch console entry point.

.. code-block::

    ┌────────┐           ┌──────────┐              ┌─────┐
    │Decrypt │  enter    │  Unlock  │   shell      │Basic│
    │ Email  │──hidden ─▶│Restricted│──unlocked───▶│ BOF │
    └────────┘   code    │  Shell   │              └─────┘
                         └──────────┘                 │
                                                   Enabled
                                                   `disarm`
                                                   command
                                                      │
                                                      ▼
                         ┌─────────┐   Disarm   ┌───────────┐
                         │ Victory │◀────the ───│  GoodBad  │
                         └─────────┘   missile  └───────────┘
"""
# ☞ Check Python interpreter ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from sys import version_info, exit

PYTHON_MIN_VERSION = (3, 5)

if version_info < PYTHON_MIN_VERSION:
    print("Python version >= {}.{} required!".format(*PYTHON_MIN_VERSION))
    exit(-1)
# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import logging

from os import environ, geteuid
from os.path import realpath, dirname, join, isfile

from colorlog import ColoredFormatter
from twisted.internet import reactor

from communication.factory import NLaunchFactory
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class Main(object):

    STATUSCODE_PERMS_DENIED = -1
    STATUSCODE_INVALID_ARGS = -2

    """The entry-point of NLaunch Console."""
    def __init__(self, port, pwd_path):
        super(Main, self).__init__()
        self._configureLogging()
        # Check if we are 'root':
        if not geteuid() == 0:
            self.logger.error("Root permissions are required")
            exit(self.STATUSCODE_PERMS_DENIED)
        # Check argument: 'pwd_path'
        if isfile(pwd_path):
            self.pwd_path = pwd_path
        else:
            self.logger.error(
                "Invalid password file '%s': it's not a regular file" %
                (pwd_path,))
            exit(self.STATUSCODE_INVALID_ARGS)
        # Check argument: 'port'
        try:
            self.port = int(port)
        except Exception as e:
            self.logger.error("Invalid port '%s': %s" % (port, e))
            exit(self.STATUSCODE_INVALID_ARGS)

    def start(self):
        """Start the NLaunch Console."""
        self.logger.info("Starting NLaunch Console " +
                         "(port='{port}', pwd_path='{pwd_path}')".format(
                            port=self.port, pwd_path=self.pwd_path))
        reactor.listenTCP(self.port, NLaunchFactory(self.pwd_path))
        reactor.run()

    def _configureLogging(self):
        loggingHandler = logging.StreamHandler()
        # Set colored formatter (using package 'colorlog')
        loggingHandler.setFormatter(ColoredFormatter(
                "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
                datefmt=None,
                reset=True,
                log_colors={
                    "DEBUG":    "cyan",
                    "INFO":     "green",
                    "WARNING":  "yellow",
                    "ERROR":    "red",
                    "CRITICAL": "red,bg_white",
                },
                secondary_log_colors={},
                style='%'
        ))
        self.logger = logging.getLogger("nlaunch")
        # Set minimum allowed logging level
        self.logger.setLevel(logging.DEBUG)
        # Add the handler to the root logger
        self.logger.addHandler(loggingHandler)


if __name__ == "__main__":  # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Main(environ["PORT"], environ["LEVELS_PWDS"]).start()
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
