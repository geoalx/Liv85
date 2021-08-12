def fhex(n):
    num = hex(n)
    if(len(num)<6):
        zer = '0'*(6-len(num))
        return zer+num[2:]
    return num[2:]

def labels(f):
    lab = {}
    cnt = 0
    for x in f:
        if(x[0]<="Z" and x[0]>="A" and x[-2]==":"):
            lab[x[:-2]]=fhex(cnt) 
        elif(x[0:3]=="MVI"):
            cnt+=2
        elif(x[0:3]=="LXI"):
            cnt+=3
        elif(x[0:3]=="STA"):
            cnt+=3
        elif(x[0:3]=="LDA"):
            cnt+=3
        elif(x[0:4]=="SHLD"):
            cnt+=3
        elif(x[0:4]=="LHLD"):
            cnt+=3
        elif(x[0:3]=="JMP" or x[0:3]=="JNZ" or x[0:3]=="JNC" or x[0:3]=="JPE" or x[0:3]=="JPO"):
            cnt+=3
        elif(x[0:2]=="JC" or x[0:2]=="JP" or x[0:2]=="JM" or x[0:2]=="JZ"):
            cnt+=3
        elif(x[0:4]=="CALL"):
            cnt+=3
        elif(x[0:3]=="CNC" or x[0:3]=="CNZ" or x[0:3]=="CPE" or x[0:3]=="CPO"):
            cnt+=3
        elif(x[0:2]=="CC" or x[0:2]=="CZ" or (x[0:2]=="CP" and x[2] != "I") or x[0:2]=="CM"):
            cnt+=3
        elif(x[0:2]=="IN" and x[2]!="R" and x[2]!="X"):
            cnt+=2
        elif(x[0:3]=="OUT"):
            cnt+=2
        elif(x[0:3]=="ADI"):
            cnt+=2
        elif(x[0:3]=="ACI"):
            cnt+=2
        elif(x[0:3]=="SBI" or x[0:3]=="SUI" or x[0:3]=="ANI" or x[0:3]=="XRI" or x[0:3]=="ORI" or x[0:3]=="CPI"):
            cnt+=2
        elif(x[0:4]==".ORG" and x[9]=="H"):
            cnt = int(x[5:9],16)
        elif(x=="\n"):
            continue
        else:
            cnt+=1
    return lab
        
