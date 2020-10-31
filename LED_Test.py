import board
import RPi.GPIO as GPIO
import neopixel
import time

#D18 LED Strip 1
#D23 LED Strip 2
#D24 LED Strip 3

pixel_count_1 = 360

GPIO.setmode(GPIO.BCM)
pixels1 = neopixel.NeoPixel(board.D18, pixel_count_1)
#pixels1 = neopixel.NeoPixel(board.D24, pixel_count_1)


print("Testing LED Strands")
while 1:
    pixels1.fill((255,255,255))
    time.sleep(1)
    pixels1.fill((255,0,0))
    time.sleep(1)


