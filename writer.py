from machine import Pin
import time
import sys

pina = []
pind = []
oe = Pin(4,Pin.OUT)
we = Pin(3,Pin.OUT)
we.on()
oe.on()
led = Pin(25,Pin.OUT)

addr_pin = [28,27,26,22,21,20,19,18,17,16,15]
data_pin = [7,8,9,10,11,12,13,14]

for i in data_pin:
    pind.append(Pin(i,Pin.OUT))

for i in addr_pin:
    pina.append(Pin(i,Pin.OUT))

with open("ask.txt") as f:
    data = f.readlines()

dbit = {}
for i in data:
    temp = i.split(':')
    dbit[temp[0]] = temp[1][:-2]
    
def delete():
    for i in range(1000):
        write(hex(i)[2:],"ff")

def normd(d):
    if(len(d)<10):
        return d[:2] + "0"*(10-len(d)) + d[2:]
    return d

def norma(a):
    if(len(a)<18):
        return a[:2] + "0"*(18-len(a)) + a[2:]
    return a
def topins(addr,data):
    bdata = normd(bin(int(data,16)))
    baddr = norma(bin(int(addr,16)))
    print((baddr,bdata))
    bit_addr = baddr[7:]
    for i in range(10,-1,-1):
        if(bit_addr[10-i]=='0'):
            pina[i].off()
        else:
            pina[i].on()
    bit_dat = bdata[2:]
    for i in range(7,-1,-1):
        if(bit_dat[7-i]=='0'):
            pind[i].off()
        else:
            pind[i].on()

def write(addr,data):
    topins(addr,data)
    led.toggle()
    we.toggle()
    time.sleep_us(1)
    we.toggle()
    led.toggle()

delete()
for key in dbit:
    write(key,dbit[key])
