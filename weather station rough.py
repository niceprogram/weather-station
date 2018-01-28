
Blockly‏ > Demos‏ > Code

Blocks	 	JavaScript	 	Python	 	PHP	 	Lua	 	Dart	 	XML	  
import math

DHTpin = None
myAPI = None
TW = None
myDelay = None
RHW = None
light = None
moisture = None
baseURL = None

# this function...read the temperature from inside or outside depending on the gpio value using an DHT11.
def read_temperature(DHTpin):
  global TW
  TW = '=Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)'
  return TW

# this function...read the humidity from inside or outside depending on the gpio value using a DHT11.
def read_humidity(DHTpin):
  global RHW
  RHW = 'Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)'
  return RHW

# this function...will send an output signal thought the LRD and measure the voltage with the input.
def read_light():
  global light
  light = 'explorerhat.analog.one.read()'
  light = 'explorerhat.analog.one.read()'
  return round(light)

# Describe this function...
def prints_out_the_values():
  pass

# this function...will send an output signal thought the hydrometer and measure the voltage with the input.
def read_hydrometer():
  global moisture
  moisture = 'explorerhat.analog.one.read()'
  moisture = 'explorerhat.analog.one.read()'
  return round(moisture)

# Describe this function...
def send_the_values_to_thingspeak():
  pass


# Setup our API and delay
myAPI = 'LHBVJLM9UNAH2K00'
# Amount of seconds between posting data.
myDelay = 15 * 60
print('starting...')
baseURL = str('https://api.thingspeak.com/update?api_key=') + str(myAPI)
print(baseURL)
while 0 == 0:
  prints_out_the_values()
  send_the_values_to_thingspeak()
