
import usb
import struct
import array
import logging
from max2837 import Max2837

logging.basicConfig()
logger = logging.getLogger('HackRf Core')
logger.setLevel(logging.DEBUG)

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

def byte_array_to_string(array):
	''' This is used to convert a array() of bytes into a string '''
	return "".join(map(chr, array))

def get_serial(serial_array):
		result = ''
		for byte in serial_array:
			result += '%0.2X' % byte
		return result

HackRfVendorRequest = enum(
	HACKRF_VENDOR_REQUEST_SET_TRANSCEIVER_MODE = 1,
	HACKRF_VENDOR_REQUEST_MAX2837_WRITE = 2,
	HACKRF_VENDOR_REQUEST_MAX2837_READ = 3,
	HACKRF_VENDOR_REQUEST_SI5351C_WRITE = 4,
	HACKRF_VENDOR_REQUEST_SI5351C_READ = 5,
	HACKRF_VENDOR_REQUEST_SAMPLE_RATE_SET = 6,
	HACKRF_VENDOR_REQUEST_BASEBAND_FILTER_BANDWIDTH_SET = 7,
	HACKRF_VENDOR_REQUEST_RFFC5071_WRITE = 8,
	HACKRF_VENDOR_REQUEST_RFFC5071_READ = 9,
	HACKRF_VENDOR_REQUEST_SPIFLASH_ERASE = 10,
	HACKRF_VENDOR_REQUEST_SPIFLASH_WRITE = 11,
	HACKRF_VENDOR_REQUEST_SPIFLASH_READ = 12,
	HACKRF_VENDOR_REQUEST_CPLD_WRITE = 13,
	HACKRF_VENDOR_REQUEST_BOARD_ID_READ = 14,
	HACKRF_VENDOR_REQUEST_VERSION_STRING_READ = 15,
	HACKRF_VENDOR_REQUEST_SET_FREQ = 16,
	HACKRF_VENDOR_REQUEST_AMP_ENABLE = 17,
	HACKRF_VENDOR_REQUEST_BOARD_PARTID_SERIALNO_READ = 18,
	HACKRF_VENDOR_REQUEST_SET_LNA_GAIN = 19,
	HACKRF_VENDOR_REQUEST_SET_VGA_GAIN = 20,
	HACKRF_VENDOR_REQUEST_SET_TXVGA_GAIN = 21)

HackRfConstants = enum(
	HACKRF_DEVICE_OUT = 0x40,
	HACKRF_DEVICE_IN = 0xC0,
	HACKRF_USB_VID = 0x1d50,
	HACKRF_USB_PID = 0x604b)

HackRfTranscieverMode = enum(
	HACKRF_TRANSCEIVER_MODE_OFF = 0,
	HACKRF_TRANSCEIVER_MODE_RECEIVE = 1,
	HACKRF_TRANSCEIVER_MODE_TRANSMIT = 2)

class HackRf():
	''' This is the base object for the HackRf Device, and interaction with it '''
	__JELLYBEAN__ = 'Jellybean'
	__JAWBREAKER__ = 'Jawbreaker'

	def __init__(self, name):
		self.name = name
		self.device = None
		self.max2837 = None
		logger.error(HackRfVendorRequest.HACKRF_VENDOR_REQUEST_SET_TRANSCEIVER_MODE)

	def setup(self):
		''' This is to setup a hackrf device '''
		if self.name  == HackRf.__JAWBREAKER__:
			self.device = usb.core.find(idVendor=HackRfConstants.HACKRF_USB_VID, idProduct=HackRfConstants.HACKRF_USB_PID)
			if self.device == None:
				logger.error('No Hack Rf Detected!')
			else:
				self.device.set_configuration()
				self.max2837 = Max2837(self)
				logger.debug('Successfully setup HackRf device')

	def get_board_id(self):
		''' Gets the board's id number '''
		return self.device.ctrl_transfer(
			HackRfConstants.HACKRF_DEVICE_IN,
			HackRfVendorRequest.HACKRF_VENDOR_REQUEST_BOARD_ID_READ,
			0,
			0,
			2)[0]

	def get_version_string(self):
		''' Returns the version string from the hackrf board '''
		return byte_array_to_string(self.device.ctrl_transfer(
			HackRfConstants.HACKRF_DEVICE_IN,
			HackRfVendorRequest.HACKRF_VENDOR_REQUEST_VERSION_STRING_READ,
			0,
			0,
			100))

	def get_board_serial_number(self):
		''' Gets the board serial number '''
		number = self.device.ctrl_transfer(
			HackRfConstants.HACKRF_DEVICE_IN,
			HackRfVendorRequest.HACKRF_VENDOR_REQUEST_BOARD_PARTID_SERIALNO_READ,
			0,
			0,
			100)
		#Only get relevant bytes
		serial = number[8:]
		#Get bytes in the right order
		serial.reverse()

		serial_one = get_serial(serial[12:])
		serial_two = get_serial(serial[8:12])
		serial_three = get_serial(serial[4:8])
		serial_four = get_serial(serial[:4])
		return (serial_one, serial_two, serial_three, serial_four)

	def set_sample_rate(self, freq, div):
		''' Sets the sample rate of the hack rf device '''
		p =  struct.pack('II', freq, div)
		print "".join(["/x%02x" % ord(c) for c in p]) #
		result = self.device.ctrl_transfer(HackRfConstants.HACKRF_DEVICE_OUT,
			HackRfVendorRequest.HACKRF_VENDOR_REQUEST_SAMPLE_RATE_SET,
			0,
			0,
			p,
			len(p))
		print result

	def set_rx_mode(self):
		''' This sets the HackRf in receive mode '''
		result = self.device.ctrl_transfer(HackRfConstants.HACKRF_DEVICE_OUT,
			HackRfVendorRequest.HACKRF_VENDOR_REQUEST_SET_TRANSCEIVER_MODE,
			HackRfTranscieverMode.HACKRF_TRANSCEIVER_MODE_RECEIVE, 0)
		print result

	def set_tx_mode(self):
		''' This sets the HackRf in tranfer mode '''
		self.device.ctrl_transfer(HackRfConstants.HACKRF_DEVICE_OUT,
			HackRfVendorRequest.HACKRF_VENDOR_REQUEST_SET_TRANSCEIVER_MODE,
			HackRfTranscieverMode.HACKRF_TRANSCEIVER_MODE_TRANSMIT, 0)
