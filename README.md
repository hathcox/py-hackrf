py-hackrf
=========
A Python library for the HackRF Device

Dependencies
-------------
pip install pyusb

Usage
-------------

<code>
//import the library
</code>
<code>
from core import HackRf
</code>

<code>
//Create a HackRf object
</code>
<code>
hr = HackRf()
</code>
<code>
hr.setup()
</code>

<code>
//Use it to do things, methods are very similair to libhackrf
</code>
<code>
hr.max2837.write_register(10, 14)
</code>
<code>
print hr.max2837.read_register(10)
</code>
<code>
print hr.get_version_string()
</code>
<code>
hr.set_frequency(50000000)
</code>
