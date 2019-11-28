import datetime
import os

import sharplitedocs


def generate_main_page(name, ver, tfiles, tent, tname, tclass):
    print("Generating main page")
    f = open("mainpage.html", 'r')
    a = f.read()
    a = a.replace("%DOCNAME%", name)
    a = a.replace("%DOCVER%", ver)
    a = a.replace("%TOTALFILES%", tfiles)
    a = a.replace("%TOTALENT%", tent)
    a = a.replace("%DOCDATE%", str(datetime.datetime.today()))
    a = a.replace("%TOTALNAMES%", tname)
    a = a.replace("%TOTALCLASSES%", tclass)
    result = open("1/mainpage.html", "w")
    result.write(a)


def generate_index(list_names, name):
    print("Generating index")
    print(list_names)
    list_names.sort(reverse=True)
    f = open("index.html", 'r')
    a = f.read()
    a = a.replace("%DOCNAME%", name)
    for i in list_names:
        if "<a>" + i + "</a><br>" not in a:
            print(i)
            letter = i[0]
            finder = ""
            finder += "<span class=\"badge badge-secondary\">" + letter.upper() + "</span><br>"
            index = a.find(finder)
            if (index >= 0):
                print("Letter:", letter, "\nFinder:", finder, "Index:", index)
                a = insert_char(a, index + len(finder), "<a>" + i + "</a><br>")
    result = open("1/index.html", "w")
    result.write(a)


def generate_dirtree(rootdir, name):
    print("Generating dirtree")
    start = "<div class=\"list-group list-group-root well\">"
    f = open("dirtree.html", 'r')
    a = f.read()
    a = a.replace("%DOCNAME%", name)
    tree = os.walk(rootdir)
    insertion = ""
    count = 0
    for i in tree:
        emptydir = True

        print(i)
        ws = i[0].count("/")
        if len(i[2]) > 0:
            for k in i[2]:
                if k.endswith(".cs"):
                    emptydir = False
            if not emptydir:
                print("<a href = \"#\" class =\"list-group-item\" >", ws * '&nbsp&nbsp', i[0], "</a>")
                insertion += "<a class =\"list-group-item\" >" + ws * '&nbsp' + i[0] + "</a>"
                for j in i[2]:
                    if (j.endswith(".cs")):
                        count += 1
                        print("<a href = \"1/items/" + j + "\" class =\"list-group-item\" >", ws * '&nbsp&nbsp', j,
                              "</a>")
                        insertion += (
                                    "<a href = \"items/" + j + ".html\" class =\"list-group-item\"" + "<span>" + "&nbsp&nbsp" * ws + "</span>" + j + "</a>")
                        # print("<a href = \"#\" class =\"list-group-item\"" + "<span>" +"&nbsp&nbsp"*ws +"</span>" + j + "</a>")
                        # print("Count:", count)
    index = a.find(start)
    print(index)
    a = insert_char(a, index + len(start), insertion)

    result = open("1/dirtree.html", "w")
    result.write(a)


def generate_item(tokens, itemname, name):
    print("Generating item")
    sharplitedocs.files += 1

    # First add using directives
    # Then add all names found in da file
    # Then add a card for each name found with details
    f = open("item.html", 'r')
    a = f.read()
    usingline = " <h3>Import directives</h3>\n"
    namesline = "<h3>Members list</h3>\n<ol class=\"list-group\" style=\"left:20px\">"

    cards = "<h3>Detailed descriptions</h3>\n <hr>"
    card1 = "<div class=\"card\" style=\"width: 80%\"><div class=\"card-body\"><h5 class=\"card-title\">"

    card2 = "</h5><p class=\"card-text\">"

    card3 = "</p><hr> <h6>Derived from that class</h6><p class=\"card-text\">"

    card4 = "</p><hr><h6>Member of:</h6><p class=\"card-text\">"

    card5 = "</p></div></div><br>"
    for k in tokens:
        if k.tokenType == "using":
            usingline += k.tokenLocalName + "\n"
        else:
            if k.tokenLocalName != None:
                namesline += "<li class=\"list-group-item\"><p>"+k.tokenType + ' ' + k.tokenLocalName + "</p></li>\n"
            else:
                namesline += " "
    namesline += "</ol>"
    a = a.replace("<h3>Import directives</h3>", usingline)
    a = a.replace("<h3>Members list</h3>", namesline)
    for i in tokens:

        if i.tokenType != "using":
            temp = ""
            for j in tokens:
                if j.superToken == i.tokenNum:
                    temp += "-" + j.tokenLocalName if j.tokenLocalName is not None else " " + "\n"
            cards += card1+i.tokenType+"     " +i.tokenLocalName if i.tokenLocalName is not None else " " + " "
            cards += card2
            cards += str(i.tokenComments)
            cards += card3
            cards += temp
            cards += card4
            for z in tokens:
                if z.tokenNum == i.superToken:
                    cards += z.tokenType
                    cards += " "
                    cards += z.tokenLocalName
            cards += card5
            print(cards)
    a = a.replace("<h3>Detailed descriptions</h3>", cards)
    a = a.replace("%DOCNAME%", name)
    a = a.replace("%ITEMNAME%", itemname)
    result = open("1/items/"+itemname+".html", "w")
    result.write(a)

def insert_char(mystring, position, chartoinsert):
    longi = len(mystring)
    mystring = mystring[:position] + chartoinsert + mystring[position:]
    return mystring
