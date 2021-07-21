#!/usr/bin/env python3

import hashlib
import os.path
import random

def getChar():
    # figure out which function to use once, and store it in _func
    if "_func" not in getChar.__dict__:
        try:
            # for Windows-based systems
            import msvcrt # If successful, we are on Windows
            getChar._func=msvcrt.getch

        except ImportError:
            # for POSIX-based systems (with termios & tty support)
            import tty, sys, termios # raises ImportError if unsupported

            def _ttyRead():
                fd = sys.stdin.fileno()
                oldSettings = termios.tcgetattr(fd)

                try:
                    tty.setcbreak(fd)
                    answer = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

                return answer

            getChar._func=_ttyRead

    return getChar._func()

def md5dir(filename):
    m = hashlib.md5()
    if (os.path.isdir(filename)):
        for f in sorted(os.listdir(filename)):
            md5 = md5dir(filename + "/" + f)
            m.update(md5.encode('utf-8'))
    else:
        with open(filename, 'rb') as f:
            data = f.read(1048576)
            while(data):
                md5 = hashlib.md5(data).hexdigest()
                m.update(md5.encode('utf-8'))
                data = f.read(1048576)
    return m.hexdigest()

def randintodd(min, max):
    int = random.randint(min,max)
    if (int % 2) == 0:
        if (int < max): int = int + 1
        else: int = int - 1
    return int

# Split a string into a list of strings no more than <maxlength> long.
def splitstringlen(string, maxlength, expandtabs=True):
    newstrings = []
    if (expandtabs):
        string = string.replace("\t", "    ")

    for i in range(0, len(string), maxlength):
        newstrings.append(string[i:i+maxlength])
    return newstrings

def dirsize(filename):
    size = 0
    if (os.path.isdir(filename)):
        for f in os.listdir(filename):
            size += dirsize(filename + "/" + f)
    else:
        size = os.path.getsize(filename)
    return size


