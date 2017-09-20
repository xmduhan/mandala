#!/usr/bin/env python
# encoding: utf-8
import dataset
from pyfiglet import Figlet
from termcolor import cprint
from prompt_toolkit import prompt as _prompt
from prompt_toolkit.history import InMemoryHistory
from itertools import count
from treelib import Tree
from pandas import DataFrame

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
    return _prompt(text, history=history).strip()


def star(w0=None):
    """ """
    if w0 is None:
        w0 = prompt(u'关键词:')
        if len(w0) == 0:
            return
    for i in count(start=1, step=1):
        w1 = prompt(u'%s --> (%d):' % (w0, i))
        if len(w1) == 0:
            break
        save(w0, w1)


def chain(w0=None):
    """ """
    if w0 is None:
        w0 = prompt(u'关键词:')
        if len(w0) == 0:
            return
    for i in count(start=1, step=1):
        w1 = prompt(u'%s --> (%d):' % (w0, i))
        if len(w1) == 0:
            break
        save(w0, w1)
        w0 = w1


def readLevel():
    while True:
        levelString = prompt(u'最大递归级数(3):')
        if len(levelString) == 0:
            levelString = 3
        try:
            level = int(levelString)
            return level
        except Exception:
            print u'输入有误, 必须是整数!'


def lookup():
    """ """
    w0 = prompt(u'关键字:')
    level = readLevel()
    qs = db.query('select w0, w1, count(*) n from relation group by w0, w1')
    df = DataFrame(list(qs))
    tree = Tree()
    tree.create_node(w0, w0)
    appendList = []

    def append(w0, level=5):
        if w0 in appendList or level == 0:
            return
        appendList.append(w0)
        for i, row in df[df['w0'] == w0].iterrows():
            w1 = row['w1']
            n = row['n']
            # print w0, '-->', w1
            if w1 not in tree:
                title = '%s[%d]' % (w1, n)
                tree.create_node(title, w1, parent=w0)
            else:
                # 出现循环
                title = '%s[%d](*)' % (w1, n)
                tree.create_node(title, i, parent=w0)
            append(w1, level - 1)

    append(w0, level)
    tree.show()


def quit():
    """ """
    print u'再见!'
    db.rollback()
    exit()


def help():
    """ """
    print u'star: 星型添加'
    print u'chain: 链式添加'
    print u'commit: 保存'
    print u'rollback: 取消'
    print u'lookup: 查找'
    print u'quit: 退出'
    print u'help: 帮助'


commands = {
    'star': star,
    'chain': chain,
    'lookup': lookup,
    'commit': commit,
    'rollback': rollback,
    'quit': quit,
    'help': help,
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
