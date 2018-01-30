import serial

ser = serial.Serial()
ser.baudrate = 19200
ser.port = ''
ser.open()
if ser.is_open:
    s = next(ser.read())
    print(s)
else :
    print("Port closed.. Or no such port present")
ser.close()

