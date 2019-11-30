import pyvjoy
from time import sleep
import serial

# Constants
NUMFRAMES = 4  # Number of bytes to capture

# Create joystick object
Joystick = pyvjoy.VJoyDevice(1)
Joystick2 = pyvjoy.VJoyDevice(2)

# Customize Parameters
# Ask for Input
print("Serial Joystick V1 - ELEX 7820")
numCtrl = input("How many controllers to connect? (MAX:2): ")
COM_LIST = []

for i in range(int(numCtrl)):
    print("Controller ", i)
    COM_PORT = input("Enter Com Port:")
    COM_LIST.append(COM_PORT)

print("Connecting...")

s = serial.Serial(COM_LIST[0], baudrate=9600)

if numCtrl == 2:
    s2 = serial.Serial(COM_LIST[1], baudrate=9600)

for com in COM_LIST:
    print("Connected to: ", com)




# B, X, RB, LB, Start, Select
FaceButtons = [2, 3, 6, 5, 8, 7]

# Up, Down, Left, Right, A, Y
DPad = [9, 10, 11, 12, 1, 4]


def SendCommands(res, Joy):
    # Slice response into separate frames

    FrameA = res[:1]
    FrameB = res[1:2]
    X = res[2:3]
    Y = res[3:4]

    # Read all the data

    Face, DRaw = bin(int.from_bytes(FrameA, "big")), bin(int.from_bytes(FrameB, "big"))
    dataX, dataY = int.from_bytes(X, "big"), int.from_bytes(Y, "big")

    # Slice DPad

    for Dir in range(len(DPad)):

        if DRaw[Dir + 4] == '1':
            Joy.set_button(DPad[Dir], 1)
        else:
            Joy.set_button(DPad[Dir], 0)

    # Slice Buttons

    for Command in range(len(FaceButtons)):

        if Face[Command + 4] == '1':

            Joy.set_button(FaceButtons[Command], 1)

        else:

            Joy.set_button(FaceButtons[Command], 0)

    # Map joystick axes

    Joy.set_axis(pyvjoy.HID_USAGE_X, dataX * 128)

    Joy.set_axis(pyvjoy.HID_USAGE_Y, dataY * 128)

    # Print to screen
    output = ("F: ", Face, "| D: ", DRaw, "| J: X: ", dataX, "| Y: ", dataY)

    return output

while True:
    res = s.read(NUMFRAMES)
    res2 = s2.read(NUMFRAMES)

    output1 = SendCommands(res, Joystick)
    output2 = SendCommands(res2, Joystick2)
    #print(output1, output2)
