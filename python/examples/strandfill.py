#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
# Forked: Daniel Bryar (rpi@bryar.com.au)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 85      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def stripGradient(strip, percent):
    if percent < 50:
        color = Color(255, 0, 0)
        length = strip.numPixels() / 2
    if percent > 49:
        red = ((2 * percent) - 100) * 255 / 100
        green = 255 - red
        color = Color(green, red, 0)
        length = percent * strip.numPixels() / 100
    for i in range(length):
        strip.setPixelColor(i, color)
    strip.show()

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-t', '--test', action='store_true', help='test the fill colour by cycling through 0-100% with a wait time in ms')
    parser.add_argument('percent', type=int, help='Specify the percentage of the strip to fill')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    if not args.clear:
        print('Use "-c" argument to clear LEDs')
    if not args.test:
        print('Use "-t" argument to test')
    if args.test:
        for j in range(1, 101):
            stripGradient(strip, j)
            print 'Car park is ', j, '% full'
            time.sleep(args.percent/1000.0)
    else:
        stripGradient(strip, args.percent)
    if args.clear:
        colorWipe(strip, Color(0,0,0), 10)
