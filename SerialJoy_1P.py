import pyvjoy
import serial
# Alpha 1

# Constants
NUMFRAMES = 4  # Number of bytes to capture

# Create joystick object
Joystick = pyvjoy.VJoyDevice(1)


# Customize Parameters
# Ask for Input
print("Serial Joystick V1 - ELEX 7820")
print("Dual Control Mode")
COM_LIST = []

COM1 = input("Enter Controller 1 port: ")

print("Connecting...")

s = serial.Serial(COM1, baudrate=9600)

print("Connected to: ", COM1)

print("Sending to vJoy")


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
    if len(DRaw) == 10 and DRaw[2] == '1' and DRaw[3] == '1':
        for Dir in range(len(DPad)):

            if DRaw[Dir + 4] == '1':
                Joy.set_button(DPad[Dir], 1)
            else:
                Joy.set_button(DPad[Dir], 0)

    # Slice Buttons

    if len(Face) == 10 and DRaw[2] == '1' and DRaw[3] == '1':
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
    res = s.read_until()

    output1 = SendCommands(res, Joystick)
    #print(output1, output2)
