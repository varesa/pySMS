#!/usr/bin/env python

from sys import argv
from sms import *

if not argv[1]:
    Exception('You must specify modem device as the first parameter')

m = Modem(argv[1])
print(m.test())

h = MessageHandler(m)

print(h.getAll())
