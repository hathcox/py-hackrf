from core import HackRf
from test import TestHackRf
import unittest
import sys

def banner():
	''' Display the information banner '''
	print 'Welcome to Py-HackRf, to run unit tests run the following command:'
	print 'python . test'

args = sys.argv
if len(args) >= 2: 
	command = args[1]
	if command.lower() != 'test':
		banner()
		sys.exit(0)
	else:
		# Start the unit tests
		suite = unittest.TestLoader().loadTestsFromTestCase(TestHackRf)
		unittest.TextTestRunner(verbosity=2).run(suite)
else:
	banner()
