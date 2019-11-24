#!/usr/bin/python
import sys
import time
import serial
import gpiozero

def receiveDataOverSerialPort():
    led1 = gpiozero.LED(4)
    led2 = gpiozero.LED(17)
    led3 = gpiozero.LED(27)
    led1_state = False
    led2_state = False
    led3_state = False
    buffer = []
    
    ser = serial.Serial(port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1)

    print('[serialPrinter]: Trying to send data over serial port...')

    if ser.isOpen():
        try:
            while True:
                ser.flushInput()
                ser.flushOutput()
                data = ser.read()
                print(data)
                if data != b'' and data != b'\r':
                    if data == b'1':
                        if led1_state == False:
                            led1.on()
                            print('LED 1 is ON')
                            led1_state = True
                        elif led1_state == True:
                            led1.off()
                            print('LED 1 is OFF')
                            led1_state = False
                    elif data == b'2':
                        if led2_state == False:
                            led2.on()
                            print('LED 2 is ON')
                            led2_state = True
                        elif led2_state == True:
                            led2.off()
                            print('LED 2 is OFF')
                            led2_state = False
                    elif data == b'3':
                        if led3_state == False:
                            led3.on()
                            print('LED 3 is ON')
                            led3_state = True
                        elif led3_state == True:
                            led3.off()
                            print('LED 3 is OFF')
                            led3_state = False
                    #ON / OFF
                    elif data == b'O':
                        if data not in buffer:
                            buffer.append(data)
                    elif data == b'N':
                        if b'O' in buffer:
                            buffer.append(data)
                            buffer = [str(buffer[i]) for i in range(len(buffer))]
                            on = buffer[0]+buffer[1]
                            print(on)
                            if on == "b'O'b'N'":
                                led1.on()
                                led2.on()
                                led3.on()
                                print('ALL LED are ON')
                                buffer.clear()
                    elif data == b'F':
                        if b'O' in buffer:
                            buffer.append(data)
                            if len(buffer) == 3:
                                buffer = [str(buffer[i]) for i in range(len(buffer))]
                                off = buffer[0]+buffer[1]+buffer[2]
                                if off == "b'O'b'F'b'F'":
                                    led1.off()
                                    led2.off()
                                    led3.off()
                                    print('All LED are OFF')
                                    buffer.clear()
                    elif data == b'b':
                        buffer.append(data)
                    elif data == b'l':
                        buffer.append(data)
                    elif data == b'i':
                        buffer.append(data)
                    elif data == b'n':
                        buffer.append(data)
                    elif data == b'k':
                        buffer.append(data)
                        if len(buffer) == 5:
                                buffer = [str(buffer[i]) for i in range(len(buffer))]
                                blink = buffer[0]+buffer[1]+buffer[2]+buffer[3]+buffer[4]
                                if blink == "b'b'b'l'b'i'b'n'b'k'":
                                    for i in range(3):
                                        led1.on()
                                        time.sleep(1)
                                        led1.off()
                                        time.sleep(1)
                                    print('blinked')
                                    buffer.clear()
                    else:
                        buffer.clear()
                            
                        
        except Exception as e1:
            logMsg ='[serialPrinter]: Communication error...:' + str(e1)
            print(logMsg)
    else:
        print('cannot open port')

if __name__ == "__main__":
    receiveDataOverSerialPort()
