from sms import Modem

m = Modem('/dev/ttyACM0')
print(m.test())