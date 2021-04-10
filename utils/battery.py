import smbus
import time

class Battery(object):
    def __init__(self, address=0x48):
        self._bus = smbus.SMBus(1)
        self._addr = address
        self._gain = 0x02 #  +/-4.096V range = Gain 1
        self._coefficient = 0.125;
               
        
    def _read_value(self):
        data = self._bus.read_i2c_block_data(self._addr, 0, 2)
        raw_adc = data[0] * 256 + data[1]
        if raw_adc > 32767:
            raw_adc -= 65535
        raw_adc = int(float(raw_adc)*self._coefficient)*4
        return raw_adc
    
    def read_voltage(self, channel=4):
        CONFIG_REG = [0x80 | (channel << 4) | self._gain, 0x80 | 0x03]
        self._bus.write_i2c_block_data(self._addr, 0x01, CONFIG_REG)
        time.sleep(0.1)
        return self._read_value()