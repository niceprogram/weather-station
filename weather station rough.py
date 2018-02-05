"""
 We are using a Raspberry Pi W zero + an Explorer HAT pro
. 2x DHT11 to measure temperature 1) on the balcony 2) inside
. 1 light sensor
. and 1 humidity checker that we have stuck in the flower pot on the balcony
 
projected inspired by:
the data is sent to  https://thingspeak.com/channels/227417/
My First Internet of Things
Temperature/Humidity Light monitor using Raspberry Pi, DHT11, and photosensor 
Data is displayed at thingspeak.com 2015/06/15
SolderingSunday.com
Based on project by Mahesh Venkitachalam at electronut.in

"""
# Import all the libraries we need to run
import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
import urllib2
import explorerhat



DEBUG = 1
# Setup the pins we are connect to
RCpin = 24
DHTpin =7
LED_switch = False

#Setup our API and delay
myAPI = "E5KT3ZSMNKTDU83L"
myDelay =  15 * 60 #how many seconds between posting data

GPIO.setmode(GPIO.BCM)
GPIO.setup(RCpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Function...read the humidity and temperature from inside or outside depending on the gpio value using an DHT
def read_DHT11(DHTpin,inside_outside):
        toggle_LED_lights(inside_outside)
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin) 
        toggle_LED_lights(inside_outside)
        return (str(humidity), str(temperature))
        
# Function ... indicates with a LED that a sensor is being read
def toggle_LED_lights(LED_colour):
  global LED_switch
  if LED_switch == False:
    explorerhat.light[LED_colour].fade(10,50,500)
    LED_switch = True
  else:
    explorerhat.light[LED_colour].off()
    LED_switch = False  
        
# Function ... (don't know if RC time or RC pin helps)
def RCtime(RCpin):
    LT = 0
    if (GPIO.input(RCpin) == True):
        LT += 1
    return (str(LT))
        
# Function ... read the moisture in the soil
def soil_moisture():
    explorerhat.output.one.on()
    toggle_LED_lights(0)
    moisture =  explorerhat.analog.one.read()
    explorerhat.output.one.off()
    toggle_LED_lights(0)
    return (str(round(moisture,1))) 
    
# Function ... read the how much light there is
def light_reading():
    explorerhat.output.two.on()
    toggle_LED_lights(1)
    light =  explorerhat.analog.two.read()
    explorerhat.output.two.off()
    toggle_LED_lights(1)
    return (str(round(light,1)))        
        
# main() function
def main():
    
    print 'starting...'
    #RHWinside= 5
    #TWinside =  6
    #RHWoutside =7
    #TWoutside = 8
    #LT = 11
    #soil_reading =  10

    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
    print baseURL
    
    while True:
        try:
            RHWinside, TWinside =  read_DHT11(7,3)
            RHWoutside,TWoutside = read_DHT11(8,2)
            LT = light_reading()
            soil_reading =  soil_moisture()
                        
            f = urllib2.urlopen(baseURL +"&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s" % (RHWinside, RHWoutside, TWinside, TWoutside, LT, soil_reading))
            print f.read()
            print "RHW-out=%s&RHW-in=%s&temp-out=%s&temp-in=%s&LT=%s&M=%s" % (RHWinside, RHWoutside, TWinside, TWoutside, LT, soil_reading)
            
            f.close() 
            

            sleep(int(myDelay))
        except:
            print 'exiting.'
            break

# call main
if __name__ == '__main__':
    main()
