import os

import filegen
import sharplitedocs


def main():
    file_iteration()


def file_iteration(rootdir=r'/Users/mihailgorsenin/Desktop/src/Accounts'):
    count = 0
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith(".cs"):
                print(os.path.join(subdir, file))
                sharplitedocs.main(os.path.join(subdir, file))
                filegen.generate_item(sharplitedocs.localtokens, file, "Azure PowerShell")
    filegen.generate_dirtree(rootdir)
    list_names = []
    for i in sharplitedocs.tokens:
        list_names.append(str(i.tokenLocalName))
    filegen.generate_index(list_names)


main()
