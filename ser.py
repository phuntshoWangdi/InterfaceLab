import serial
import gpiozero

ser = serial.Serial(port='/dev/ttyS0',
                    baudrate=9600,
                    stopbits=serial.STOPBITS_ONE,
                    parity=serial.PARITY_NONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=None)
buffer = []
word=''
if ser.isOpen():
    try:
        while True:
            ser.flushInput()
            ser.flushOutput()
            data = ser.read()
            data = data.decode()
            if data != '\r':
                buffer.append(data)
            elif data=='\r':
                for i in range(len(buffer)):
                    word+=buffer[i]
                print(word)
                word=''
                del buffer[:]

    except KeyboardInterrupt:
        pass
