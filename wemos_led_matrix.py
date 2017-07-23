
class WemosLedMatrix:
    ''' A Micropython driver for the Wemos LED Matrix Shield.

    The shield uses the Titan Micro TM1640 LED controller that has an unusual
    communications protocol (not I2C, not SPI). This driver should port
    reasonably easily to any hardware using the TM1640 but is especially easy
    to use when a Wemos D1 variant is combined with the official LED Matrix
    shield.

    The display a checkerboard pattern for example:

      matrix = WemosLedMatrix(clockpin=Pin(14, Pin.OUT), datapin=Pin(13, Pin.OUT))
      matrix.send_bytes([0x55, 0xAA]*4)

    '''

    def __init__(self, clockpin, datapin, intensity=7, activate=True):
        self.clock_pin = clockpin
        self.data_pin = datapin
        self.intensity = intensity
        self.active = activate

        clockpin.off()
        clockpin.on()
        datapin.on()

        self.clear()
        self.brightness(intensity)

    def send(self, data):
        ''' The TM1640 uses a quirky protocol. It's not I2C and it's not SPI.
        Bit-bashing is required! Data is read on the rising edge of the clock.
        See datasheet for details.'''
        for _ in range(0, 8):
            self.clock_pin.off()
            self.data_pin.value(1 if data & 1 else 0)
            data >>= 1
            self.clock_pin.on()

    def send_command(self, cmd):
        ''' Send a command. Commands must be begun and terminated correctly. '''
        self.data_pin.off()
        self.send(cmd)
        self.end()

    def send_data(self, address, data):
        ''' Send a single byte to a fixed address. '''
        self.send_command(0x44) # Fixed address
        self.data_pin.off()
        self.send(0xC0 | address)
        self.send(data)
        self.end()

    def send_bytes(self, data):
        ''' Send a sequence of data to the display. '''
        self.send_command(0x40) # Address auto + 1
        self.data_pin.off()
        self.send(0xC0)
        for b in data:
            self.send(b)
        self.end()

    def clear(self):
        ''' Set all the LED's off. '''
        self.send_bytes([0] * 8)

    def end(self):
        ''' Commands and data transfers need to be terminated correctly. See
        datasheet for details. '''
        self.data_pin.off()
        self.clock_pin.off()
        self.clock_pin.on()
        self.data_pin.on()

    def brightness(self, level):
        ''' Level must be between 0 and 7. 0 is dimmest, 7 is brightest. '''
        self.intensity = max(0, min(7, level))
        self.send_command(0x80 | self.intensity | (0x08 if self.active else 0))

    def activate(self, display_on):
        ''' The display can be de/activated.
        Any LEDs left on when the display was deactivated will be shown again
        when reactivated.'''
        self.active = display_on
        self.send_command(0x80 | self.intensity | (0x08 if self.active else 0))

from machine import Pin

leds = WemosLedMatrix(clockpin=Pin(14, Pin.OUT), datapin=Pin(13, Pin.OUT), intensity=0)
