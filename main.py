import pyvjoy
import serial

# Create joystick object
Joystick = pyvjoy.VJoyDevice(1)

# Customize Parameters
COM = "COM5"  # Com Port
NUMFRAMES = 4  # Number of bytes to capture

print("Connecting...")
s = serial.Serial(COM)
print("Connected to -> ", COM)

while True:
    res = s.read(NUMFRAMES)

    # Slice response into separate frames
    FrameA = res[:1]
    FrameB = res[1:2]
    X = res[2:3]
    Y = res[3:4]

    Face, DPad = int.from_bytes(FrameA, "big"), int.from_bytes(FrameB, "big")
    dataX, dataY = int.from_bytes(X, "big"), int.from_bytes(Y, "big")

    print("F: ", Face, "| D: ", DPad, "| J: X: ", dataX, "| Y: ", dataY)

    # Map joystick axes
    Joystick.set_axis(pyvjoy.HID_USAGE_X, dataX * 128)
    Joystick.set_axis(pyvjoy.HID_USAGE_Y, dataY * 128)
