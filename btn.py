import RPi.GPIO as gpio

btn =23
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(btn, gpio.IN, pull_up_down=gpio.PUD_DOWN)

while True:
    if gpio.input(btn)==gpio.HIGH:
        print('btn pressed')