#uPower-ISA simulator
reg_files=[]
for i in range(32):
    reg_files.append(0)
regcr='0'
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
    print('cmp')
    a=reg_files[int(instruction[11:16],2)]
    b=reg_files[int(instruction[16:21],2)]
    if a<b:
        c='1000'
    elif a>b:
        c='0100'
    else:
        c='0010'
    print(c)
    global regcr
    regcr=c
def bc(instruction):
    if(reg_files[int(instruction[6:11],2)]==reg_files[int(instruction[11:16],2)]):
        print('inside')
        global i
        if int(instruction[16])==0:
            i=i+int(instruction[17:],2)-2**15*int(instruction[16])
        else:
            i = i + int(instruction[17:], 2) - 2 ** 15 * int(instruction[16])+1
        print(i)
def lwz(instruction):
    global reg_files
    global data_addr
    global dataline
    datafile.seek(0,0)
    dataline=datafile.readline()
    stadd=int(reg_files[int(instruction[11:16],2)])+int(instruction[17:30],2)-(2**13)* int(instruction[16])-data_addr
    if int(dataline[8*stadd])==0:
        reg_files[int(instruction[6:11],2)]=int(dataline[8*stadd:8*stadd+32],2)
    else:
        reg_files[int(instruction[6:11], 2)] = int(dataline[8 * stadd+1:8 * stadd + 32], 2)-int(2**31)*int(dataline[8*stadd])
def lav(instruction):
    global reg_files
    global i
    temp=sym_lines[int(instruction[11:],2)].split(' ')
    reg_files[int(instruction[6:11],2)]=temp[1].strip()
def bne(instruction):
    if (reg_files[int(instruction[6:11], 2)] != reg_files[int(instruction[11:16], 2)]):
        glob[1].strip()
def bne(instruction):
    if (reg_files[int(instruction[6:11], 2)] != reg_files[int(instruction[11:16], 2)]):
        global  i
        if int(instruction[16]) == 0:
            i = i + int(instruction[17:], 2) - 2 ** 15 * int(instruction[16])
        else:
            i = i + int(instruction[17:], 2) - 2 ** 15 * int(instruction[16]) + 1
        print(i)
def stw(instruction):
    si=int(instruction[17:],2)-2**15 * int(instruction[16])
    EA=int(int(reg_files[int(instruction[11:16],2)])+int(si))
    EA=EA-data_addr
    print(int(reg_files[int(instruction[11:16],2)]))
    print("si EA are "+str(si)+' '+str(EA))
    datafile.seek(8*EA,0)
    if int(reg_files[int(instruction[6:11],2)])>=0:
        string=bin(int(reg_files[int(instruction[6:11],2)]))[2:].zfill(32)
    else:
        string = bin(int(reg_files[int(instruction[6:11], 2)])&(2**32-1))[2:]
    print(reg_files[int(instruction[6:11],2)])
    datafile.write(string)
def lhz(instruction):
    global reg_files
    global data_addr
    global dataline
    stadd=int(reg_files[int(instruction[11:16],2)])+int(instruction[17:30],2)-(2**15)* int(instruction[16])-data_addr
    reg_files[int(instruction[6:11],2)]=int(dataline[8*stadd:8*stadd+16],2)
def lha(instruction):
    global reg_files
    global data_addr
    global dataline
    stadd=int(reg_files[int(instruction[11:16],2)])+int(instruction[17:30],2)-(2**15)* int(instruction[16])-data_addr
    reg_files[int(instruction[6:11],2)]=int(dataline[8*stadd:8*stadd+16],2)

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
#---------------------------------------------------------------------------------------------
def print_registers():
    i=0
    while(i<32):
        for j in range(8):
            print("reg[%2d]=%d "%(i+j,int(reg_files[i+j])),end='')
        print("")
        i=i+8
    print('regcr= %d'%(int(regcr,2)))
f=open("objectfile","r")
instructions=f.readlines()
i=0
while i<(len(instructions)):
    decoderfunc(instructions[i])
    print(instructions[i])
    datafile.seek(0,0)
    dataline=datafile.readline()
    print_registers()
    print('')
    i=i+1
f.close()