from pyimager import *

usage_colors = {
    "control": COL.rebeccaPurple,
    "format": "#f58231",
    "diac ab": "#ffe119",
    "diac bl": "#bfef45",
    "in diac": "#42d4f4",
    "symbols": "#911eb4",
    "LATIN": "#f032e6",
    "latin": "#f032e6",
    "CYRILIC": "#fabebe",
    "cyrilic": "#fabebe","VIET": "#469990","viet": "#469990","GREEK": "#0000a5","greek": "#0000a5","A.GREEK": "#4363d8","a.greek": "#4363d8","O.GREEK": "#a9a9a9","o.greek": "#a9a9a9","hebrew": "#ffe15f","mkhedruli": "#dcbeff","hiragana": "#9A6324","katakana": "#fffac8","ARMENIAN": "#800000","armenian": "#800000","si po of": "#aaffc3","si po co": "#808000","si po ra": "#ffd8b1","si po al": "#000000","...": "#dddddd","/**/": "#dddddd"}
chars = [("00", "09", "control"),("20", "32", "format"),("40", "54", "diac ab"),("60", "64", "diac bl"),("80", "80", "in diac"),("A0", "G2", "symbols"),("A00", "A29", "LATIN"),("A30", "A62", "CYRILIC"),("A63", "A63", "VIET"),("A70", "A94", "GREEK"),("A95", "A97", "A.GREEK"),("A98", "A99", "o.greek"),("B00", "B29", "latin"),("B30", "B62", "cyrilic"),("B63", "B63", "viet"),("B70", "B94", "greek"),("B95", "B97", "a.greek"),("B98", "B99", "o.greek"),("C00", "C39", "hebrew"),("C40", "C72", "mkhedruli"),("D00", "D47", "hiragana"),("D50", "D97", "katakana"),("E00", "E37", "ARMENIAN"),("E40", "E77", "armenian"),("F00", "G17", "si po of"),("G20", "G32", "si po co"),("G40", "G49", "si po ra"),("G50", "G89", "si po al"),]
size = 1000
D = size//10; dists = [i for i in range(0, size+1, D)]

ALP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

if True:
    img_00_99 = new_img(dimensions=[size, size])
    for d, f, c in chars:
        if d.isdecimal():
            for i in range(int(d), int(f)+1):
                i = f"{i:0>2}"; x, y = int(i[1]), int(i[0])
                img_00_99.rectangle([dists[x], dists[y]], [dists[x]+D, dists[y]+D], COL.new(usage_colors[c]), 0, 2)
                img_00_99.write(c[0], [dists[x]+D/3, dists[y]+D/3*2], COL.green, D//50, D/50, lineType=2)
    for i in range(0, size+1, D):
        img_00_99.line([0, i], [size, i], COL.gray, 1, 2)
        img_00_99.line([i, 0], [i, size], COL.gray, 1, 2)
    img_00_99.save_img("./", "00-99.jpg")

if True:
    D = size//10; dists = [i for i in range(0, size+1, D)]
    img_A0_Z9 = new_img(dimensions=[size, size/10*26])
    for d, f, c in chars:
        if not d.isdecimal() and len(d) == 2:
            y1, y2 = ALP.index(d[0]), ALP.index(f[0])
            for y in range(y1, y2+1):
                x1, x2 = 0 if y>y1 else int(d[1]), 9 if y<y2 else int(f[1])
                for x in range(x1, x2+1):
                    img_A0_Z9.rectangle([dists[x], dists[y]], [dists[x]+D, dists[y]+D], COL.new(usage_colors[c]), 0, 2)
                    img_A0_Z9.write(c[0], [dists[x]+D/3, dists[y]+D/3*2], COL.green, D//50, D/50, lineType=2)
    for i in range(26):
        img_A0_Z9.line([0, D*i], [size, D*i], COL.gray, 1, 2)
        img_A0_Z9.line([D*i, 0], [D*i, size/10*26], COL.gray, 1, 2)
    img_A0_Z9.save_img("./", "A0-Z9.jpg")

if True:
    D = size//100; dists = [i for i in range(0, size+1, D)]
    img_A00_Z99 = new_img(dimensions=[size, size/100*26])
    for d, f, c in chars:
        if not d.isdecimal() and len(d) == 3:
            y1, y2 = ALP.index(d[0]), ALP.index(f[0])
            for y in range(y1, y2+1):
                x1, x2 = 0 if y>y1 else int(d[1::]), 99 if y<y2 else int(f[1::])
                for x in range(x1, x2+1):
                    img_A00_Z99.rectangle([dists[x], dists[y]], [dists[x]+D, dists[y]+D], COL.new(usage_colors[c]), 0, 2)
    for i in range(260):
        img_A00_Z99.line([0, D*i], [size, D*i], COL.gray, 1, 2)
        img_A00_Z99.line([D*i, 0], [D*i, size/100*26], COL.gray, 2 if i%10 == 0 else 1, 2)
    img_A00_Z99.save_img("./", "A00-Z99.jpg")

img_A00_Z99.build()
while img_A00_Z99.is_opened():
    wk = img_A00_Z99.show()