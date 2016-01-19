# -*- coding: utf-8 -*-
"""Define common text utilities."""
# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import termcolor
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def color_success(msg):
    """Color the provided string as a success message.

    :param msg: The string to be colored.
    :type msg: str
    """
    return termcolor.colored(msg, "green", attrs=["underline"])


def color_info(msg):
    """Color the provided string as an informative message.

    :param msg: The string to be colored.
    :type msg: str
    """
    return termcolor.colored(msg, "cyan")


def color_error(msg):
    """Color the provided string as an error message.

    :param msg: The string to be colored.
    :type msg: str
    """
    return termcolor.colored(msg, "red", attrs=["underline"])


def color_token(token):
    """Color the provided string as a token.

    :param token: The string to be colored.
    :type token: str
    """
    return termcolor.colored(token, "magenta", attrs=["bold"])
