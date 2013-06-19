import usb
import struct
import logging
import hackrf 
logger = logging.getLogger('HackRf SI5351C')
logger.setLevel(logging.DEBUG)

class SI5351C():

	def __init__(self, hackRf):
		self.hackRf = hackRf		

	def write_register(self, register_number, value):
		''' Writes a value to the SI5351C chip's register '''
		if register_number in range(255):
			self.hackRf.device.ctrl_transfer(hackrf.HackRfConstants.HACKRF_DEVICE_OUT,
			hackrf.HackRfVendorRequest.HACKRF_VENDOR_REQUEST_SI5351C_WRITE,
			value,
			register_number)
		else:
			logger.warning('Invalid Register Number [%d]' % register_number)

	def read_register(self, register_number):
		''' Read a value from the SI5351C chip's register '''
		if register_number in range(255):
			return self.hackRf.device.ctrl_transfer(hackrf.HackRfConstants.HACKRF_DEVICE_IN,
			hackrf.HackRfVendorRequest.HACKRF_VENDOR_REQUEST_SI5351C_READ, 
			0, 
			register_number,
			2) [0]
		else:
			logger.warning('Invalid Register Number [%d]' % register_number)

	def display_registers(self):
		for register in range(255):
			value = self.read_register(register)
			print "Register [%d] Value [%d]" % (register, value)