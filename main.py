import sys
# Code to convert assembley language to instruction set
try:
    file = open(sys.argv[1], "r")
except:
    print('no file found')
    exit()
objf = open("objectfile","w")
symf = open("symboltable","w")
datafile = open("datafile","w")
datadic={}
lines = file.readlines()
gp='0x10008000'
stp='0x0000003FFFFFFFF0'
pc='0x0000000000400000'
R = 'R'
r = 'r'
for i in range(len(lines)):
    lines[i].strip()
    # print(lines[i])
    if lines[i].strip() == ".data":
        data_sec = i
    elif lines[i].strip() == ".text":
        text_sec = i
try:
    data_sec = data_sec
    text_sec = text_sec
except NameError:
    print("either of  data section or text section is missing")
    exit(1)
# code for data section--------------------------------
j = data_sec + 1
data_addr = 0x10000000
while j < len(lines) and j < text_sec:
    lines[j] = lines[j].strip()
    val = lines[j].split(' ')
    if len(val) != 3:
        print("error in data section line %d", j + 1)
        exit()
    if val[0][-1] == ':':
        symf.write(val[0][:-1] + ' ')
    symf.write(str(data_addr) + ' ')
    #print(val, end='')
    if val[1].strip()[0] == '.':
        if val[1].strip()[1:] == 'word':
            val[2] = val[2].strip().split(',')
            #print(val[2])
            l=0
            while l<len(val[2]):
                data_addr = data_addr + 4
                if int(val[2][l].strip()) >= 0:
                    datafile.write(bin(int(val[2][l]))[2:].zfill(32))
                else:
                    datafile.write(bin(int(val[2][l].strip()) & (2 ** 32 - 1))[2:])
                l=l+1
        elif val[1].strip()[1:] == 'byte':
            data_addr = data_addr + 1
            if int(val[2].strip()) >= 0:
                datafile.write(bin(int(val[2]))[2:].zfill(8))
            else:
                datafile.write(bin((int(val[2].strip()) * -1) & (2 ** 8 - 1))[2:])
        elif val[1].strip()[1:] == 'asciiz':
            y = len(val[2])
            p = [bin(ord(ch))[2:].zfill(8) for ch in val[2]]
            q = ''.join(p)
            datafile.write(q + '00000000')
            data_addr = data_addr + len(val[2].strip()) + 1
    symf.write('\n')
    print('')
    j = j + 1


# --------------------------------------------------------------------
# --------------findlabel--------------------
def findlabel(label):
    global lines
    global j
    j = 0
    for j in range(len(lines)):
        if lines[j].strip()[:-1] == label:
            return


def findnum(var):
    global lines
    global j
    j = data_sec + 1
    while j < len(lines) and j < text_sec:
        reg = lines[j].split(':')
        if reg[0] == var:
            j=j-data_sec-1
            return
        j = j + 1


# -------------------------------------------------------
# code for converting instructions---------------------------------------------------
i = text_sec + 1
if data_sec < text_sec:
    pass
else:
    pass
while i < len(lines):
    instruction = []
    lines[i] = lines[i].strip()

    # instruction 1
    if lines[i].strip()[:4] == "add ":
        opcode = 31
        lines[i] = lines[i].strip()
        instruction.append(bin(opcode)[2:].zfill(6))
        reg = lines[i][4:].split(',')
        if len(reg) != 3:
            print("error in line %d" % (i + 1))
            exit()
        for j in range(3):
            reg[j] = reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
                if int(reg[j]) > 31:
                    print("error in line %d " % (i + 1))
                    exit()
            else:
                print("no register found as %s in line %d" % (reg[j], i + 1))
                exit()
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        instruction.append(bin(int(reg[2]))[2:].zfill(5))
        OE = 0
        Rc = 0
        XO = 266
        instruction.append(str(OE))
        instruction.append(bin(XO)[2:].zfill(9))
        instruction.append(str(Rc))

    # instruction 3
    elif lines[i][:5] == "andis":  # instruction 3
        opcode = 15
        instruction.append(bin(opcode)[2:].zfill(6))
        reg = lines[i][6:].split(',')
        if len(reg) != 3:
            print("error in line %d" % (i + 1))
            exit()
        for j in range(2):
            reg[j] = reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
            else:
                print("no register found as %s error in line %d" % (reg[j], i + 1))
                exit()
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        if int(reg[2]) < 0:
            instruction.append(bin(int(reg[2]) & 2 ** 16 - 1)[2:])
        else:
            instruction.append(bin(int(reg[2]))[2:].zfill(16))
    # instruction 2
    elif lines[i][:4] == "addi":
        reg = lines[i][5:].split(",")
        if len(reg) != 3:
            print("error in line %d" % (i + 1))
            exit()
        for j in range(2):
            reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
            else:
                print("no register found as %s error in line %d" % (reg[j], i + 1))
                exit()
        opcode = 14
        instruction.append(bin(opcode)[2:].zfill(6))
        instruction.append((bin(int(reg[0]))[2:].zfill(5)))
        instruction.append((bin(int(reg[1]))[2:].zfill(5)))
        if int(reg[2]) < 0:
            instruction.append(bin(int(reg[2]) & (2 ** 16 - 1))[2:].zfill(16))
        else:
            instruction.append(bin(int(reg[2]))[2:].zfill(16))
    # instruction 4
    elif (lines[i][:4] == "and "):
        reg = lines[i][4:].split(",")
        if len(reg) != 3:
            print("not valid instruction in line %d" % (i + 1))
            exit()
        for j in range(3):
            reg[j] = reg[j].strip()
            if reg[j][0] == 'R' or reg[j][0] == 'r':
                reg[j] = reg[j][1:]
            else:
                print("no register found as %s error in %d line" % (reg[j], i + 1))
                exit()
        opcode = 31
        instruction.append(bin(opcode)[2:].zfill(6))
        instruction.append((bin(int(reg[1]))[2:].zfill(5)))
        instruction.append((bin(int(reg[0]))[2:].zfill(5)))
        instruction.append((bin(int(reg[2]))[2:].zfill(5)))
        XO = 28
        instruction.append(bin(XO)[2:].zfill(10))
        Rc = 0
        instruction.append(bin(Rc)[2:].zfill(1))

    # instruction 5
    elif lines[i][:4] == "andi":
        opcode = 28
        instruction.append(bin(opcode)[2:].zfill(6))
        reg = lines[i][5:].split(',')
        if len(reg) != 3:
            print("error in line %d" % (i + 1))
            exit()
        for j in range(2):
            reg[j].strip(" ")
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
            else:
                print("no register found as %s error in line %d" % (reg[j], i + 1))
                exit()
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        instruction.append(bin(int(reg[2]))[2:].zfill(16))

    # instruction 7
    elif lines[i][:4] == "nand":
        reg = lines[i][5:].split(",")
        if len(reg) != 3:
            print("not valid instruction in line %d" % (i + 1))
            exit()
        for j in range(3):
            reg[i] = reg[j].strip()
            if reg[j][0] == r or reg[j][0] == R:
                reg[j] = reg[j][1:]
            else:
                print("error in line %d " % (i + 1))
                exit()
        opcode = 31
        instruction.append(bin(opcode)[2:].zfill(6))
        instruction.append((bin(int(reg[1]))[2:].zfill(5)))
        instruction.append((bin(int(reg[0]))[2:].zfill(5)))
        instruction.append((bin(int(reg[2][:-1]))[2:].zfill(5)))
        XO = 476
        instruction.append(bin(XO)[2:].zfill(10))
        Rc = 0
        instruction.append(bin(Rc)[2:].zfill(1))

    # instruction 8
    elif lines[i][:3] == "or ":
        reg = lines[i][3:].split(",")
        if len(reg) != 3:
            print("not valid instruction in line %d" % (i + 1))
            exit()
        for j in range(3):
            reg[j] = reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
            else:
                print("no register %s found error in line %d" % (reg[j], i + 1))
                exit()
        opcode = 31
        instruction.append(bin(opcode)[2:].zfill(6))
        instruction.append((bin(int(reg[1]))[2:].zfill(5)))
        instruction.append((bin(int(reg[0]))[2:].zfill(5)))
        instruction.append((bin(int(reg[2]))[2:].zfill(5)))
        XO = 444
        instruction.append(bin(XO)[2:].zfill(10))
        Rc = 0
        instruction.append(bin(Rc)[2:].zfill(1))

    # instruction 9
    elif lines[i][:3] == "ori":
        reg = lines[i][4:].split(",")
        if len(reg) != 3:
            print("not valid instruction in line %d" % (i + 1))
            exit()
        for j in range(2):
            reg[j] = reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
                if int(reg[j]) > 31:
                    print("error in line %d " % (i + 1))
                    exit()
            else:
                print("no register %s found error in line %d" % (reg[j], i + 1))
                exit()
        opcode = 24
        instruction.append(bin(opcode)[2:].zfill(6))
        instruction.append((bin(int(reg[1]))[2:].zfill(5)))
        instruction.append((bin(int(reg[0]))[2:].zfill(5)))
        instruction.append(bin(int(reg[2]))[2:].zfill(16))

    # instruction 10
    elif lines[i][:4] == "subf":
        opcode = 31
        OE = 0
        XO = 40
        Rc = 1
        instruction.append(bin(opcode)[2:].zfill(6))
        reg = lines[i][5:].split(',')
        if len(reg) != 3:
            print("error in line %d" % (i + 1))
            exit()
        for j in range(3):
            reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
            else:
                print("no register found as %s error in line %d" % (reg[j], i + 1))
                exit()
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        instruction.append(bin(int(reg[2]))[2:].zfill(5))
        instruction.append(bin(OE)[2:].zfill(1))
        instruction.append(bin(XO)[2:].zfill(9))
        instruction.append(bin(Rc)[2:].zfill(1))

    # instruction 11
    elif lines[i][:4] == "xor ":
        reg = lines[i][4:].split(",")
        if len(reg) != 3:
            print("not valid instruction in line %d" % (i + 1))
            exit()
        for j in range(3):
            reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
                if int(reg[j]) > 31:
                    print("error in line %d " % (i + 1))
                    exit()
            else:
                print("no register %s found error in line %d" % (reg[j], i + 1))
                exit()
        opcode = 31
        instruction.append(bin(opcode)[2:].zfill(6))
        instruction.append((bin(int(reg[1]))[2:].zfill(5)))
        instruction.append((bin(int(reg[0]))[2:].zfill(5)))
        instruction.append((bin(int(reg[2]))[2:].zfill(5)))
        XO = 316
        instruction.append(bin(XO)[2:].zfill(10))
        Rc = 0
        instruction.append(bin(Rc)[2:].zfill(1))

    # instruction 12
    elif lines[i][:4] == "xori":
        reg = lines[i][5:].split(",")
        if len(reg) != 3:
            print("not valid instruction in line %d" % (i + 1))
            exit()
        for j in range(2):
            reg[j] = reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
                if int(reg[j]) > 31:
                    print("error in line %d " % (i + 1))
            else:
                print("no register %s found error in line %d" % (reg[j], i + 1))
                exit()
        opcode = 26
        instruction.append(bin(opcode)[2:].zfill(6))
        instruction.append((bin(int(reg[1]))[2:].zfill(5)))
        instruction.append((bin(int(reg[0]))[2:].zfill(5)))
        instruction.append(bin(int(reg[2]))[2:].zfill(16))

    # instruction 13
    if lines[i].strip()[:3] == "ld ":
        opcode = 58

        instruction.append(bin(opcode)[2:].zfill(6))
        reg = lines[i].strip()[3:].split(',')
        if len(reg) != 2:
            print("error in line %d" % (i + 1))
            exit()

        reg[0] = reg[0].strip()
        if reg[0][0] == R or reg[0][0] == r:
            reg[0] = reg[0][1:]
        else:
            print("error in line %d " % (i + 1))
            exit()
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        reg[1] = reg[1].strip()
        reg = reg[1].split('(')
        reg[0] = reg[0].strip()
        reg[1] = reg[1].strip()
        reg[1] = reg[1][:-1]
        if reg[1][0] == R or reg[1][0] == r:
            reg[1] = reg[1][1:]
            if (int(reg[1]) > 31):
                print("error in line %d" % (i + 1))
        else:
            print("error in line %d" % (i + 1))
            exit()

        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        if int(reg[0]) < 0:
            instruction.append(bin(int(reg[0]) & 2 ** 14 - 1)[2:])
        else:
            instruction.append(bin(int(reg[0]))[2:].zfill(14))
        XO = 0
        instruction.append(bin(XO)[2:].zfill(2))

    # instruction 14
    elif lines[i].strip()[:3] == "lwz":
        opcode = 32
        reg = lines[i].strip()[4:].split(',')
        if len(reg) != 2:
            print("error in line %d" % (i + 1))
            exit()
        reg[0] = reg[0].strip()
        if reg[0][0] == R or reg[0][0] == r:
            reg[0] = reg[0][1:]
            if int(reg[0]) > 31:
                print("error in line  %d" % (i + 1))
                exit()
        instruction.append(bin(int(opcode))[2:].zfill(6))
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        reg = reg[1].split('(')
        reg[1] = reg[1].strip()
        reg[1] = reg[1][:-1]
        if reg[1][0] == R or reg[1][0] == r:
            reg[1] = reg[1][1:]
        else:
            print("error in line  %d" % (i + 1))
            exit()
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        if int(reg[0]) < 0:
            instruction.append(bin(int(reg[0]) & 2 ** 14 - 1)[2:])
        else:
            instruction.append(bin(int(reg[0]))[2:].zfill(14))
        XO = 0
        instruction.append(bin(int(XO))[2:].zfill(2))

    # instruction 15
    elif lines[i].strip()[:4] == "std ":
        opcode = 62
        instruction.append(bin(opcode)[2:].zfill(6))
        reg = lines[i].strip()[4:].split(',')
        if len(reg) != 2:
            print("error in line %d" % (i + 1))
            exit()

        reg[0] = reg[0].strip()
        if reg[0][0] == R or reg[0][0] == r:
            reg[0] = reg[0][1:]
        else:
            print("error in line %d " % (i + 1))
            exit()
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        reg[1] = reg[1].strip()
        reg = reg[1].split('(')
        reg[0] = reg[0].strip()
        reg[1] = reg[1].strip()
        reg[1] = reg[1][:-1]
        if reg[1][0] == R or reg[1][0] == r:
            reg[1] = reg[1][1:]
            if (int(reg[1]) > 31):
                print("error in line %d" % (i + 1))
        else:
            print("error in line %d" % (i + 1))
            exit()

        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        if int(reg[0]) < 0:
            instruction.append(bin(int(reg[0]) & 2 ** 14 - 1)[2:])
        else:
            instruction.append(bin(int(reg[0]))[2:].zfill(14))
        XO = 0
        instruction.append(bin(XO)[2:].zfill(2))

        # instruction 16
    elif lines[i].strip()[:3] == "stw":
        opcode = 36
        reg = lines[i].strip()[4:].split(',')
        if len(reg) != 2:
            print("error in line %d" % (i + 1))
            exit()
        reg[0] = reg[0].strip()
        if reg[0][0] == R or reg[0][0] == r:
            reg[0] = reg[0][1:]
            if int(reg[0]) > 31:
                print("error in line  %d" % (i + 1))
                exit()
        instruction.append(bin(int(opcode))[2:].zfill(6))
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        reg = reg[1].split('(')
        reg[1] = reg[1].strip()
        reg[1] = reg[1][:-1]
        if reg[1][0] == R or reg[1][0] == r:
            reg[1] = reg[1][1:]
        else:
            print("error in line  %d" % (i + 1))
            exit()
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        if int(reg[0]) < 0:
            instruction.append(bin(int(reg[0]) & 2 ** 16 - 1)[2:])
        else:
            instruction.append(bin(int(reg[0]))[2:].zfill(16))

        # instruction 17
    elif lines[i].strip()[:4] == "stwu":
        opcode = 37
        reg = lines[i].strip()[4:].split(',')
        if len(reg) != 2:
            print("error in line %d" % (i + 1))
            exit()
        reg[0] = reg[0].strip()
        if reg[0][0] == R or reg[0][0] == r:
            reg[0] = reg[0][1:]
            if int(reg[0]) > 31:
                print("error in line  %d" % (i + 1))
                exit()
        instruction.append(bin(int(opcode))[2:].zfill(6))
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        reg = reg[1].split('(')
        reg[1] = reg[1].strip()
        reg[1] = reg[1][:-1]
        if reg[1][0] == R or reg[1][0] == r:
            reg[1] = reg[1][1:]
        else:
            print("error in line  %d" % (i + 1))
            exit()
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        if int(reg[0]) < 0:
            instruction.append(bin(int(reg[0]) & 2 ** 16 - 1)[2:])
        else:
            instruction.append(bin(int(reg[0]))[2:].zfill(16))

        # instruction 18
    elif lines[i].strip()[:3] == "lhz":
        opcode = 40
        reg = lines[i].strip()[4:].split(',')
        if len(reg) != 2:
            print("error in line %d" % (i + 1))
            exit()
        reg[0] = reg[0].strip()
        if reg[0][0] == R or reg[0][0] == r:
            reg[0] = reg[0][1:]
            if int(reg[0]) > 31:
                print("error in line  %d" % (i + 1))
                exit()
        instruction.append(bin(int(opcode))[2:].zfill(6))
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        reg = reg[1].split('(')
        reg[1] = reg[1].strip()
        reg[1] = reg[1][:-1]
        if reg[1][0] == R or reg[1][0] == r:
            reg[1] = reg[1][1:]
        else:
            print("error in line  %d" % (i + 1))
            exit()
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        if int(reg[0]) < 0:
            instruction.append(bin(int(reg[0]) & 2 ** 16 - 1)[2:])
        else:
            instruction.append(bin(int(reg[0]))[2:].zfill(16))

    # instruction 19
    elif lines[i].strip()[:3] == "lha":
        opcode = 42
        reg = lines[i].strip()[4:].split(',')
        if len(reg) != 2:
            print("error in line %d" % (i + 1))
            exit()
        reg[0] = reg[0].strip()
        if reg[0][0] == R or reg[0][0] == r:
            reg[0] = reg[0][1:]
            if int(reg[0]) > 31:
                print("error in line  %d" % (i + 1))
                exit()
        instruction.append(bin(int(opcode))[2:].zfill(6))
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        reg = reg[1].split('(')
        reg[1] = reg[1].strip()
        reg[1] = reg[1][:-1]
        if reg[1][0] == R or reg[1][0] == r:
            reg[1] = reg[1][1:]
        else:
            print("error in line  %d" % (i + 1))
            exit()
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        if int(reg[0]) < 0:
            instruction.append(bin(int(reg[0]) & 2 ** 16 - 1)[2:])
        else:
            instruction.append(bin(int(reg[0]))[2:].zfill(16))

    # instruction 20
    elif lines[i].strip()[:3] == "sth":
        opcode = 44
        reg = lines[i].strip()[4:].split(',')
        if len(reg) != 2:
            print("error in line %d" % (i + 1))
            exit()
        reg[0] = reg[0].strip()
        if reg[0][0] == R or reg[0][0] == r:
            reg[0] = reg[0][1:]
            if int(reg[0]) > 31:
                print("error in line  %d" % (i + 1))
                exit()
        instruction.append(bin(int(opcode))[2:].zfill(6))
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        reg = reg[1].split('(')
        reg[1] = reg[1].strip()
        reg[1] = reg[1][:-1]
        if reg[1][0] == R or reg[1][0] == r:
            reg[1] = reg[1][1:]
        else:
            print("error in line  %d" % (i + 1))
            exit()
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        if int(reg[0]) < 0:
            instruction.append(bin(int(reg[0]) & 2 ** 16 - 1)[2:])
        else:
            instruction.append(bin(int(reg[0]))[2:].zfill(16))

    # instruction 21
    elif lines[i].strip()[:3] == "lbz":
        opcode = 34
        reg = lines[i].strip()[4:].split(',')
        if len(reg) != 2:
            print("error in line %d" % (i + 1))
            exit()
        reg[0] = reg[0].strip()
        if reg[0][0] == R or reg[0][0] == r:
            reg[0] = reg[0][1:]
            if int(reg[0]) > 31:
                print("error in line  %d" % (i + 1))
                exit()
        instruction.append(bin(int(opcode))[2:].zfill(6))
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        reg = reg[1].split('(')
        reg[1] = reg[1].strip()
        reg[1] = reg[1][:-1]
        if reg[1][0] == R or reg[1][0] == r:
            reg[1] = reg[1][1:]
        else:
            print("error in line  %d" % (i + 1))
            exit()
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        if int(reg[0]) < 0:
            instruction.append(bin(int(reg[0]) & 2 ** 16 - 1)[2:])
        else:
            instruction.append(bin(int(reg[0]))[2:].zfill(16))

    # instruction 22
    elif lines[i].strip()[:3] == "stb":
        opcode = 38
        reg = lines[i].strip()[4:].split(',')
        if len(reg) != 2:
            print("error in line %d" % (i + 1))
            exit()
        reg[0] = reg[0].strip()
        if reg[0][0] == R or reg[0][0] == r:
            reg[0] = reg[0][1:]
            if int(reg[0]) > 31:
                print("error in line  %d" % (i + 1))
                exit()
        instruction.append(bin(int(opcode))[2:].zfill(6))
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        reg = reg[1].split('(')
        reg[1] = reg[1].strip()
        reg[1] = reg[1][:-1]
        if reg[1][0] == R or reg[1][0] == r:
            reg[1] = reg[1][1:]
        else:
            print("error in line  %d" % (i + 1))
            exit()
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        if int(reg[0]) < 0:
            instruction.append(bin(int(reg[0]) & 2 ** 16 - 1)[2:])
        else:
            instruction.append(bin(int(reg[0]))[2:].zfill(16))

    # instruction 23
    elif lines[i].strip()[:6] == "rlwinm":
        opcode = 21
        reg = lines[i].strip()[6:].split(',')
        if len(reg) != 5:
            print("error1 in line %d" % (i + 1))
            exit()
        for j in range(5):
            reg[j] = reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
                if int(reg[j]) > 31:
                    print("error in line  %d" % (i + 1))
                    exit()
        instruction.append(bin(opcode)[2:].zfill(6))
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        instruction.append(bin(int(reg[2]))[2:].zfill(5))
        instruction.append(bin(int(reg[3]))[2:].zfill(5))
        instruction.append(bin(int(reg[4]))[2:].zfill(5))
        Rc = 0
        instruction.append(bin(Rc)[2:].zfill(1))

    # instruction 25
    elif lines[i].strip()[:4] == "sld ":
        opcode = 31
        instruction.append(bin(opcode)[2:].zfill(6))

        reg = lines[i].strip()[4:].split(",")
        if len(reg) != 3:
            print("error in line %d" % (i + 1))
            exit()
        for j in range(3):
            reg[j] = reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
                if int(reg[j]) > 31:
                    print("error in line %d" % (i + 1))
                    exit()
            else:
                print("no register found as %s in line %d" % (reg[j], i + 1))
                exit()
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        instruction.append(bin(int(reg[2]))[2:].zfill(5))
        XO = 27
        Rc = 0
        instruction.append(bin(XO)[2:].zfill(10))
        instruction.append(bin(Rc)[2:].zfill(1))

    # instruction 26
    elif lines[i].strip()[:4] == "srd ":
        opcode = 31
        instruction.append(bin(opcode)[2:].zfill(6))

        reg = lines[i].strip()[4:].split(",")
        if len(reg) != 3:
            print("error in line %d" % (i + 1))
            exit()
        for j in range(3):
            reg[j] = reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
                if int(reg[j]) > 31:
                    print("error in line %d" % (i + 1))
                    exit()
            else:
                print("no register found as %s in line %d" % (reg[j], i + 1))
                exit()
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        instruction.append(bin(int(reg[2]))[2:].zfill(5))
        XO = 539
        Rc = 0
        instruction.append(bin(XO)[2:].zfill(10))
        instruction.append(bin(Rc)[2:].zfill(1))

    # instruction 27
    elif lines[i].strip()[:5] == "srad ":
        opcode = 31
        instruction.append(bin(opcode)[2:].zfill(6))

        reg = lines[i].strip()[5:].split(",")
        if len(reg) != 3:
            print("error in line %d" % (i + 1))
            exit()
        for j in range(3):
            reg[j] = reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
                if int(reg[j]) > 31:
                    print("error in line %d" % (i + 1))
                    exit()
            else:
                print("no register found as %s in line %d" % (reg[j], i + 1))
                exit()
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        instruction.append(bin(int(reg[2]))[2:].zfill(5))
        XO = 794
        Rc = 0
        instruction.append(bin(XO)[2:].zfill(10))
        instruction.append(bin(Rc)[2:].zfill(1))

    # instruction 28
    elif lines[i].strip()[:6] == "sradi ":
        lines[i] = lines[i].strip()[6:]
        lines[i] = lines[i].strip()
        reg = lines[i].split(',')
        for j in range(3):
            reg[j] = reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
            if int(reg[j]) < 0 and int(reg[j]) > 31:
                print("error in line %d" % (i + 1))
                exit()
        opcode = 31
        instruction.append(bin(opcode)[2:].zfill(6))
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        instruction.append(bin(int(reg[2]))[2:].zfill(5))
        XO = 413
        Rc = 0
        sh = 0
        instruction.append(bin(int(XO))[2:].zfill(9))
        instruction.append(bin(int(sh))[2:].zfill(1))
        instruction.append(bin(int(Rc))[2:].zfill(1))
    # instruction 29
    elif lines[i][0:2] == 'b ':
        opcode = 18
        reg = lines[i][1:]
        instruction.append(bin(opcode)[2:].zfill(6))
        reg = reg.strip()
        if int(reg) >= 0:
            instruction.append(bin(int(reg))[2:].zfill(24))
        else:
            instruction.append(bin(int(reg) & 2 ** 24 - 1)[2:])
        AA = 0
        instruction.append(str(AA))
        LK = 0
        instruction.append(str(LK))

    # instruction 29b
    elif lines[i][0:2] == 'ba':
        opcode = 18
        lines[i] = lines[i].strip()
        reg = lines[i][2:]
        print(reg[0])
        instruction.append(bin(opcode)[2:].zfill(6))
        reg = reg.strip()
        if int(reg) >= 0:
            instruction.append(bin(int(reg))[2:].zfill(24))
        else:
            instruction.append(bin(int(reg) & 2 ** 24 - 1)[2:])
        AA = 1
        instruction.append(str(AA))
        LK = 0
        instruction.append(str(LK))
    # instruction 30----------------------------------------------------------------------------
    elif lines[i][0:2] == 'bl':
        opcode = 18
        lines[i] = lines[i].strip()
        reg = lines[i][2:]
        print(reg[0])
        instruction.append(bin(opcode)[2:].zfill(6))
        reg = reg.strip()
        if int(reg) >= 0:
            instruction.append(bin(int(reg))[2:].zfill(24))
        else:
            instruction.append(bin(int(reg) & 2 ** 24 - 1)[2:])
        AA = 0
        instruction.append(str(AA))
        LK = 1
        instruction.append(str(LK))
#instruction 33--------------
    elif lines[i].strip()[:4] == 'bca ':
        opcode = 19
        lines[i] = lines[i].strip()
        reg = lines[i][3:].strip().split(',')
        if len(reg) != 3:
            print("error in line %d" % (i + 1))
            exit()
        for j in range(3):
            reg[j] = reg[j].strip()
        instruction.append(bin(int(opcode))[2:].zfill(6))
        BO = 0
        BI=int(reg[1])
        instruction.append(bin(int(BO))[2:].zfill(5))
        if BI == 28 or BI == 29 or BI == 30 :
            instruction.append(bin(int(BI))[2:].zfill(5))
        else:
            print('error bca')
            exit()
        findlabel(reg[2].strip())
        if j - i - 1 > 0:
            instruction.append(bin(j-i-1)[2:].zfill(14))
        else:
            instruction.append(bin((j - i - 1) & 2 ** 14-1)[2:])
        AA = 1
        LK = 0
        instruction.append(bin(int(AA))[2:].zfill(1))
        instruction.append(bin(int(LK))[2:].zfill(1))
    # instruction 34
    elif lines[i][:3] == "cmp":
        opcode = 31
        instruction.append(bin(opcode)[2:].zfill(6))
        reg = lines[i][3:].split(',')
        if len(reg) != 4:
            print("error in line %d" % (i + 1))
            exit()
        BF = 7
        instruction.append(bin(BF)[2:].zfill(5))
        for j in range(2):
            reg[j + 2] = reg[j + 2].strip()
            if reg[j + 2][0] == 'R' or reg[j + 2][0] == 'r':
                reg[j + 2] = reg[j + 2][1:]
            else:
                print("error in line %d" % (i + 1))
                exit()
            if int(reg[j + 2]) >= 0 and int(reg[j + 2]) < 32:
                instruction.append(bin(int(reg[j + 2]))[2:].zfill(5))
            else:
                print("error in line %d " % (i + 1))
                exit()
        XO = 0
        instruction.append(bin(XO)[2:].zfill(10))
        L = 1
        instruction.append(bin(L)[2:].zfill(1))
    elif lines[i][:4] == "subi":
        reg = lines[i][5:].split(",")
        if len(reg) != 3:
            print("error in line %d" % (i + 1))
            exit()
        for j in range(2):
            reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
            else:
                print("no register found as %s error in line %d" % (reg[j], i + 1))
                exit()
        opcode = 14
        instruction.append(bin(opcode)[2:].zfill(6))
        instruction.append((bin(int(reg[0]))[2:].zfill(5)))
        instruction.append((bin(int(reg[1]))[2:].zfill(5)))
        if int(reg[2]) > 0:
            instruction.append(bin((int(reg[2]) * -1) & (2 ** 16 - 1))[2:].zfill(16))
        else:
            instruction.append(bin(int(reg[2]) * -1)[2:].zfill(16))
    # load immediate instruction--------------------------------------------------------------
    elif lines[i].strip()[:2] == "li":
        reg = lines[i].strip()[2:].split(",")
        if len(reg) != 2:
            print("error in line %d" % (i + 1))
            exit()

        reg[0] = reg[0].strip()
        reg[1] = reg[1].strip()
        if reg[0][0] == R or reg[0][0] == r:
            reg[0] = reg[0][1:]
        else:
            print("no register found as %s error in line %d" % (reg[0], i + 1))
            exit()
        opcode = 14
        instruction.append(bin(opcode)[2:].zfill(6))
        instruction.append((bin(int(reg[0]))[2:].zfill(5)))
        instruction.append((bin(0)[2:].zfill(5)))
        if int(reg[1]) < 0:
            instruction.append(bin(int(reg[1]) & (2 ** 16 - 1))[2:].zfill(16))
        else:
            instruction.append(bin(int(reg[1]))[2:].zfill(16))
        # instruction move---------------------------------------------------------------
    elif lines[i].strip()[:3] == "mr ":
        reg = lines[i].strip()[3:].split(",")
        if len(reg) != 2:
            print("not valid instruction in line %d" % (i + 1))
            exit()
        for j in range(2):
            reg[j] = reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
            else:
                print("no register %s found error in line %d" % (reg[j], i + 1))
                exit()
        opcode = 31
        instruction.append(bin(opcode)[2:].zfill(6))
        instruction.append((bin(int(reg[1]))[2:].zfill(5)))
        instruction.append((bin(int(reg[0]))[2:].zfill(5)))
        instruction.append((bin(int(reg[1]))[2:].zfill(5)))
        XO = 444
        instruction.append(bin(XO)[2:].zfill(10))
        Rc = 0
        instruction.append(bin(Rc)[2:].zfill(1))
        # instruction load address-----------------------------------------------------------------------
    elif lines[i].strip()[:3] == 'la ':
        opcode = 50
        reg = lines[i].strip()[3:].split(',')
        if len(reg) == 2:
            reg[0] = reg[0].strip()
            if reg[0][0] == r or reg[0][0] == R:
                reg[0] = reg[0][1:]
            instruction.append(bin(opcode)[2:].zfill(6))
            instruction.append(bin(int(reg[0]))[2:].zfill(5))
            findnum(reg[1].strip())
            instruction.append(bin(int(j))[2:].zfill(21))



        elif lines[i].strip()[:3] == "la ":
            reg = lines[i].strip()[2:].split(",")
            if len(reg) != 3:
                print("error in line %d" % (i + 1))
                exit()

            reg[0] = reg[0].strip()
            if reg[0][0] == R or reg[0][0] == r:
                reg[0] = reg[0][1:]
            else:
                print("no register found as %s error in line %d" % (reg[0], i + 1))
                exit()
            opcode = 14
            reg1 = reg[1].strip().split("(")
            reg1[0] = reg1[0].strip()
            if reg1[1].strip()[0] == R or reg1[1].strip()[0] == r:
                reg1[1] = reg1[1].strip()[1:-1]
            else:
                print("no register found as %s error in line %d" % (reg1[1], i + 1))
                exit()
            instruction.append(bin(opcode)[2:].zfill(6))
            instruction.append((bin(int(reg[0]))[2:].zfill(5)))
            instruction.append((bin(int(reg1[1]))[2:].zfill(5)))
            if int(reg1[0]) < 0:
                instruction.append(bin(int(reg1[0]) & (2 ** 16 - 1))[2:].zfill(16))
            else:
                instruction.append(bin(int(reg1[0]))[2:].zfill(16))

    elif lines[i].strip()[:4] == 'beq ' or lines[i].strip()[:4] == 'bne ':
        if lines[i].strip()[:4] == 'beq ':
            opcode = 60
        else:
            opcode=61
        lines[i] = lines[i].strip()
        reg = lines[i][3:].strip().split(',')
        if len(reg) != 3:
            print("error in line %d " % (i + 1))
            exit()
        for j in range(2):
            reg[j] = reg[j].strip()
            if reg[j][0] == R or reg[j][0] == r:
                reg[j] = reg[j][1:]
            else:
                print("error in line %d " % (i + 1))
        instruction.append(bin(int(opcode))[2:].zfill(6))
        instruction.append(bin(int(reg[0]))[2:].zfill(5))
        instruction.append(bin(int(reg[1]))[2:].zfill(5))
        findlabel(reg[2].strip())
        if j-i-1>0:
            instruction.append(bin(j-i-1)[2:].zfill(16))
        else:
            instruction.append(bin((j-i-1)& 2**16-1)[2:])
#system call----------------------------------------------------
    elif lines[i].strip()[:2] == 'sc':
        opcode = 17
        reg = lines[i].strip()[2:]
        reg = reg.strip()
        if (int(reg) < 0):
            print('error in instruction sc')
        else:
            instruction.append(bin(opcode)[2:].zfill(6))
            instruction.append(bin(0)[2:].zfill(14))
            instruction.append(bin(int(reg))[2:].zfill(7))
            instruction.append(bin(0)[2:].zfill(3))
            instruction.append(bin(1)[2:].zfill(1))
            instruction.append(bin(0)[2:].zfill(1))

    # ---------------------------------------------------------------------------------------------------------

    if len("".join(instruction)):
        objf.write("".join(instruction))
        #print(instruction)
        objf.write('\n')
    i = i + 1
file.close()
objf.close()
symf.close()
datafile.close()
print("done with assembling\n")
#---------------------------------------------------------------------------------------------------------
#uPower-ISA simulator
reg_files=[]
for i in range(32):
    reg_files.append(0)
regcr='0'
reg_files[28]=int(gp,16)
datafile=open("datafile","r+")
symf=open("symboltable","r+")
sym_lines=symf.readlines()
dataline=datafile.readline()
data_addr=0x10000000
#instruction functions------------------------
def add(instruction):
    reg_files[int(instruction[6:11],2)]=reg_files[int(instruction[11:16],2)]+reg_files[int(instruction[16:21],2)]
    return

def addi(instruction):
    if int(instruction[16])==0:
        reg_files[int(instruction[6:11],2)]=reg_files[int(instruction[11:16],2)]+int(instruction[16:],2)
    elif int(instruction[16])==1:
        reg_files[int(instruction[6:11], 2)] = reg_files[int(instruction[11:16], 2)] +int(instruction[17:], 2)-2**15
    return
def andi(instruction):
    reg_files[int(instruction[11:16], 2)]=(reg_files[int(instruction[6:11], 2)]&reg_files[int(instruction[16:], 2)])
    return
def andinstruction(instruction):
    reg_files[int(instruction[11:16],2)]=reg_files[int(instruction[6:11],2)]&reg_files[int(instruction[16:21],2)]
    return
def ori(instruction):
    reg_files[int(instruction[11:16], 2)   ]=reg_files[int(instruction[6:11],2)]| int(instruction[16:],2)
def subf(instruction):
    reg_files[int(instruction[6:11], 2)] = reg_files[int(instruction[16:21], 2)]-reg_files[int(instruction[11:16], 2)]
def orinstruction(instruction):
    reg_files[int(instruction[11:16],2)]=reg_files[int(instruction[6:11],2)]|reg_files[int(instruction[16:21],2)]
    return
def cmp(instruction):
    a=reg_files[int(instruction[11:16],2)]
    b=reg_files[int(instruction[16:21],2)]
    if a<b:
        c=8
    elif a>b:
        c=4
    else:
        c=2
    global regcr
    regcr=int(c)
def bc(instruction):
    if(reg_files[int(instruction[6:11],2)]==reg_files[int(instruction[11:16],2)]):
        global k
        if int(instruction[16])==0:
            k=k+int(instruction[17:],2)-2**15*int(instruction[16])
        else:
            k = k + int(instruction[17:], 2) - 2 ** 15 * int(instruction[16])+1
        print(i)
def lwz(instruction):
    global reg_files
    global data_addr
    global dataline
    datafile.seek(0,0)
    dataline=datafile.readline()
    stadd=int(reg_files[int(instruction[11:16],2)])+int(instruction[17:],2)-(2**15)* int(instruction[16])-data_addr
    try:
        if int(dataline[8*stadd])==0:
            reg_files[int(instruction[6:11],2)]=int(dataline[8*stadd:8*stadd+32],2)
        else:
            reg_files[int(instruction[6:11], 2)] = int(dataline[8 * stadd+1:8 * stadd + 32], 2)-int(2**31)*int(dataline[8*stadd])
    except:
        print('except in loading')
        exit()
        if stadd in datadic:
            if int(dataline[8 * stadd]) == 0:
                reg_files[int(instruction[6:11], 2)] = int(dataline[8 * stadd:8 * stadd + 32], 2)
            else:
                reg_files[int(instruction[6:11], 2)] = int(dataline[8 * stadd + 1:8 * stadd + 32], 2) - int(
                    2 ** 31) * int(dataline[8 * stadd])
        else:
            print('error in loading')

def lav(instruction):
    global reg_files
    global i
    temp=sym_lines[int(instruction[11:],2)].split(' ')
    reg_files[int(instruction[6:11],2)]=temp[1].strip()
'''
def bne(instruction):
    if (reg_files[int(instruction[6:11], 2)] != reg_files[int(instruction[11:16], 2)]):
        glob[1].strip()
'''
def bne(instruction):
    if (reg_files[int(instruction[6:11], 2)] != reg_files[int(instruction[11:16], 2)]):
        global  k
        if int(instruction[16]) == 0:
            k = k + int(instruction[17:], 2) - 2 ** 15 * int(instruction[16])
        else:
            k = k + int(instruction[17:], 2) - 2 ** 15 * int(instruction[16]) + 1
        print(k)
def stw(instruction):
    si=int(instruction[17:],2)-2**15 * int(instruction[16])
    EA=int(int(reg_files[int(instruction[11:16],2)])+int(si))
    EA=EA-data_addr

    try:
        datafile.seek(8 * EA, 0)
        if int(reg_files[int(instruction[6:11],2)])>=0:
            string=bin(int(reg_files[int(instruction[6:11],2)]))[2:].zfill(32)
        else:
            string = bin(int(reg_files[int(instruction[6:11], 2)])&(2**32-1))[2:]
        datafile.write(string)
    except:
        print('except')
        if int(reg_files[int(instruction[6:11],2)])>=0:
            string=bin(int(reg_files[int(instruction[6:11],2)]))[2:].zfill(32)
        else:
            string = bin(int(reg_files[int(instruction[6:11], 2)])&(2**32-1))[2:]
        datadic[EA]=string
        print(datadic)
def lhz(instruction):
    global reg_files
    global data_addr
    global dataline
    stadd=int(reg_files[int(instruction[11:16],2)])+int(instruction[17:],2)-(2**15)* int(instruction[16])-data_addr
    reg_files[int(instruction[6:11],2)]=int(dataline[8*stadd:8*stadd+16],2)
def lha(instruction):
    global reg_files
    global data_addr
    global dataline
    stadd=int(reg_files[int(instruction[11:16],2)])+int(instruction[17:30],2)-(2**15)* int(instruction[16])-data_addr
    reg_files[int(instruction[6:11],2)]=int(dataline[8*stadd:8*stadd+16],2)
def bca(instruction):
    global regcr
    global k
    if(int(instruction[11:16],2)==28) and regcr==4:
        if int(instruction[16])==0:
            k = k+int(instruction[17:30],2)-2**13*int(instruction[16])
        else:
            k = k + int(instruction[17:30], 2) - 2 ** 13 * int(instruction[16])+1
    elif (int(instruction[11:16], 2) == 29) and regcr == 8:
        if int(instruction[16]) == 0:
            k = k + int(instruction[17:30], 2) - 2 ** 13 * int(instruction[16])
        else:
            k = k + int(instruction[17:30], 2) - 2 ** 13 * int(instruction[16]) + 1
    elif (int(instruction[11:16], 2) == 30) and regcr == 2:
        if int(instruction[16]) == 0:
            k = k + int(instruction[17:30], 2) - 2 ** 13 * int(instruction[16])
        else:
            k = k + int(instruction[17:30], 2) - 2 ** 13 * int(instruction[16]) + 1
def asciiz(instruction):
    temp = int(reg_files[18])
    global data_addr
    temp = temp -data_addr
    datafile.seek(0, 0)
    dataline = datafile.readline()
    while(int(dataline[8 * temp:8 * temp + 8], 2) != 0):
        print(chr(int(dataline[8 * temp:8 * temp + 8], 2)),end='')
        temp = temp + 1
    print('')

#---------------------------------------------------------------------------------------------

#decoding opcode------------------------------------------------------------------------------
def decoderfunc(instruction):
    if not len(instruction):
        return
    elif int(instruction[0:6],2)==31 and int(instruction[21:31],2)==266:
        add(instruction)
    elif int(instruction[0:6],2)==14:
        addi(instruction)
    elif int(instruction[0:6],2)==28:
        andi(instruction)
    elif int(instruction[0:6], 2) == 31 and int(instruction[21:31], 2) == 28:
        andinstruction(instruction)
    elif int(instruction[0:6],2)==24:
        ori(instruction)
    elif int(instruction[0:6],2)==31 and int(instruction[21:31],2)==40:
        subf(instruction)
    elif int(instruction[0:6], 2) == 31 and int(instruction[21:31], 2) == 444:
        orinstruction(instruction)
    elif int(instruction[0:6], 2) == 31 and int(instruction[31]) == 1 and int(instruction[21:31]) == 0:
        cmp(instruction)
    elif int(instruction[0:6], 2) == 60:
        bc(instruction)
    elif int(instruction[0:6], 2) == 32:
        lwz(instruction)
    elif int(instruction[0:6],2)==50:
        lav(instruction)
    elif int(instruction[0:6],2)==61:
        bne(instruction)
    elif int(instruction[0:6],2)==36:
        stw(instruction)
    elif int(instruction[0:6], 2) == 40:
        lhz(instruction)
    elif int(instruction[0:6], 2) == 42:
        lha(instruction)
    elif int(instruction[0:6], 2) == 19 and int(instruction[30], 2) == 1 and int(instruction[31], 2) == 0:
        bca(instruction)
    elif int(instruction[0:6], 2) == 17 and int(instruction[20:27], 2) == 4:
        asciiz(instruction)
#---------------------------------------------------------------------------------------------
def print_registers(ins):
    i=0
    while(i<32):
        for j in range(8):
            print("reg[%2d]=%d "%(i+j,int(reg_files[i+j])),end='')
        print("")
        i=i+8
    print('regcr= %d'%(int(regcr)),end=' ')
    print('gp=',gp,' ','stp=',stp,' ','pc=',hex(int(pc,16)+4*ins))
f=open("objectfile","r")
instructions=f.readlines()
i=0
k=0
while i<len(instructions):
    k=0
    ch=int(input('enter 1 to execute all instructions\nenter 2 to execute few instructions\nenter 3 to execute one instruction\nenter 4 to quit\n'))
    if ch==1:
        no=int(len(instructions))-i
    elif ch==2:
        no=int(input('enter number of instructions to execute'))
    elif ch==3:
        no=1
    elif ch==4:
        exit()
    k=0
    while k<no:
        decoderfunc(instructions[i+k])
        #print(instructions[i+k])
        datafile.seek(0,0)
        dataline=datafile.readline()
        k=k+1
    i = i + no
    print_registers(i)
    print('')
f.close()
