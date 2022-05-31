# Pippy4Deck
This Arm mounted computer successfully reads all bio signatures from its three sensors (GY-BMP280, altitude, DHT11, MPU6050). This information is displayed on the LCD in a set of three rotating screens. 
The temperature is also cross referenced on screen for the convenience. This information is relayed back to the server on Thingspeak either for later analysis or real-time monitoring. 

In addition to the LCD for the user’s convenience, there are also two buttons included. A yellow LCD light is used to create a bright white light to help in low light environments. The red one is used when the system goes into rescue mode thus creating a very user-friendly format.  Should the Pippy 4D device fail, this will trigger an SOS alarm beacon and a series of red lights. The control server can also monitor for life vitals or sudden changes in orientation or acceleration in case of a fall or other accident before initiating SOS alarm sequence remotely. This could also be done as a rescue action as well or security measure to mitigate theft. If the rescue/lockdown mode is enabled by the server, then the button will not end the Pippy 4D’s current state.  Together, these features allow a user to operate, explore and work in new frontier environments with increased safety and knowledge.  

Pippy 4D can be operated as a standalone arm mounted unit or as a built-in module for a hazardous environment suit. 
Some fields these can include but not limited to are: sea and space exploration, orbital maintenance, global warming, ecological surveys, worker safety, rescue, mining, and weather monitoring.

The device uses the GY-BMP280 sensor for temperature, pressure and altitude. The DHT11 sensor is used to read humidity and the MPU6050 sensor is used for the gyroscopic and acceleration readings. It is displayed on the LCD 1602 which then uploads the data to Thingspeak for analysis and security purposes. IoT portal was implemented for analysis and Node-Red and for security lockdown. 

This started of as a reverse engineering project and grew into a functional prototype wearable
The orignal prototype was built from a Raspberry Pi costing about 100-150$ to produce including addon modules and fabrication.

CHALLENGES:  

A number of programming bugs became major setbacks including overlapping settings from two libraries and threads. Primarily, the GPIO.Zero library and the Rpi.GPIO library were found to be incompatible although some basic functions were compatible up to a point. Advanced settings related to the pins on the GPIO board began to conflict with one another. This led a decisive decision to convert to Rpi.GPIO library. It should be noted that all major modules were already using this library.  Getting all the Python3 modules to work together was certainly a challenge, However, by using a modular design for each component of the Pippy 4D, it was easier to locate bugs and import modules one at a time. 

Repeated debugging and modularization resulted in skill strengthening through the construction of this project. 

