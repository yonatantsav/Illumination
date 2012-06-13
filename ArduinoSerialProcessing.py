import processing.serial.Serial as Serial

class ArduinoSerial(object):

	def __init__(self):
		self.NOTHING = 0
		self.OPEN = 1   # clip is open, in transit (fsr low, switch low)
		self.EMPTY = 2   # clip is closed, no paper in (fsr high, switch high)
		self.READY = 3   # clip is closed, paper in place (fsr high, switch low)
		self.UNKNOWN = 4   # initial state 
		self.initSerial()
		#self.ser = None
		
	def initSerial(self):
		# configure the serial connections (the parameters differs on the device you are connecting to)
		portName = Serial.list()[0];
		#try:
  		self.ser = Serial(this, portName, 9600)
  		#except:
  		#	print "ERROR: Arduino Unavailable, Serial object could not be initialized."

	def check(self):
		retVal = self.NOTHING
		#check to see if we have a serial object
		#if self.ser:
		if self.ser.available() > 0:
			out = int(self.ser.read())
			out = out-48
			if out != self.NOTHING:
				retVal = out
		return retVal
		
if __name__ == '__main__':
	import time
	ser1 = ArduinoSerial()
	tmp = -1
	while 1:
		print "looping"
		tmp = ser1.check()
		if tmp != ser1.NOTHING:
			print tmp
		time.sleep(0.5)