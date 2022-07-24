import os

ROOT_DIR = os.path.dirname(os.path.abspath('bot.py'))
FILE = ROOT_DIR + '/' + 'groups.txt'


def groups_list():
    file = 'groups.txt'
    groups_list = []

    if not os.path.exists(FILE):
        with open(file, 'w') as new:
            pass

    with open(file, 'r') as f:
        lines = f.readlines()
        for i in lines:
            groups_list.append(i.replace("\n", ""))
    return groups_list
