import RPi.GPIO as GPIO
#import alarm
from Bodythermo import setColor
from buzzer import buzz
ledPin = 12 # define ledPin
buttonPinY = 37 # define buttonPin
buttonPinR = 35###
ledState = False
RGBState = False

def setup():
    GPIO.setmode(GPIO.BOARD) # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPin, GPIO.OUT) # set ledPin to OUTPUT mode
    GPIO.setup(buttonPinY, GPIO.IN, pull_up_down=GPIO.PUD_UP) # set buttonPin to PULL UP INPUT mode
    GPIO.setup(buttonPinR, GPIO.IN, pull_up_down=GPIO.PUD_UP) # set buttonPin to PULL UP INPUT mode

def buttonEventR(channel): # When button is pressed, this function will be executed
    global ledState
    print ('buttonEvent GPIO%d' %channel)
    ledState = not ledState
    if ledState :
        print ('Alarm turned on >>>')
        setColor(0,100,100)
        GPIO.output(ledPin,ledState)
        buzz()           
    else :
        print ('Alarm turned off <<<')
        setColor(100,100,100)
        GPIO.output(ledPin,ledState)
    #GPIO.output(ledPin,ledState)

def buttonEventY(channel):
    global RGBState
    print ('buttonEvent GPIO%d' %channel)
    RGBState = not RGBState
    if RGBState :
        setColor(0,0,0)#Flashlight enable>>requires yellow button still
        print("flashlight on")
    else:
        print("flashlight off")
        setColor(100,100,100)
    
def loop():
    #Button detect
    GPIO.add_event_detect(buttonPinR,GPIO.FALLING,callback = buttonEventR,bouncetime=300)
    GPIO.add_event_detect(buttonPinY,GPIO.FALLING,callback = buttonEventY,bouncetime=300)
    print("button enabled")
    #while True:
        #pass


def destroy():
    GPIO.cleanup() # Release GPIO resource
if __name__ == '__main__': # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()