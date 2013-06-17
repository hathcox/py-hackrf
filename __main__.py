from core import HackRf

hr = HackRf(HackRf.__JAWBREAKER__)
hr.setup()
print hr.max2837.read_register(10)
hr.max2837.write_register(10, 14)
print hr.max2837.read_register(10)

print hr.get_board_serial_number()
hr.set_rx_mode()
hr.set_sample_rate(1, 2)
