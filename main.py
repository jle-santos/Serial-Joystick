#Accept serial commands and output Joystick
#Expecting four frames to receive from serial
import serial

#Customize Parameters
COM = "COM5"
NUMFRAMES = 2

print("Connecting...")
s = serial.Serial(COM)
print("Connected to -> ", COM)

while True:
    res = s.read(NUMFRAMES)

    #Slice response into separate frames
    X = res[:1]
    Y = res[1:2]

    dataX, dataY = int.from_bytes(X, "big"), int.from_bytes(Y, "big")

    print("Joystick Data: X: ",dataX, "| Y: ", dataY)

