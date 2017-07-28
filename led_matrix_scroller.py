from wemos_led_matrix import leds
from font8x8_basic import font
from time import sleep_ms

def shift_row(a, b, offset):
    return (a >> offset) | (b << (8 - offset))
   
def scroll(message, sleep_period):
    for c1, c2 in zip(message[:-1], message[1:]):
        for column in range(8):
            leds.send_bytes(shift_row(a, b, column) for a, b in zip(font[c1], font[c2]))
            sleep_ms(sleep_period)
