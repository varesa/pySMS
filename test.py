from sms import *

m = Modem('/dev/ttyACM0')
print(m.test())

h = MessageHandler(m)

print(h.getAll())