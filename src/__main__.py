import sys
from __init__ import Bot

MESSAGE_USAGE = "Usage is python %s [name] [token]"

if __name__ == "__main__":
    if len(sys.argv) == 3:
        Bot(sys.argv[1], sys.argv[2])
    else:
        print(MESSAGE_USAGE.format(sys.argv[0]))
