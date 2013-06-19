import usb
import struct
import logging
import hackrf 
logger = logging.getLogger('HackRf RFFC5071')
logger.setLevel(logging.DEBUG)

class RFFC5071():

	def __init__(self, hackRf):
		self.hackRf = hackRf		

	def write_register(self, register_number, value):
		''' Writes a value to the RFFC5071 chip's register '''
		if register_number in range(30):
			self.hackRf.device.ctrl_transfer(hackrf.HackRfConstants.HACKRF_DEVICE_OUT,
			hackrf.HackRfVendorRequest.HACKRF_VENDOR_REQUEST_RFFC5071_WRITE,
			value,
			register_number)
		else:
			logger.warning('Invalid Register Number [%d]' % register_number)

	def read_register(self, register_number):
		''' Read a value from the RFFC5071 chip's register '''
		if register_number in range(30):
			return struct.unpack('<H', self.hackRf.device.ctrl_transfer(hackrf.HackRfConstants.HACKRF_DEVICE_IN,
			hackrf.HackRfVendorRequest.HACKRF_VENDOR_REQUEST_RFFC5071_READ, 
			0, 
			register_number,
			2))[0]
		else:
			logger.warning('Invalid Register Number [%d]' % register_number)

	def display_registers(self):
		for register in range(32):
			value = self.read_register(register)
			print "Register [%d] Value [%d]" % (register, value)