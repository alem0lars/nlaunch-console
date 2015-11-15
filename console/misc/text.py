from io import StringIO
from textwrap import dedent

import couleur

def formatMsg(msg):
    s = StringIO()
    couleur.proxy(s).enable()
    s.write(dedent(msg))
    couleur.proxy(s).disable()
    res = s.getvalue()
    s.close()
    return res
