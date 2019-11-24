import time
import serial
import gpiozero

l1 = 4
l2 = 17
l3 = 27

led1 = gpiozero.LED(l1)
led2 = gpiozero.LED(l2)
led3 = gpiozero.LED(l3)

led1_state = False
led2_state = False
led3_state = False

buffer = []

ser = serial.Serial(port='/dev/ttyS0',
                    baudrate=9600,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=None)

while True:
        try:
            if ser.isOpen():
                ser.flushInput()
                ser.flushOutput()

                data = ser.read()
                data = data.decode()

                if data=='1':
                    if led1_state==False:
                        led1.on()
                        print('Led1 is On')
                        led1_state=True
                    else:
                        led1.off()
                        print('Led1 is Off')
                        led1_state=False
                elif data=='2':
                    if led2_state==False:
                        led2.on()
                        print('Led2 is On')
                        led2_state=True
                    else:
                        led2.off()
                        print('Led2 is Off')
                        led2_state=False
                elif data=='3':
                    if led3_state==False:
                        led3.on()
                        print('Led3 is On')
                        led3_state=True
                    else:
                        led3.off()
                        print('Led3 is Off')
                        led3_state=False
                elif data=='O':
                    if len(buffer)==0:
                        buffer.append(data)
                elif data=='N':
                    if len(buffer)==1:
                        if buffer[0]=='O':
                            buffer.append(data)
                            print(buffer[0]+buffer[1])
                            del buffer[:]
                elif data=='F':
                    if len(buffer)==1:
                        if buffer[0]=='O':
                            buffer.append(data)
                    elif len(buffer)==2:
                        if buffer[0]=='O' and buffer[1]=='F':
                            buffer.append(data)
                            print(buffer[0]+buffer[1]+buffer[2])
                            del buffer[:]
                elif data=='b':
                    if len(buffer)==0:
                        buffer.append(data)
                elif data =='l':
                    if len(buffer)==1 and buffer[0]=='b':
                        buffer.append(data)
                elif data =='i':
                    if len(buffer)==2 and buffer == ['b','l']:
                        buffer.append(data)
                elif data =='n':
                    if len(buffer)==3 and buffer == ['b','l','i']:
                        buffer.append(data)
                elif data =='k':
                    if len(buffer)==4 and buffer == ['b','l','i','n']:
                        buffer.append(data)
                        if buffer == ['b','l','i','n','k']:
                            print('led blinking..')
                            for i in range(5):
                                    led1.on()
                                    time.sleep(.5)
                                    led.1.off()
                                    time.sleep(.5)
                            del buffer[:]
                
        except KeyboardInterrupt:
            pass
