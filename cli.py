import argparse
import errno
import os

from pyfiglet import Figlet

import filegen
import sharplitedocs


def dir_parsing(path, destination, name):
    if os.path.isdir(path):
        for filename in os.listdir(path):
            if filename.endswith(".cs"):
                #print(filename)
                sharplitedocs.main(path + "/" + filename)
                #print(os.path.join(filename))
                # input("Debug stop")
                filegen.generate_item(sharplitedocs.localtokens, filename, name, destination)
                continue

            else:
                continue
    else:
        print("Not a directory")


def file_parsing(filename, destination, name):
    if os.path.isfile(filename):
        if filename.endswith(".cs"):
            #print(filename)
            sharplitedocs.main(filename)
            #print(filename)
            # input("Debug stop")
            filegen.generate_item(sharplitedocs.localtokens, filename, name, destination)
    else:
        print("Not a file")


def all_parsing(rootdir, destination, name):
    if os.path.isdir(rootdir):
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                if file.endswith('.cs') and not file.endswith('.bindings.cs'):
                    print(os.path.join(subdir, file))
                    sharplitedocs.main(os.path.join(subdir, file))
                    #print(os.path.join(subdir, file))
                    # input("Debug stop")
                    filegen.generate_item(sharplitedocs.localtokens, file, name, destination)
    else:
        print("Not a directory")


cli_parser = argparse.ArgumentParser(description="Generate documentation for C#/.NET code")
group = cli_parser.add_mutually_exclusive_group()
group.add_argument("-f", "--file", action="store_true", help="parse file at <path>")
group.add_argument("-d", "--directory", action="store_true", help="parse all files in <path> directory")
group.add_argument("-a", "--all", action="store_true", help="parse all files and directories in <path> directory")
cli_parser.add_argument("path", help="path to files")
cli_parser.add_argument("name", help="name of documentation", nargs="?", default="Documentation")
cli_parser.add_argument("destination", help="path to output", nargs="?", default="1/")
args = cli_parser.parse_args()
custom_fig = Figlet(font='ogre')
print(custom_fig.renderText('Hyst3r1a'))
print("\n Sharp Lite Docs - a C# Documentation Generator")
print("\n Michael Gorshenin, 2019\n\n")
if not os.path.exists(os.path.dirname(args.destination + "kek.html")):
    try:
        os.makedirs(os.path.dirname(args.destination+"kek.html"))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
if not os.path.exists(os.path.dirname(args.destination + "/items/kek.html")):
    try:
        os.makedirs(os.path.dirname(args.destination+"/items/kek.html"))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
if args.file:
    file_parsing(args.path, args.destination, args.name)
elif args.directory:
    dir_parsing(args.path, args.destination, args.name)
elif args.all:
    all_parsing(args.path, args.destination, args.name)
filegen.generate_dirtree(args.path, args.name, args.destination)
list_names = []
a = b = 0
for c in sharplitedocs.tokens:
    if c.tokenType == "class":
        a += 1
    if c.tokenType == "namespace":
        b += 1
filegen.generate_main_page(args.name, "v0.1", str(sharplitedocs.files), str(len(sharplitedocs.tokens)), str(a), str(b), args.destination)

for i in sharplitedocs.tokens:
    list_names.append(str(i.tokenLocalName))
filegen.generate_index(list_names, args.name, args.destination)
