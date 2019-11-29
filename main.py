import serial
import keyboard

# Customize Parameters
COM = "COM5"  # Com Port
NUMFRAMES = 4  # Number of bytes to capture

print("Connecting...")
s = serial.Serial(COM)
print("Connected to -> ", COM)

# B, X, RB, LB, Start, Select
FaceButtons = ['c', 'v', 'e', 'q', 'z', 'x']

# Up, Down, Left, Right, A, Y
DPad = ['w', 's', 'a', 'd', 'f', 'g']

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
