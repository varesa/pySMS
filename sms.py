import re
import serial
from time import sleep

class Modem:
	serPort = None

	def __init__(self, modem=None,timeout=3):
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

	def read(self):
		if self.serPort is None:
			raise Exception('Port is not open')
		else:
			return self.serPort.read(self.serPort.inWaiting())

	def clear(self):
		self.serPort.flushInput()


	def runcmd(self,cmd):
		self.clear()
		self.write(cmd)
		sleep(1)
		return self.read().strip()

	def test(self):
		if self.serPort is None:
			raise Exception('Port is not open')
		
		result = self.runcmd("AT")
		if re.search("OK",result):
		    return True
		else:
		    return False
		    
class Message:
	number 	= None
	text 	= None
	header	= None

	def __init__(self, number="", text="", header=""):
		self.number=number
		self.text=text
		self.header=header


class MessageHandler:
	modem = None

	def __init__(self, modem):
		if not isinstance(modem, Modem):
			raise Exception('Argument must be instance of Modem')
		self.modem = modem

	def send(self, message):
		if not isinstance(message, Message):
			raise Exception('Argument must be instance of Message')
		return self.modem.runcmd("AT+CMGS=\"" + message.number + "\"" + chr(0x0D) + message.text + chr(0x1A))

	def get(self, index):
		pass
	
	def getAll(self):
		self.modem.runcmd("AT+CMGF=1") # Set text mode
		result = self.modem.runcmd("AT+CMGL=\"ALL\"")
		messages = result.split("\r\n")[1:len(result.split("\r\n"))-2]
		received = list()
		for num in range(0,len(messages),2):
			if re.search("REC", messages[num]):
			    received.append(Message(header=messages[num],text=messages[num+1]))
		return received
		
