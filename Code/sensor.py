#!/usr/bin/python3
import RPi.GPIO as GPIO #using the RPI.GPIO library     
import dht11 #Importing the dht11 tempertaure/humidity      
from time import*
import math
import bme280

def setup():

	#GPIO.setmode(GPIO.BCM)
	#GPIO.setmode(GPIO.BOARD)  
	GPIO.setwarnings(False)
	#GPIO.cleanup()
def Humidity():

	instance = dht11.DHT11(7)#gpio4
	result = instance.read()
	if result.is_valid(): #if there is data read from pin 4 above then print below                                      
                                 
    		print("Humidity : %-3.2f %%" % result.humidity) # printing the humidity                                        
	else:                                                                                                        
    		print("Error: %d" % result.error_code) #print error 
	return(result.humidity)


def Climate():
	temperature,pressure, humidity = bme280.readBME280All()
	print("Temperature : %-3.2f C " % temperature)
	print("Pressure : %-3.2f hPa " % pressure)
	height = ((math.pow((1013.25/pressure),(1/5.257))-1)*(temperature+273.15))/0.0065
	print("Altitude : %-3.2f m" % height)
	return_list = [temperature, pressure, height]
	return return_list


if __name__ =='__main__':
	setup()
