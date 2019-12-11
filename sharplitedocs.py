import itertools
import sys
import threading
import time


line_start_modifiers = ["private", "public", "protected", "static", "final", "abstract", "virtual", "interface",
                        "class", "enum", "struct", "namespace"]
comments = []
currentLevel = 0
currentIndex = 0
obodict = {0: 0}
hierarchy = []
tree = ""
done = False
tokens = []
localtokens = []
files = 0
filename  = ""


class Token:
    tokenType = ""
    tokenNum = 0
    tokenSpecials = []
    tokenLocalName = None
    superToken = 0
    tokenCommons = []
    tokenComments = []
    tokenFile = ""
    f = ""
    def __init__(self):
        self.tokenComments = list()


def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rprocessing ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    #sys.stdout.write('\rDone!     ')


# TODO: link comment blocks to closest tokens
# TODO: link tokens to their superiors(0 for superiors themselves)


def start_parse(filestring):
    global f
    global a
    global done
    global files
    f = open(filestring, 'r')
    try:
        a = f.readlines()
    except UnicodeDecodeError:
        print("Corrupted file.")
        return
    flag = False
    for b in range(len(a)):
        # time.sleep(0.15)
        # #  print(a[b])
        if a[b].strip().startswith("///"):
            comments.append(a[b].strip())
            #  print("COMMENT", a[b].strip())
            if b != 0 and a[b - 1].lstrip().startswith("///"):
                # #  print("COMMENT", a[b].strip())
                # comments.append(a[b].strip())
                #  print("MISHON", comments)
                flag = True

        if not a[b].strip().startswith("///"):
            # this finds where the comment block ends
            if flag:
                #  print("END OF XML COMMENT BLOCK\n")
                flag = False
            #  print("Type:", obodict[currentIndex], "Index:", currentIndex, "Level:", currentLevel, "Line:", b + 1,
                 # "Current super:", hierarchy[len(hierarchy) - 1] if len(hierarchy) > 0 else 0)
            what_it_is(a[b].strip())
            comments.clear()

    #  print(obodict)
    #  print(tree)
     #for a in tokens:
        #  print(a.tokenType, " ", a.tokenLocalName, " ", a.superToken, " ", a.tokenNum)
    #  print("\n")
    #temporary_dox()
    done = True


def find_usages(token):
    strings_using = " "
    str_py = token.tokenLocalName.split()
    if len(str_py)>1:
        lookup = token.tokenLocalName.split()[1]
    else:
        return "-"
    for num, line in enumerate(f, 1):
        if lookup in line:
            print('found at line:', num)
    return strings_using

def what_it_is(string):
    global currentLevel
    global currentIndex
    global tree
    global filename
    currentSuper = hierarchy[len(hierarchy) - 1] if len(hierarchy) > 0 else 0
    # function to get the type of commented value

    if string.startswith("//"):
         #print("C-Style Comment", string)
        pass
    elif string.startswith(tuple(line_start_modifiers)):

        #  print("Something of value:")
        splitted = string.split()
        #  print(splitted)
        if "class" in splitted:
            #  print("got a class\n", string)
            obodict[len(obodict)] = "class"
            currentIndex = len(obodict) - 1
            tree += "  " * currentLevel + "-"
            tree += str(currentSuper) + "class\n"
            # fill the Token object
            temptoken = Token()
            temptoken.tokenFile = filename
            temptoken.superToken = currentSuper
            temptoken.tokenComments = list()
            for item in comments:
                temptoken.tokenComments.append(item)
            # temptoken.tokenComments.append(comments)
            #  print("ADDED", temptoken.tokenComments)
            comments.clear()
            #  print("ADDED", temptoken.tokenComments)
            #  print("Comments:", comments)
            temptoken.tokenType = "class"
            temptoken.tokenNum = currentIndex
            readingAncestors = False
            for temp in splitted:
                if splitted.index(temp) < len(splitted):
                    if temptoken.tokenLocalName is None and (splitted.index(temp) == len(splitted) - 1):
                        temptoken.tokenLocalName = temp
                        #  print(temptoken.tokenLocalName)
                    elif temp == ":":
                        readingAncestors = True
                        if temptoken.tokenLocalName is None:
                            temptoken.tokenLocalName = splitted[splitted.index(temp) - 1]
                            #  print(temptoken.tokenLocalName)
                    elif readingAncestors:
                        temptoken.tokenSpecials.append(temp)
                        #  print(temptoken.tokenSpecials)
                    else:
                        temptoken.tokenCommons.append(temp)
                        #  print(temptoken.tokenCommons)
            tokens.append(temptoken)
            localtokens.append(temptoken)

        elif "enum" in splitted:
            #  print("got an enum\n", string)
            obodict[len(obodict)] = "enum"
            currentIndex = len(obodict) - 1
            tree += "  " * currentLevel + "-"
            tree += str(currentSuper) + "enum\n"

            # fill the Token object
            temptoken = Token()
            temptoken.tokenFile = filename
            temptoken.superToken = currentSuper
            temptoken.tokenComments = list()
            for item in comments:
                temptoken.tokenComments.append(item)
            # temptoken.tokenComments.append(comments)
            #  print("ADDED", temptoken.tokenComments)
            comments.clear()
            #  print("ADDED", temptoken.tokenComments)
            temptoken.tokenType = "enum"
            temptoken.tokenNum = currentIndex
            readingAncestors = False
            for temp in splitted:
                if splitted.index(temp) < len(splitted):
                    if temptoken.tokenLocalName is None and (splitted.index(temp) == len(splitted) - 1):
                        temptoken.tokenLocalName = temp
                        #  print(temptoken.tokenLocalName)
                    else:
                        temptoken.tokenCommons.append(temp)
                        #  print(temptoken.tokenCommons)
            tokens.append(temptoken)
            localtokens.append((temptoken))
        elif "struct" in splitted:
            #  print("got an struct\n", string)
            obodict[len(obodict)] = "struct"
            currentIndex = len(obodict) - 1
            tree += "  " * currentLevel + "-"
            tree += str(currentSuper) + "struct\n"
            # fill the Token object
            temptoken = Token()
            temptoken.tokenFile = filename
            temptoken.superToken = currentSuper
            temptoken.tokenComments = list()
            for item in comments:
                temptoken.tokenComments.append(item)
            # temptoken.tokenComments.append(comments)
            #  print("ADDED", temptoken.tokenComments)
            comments.clear()
            #  print("ADDED", temptoken.tokenComments)
            temptoken.tokenType = "struct"
            temptoken.tokenNum = currentIndex
            readingAncestors = False
            for temp in splitted:
                if splitted.index(temp) < len(splitted):
                    if temptoken.tokenLocalName is None and (splitted.index(temp) == len(splitted) - 1):
                        temptoken.tokenLocalName = temp
                        #  print(temptoken.tokenLocalName)
                    elif temp == ":":
                        readingAncestors = True
                        if temptoken.tokenLocalName is None:
                            temptoken.tokenLocalName = splitted[splitted.index(temp) - 1]
                            #  print(temptoken.tokenLocalName)
                    elif readingAncestors:
                        temptoken.tokenSpecials.append(temp)
                        #  print(temptoken.tokenSpecials)
                    else:
                        temptoken.tokenCommons.append(temp)
                        #  print(temptoken.tokenCommons)
            tokens.append(temptoken)
            localtokens.append((temptoken))
        elif "interface" in splitted:
            #  print("got an interface\n", string)
            obodict[len(obodict)] = "interface"
            currentIndex = len(obodict) - 1
            tree += "  " * currentLevel + "-"
            tree += str(currentSuper) + "interface\n"
            # fill the Token object
            temptoken = Token()
            temptoken.tokenFile = filename
            temptoken.superToken = currentSuper
            temptoken.tokenComments = list()
            for item in comments:
                temptoken.tokenComments.append(item)
            # temptoken.tokenComments.append(comments)
            #  print("ADDED", temptoken.tokenComments)
            comments.clear()
            #  print("ADDED", temptoken.tokenComments)
            temptoken.tokenType = "interface"
            temptoken.tokenNum = currentIndex
            readingAncestors = False
            for temp in splitted:
                if splitted.index(temp) < len(splitted):
                    if temptoken.tokenLocalName is None and (splitted.index(temp) == len(splitted) - 1):
                        temptoken.tokenLocalName = temp
                        #  print(temptoken.tokenLocalName)
                    elif temp == ":":
                        readingAncestors = True
                        if temptoken.tokenLocalName is None:
                            temptoken.tokenLocalName = splitted[splitted.index(temp) - 1]
                            #  print(temptoken.tokenLocalName)
                    elif readingAncestors:
                        temptoken.tokenSpecials.append(temp)
                        #  print(temptoken.tokenSpecials)
                    else:
                        temptoken.tokenCommons.append(temp)
                        #  print(temptoken.tokenCommons)
            tokens.append(temptoken)
            localtokens.append((temptoken))
        elif "namespace" in splitted:
            #  print("got an namespace\n", string)
            obodict[len(obodict)] = "namespace"
            currentIndex = len(obodict) - 1
            tree += "  " * currentLevel + "-"
            tree += str(currentSuper) + "namespace\n"
            # fill the Token object
            temptoken = Token()
            temptoken.tokenFile = filename
            temptoken.superToken = currentSuper
            temptoken.tokenComments = list()
            for item in comments:
                temptoken.tokenComments.append(item)
            # temptoken.tokenComments.append(comments)
            #  print("ADDED", temptoken.tokenComments)
            comments.clear()
            #  print("ADDED", temptoken.tokenComments)
            temptoken.tokenType = "namespace"
            temptoken.tokenNum = currentIndex
            readingAncestors = False
            for temp in splitted:
                if splitted.index(temp) < len(splitted):
                    if temptoken.tokenLocalName is None and (splitted.index(temp) == len(splitted) - 1):
                        temptoken.tokenLocalName = temp
                        #  print(temptoken.tokenLocalName)
                    else:
                        temptoken.tokenCommons.append(temp)
                        #  print(temptoken.tokenCommons)
            tokens.append(temptoken)
            localtokens.append((temptoken))
        else:

            if splitted[len(splitted) - 1].endswith(";") and "{" not in string and "}" not in string:
                #  print("Value found. ")
                obodict[len(obodict)] = "value"
                tree += "  " * currentLevel + "-"
                tree += str(currentSuper) + "value\n"
                # fill the Token object
                temptoken = Token()
                temptoken.tokenFile = filename
                temptoken.superToken = currentSuper
                temptoken.tokenComments = list()
                for item in comments:
                    temptoken.tokenComments.append(item)
                # temptoken.tokenComments.append(comments)
                #  print("ADDED", temptoken.tokenComments)
                comments.clear()
                #  print("ADDED", temptoken.tokenComments)
                temptoken.tokenType = "value"
                temptoken.tokenNum = -1
                readingAncestors = False
                for temp in splitted:
                    if splitted.index(temp) < len(splitted):
                        if temptoken.tokenLocalName is None and (splitted.index(temp) == len(splitted) - 1):
                            temptoken.tokenLocalName = temp
                            #  print(temptoken.tokenLocalName)
                        elif temp.startswith("="):
                            temptoken.tokenLocalName = splitted[splitted.index(temp) - 1]
                            #  print(temptoken.tokenLocalName)
                        else:
                            temptoken.tokenCommons.append(temp)
                            #  print(temptoken.tokenCommons)
                tokens.append(temptoken)
                localtokens.append((temptoken))
            elif splitted[len(splitted) - 1].endswith(")") or splitted[len(splitted) - 1].endswith("{") or (
                    splitted[len(splitted) - 1].endswith(";") and "=>" in string):
                #  print("Method found. ")
                obodict[len(obodict)] = "method"
                currentIndex = len(obodict) - 1
                tree += "  " * currentLevel + "-"
                tree += str(currentSuper) + "method\n"
                # fill the Token object
                temptoken = Token()
                temptoken.tokenFile = filename
                temptoken.superToken = currentSuper
                temptoken.tokenComments = list()
                for item in comments:
                    temptoken.tokenComments.append(item)
                # temptoken.tokenComments.append(comments)
                #  print("ADDED", temptoken.tokenComments)
                comments.clear()
                #  print("ADDED", temptoken.tokenComments)
                temptoken.tokenType = "method"
                temptoken.tokenNum = currentIndex
                readingAncestors = False
                for temp in splitted:
                    if splitted.index(temp) < len(splitted):
                        if temptoken.tokenLocalName is None and (splitted.index(temp) == len(splitted) - 1):
                            temptoken.tokenLocalName = temp
                            #  print(temptoken.tokenLocalName)

                        elif "(" in temp:
                            tempsplit = temp.split("(")
                            temptoken.tokenLocalName = tempsplit[0] + "()"
                            #  print(temptoken.tokenLocalName)
                        else:
                            temptoken.tokenCommons.append(temp)
                            #  print(temptoken.tokenCommons)
                tokens.append(temptoken)
                localtokens.append((temptoken))
            elif len(splitted)>=2 and string.rstrip().endswith("}") or ("{" in string and "}" in string and "=" in string and string.rstrip().endswith(";")):
                #  print("Property found")
                obodict[len(obodict)] = "property"
                currentIndex = len(obodict) - 1
                tree += "  " * currentLevel + "-"
                tree += str(currentSuper) + "property\n"
                # fill the Token object
                temptoken = Token()
                temptoken.tokenFile = filename
                temptoken.superToken = currentSuper
                temptoken.tokenComments = list()
                for item in comments:
                    temptoken.tokenComments.append(item)
                # temptoken.tokenComments.append(comments)
                #  print("ADDED", temptoken.tokenComments)
                comments.clear()
                #  print("ADDED", temptoken.tokenComments)
                temptoken.tokenType = "property"
                temptoken.tokenNum = currentIndex
                readingAncestors = False
                for temp in splitted:

                    if splitted.index(temp) < len(splitted):
                        if temptoken.tokenLocalName is None and splitted.index(temp) != len(splitted)-1 and "{" in splitted[splitted.index(temp)+1]:
                            temptoken.tokenLocalName = temp
                            #  print("HIPPITY HOPPITY NAME OF THE PROPERTY", temp)

                            #  print(temptoken.tokenLocalName)


                        else:
                            temptoken.tokenCommons.append(temp)
                            #  print(temptoken.tokenCommons)
                tokens.append(temptoken)
                localtokens.append((temptoken))
    elif string.lstrip().startswith("using"):
        #  print("Using directive", string.strip())
        temptoken = Token()
        temptoken.tokenFile = filename
        temptoken.superToken = currentSuper
        temptoken.tokenComments = list()
        for item in comments:
            temptoken.tokenComments.append(item)
        temptoken.tokenLocalName = string+"<br>"
        #  print("ADDED", temptoken.tokenComments)
        comments.clear()
        #  print("ADDED", temptoken.tokenComments)
        temptoken.tokenType = "using"
        temptoken.tokenNum = currentIndex
        tokens.append(temptoken)
        localtokens.append((temptoken))
    for a in string:
        if a == "{":
            currentLevel += 1
            hierarchy.append(currentIndex)
            #  print("\n", "New Level", currentLevel, "\n")
        if a == "}":
            currentLevel -= 1
            if len(hierarchy) > 0:
                hierarchy.pop()
            #  print("\n", "New Level", currentLevel, "\n")
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
    #  print(str_d)
    # work with str_a prepared string by taking identifiers and converting them to HTML

    html_dict = {"<summary>": "<a class=summary>", "</summary>": "</a>", "<remarks>": "<a class=remarks>",
                 "</remarks>": "</a>",
                 "<c>": "<pre>", "</c>": "</pre>", "<code>": "<pre>", "</code>": "</pre>", "<exception>": "<a>Throws ",
                 "</exception>": "</a>", "<returns>": "<a class=returns>", "</returns>": "</a>"}

    return str_d


def insert_str(string, str_to_insert, index):
    return string[:index] + str_to_insert + string[index:]


def main(file):
    global localtokens
    global filename

    filename = file


    t = threading.Thread(target=animate)
    t.start()
    localtokens = []
    start_parse(file)


def temporary_dox():
    for tok in tokens:
        if tok.superToken == 0:
            #  print(tok.tokenType, tok.tokenLocalName, tok.tokenComments)
            for tokt in tokens:
                if tokt.superToken == tok.tokenNum:
                     print(" ", tokt.tokenType, " ", tokt.tokenLocalName, " ", tokt.tokenComments)


