from tkinter import *
import serial
import keyboard

global s

window = Tk()
window.title("Serial Joystick - V1")
window.geometry("500x500")

top_title = Label(window, text="Serial Joystick - 2019")
top_title.grid(column=0, row=0)

com_label = Label(window, text="Connect to COM:")
com_label.grid(column=0, row = 1)
com_status = Label(window, text="Not connected")
com_status.grid(column=3, row=1)
COM = Entry(window, width=10)
COM.grid(column=2, row=1)

def enter_com():
    s = serial.Serial(COM.get())

    if s.isOpen() == True:
        com_status.configure(text="Connected!")
    else:
        com_status.configure(window, text="Unavailable")

com_button = Button(window, text="Connect", command=enter_com)
com_button.grid(column=1, row = 1)

if s.isOpen():
    # B, X, RB, LB, Start, Select
    FaceButtons = ['c', 'v', 'e', 'q', 'z', 'x']

    # Up, Down, Left, Right, A, Y
    DPad = ['w', 's', 'a', 'd', 'f', 'g']

    while True:
        res = s.read(4)

        # Slice response into separate frames
        FrameA = res[:1]
        FrameB = res[1:2]
        X = res[2:3]
        Y = res[3:4]

        # Read all the data
        Face, DRaw = bin(int.from_bytes(FrameA, "big")), bin(int.from_bytes(FrameB, "big"))
        dataX, dataY = int.from_bytes(X, "big"), int.from_bytes(Y, "big")

        # Left Stick X
        if dataX > 200:
            keyboard.press('d')
        elif dataX < 100:
            keyboard.press('a')
        else:
            keyboard.release('a')
            keyboard.release('d')

        #Right Stick Y
        if dataY > 200:
            keyboard.press('w')
        elif dataY < 100:
            keyboard.press('s')
        else:
            keyboard.release('w')
            keyboard.release('s')

        for i, keyD in enumerate(DPad):
            if Face[i+4] == '1':
                keyboard.press(keyD)
            else:
                keyboard.release(keyD)

        for j, keyF in enumerate(FaceButtons):
            if DRaw[j+4] == '1':
                keyboard.press(keyF)
            else:
                keyboard.release(keyF)

        #Print to screen
        output = ("F: ", Face, "| D: ", DRaw, "| J: X: ", dataX, "| Y: ", dataY)

window.mainloop()
