py-hackrf
=========
A Python library for the HackRF Device

Dependencies
-------------
pip install pyusb

Usage
-------------

//import the library

from core import HackRf

//Create a HackRf object

hr = HackRf()

hr.setup()

//Use it to do things, methods are very similair to libhackrf

hr.max2837.write_register(10, 14)

print hr.max2837.read_register(10)

print hr.get_version_string()

hr.set_frequency(50000000)
