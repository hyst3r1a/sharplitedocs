line_start_modifiers = ["private", "public", "protected", "static", "final", "abstract", "virtual", "interface",
                        "class", "enum", "struct", "namespace"]
comments = []
currentLevel = 0
currentIndex = 0
obodict = {0: 0}
tree = ""
f = open('text.cs', 'r')
a = f.readlines()
class Ns:
    def _init_(self):
        print("New namespace rdy")


def main():
    global f
    global a
    f = open('text.cs', 'r')
    a = f.readlines()
    # for b in range(len(a)):
    # print(a[b], "\n")
    flag = False
    for b in range(len(a)):
        if a[b].strip().startswith("///"):
            if b != 0 and a[b - 1].lstrip().startswith("///"):
                comments.append(a[b])
                print("COMMENT", a[b].strip())
                xml_to_html(a[b].strip())
                flag = True

        if not a[b].strip().startswith("///"):
            # this finds where the comment block ends

            if flag:
                print("END OF XML COMMENT BLOCK\n")
                flag = False
            print("Type:",obodict[currentIndex], "Index:", currentIndex, "Level:", currentLevel, "Line:", b+1)
            what_it_is(a[b].strip());
    print(obodict)
    print(tree)

# TODO: link comment blocks to closest tokens
# TODO: link tokens to their superiors(0 for superiors themselves)


def what_it_is(string):
    global currentLevel
    global currentIndex
    global tree
    # function to get the type of commented value

    if string.startswith("//"):
        print("C-Style Comment", string)
    elif string.startswith(tuple(line_start_modifiers)):

        print("Something of value:")
        splitted = string.split()
        print(splitted)
        if splitted[1] == "class":
            print("got a class\n", string)
            obodict[len(obodict)] = "class"
            currentIndex = len(obodict)-1
            tree += "  " * currentLevel + "-"
            tree += "class\n"
        elif splitted[1] == "enum":
            print("got an enum\n", string)
            obodict[len(obodict)] = "enum"
            currentIndex = len(obodict) - 1
            tree += "  " * currentLevel + "-"
            tree += "enum\n"
        elif splitted[1] == "struct":
            print("got an struct\n", string)
            obodict[len(obodict)] = "struct"
            currentIndex = len(obodict) - 1
            tree += "  " * currentLevel + "-"
            tree += "struct\n"
        elif splitted[1] == "interface" or splitted[0] == "interface":
            print("got an interface\n", string)
            obodict[len(obodict)] = "interface"
            currentIndex = len(obodict) - 1
            tree += "  " * currentLevel + "-"
            tree += "interface\n"
        elif splitted[1] == "namespace":
            print("got an namespace\n", string)
            obodict[len(obodict)] = "namespace"
            currentIndex = len(obodict) - 1
            tree += "  " * currentLevel + "-"
            tree += "namespace\n"
        else:

            if splitted[len(splitted) - 1].endswith(";"):
                print("Value found. ")
                obodict[len(obodict)] = "value"
                tree += "  " * currentLevel + "-"
                tree += "value\n"
            elif splitted[len(splitted) - 1].endswith(")") or splitted[len(splitted) - 1].endswith("{") or (
                            splitted[len(splitted) - 1].endswith(";") and "=>" in string):
                print("Method found. ")
                obodict[len(obodict)] = "method"
                currentIndex = len(obodict) - 1
                tree += "  " * currentLevel + "-"
                tree += "method\n"
    elif string.startswith("using"):
        print("Using directive", string.strip())
    # else:
        # check_value_or_method(string)

    for a in string:
        if a == "{":
            currentLevel += 1

            print("\n", "New Level", currentLevel, "\n")
        if a == "}":
            currentLevel -= 1

            print("\n", "New Level", currentLevel, "\n")
    return None


def xml_to_html(str_a):
    str_b = None
    str_d = []
    for d in range(len(str_a.split())):
        str_c = str_a.split()
        str_b = str_a.split()[d]
        for e in str_c[d]:

            if e == "<":
                str_b = insert_str(str_b, ' ', str_b.index(e))
            if e == ">":
                str_b = insert_str(str_b, ' ', str_b.index(e) + 1)
        str_d.extend(str_b.split())
    print(str_d)
    # work with str_a prepared string by taking identifiers and converting them to HTML

    html_dict = {"<summary>": "<a class=summary>", "</summary>": "</a>", "<remarks>": "<a class=remarks>", "</remarks>": "</a>",
                 "<c>": "<pre>", "</c>": "</pre>", "<code>": "<pre>", "</code>": "</pre>", "<exception>": "<a>Throws ",
                 "</exception>": "</a>", "<returns>": "<a class=returns>", "</returns>": "</a>"}
    return None


def insert_str(string, str_to_insert, index):
    return string[:index] + str_to_insert + string[index:]

main()
