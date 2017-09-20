#!/usr/bin/env python
# encoding: utf-8
import dataset
from pyfiglet import Figlet
from termcolor import cprint
from prompt_toolkit import prompt as _prompt
from prompt_toolkit.history import InMemoryHistory
from itertools import count

history = InMemoryHistory()
db = dataset.connect('sqlite:///db.sqlite')
table = db['relation']
db.begin()


def commit():
    """ """
    db.commit()
    db.begin()
    print u'保存成功!'


def rollback():
    """ """
    db.rollback()
    db.begin()
    print u'操作撤销'


def save(w0, w1):
    """ """
    table.insert({'w0': w0, 'w1': w1})
    # print u'%s --> %s: ' % (w0, w1)
    cprint('  |-- ', 'green', end='')
    cprint('%s --> %s: ' % (w0, w1), color='blue', end='')
    cprint('+1', 'red')


def prompt(text):
    return _prompt(text, history=history)


def hfeed(w0=None):
    """ """
    if w0 is None:
        w0 = prompt(u'关键词:')
        w0 = w0.strip()
        if len(w0) == 0:
            return
    for i in count(start=1, step=1):
        w1 = prompt(u'%s --> (%d):' % (w0, i))
        if len(w1) == 0:
            break
        save(w0, w1)


def vfeed(w0=None):
    """ """
    if w0 is None:
        w0 = prompt(u'关键词:')
        w0 = w0.strip()
        if len(w0) == 0:
            return
    for i in count(start=1, step=1):
        w1 = prompt(u'%s --> (%d):' % (w0, i))
        if len(w1) == 0:
            break
        save(w0, w1)
        w0 = w1


def lookup():
    """ """
    pass


def quit():
    print u'再见!'
    db.rollback()
    exit()


commands = {
    'hfeed': hfeed,
    'vfeed': vfeed,
    'lookup': lookup,
    'commit': commit,
    'rollback': rollback,
    'quit': quit,
}


def main():
    """ """
    # 打印logo
    f = Figlet(font='slant')
    print f.renderText('Mandala')

    # 读取并执行命令
    try:
        while True:
            cmd = prompt(u'mandala>')
            if cmd in commands:
                commands[cmd]()
            else:
                print u'无效命令'
    except KeyboardInterrupt:
        quit()


if __name__ == "__main__":
    main()
