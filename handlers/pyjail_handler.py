from handlers.process_handler import ProcessHandler


PYJAIL_WELCOME_MSG = """
To prevent unauthorized access you are now inside a restricted shell..
If you are the right person, you already know how to bypass the restrictions..

To get real access to the backdoor, you need to use the hidden password, found
inside the file '002-password'
"""


class PyJailHandler(ProcessHandler):
    """Handler for PyJail commands."""
    def __init__(self, manager):
        super(PyJailHandler, self).__init__(manager,
            ["python", "pyjail.py"], "level-001",
            welcome_msg=PYJAIL_WELCOME_MSG)
