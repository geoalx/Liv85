import sys
import re

if(len(sys.argv)<=1):
    raise Exception("file not inserted")
elif(sys.argv[1][-4:] != ".asm"):
    raise Exception("file not supported or empty")

with open(sys.argv[1],"r") as f:
    instr = f.readlines()

def ishex(ch):
    if((ch[0]<="9" and ch[0]>="0") or (ch[0]<="F" and ch[0]>="A")):
        if((ch[1]<="9" and ch[1]>="0") or (ch[1]<="F" and ch[1]>="A")):
            return True
    return False

def fhex(n):
    num = hex(n)
    if(len(num)<6):
        zer = '0'*(6-len(num))
        return zer+num[2:]
    return num[2:]

def rhex(r):
    if(r=="A"):
        return int('111',2)
    elif(r=="B"):
        return int('000',2)
    elif(r=="C"):
        return int('001',2)
    elif(r=="D"):
        return int('010',2)
    elif(r=="E"):
        return int('011',2)
    elif(r=="H"):
        return int('100',2)
    elif(r=="L"):
        return int('101',2)
    elif(r=="M"):
        return int('110',2)
    raise Exception("Wrong Register")


def assemble(f):
    reg = "ABCDEHL"
    bit = []
    cnt = 1
    labels = {}
    for x in f:
        if(x=="\n"):
            cnt += 1
            continue
        print(x[:-1])
        if(x[0:4] == "MOV " and x[5]==","):
            if(x[4] in reg or x[4]=="M"):
                if(x[6] in reg and x[6]!=x[4] or x[6]=="M"):
                    bit.append(int('01000000',2)+(rhex(x[4])<<3)+rhex(x[6]))
                else:
                    raise Exception(f"LINE {cnt} MOV {x[4]},HERE({x[6]})")
            else:
                raise Exception(f"LINE {cnt} MOV HERE({x[4]})")
        elif(x[0:4] == "MVI " and x[5]==","):
            if(x[4] in reg or x[4]=="M"):
                if(ishex(x[6:8]) and x[8]=="H"):
                    bit.append(int('00000000',2)+(rhex(x[4])<<3)+int('00000110',2))
                    bit.append(int(x[6:8],16))
                else:
                    raise Exception(f"LINE {cnt} MVI {x[4]},HERE({x[6:8]})")
            else:
                raise Exception(f"LINE {cnt} MVI HERE({x[4]})")
        elif(x[0:2]=="EI" and x[2:4]=="\n"):
            bit.append(int('11111011',2))
        elif(x[0:2]=="DI" and x[2:4]=="\n"):
            bit.append(int('11110011',2))
        elif(x[0:3]=="HLT" and x[3:5]=="\n"):
            bit.append(int('01110110',2))
        elif(x[0:3]=="RIM" and x[3:5]=="\n"): #ONLY ON 8085AH
            bit.append(int('00100000',2))
        elif(x[0:3]=="SIM" and x[3:5]=="\n"): #ONLY ON 8085AH
            bit.append(int('00110000',2))
        elif(x[0:3]=="NOP" and x[3:5]=="\n"):
            bit.append(0)
        elif(x[0:3]=="RLC" and x[3:5]=="\n"):
            bit.append(int('00000111',2))
        elif(x[0:3]=="RRC" and x[3:5]=="\n"):
            bit.append(int('00001111',2))
        elif(x[0:3]=="RAL" and x[3:5]=="\n"):
            bit.append(int('00010111',2))
        elif(x[0:3]=="RAR" and x[3:5]=="\n"):
            bit.append(int('00011111',2))
        elif(x[0:3]=="CMA" and x[3:5]=="\n"):
            bit.append(int('00101111',2))
        elif(x[0:3]=="STC" and x[3:5]=="\n"):
            bit.append(int('00110111',2))
        elif(x[0:3]=="CMC" and x[3:5]=="\n"):
            bit.append(int('00111111',2))
        elif(x[0:3]=="DAA" and x[3:5]=="\n"):
            bit.append(int('00100111',2))
        elif(x[0:4]=="LXI " and x[5]==","):
            if(x[4]=="B"):
                bit.append(1)
            elif(x[4]=="D"):
                bit.append(int('00010001',2))
            elif(x[4]=="H"):
                bit.append(int('00100001',2))
            else:
                raise Exception(f"LINE {cnt} LXI HERE({x[4]})")
            if(x[10]=="H" and ishex(x[6:8]) and ishex(x[8:10])):
                bit.append(int(x[8:10],16))
                bit.append(int(x[6:8],16))
            else:
                raise Exception(f"LINE {cnt} LXI {x[4]},HERE({x[6:10]})")
        elif(x[0:5]=="STAX "):
            if(x[5]=="B"):
                bit.append(2)
            elif(x[5]=="D"):
                bit.append(int('00010010',2))
            else:
                raise Exception(f"LINE {cnt} STAX HERE({x[5]})")
        elif(x[0:5]=="LDAX "):
            if(x[5]=="B"):
                bit.append(int('00101010',2))
            elif(x[5]=="D"):
                bit.append(int('00011010',2))
            else:
                raise Exception(f"LINE {cnt} LDAX HERE({x[5]})")
        elif(x[0:4]=="STA " and ishex(x[4:6]) and ishex(x[6:8]) and x[8]=="H"):
            bit.append(int('00110010',2))
            bit.append(int(x[6:8],16))
            bit.append(int(x[4:6],16))
        elif(x[0:4]=="LDA " and ishex(x[4:6]) and ishex(x[6:8]) and x[8]=="H"):
            bit.append(int('00111010',2))
            bit.append(int(x[6:8],16))
            bit.append(int(x[4:6],16))
        elif(x[0:5]=="SHLD " and ishex(x[5:7]) and ishex(x[7:9]) and x[9]=="H"):
            bit.append(int('00100010',2))
            bit.append(int(x[7:9],16))
            bit.append(int(x[5:7],16))
        elif(x[0:5]=="LHLD " and ishex(x[5:7]) and ishex(x[7:9]) and x[9]=="H"):
            bit.append(int('00101010',2))
            bit.append(int(x[7:9],16))
            bit.append(int(x[5:7],16))
        elif(x[0:4]=="XCHG"):
            bit.append(int('11101011',2))
        elif(x[0:5]=="PUSH "):
            if(x[5]=="B"):
                bit.append(int('11000101',2))
            elif(x[5]=="D"):
                bit.append(int('11010101',2))
            elif(x[5]=="H"):
                bit.append(int('11100101',2))
            elif(x[5:8]=="PSW"):
                bit.append(int('11110101',2))
            else:
                raise Exception(f"LINE {cnt} PUSH HERE({x[5]})")
        elif(x[0:4]=="POP "):
            if(x[4]=="B"):
                bit.append(int('11000001',2))
            elif(x[4]=="D"):
                bit.append(int('11010001',2))
            elif(x[4]=="H"):
                bit.append(int('11100001',2))
            elif(x[4:7]=="PSW"):
                bit.append(int('11110001',2))
            else:
                raise Exception(f"LINE {cnt} PUSH HERE({x[4]})")
        elif(x[0:4]=="XTHL"):
            bit.append(int('11100011',2))
        elif(x[0:4]=="SPHL"):
            bit.append(int('11111001',2))
        elif(x[:6]=="LXI SP"):
            bit.append(int('00110001',2))
        elif(x[0:4]=="INX "):
            if(x[4]=="B"):
                bit.append(3)
            elif(x[4]=="D"):
                bit.append(int('00010011',2))
            elif(x[4]=="H"):
                bit.append(int('00100011',2))
            elif(x[4:6]=="SP"):
                bit.append(int('00110011',2))
            else:
                raise Exception(f"LINE {cnt} INX HERE({x[4]})")
        elif(x[0:4]=="DCX "):
            if(x[4]=="B"):
                bit.append(int('00000011',2))
            elif(x[4]=="D"):
                bit.append(int('00011011',2))
            elif(x[4]=="H"):
                bit.append(int('00101011',2))
            elif(x[4:6]=="SP"):
                bit.append(int('00111011',2))
            else:
                raise Exception(f"LINE {cnt} DCX HERE({x[4]})")
        elif(x[0]<="Z" and x[0]>="A" and x[-2]==":"):
            labels[x[:-2]]=fhex(cnt)
        elif(x[0:4]=="JMP " and x[4:-1] in labels):
            bit.append(int('11000011',2))
            bit.append(int(labels[x[4:-1]][2:],16))
            bit.append(int(labels[x[4:-1]][:2],16))
        elif(x[0:3]=="JC " and x[3:-1] in labels):
            bit.append(int('11011010',2))
            bit.append(int(labels[x[3:-1]][2:],16))
            bit.append(int(labels[x[3:-1]][:2],16))
        elif(x[0:4]=="JNC " and x[4:-1] in labels):
            bit.append(int('11010010',2))
            bit.append(int(labels[x[4:-1]][2:],16))
            bit.append(int(labels[x[4:-1]][:2],16))
        elif(x[0:3]=="JZ " and x[3:-1] in labels):
            bit.append(int('11001010',2))
            bit.append(int(labels[x[3:-1]][2:],16))
            bit.append(int(labels[x[3:-1]][:2],16))
        elif(x[0:4]=="JNZ " and x[4:-1] in labels):
            bit.append(int('11000010',2))
            bit.append(int(labels[x[4:-1]][2:],16))
            bit.append(int(labels[x[4:-1]][:2],16))
        elif(x[0:3]=="JP " and x[3:-1] in labels):
            bit.append(int('11110010',2))
            bit.append(int(labels[x[3:-1]][2:],16))
            bit.append(int(labels[x[3:-1]][:2],16))
        elif(x[0:3]=="JM " and x[3:-1] in labels):
            bit.append(int('11111010',2))
            bit.append(int(labels[x[3:-1]][2:],16))
            bit.append(int(labels[x[3:-1]][:2],16))
        elif(x[0:4]=="JPE " and x[4:-1] in labels):
            bit.append(int('11101010',2))
            bit.append(int(labels[x[4:-1]][2:],16))
            bit.append(int(labels[x[4:-1]][:2],16))
        elif(x[0:4]=="JPO " and x[4:-1] in labels):
            bit.append(int('11100010',2))
            bit.append(int(labels[x[4:-1]][2:],16))
            bit.append(int(labels[x[4:-1]][:2],16))
        elif(x[0:4]=="PCHL"):
            bit.append(int('11101001',2))
        elif(x[0:3]=="RET"):
            bit.append(int('11001001',2))
        elif(x[0:2]=="RC"):
            bit.append(int('11011000',2))
        elif(x[0:3]=="RNC"):
            bit.append(int('11010000',2))
        elif(x[0:2]=="RZ"):
            bit.append(int('11001000',2))
        elif(x[0:3]=="RNZ"):
            bit.append(int('11000000',2))
        elif(x[0:2]=="RP"):
            bit.append(int('11110000',2))
        elif(x[0:2]=="RM"):
            bit.append(int('11111000',2))
        elif(x[0:3]=="RPE"):
            bit.append(int('11101000',2))
        elif(x[0:3]=="RPO"):
            bit.append(int('11100000',2))
        elif(x[0:5]=="CALL " and x[5:-1] in labels):
            bit.append(int('11001101',2))
            bit.append(int(labels[x[5:-1]][2:],16))
            bit.append(int(labels[x[5:-1]][:2],16))
        elif(x[0:3]=="CC " and x[3:-1] in labels):
            bit.append(int('11011100',2))
            bit.append(int(labels[x[3:-1]][2:],16))
            bit.append(int(labels[x[3:-1]][:2],16))
        elif(x[0:4]=="CNC " and x[4:-1] in labels):
            bit.append(int('11010100',2))
            bit.append(int(labels[x[4:-1]][2:],16))
            bit.append(int(labels[x[4:-1]][:2],16))
        elif(x[0:3]=="CZ " and x[3:-1] in labels):
            bit.append(int('11001100',2))
            bit.append(int(labels[x[3:-1]][2:],16))
            bit.append(int(labels[x[3:-1]][:2],16))
        elif(x[0:4]=="CNZ " and x[4:-1] in labels):
            bit.append(int('11000100',2))
            bit.append(int(labels[x[4:-1]][2:],16))
            bit.append(int(labels[x[4:-1]][:2],16))
        elif(x[0:3]=="CP " and x[3:-1] in labels):
            bit.append(int('11110100',2))
            bit.append(int(labels[x[3:-1]][2:],16))
            bit.append(int(labels[x[3:-1]][:2],16))
        elif(x[0:3]=="CM " and x[3:-1] in labels):
            bit.append(int('11111100',2))
            bit.append(int(labels[x[3:-1]][2:],16))
            bit.append(int(labels[x[3:-1]][:2],16))
        elif(x[0:4]=="CPE " and x[4:-1] in labels):
            bit.append(int('11101100',2))
            bit.append(int(labels[x[4:-1]][2:],16))
            bit.append(int(labels[x[4:-1]][:2],16))
        elif(x[0:4]=="CPO " and x[4:-1] in labels):
            bit.append(int('11100100',2))
            bit.append(int(labels[x[4:-1]][2:],16))
            bit.append(int(labels[x[4:-1]][:2],16))
        elif(x[0:4]=="RST " and x[4]>="0" and x[4]<="7"):
            temp = int(x[4])
            bit.append(int('11000111',2)+ (temp<<3))
        elif(x[0:3]=="IN " and ishex(x[3:5]) and x[5]=="H"):
            bit.append(int('11011011',2))
            bit.append(int(x[3:5],16))
        elif(x[0:4]=="OUT " and ishex(x[4:6]) and x[6]=="H"):
            bit.append(int('11010011',2))
            bit.append(int(x[4:6],16))
        elif(x[0:4]== "INR " and x[4] in reg or x[4]=="M"):
            bit.append(int('00000100',2) + (rhex(x[4])<<3))
        elif(x[0:4]=="DCR " and x[4] in reg or x[4]=="M"):
            bit.append(int('00000101',2)+ (rhex(x[4])<<3))
        elif(x[0:4]=="ADD " and x[4] in reg or x[4]=="M"):
            bit.append(int('10000000',2)+ rhex(x[4]))
        elif(x[0:4]=="ADC " and x[4] in reg or x[4]=="M"):
            bit.append(int('10001000',2)+ rhex(x[4]))
        elif(x[0:4]=="ADI " and ishex(x[4:6]) and x[6]=="H"):
            bit.append(int('11000110',2))
            bit.append(int(x[4:6],16))
        elif(x[0:4]=="ACI " and ishex(x[4:6]) and x[6]=="H"):
            bit.append(int('11001110',2))
            bit.append(int(x[4:6],16))
        elif(x[0:4]=="DAD "):
            if(x[4]=="B"):
                bit.append(int('00001001',2))
            elif(x[4]=="D"):
                bit.append(int('00011001',2))
            elif(x[4]=="H"):
                bit.append(int('00101001',2))
            elif(x[4:6]=="SP"):
                bit.append(int('00111001',2))
            else:
                raise Exception(f"LINE {cnt} DAD HERE({x[4]})")
        elif(x[0:4]=="SUB " and x[4] in reg or x[4]=="M"):
            bit.append(int('10010000',2) + rhex(x[4]))
        elif(x[0:4]=="SBB " and x[4] in reg or x[4]=="M"):
            bit.append(int('10011000',2) + rhex(x[4]))
        elif(x[0:4]=="SUI " and ishex(x[4:6]) and x[6]=="H"):
            bit.append(int('11010110',2))
            bit.append(int(x[4:6],16))
        elif(x[0:4]=="SBI " and ishex(x[4:6]) and x[6]=="H"):
            bit.append(int('11011110',2))
            bit.append(int(x[4:6],16))
        elif(x[0:4]=="ANA " and x[4] in reg or x[4]=="M"):
            bit.append(int('10100000',2) + rhex(x[4]))
        elif(x[0:4]=="XRA " and x[4] in reg or x[4]=="M"):
            bit.append(int('10101000',2)+ rhex(x[4]))
        elif(x[0:4]=="ORA " and x[4] in reg or x[4]=="M"):
            bit.append(int('10110000',2) + rhex(x[4]))
        elif(x[0:4]=="CMP " and x[4] in reg or x[4]=="M"):
            bit.append(int('10111000',2) + rhex(x[4]))
        elif(x[0:4]=="ANI " and ishex(x[4:6]) and x[6]=="H"):
            bit.append(int('11100110',2))
            bit.append(int(x[4:6],16))
        elif(x[0:4]=="XRI " and ishex(x[4:6]) and x[6]=="H"):
            bit.append(int('11101110',2))
            bit.append(int(x[4:6],16))
        elif(x[0:4]=="ORI " and ishex(x[4:6]) and x[6]=="H"):
            bit.append(int('11110110',2))
            bit.append(int(x[4:6],16))
        elif(x[0:4]=="CPI " and ishex(x[4:6]) and x[6]=="H"):
            bit.append(int('11111110',2))
            bit.append(int(x[4:6],16))
        else:
            raise Exception(f"LINE {cnt} Wrong Statement")

        cnt +=1
    print(*labels)
    return bit

ans = assemble(instr)
print(*ans)
