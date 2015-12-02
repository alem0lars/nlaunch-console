# ☞ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from termcolor import colored
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def color_success(msg):
    return colored(msg, "green", attrs=["underline"])

def color_info(msg):
    return colored(msg, "cyan")

def color_error(msg):
    return colored(msg, "red", attrs=["underline"])

def color_token(token):
    return colored(token, "magenta", attrs=["bold"])
