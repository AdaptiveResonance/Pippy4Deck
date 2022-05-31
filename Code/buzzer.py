#buzzer2.py
#!/usr/bin/python3

#Libraries
import RPi.GPIO as GPIO
from time import sleep

#Disable warnings
GPIO.setwarnings(False)
#Select GPIO mode
GPIO.setmode(GPIO.BOARD)
buzzer=29 

def setup():  
    GPIO.setup(buzzer,GPIO.OUT)

def shorter():
    GPIO.output(buzzer,GPIO.HIGH)
    sleep(0.3) # Delay in seconds
    GPIO.output(buzzer,GPIO.LOW)
    sleep(0.3)
    GPIO.output(buzzer,GPIO.HIGH)
    sleep(0.3) # Delay in seconds
    GPIO.output(buzzer,GPIO.LOW)
    sleep(0.3)
    GPIO.output(buzzer,GPIO.HIGH)
    sleep(0.3) # Delay in seconds
    GPIO.output(buzzer,GPIO.LOW)
    sleep(0.3)
def longer():
    GPIO.output(buzzer,GPIO.HIGH)
    sleep(0.5) # Delay in seconds
    GPIO.output(buzzer,GPIO.LOW)
    sleep(0.5)
    GPIO.output(buzzer,GPIO.HIGH)
    sleep(0.5) # Delay in seconds
    GPIO.output(buzzer,GPIO.LOW)
    sleep(0.5)
    GPIO.output(buzzer,GPIO.HIGH)
    sleep(0.5) # Delay in seconds
    GPIO.output(buzzer,GPIO.LOW)
    sleep(0.5)

def buzz():
    shorter()
    longer()
    shorter()

if __name__=='__main__':
    setup()
    buzz()