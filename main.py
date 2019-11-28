import pyvjoy
import serial

# Create joystick object
Joystick = pyvjoy.VJoyDevice(1)

# Customize Parameters
COM = "COM4"  # Com Port
NUMFRAMES = 4  # Number of bytes to capture

print("Connecting...")
s = serial.Serial(COM)
print("Connected to -> ", COM)

# B, X, RB, LB, Start, Select
FaceButtons = [2, 3, 6, 5, 8, 7]

# Up, Down, Left, Right, A, Y
DPad = [9, 10, 11, 12, 1, 4]

while True:
    res = s.read(NUMFRAMES)

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
        if DRaw[Dir+2] == '1':
            Joystick.set_button(DPad[Dir], 1)
        else:
            Joystick.set_button(DPad[Dir], 0)

    # Slice Buttons
    for Command in range(len(FaceButtons)):
        if Face[Command+2] == '1':
            Joystick.set_button(FaceButtons[Command], 1)
        else:
            Joystick.set_button(FaceButtons[Command], 0)

    # Map joystick axes
    Joystick.set_axis(pyvjoy.HID_USAGE_X, dataX * 128)
    Joystick.set_axis(pyvjoy.HID_USAGE_Y, dataY * 128)

    #Print to screen
    print("F: ", Face, "| D: ", DRaw, "| J: X: ", dataX, "| Y: ", dataY)
