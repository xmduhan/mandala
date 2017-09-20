#!/usr/bin/env python
# encoding: utf-8
from prompt_toolkit import prompt as _prompt
from prompt_toolkit.history import InMemoryHistory

history = InMemoryHistory()


def prompt(text):
    return _prompt(text, history=history)


def hfeed():
    """ """
    print u'hfeed'


def quit():
    print u'再见!'
    exit()


commands = {
    'hfeed': hfeed,
    'quit': quit,
}


def main():
    """ """
    while True:
        cmd = prompt(u'mandala>')
        if cmd in commands:
            commands[cmd]()
        else:
            print u'无效命令'


if __name__ == "__main__":
    main()
