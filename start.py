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

def rhex(r):
    if(r=="A"):
        return int('000',2)
    elif(r=="B"):
        return int('001',2)
    elif(r=="C"):
        return int('010',2)
    elif(r=="D"):
        return int('011',2)
    elif(r=="H"):
        return int('100',2)
    elif(r=="L"):
        return int('101',2)
    elif(r=="M"):
        return int('110',2)
    raise Exception("Wrong Register")


def assemble(f):
    reg = "ABCDHL"
    bit = []
    cnt = 1
    for x in f:
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
        else:
            raise Exception(f"LINE {cnt} Wrong Statement")

        cnt +=1
    return bit

ans = assemble(instr)
print(*ans)
