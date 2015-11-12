from sys import stdout, stderr


def log(msg):
    print >>stderr, msg

def send(s):
    log("sending %s" % (s,))
    print >>stdout, s


if __name__ == "__main__":
    while (True):
        line = raw_input("PyJail> ")
        send("Inserted %s" % (line,))
