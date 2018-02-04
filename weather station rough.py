""" 
dht22.py 
Temperature/Humidity monitor using Raspberry Pi and DHT22. 
Data is displayed at thingspeak.com
Original author: Mahesh Venkitachalam at electronut.in 
Modified by Adam Garbo on December 1, 2016 
"""

# Import all the libraries we need to run
import Adafruit_DHT
import RPi.GPIO as GPIO
#import explorerhat
import sys 
import os
from time import sleep 
import urllib2
GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.IN)
GPIO.setup(8, GPIO.IN)



#Setup our API and delay
LED_switch = False
myAPI = "E5KT3ZSMNKTDU83L"
myDelay =  10#how many seconds between posting data 60

# Function...read the humidity and temperature from inside or outside depending on the gpio value using an DHT11.
def read_DHT11(DHTpin,inside_outside):
	#toggle_LED_lights(inside_outside)
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin) 
	#toggle_LED_lights(inside_outside)
	return (str(humidity), str(temperature))

# Function ... indicates which sensor is being read
def toggle_LED_lights(LED_colour):
  global LED_switch
  if LED_switch == False:
    #explorerhat.light[LED_colour].on()
    LED_switch = True
  else:
    #explorerhat.light[LED_colour].off()
    LED_switch = False  

# main() function
def main(): 
   print 'starting...' 
   baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 
   while True: 
       try:
           RHWinside, TWinside =  read_DHT11(7,3)
           RHWoutside,TWoutside = read_DHT11(8,2)
           f = urllib2.urlopen(baseURL +
                               "&field1=%s&field2=%s&field3=%s&field4=%s" % (RHWinside, RHWoutside, TWinside, TWoutside))
           print "&field1=%s&field2=%s&field3=%s&field4=%s" % (RHWinside, RHWoutside, TWinside, TWoutside)
           f.close() 
           sleep(60) #uploads DHT11 sensor values every 5 minutes 
       except: 
           print 'exiting.' 
           break 
# call main 
if __name__ == '__main__': 
   main()  
