"""
Pippy 4Deck
March 2021

Example of MQTT protocol Publish function
This example uses MQTT v3.11 to subscribe to "Field 5" topic of my private ThingSpeak Channel
Use this example as a template for Lab 6 and/or the final Project

For this to work, you need to instal paho-mqtt library:
sudo pip3 install paho-mqtt
""" 
from random import randint
from time import sleep
import paho.mqtt.client as mqtt
import Bodythermo
import MPU6050RAW
from time import sleep
import I2C_LCD_driver as lcd_d
import sensor
import RPi.GPIO as GPIO 
import buzzer
from signal import pause
import buttons
from math import sqrt

#change below values according to your Thinkspeak.com account
MQTT_CLIENT_ID = "Pippy 6D" # This is for your own client identification. Can be anything
MQTT_USERNAME = "mwa0000012345678" #This is the ThingsSpeak's Author
MQTT_PASSWD = "2IRTIFR1B8LPDD4D" #This is the MQTT API Key found under My Profile in ThingSpeak
MQTT_HOST = "mqtt.thingspeak.com" #This is the ThingSpeak hostname
MQTT_PORT = 1883 #Typical port # for MQTT protocol. If using TLS -> 8883
CHANNEL_ID = "1364416" #Channel ID found on ThingSpeak website
MQTT_WRITE_APIKEY = "P7E4N2PPEDIN1L78" # Write API Key found under ThingSpeak Channel Settings
MQTT_PUBLISH_TOPIC = "channels/" + CHANNEL_ID + "/publish/" + MQTT_WRITE_APIKEY
MQTT_READ_APIKEY = "HMMYJE12345DYMZB" # Read API Key found under ThingSpeak Channel Settings
MQTT_SUBSCRIBE_TOPIC = "channels/" + CHANNEL_ID + "/subscribe/fields/field6/" + MQTT_READ_APIKEY

Security=0
Yellow=0
Red=0
count =1 #of 1/5 channels
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

Bodythermo.setup()#setup ADC and RGB
MPU6050RAW.setup()#gyro
sensor.setup()#
mylcd = lcd_d.lcd()
buzzer.setup()
buttons.setup() #setup buttons
buttons.loop() #setup button callbacks

""" 
Standard callback functions. See Phao MQTT documentation for more

This function will be called upon connection
"""
def on_message(client, userdata, message):
    print("Message topic: ", message.topic)    
    print("Message payload: ", message.payload)
    print("Message QoS: ", message.qos)

def on_connect(client, userdata, flags, rc):
    print("Connected ", rc)

"""
This function is called upon Publishing of data to predefined topic
"""

def on_publish(client, userdata, result):
    print("Published ", result)

""" 
This function is used for logging. For this to work, you must uncomment the callback binding
"""

def on_log(client, userdata, level, buf):
    print("log:", buf)

try:
    """ create client instance"""
    client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
    
    """ standard callback bindings """

    client.on_connect = on_connect
    client.on_message = on_message
    #client.on_subscribe = on_subscribe
    #client.on_unsubscribe = on_unsubscribe
    #client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    #client.on_log = on_log

    """ Set the conneciton authentication. """
    client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWD)
    """ Connect client """
    client.connect(MQTT_HOST, port=MQTT_PORT, keepalive=60)
    """ start the looping of client connection. This needs to be done otherwise the connection will only happen once and expire """
    client.loop_start()
    client.subscribe(MQTT_SUBSCRIBE_TOPIC, qos=0)

    while True:			#Main Program loop
        #trigger for sensors
        #print("Message payload: ", message.payload)
        btemp = Bodythermo.loop()
        humidity = sensor.Humidity()
        env=sensor.Climate()
        mylcd.lcd_clear()
        mylcd.lcd_display_string("TMP:"+str(round(btemp))+"/"+str(round(env[0])), 1, 0)
        mylcd.lcd_display_string("HUM:"+str(humidity), 1, 10)
        mylcd.lcd_display_string("ALT:"+str(round(env[2])), 2, 0)
        mylcd.lcd_display_string("Hpa:"+str(round(env[1])), 2, 8)
        mylcd.backlight(1)
        sleep(2)

        #trigger for Gyro
        AccGyro=MPU6050RAW.loop()#gyro
        mylcd.lcd_clear()
        mylcd.lcd_display_string(str(round(AccGyro[3], 2))+" "+str(round(AccGyro[4], 2))+" "+str(round(AccGyro[5], 2)), 1, 0)
        mylcd.lcd_display_string("d/s   d/s   d/s", 2,0)
        sleep(2)

        #trigger for Accelerometer
        mylcd.lcd_clear()
        mylcd.lcd_display_string("a/g   a/g   a/g", 2, 0)
        mylcd.lcd_display_string(str(round(AccGyro[0], 2))+" "+str(round(AccGyro[1], 2))+" "+str(round(AccGyro[2], 2)), 1, 0)

        #trigger for server
        while count>0:
            sleep(2)
            if not client.is_connected():
                print("Client disconnected. Trying to reconnect.")
                client.reconnect()
            if count == 1:
                pub_topic = "field1=" + str(env[0]) #publish temperature
            if count == 2:
                pub_topic = "field2=" + str(env[1])#pressure
            if count == 3:
                pub_topic = "field3=" + str(humidity)#humidty
            if count == 4:
                pub_topic = "field4=" + str(env[2])#Altitude
            if count == 5:
                pub_topic = "field5=" + str(sqrt((AccGyro[0]*AccGyro[0])+(AccGyro[1]*AccGyro[1])+(AccGyro[2]*AccGyro[2])))#accerleration
                count=0
            client.publish(MQTT_PUBLISH_TOPIC, pub_topic)
            count=count+1
            sleep(1)
            break

        print("end of pipD loop")
        mylcd.lcd_clear()

    #cleanup
except KeyboardInterrupt:
    client.unsubscribe(MQTT_SUBSCRIBE_TOPIC)
    client.disconnect()
    Bodythermo.destroy()
    GPIO.cleanup()
    print("end pipD program")