# Test STP constant current driver
# Toggle LE like this, then use PIO for OE and trig

from machine import Pin, SPI
import time

# 1. Initialize GPIO Control Pins
# OE is active LOW. Pull it LOW to enable the outputs immediately.
oe = Pin(16, Pin.OUT, value=0)
le = Pin(17, Pin.OUT, value=0)

# 2. Initialize SPI0 (Baudrate max 30MHz for the STP16CPC26)
# Default pins for SPI0 on Pico: SCK=GP18, MOSI=GP19
spi = SPI(0, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))

def write_leds(pattern_16bit):
    """Writes a 16-bit integer state pattern to the STP16CPC26 outputs."""
    # Split the 16-bit integer into two 8-bit bytes (MSB first)
    buffer = bytearray([(pattern_16bit >> 8) & 0xFF, pattern_16bit & 0xFF])

    # Send the data over SPI
    spi.write(buffer)

    # Pulse Latch Enable (LE) HIGH to transfer data from shift register to outputs
    le.value(1)
    le.value(0)

# --- Main Demo Loop ---
try:
    while True:
        # Alternating pattern: 1010101010101010 (0xAAAA)
        write_leds(0xAAAA)
        time.sleep(0.5)

        # Inverted alternating pattern: 0101010101010101 (0x5555)
        write_leds(0x5555)
        time.sleep(0.5)

        # Cycle through every single LED one by one
        for i in range(16):
            write_leds(1 << i)
            time.sleep(0.1)

except KeyboardInterrupt:
    # Clear all LEDs on exit
    write_leds(0x0000)
