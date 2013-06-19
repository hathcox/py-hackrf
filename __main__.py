from core import HackRf

hr = HackRf(HackRf.__JAWBREAKER__)
hr.setup()
print hr.rffc5071.read_register(10)
hr.rffc5071.write_register(10, 14)
print hr.rffc5071.read_register(10)

# hr.si5351c.display_registers()
print hr.get_board_serial_number()
hr.set_baseband_filter_bandwidth(500000)
#hr.set_rx_mode()
#hr.set_sample_rate(10000000, 1)
