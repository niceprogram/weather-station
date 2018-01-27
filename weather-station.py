"""
My First Internet of Things

Temperature/Humidity Light monitor using Raspberry Pi, DHT11, and photosensor 
Data is displayed at thingspeak.com
2015/06/15
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

#Setup our API and delay
myAPI = "LHBVJLM9UNAH2K00"
myDelay =  15 * 60#how many seconds between posting data 60

GPIO.setmode(GPIO.BCM)
GPIO.setup(RCpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



def getSensorData():
    RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
    
    TWF = 9/5*TW+32
   
    # return dict
    return (str(RHW), str(TW),str(TWF))

def RCtime(RCpin):
    LT = 0
    
    if (GPIO.input(RCpin) == True):
        LT += 1
    return (str(LT))
    
def soil_moisture():
    global moisture
    moisture =  explorerhat.analog.one.read()
    
    return (str(round(moisture,1))) 
    
# main() function
def main():
    
    print 'starting...'

    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
    print baseURL
    
    while True:
        try:
            RHW, TW, TWF = getSensorData()
            LT = RCtime(RCpin)
            TWF = (soil_moisture())
            f = urllib2.urlopen(baseURL + 
                                "&field1=%s&field2=%s&field3=%s" % (TW, TWF, RHW)+
                                "&field4=%s" % (LT))
            print f.read()
            print TW + " " + TWF + " " + RHW + " " + LT
            
            f.close()
            

            sleep(int(myDelay))
        except:
            print 'exiting.'
            break

# call main
if __name__ == '__main__':
    main()
