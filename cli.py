import argparse
import os

import filegen
import sharplitedocs


def dir_parsing(path):
    if os.path.isdir(path):
        for filename in os.listdir(path):
            if filename.endswith(".cs"):
                print(filename)
                sharplitedocs.main(path + "/" + filename)
                print(os.path.join(filename))
                # input("Debug stop")
                filegen.generate_item(sharplitedocs.localtokens, filename, "Azure PowerShell")
                continue
            else:
                continue
    else:
        print("Not a directory")


def file_parsing(filename):
    if os.path.isfile(filename):
        if filename.endswith(".cs"):
            print(filename)
            sharplitedocs.main(filename)
            print(filename)
            # input("Debug stop")
            filegen.generate_item(sharplitedocs.localtokens, filename, "Azure PowerShell")
    else:
        print("Not a file")


def all_parsing(rootdir):
    if os.path.isdir(rootdir):
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                if file.endswith('.cs'):
                    print(os.path.join(subdir, file))
                    sharplitedocs.main(os.path.join(subdir, file))
                    print(os.path.join(subdir, file))
                    # input("Debug stop")
                    filegen.generate_item(sharplitedocs.localtokens, file, "Azure PowerShell")
    else:
        print("Not a directory")


cli_parser = argparse.ArgumentParser(description="Generate documentation for C#/.NET code")
group = cli_parser.add_mutually_exclusive_group()
group.add_argument("-f", "--file", action="store_true", help="parse file at <path>")
group.add_argument("-d", "--directory", action="store_true", help="parse all files in <path> directory")
group.add_argument("-a", "--all", action="store_true", help="parse all files and directories in <path> directory")
cli_parser.add_argument("path", help="path to files")
cli_parser.add_argument("name", help="name of documentation", nargs="?", default="Documentation")
args = cli_parser.parse_args()
if args.file:
    file_parsing(args.path)
elif args.directory:
    dir_parsing(args.path)
elif args.all:
    all_parsing(args.path)
filegen.generate_dirtree(args.path, args.name)
list_names = []
for i in sharplitedocs.tokens:
    list_names.append(str(i.tokenLocalName))
filegen.generate_index(list_names, args.name)
a = b = 0
for c in sharplitedocs.tokens:
    if c.tokenType == "class":
        a += 1
    if c.tokenType == "namespace":
        b += 1
filegen.generate_main_page(args.name, "v0.1", str(sharplitedocs.files), str(len(sharplitedocs.tokens)), str(a), str(b))
