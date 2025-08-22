import socket
from time import sleep
import threading
import json

# -------------------------------------------

import subprocess

# 🖱️ Move Mouse
def move_mouse(x, y):
    subprocess.run(["ydotool", "mousemove", f"-x {x}", f"-y {y}"])

# 🖱️ Left Mouse
def left_mouse_down():
    subprocess.run(["ydotool","click","0x40"])

def left_mouse_up():
    subprocess.run(["ydotool","click","0x80"])

# 🖱️ Right Mouse
def right_mouse_down():
    subprocess.run(["ydotool", "click", "0x41"])

def right_mouse_up():
    subprocess.run(["ydotool", "click", "0x81"])

# 🖱️ Scroll
def scroll_up():
    #no idea
    pass

def scroll_down():
    #no idea
    pass


# -------------------------------------------






def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

def getBroadcastAdd(ip):
    block = ip.split('.')
    return block[0]+'.'+block[1]+'.'+block[2]+'.255'

ip_server = getNetworkIp()
ip_broadcast = getBroadcastAdd(ip_server)
ECHO_PORT = 5560
SERVER_PORT = 5559
cursorSen = [1, 1]
scrollSen = [2, 2]

def echo():
    while(True):
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock2.bind((ip_broadcast, ECHO_PORT))
        sock2.sendto(b'x', ("255.255.255.255", ECHO_PORT))
        print('---- Sending echo ---')
        sock2.close()
        sleep(3)

def server():
    while(True):
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock1.bind((ip_server, SERVER_PORT))
        data, addr = sock1.recvfrom(1024)
        parseInputCommand(data)

def parseInputCommand(input):
    obj = json.loads(input)
    inputType = int(obj['dwFlags'])
    inputKeyboard = int(obj['type'])
    inputKeyboardKeyId= int(obj['wVk'])
    print(input)

    # --------------------
    # Keyboard settings here
    if inputKeyboard == 1:
        """
        inputType("dwFlags")
        inputType 0 -> Key Pressed
        inputType 2 -> Key Released

        obj["wVk"] -> KeyId

        Visit:
        /usr/include/linux/input-event-codes.h

        There is some keys and their ids,
        It's not same as this app ids,
        > this app: (a: 65)
        > input-event-codes.h: (a: 30)


        For example:
            > x = 45

        Then (45:1 and 45:0)
        - pressing "x":
            > subprocess.run(["ydotool", "key", "45:1"])
        - releasing "x"
            > subprocess.run(["ydotool", "key", "45:0"])
        """

        # use this for exporting keys ids into ./keys/app_key.py (manualy :D)
        # subprocess.run(["ydotool", "type", str(inputKeyboardKeyId)])

        pass
    # --------------------
    else:
        # move mouse
        if inputType == 1:
            xDisp = int(obj['dx']) * cursorSen[0]
            yDisp = int(obj['dy']) * cursorSen[1]

            move_mouse(xDisp, yDisp)

        # lmb down
        if inputType == 2:
            print('Left Mouse down')
            left_mouse_down()

        # lmb up
        if inputType == 4:
            print('Left Mouse up')
            left_mouse_up()

        # rmb down
        if inputType == 8:
            print('Right Mouse down')
            right_mouse_down()

        # rmb up
        if inputType == 16:
            print('Right Mouse up')
            right_mouse_up()

        # scroll
        if inputType == 4096:
            print('Scroll Mouse')
            if(obj["mouseData"]=="1"): # scroll up
                scroll_up()
            else:
                scroll_down()


x1 = threading.Thread(target=echo)
x2 = threading.Thread(target=server)

x1.start()
x2.start()


