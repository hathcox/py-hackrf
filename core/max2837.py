import usb
import struct
import logging
import hackrf 
logger = logging.getLogger('HackRf Max2837')
logger.setLevel(logging.DEBUG)

class Max2837():

	def __init__(self, hackRf):
		self.hackRf = hackRf		

	def write_register(self, register_number, value):
		''' Writes a value to the Max 2837 chip's register '''
		if register_number in range(32):
			self.hackRf.device.ctrl_transfer(hackrf.HackRfConstants.HACKRF_DEVICE_OUT,
			hackrf.HackRfVendorRequest.HACKRF_VENDOR_REQUEST_MAX2837_WRITE,
			value,
			register_number)
		else:
			logger.warning('Invalid Register Number [%d]' % register_number)

	def read_register(self, register_number):
		''' Read a value from the Max 2837 chip's register '''
		if register_number in range(32):
			return struct.unpack('<H', self.hackRf.device.ctrl_transfer(hackrf.HackRfConstants.HACKRF_DEVICE_IN,
			hackrf.HackRfVendorRequest.HACKRF_VENDOR_REQUEST_MAX2837_READ, 
			0, 
			register_number,
			2))[0]
		else:
			logger.warning('Invalid Register Number [%d]' % register_number)
