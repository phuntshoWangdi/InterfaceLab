import RPi.GPIO as gpio
import gpiozero
import time
from datetime import datetime
import smtplib
#setup for sending email
def send_email():
    smtpUser = 'ad9689@gmail.com'
    stmpPass = '30286779'

    toAdd = 'aditya_raj01@hotmail.com'
    fromAdd = smtpUser

    subject = 'Intruder Detected!!!'
    header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
    body = 'INTRUDER!!!'

    sss = smtplib.SMTP('smtp.gmail.com',587)

    sss.ehlo()
    sss.starttls()
    sss.ehlo()
    sss.login(smtpUser, stmpPass)
    sss.sendmail(fromAdd, toAdd, header + '\n' + body)
    
    sss.quit()

pir_pin = 22
btn = 23
led = 4
mode = 'night_mode'
st = 10000.0
sent_flag = False
email_sent_time = 100000.0

def _setup():

    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(pir_pin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    gpio.setup(btn, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    gpio.setup(led, gpio.OUT, initial=gpio.LOW)

def mode_callback(c):
    global mode
    if mode == 'night_mode':
        print('alert_mode')
        mode = 'alert_mode'
    else:
        print('night_mode')
        mode = 'night_mode'

def sensor_callback(c):
    global st #starting time
    if mode == 'night_mode':
        st = time.process_time()
        #now = datetime.now() #variable to hold current time
        #ct = now.strftime('%H') #puts current time to ct
        ct = 18
        print('Current time: ',ct)
        
        if int(ct) >= 18 or int(ct) <= 6: #led only works between time 6pm-6
            print('Led will be turned On')
            start = time.process_time()
            gpio.output(led,gpio.HIGH)
            print('led is on')
        else:
            print('Led will not be turned On, because its still day time')
    
    elif mode == 'alert_mode':
        st = time.process_time()
        gpio.output(led,gpio.HIGH)
        #if sent_flag == False:
        print('Sending alert email...')
        send_email()
        print('email sent')
        #when email is sent sent_flag is set to true
        #to prevent spam
        #record the time of email sent

try:
    _setup()
    gpio.add_event_detect(btn, gpio.RISING, callback=mode_callback, bouncetime=300)
    gpio.add_event_detect(pir_pin, gpio.RISING, callback=sensor_callback, bouncetime=300)
    while 1:
        #it keeps the led on for 2 second and turns off
        if time.process_time()-st > 3:
            if gpio.input(led) == gpio.HIGH:
                gpio.output(led,gpio.LOW)
        #after 5 min sent_flag is set to false again
        #this allows to sent the email again after 5 min
        #if sent_flag == True:          

except KeyboardInterrupt:
    #release all the resources
    gpio.cleanup()

