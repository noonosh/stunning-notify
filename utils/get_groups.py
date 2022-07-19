import os


def get_groups(file):
    if not os.path.exists(file):
        return 1
    groups_list = []
    with open(file, 'r') as f:
        lines = f.readlines()
        for i in lines:
            groups_list.append(int(i.replace("\n", "")))
    return groups_list
