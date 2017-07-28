from wemos_led_matrix import leds
from time import sleep_ms
from font8x8_basic import font8x8_basic 

def shift_row(a, b, offset):
    return (a >> offset) | (b << (8 - offset))
   
def scroll(message, sleep_period):
    for l1, l2 in zip(message[:-1], message[1:]):
        for column in range(0, 8):
            leds.send_bytes([int(shift_row(a, b, column)) for a,b in zip(list(font8x8_basic[l1])[::-1], list(font8x8_basic[l2])[::-1])])
            sleep_ms(sleep_period)
