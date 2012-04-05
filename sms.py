import re
import serial

class Modem:
	serPort = None

	def __init__(self, modem=None,timeout=2):
		if modem is not None:
			self.serPort = serial.Serial(modem,timeout=timeout)

	def __unicode__(self):
		if self.serPort is None:
			return "Uninitialised modem-instance"
		else:
			return "Modem: " + self.serPort.name()


	def open(self, modem):
		if self.serPort is not None:
			self.serPort.close()
		if modem is None:
			raise Exception('You must pass modem path')
		self.serPort = serial.Serial(modem)

	def close(self):
		if self.serPort is None:
			raise Exception('Port is not open')
		else:
			self.serPort.close()


	def write(self, string):
		if self.serPort is None:
			raise Exception('Port is not open')
		else:
			self.serPort.write(string + chr(0x0d))

	def read(self, length=10):
		if self.serPort is None:
			raise Exception('Port is not open')
		else:
			return self.serPort.read(length)
	
	def clear(self):
		self.serPort.flushInput()

	def test(self):
		if self.serPort is None:
			raise Exception('Port is not open')
		
		self.clear()
		self.write("AT")
		result = self.read()
		#print(result)
		if re.search("OK",result):
		    return True
		else:
		    return False
		    
class Message:
	Number = None
	Text = None

	def __init(self, number, message):
		pass


class MessageHandler:
	modem = None

	def __init__(self, modem):
		if not isinstance(modem, Modem):
			raise Exception('Argument must be instance of Modem')
		self.modem = modem

	def send(self):
		pass
		
	def get(self, index):
		pass
	
	def getAll(self):
		pass