# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from termcolor import colored
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def colorSuccess(msg):
    return colored(msg, "green", attrs=["underline"])

def colorInfo(msg):
    return colored(msg, "cyan")

def colorError(msg):
    return colored(msg, "red", attrs=["underline"])

def colorToken(token):
    return colored(token, "magenta", attrs=["bold"])
