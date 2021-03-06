from ..i2c_device import I2cDevice
from ..base.transducer import Transducer


class MCP9808(I2cDevice, Transducer):
    '''Library for the Adafruit MCP9808 Temperature sensor'''
    
    _DEFAULT_I2C_ADDRESS    = 0x18
    
    # Register addresses.
    _REG_CONFIG             = 0x01
    _REG_UPPER_TEMP         = 0x02
    _REG_LOWER_TEMP         = 0x03
    _REG_CRIT_TEMP          = 0x04
    _REG_AMBIENT_TEMP       = 0x05
    _REG_MANUF_ID           = 0x06
    _REG_DEVICE_ID          = 0x07
    
    def __init__(self, i2cAddress= _DEFAULT_I2C_ADDRESS, itype=None, other_data=None, **kwargs):
        super(MCP9808, self).__init__(i2cAddress, **kwargs)
        if other_data is None:
            other_data = {}
        Transducer.__init__(self, "TEMP", itype, **other_data)
    
    def readC(self):
        # Read temperature value
        t = self.read_word_data(self._REG_AMBIENT_TEMP)
        # Convert to Big Endian
        t = ((t << 8) & 0xFF00) + (t >> 8)
        
        # Scale and convert to signed value
        temp = (t & 0x0FFF) / 16.0
        if t & 0x1000:
            temp -= 256.0
            
        return temp
        
    def readF(self):
        return (self.readC() * 9/5) + 32
    
    def read(self):
        return {'temp_c': self.readC()}
