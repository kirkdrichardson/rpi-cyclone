#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import enum


# Output pins associated with LED lights
pins = [11, 12, 13, 15, 16, 18, 22, 7, 35, 37]
reversed_pins = pins[::-1]


class Mode(enum.Enum):
	Off = 1
	Two_Player = 2


def setup():
	GPIO.setmode(GPIO.BOARD)        # Numbers GPIOs by physical location
	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)   # Set all pins' mode is output
		GPIO.output(pin, GPIO.HIGH) # Set all pins to high(+3.3V) to off led

def loop():
	current_mode = Mode.Two_Player
	current_pins = None


	while current_mode is not Mode.Off:
		# Toggle list to switch direction of LED lights
		current_pins = reversed_pins if (current_pins == pins) else pins

		for pin in current_pins:
			GPIO.output(pin, GPIO.LOW)
			time.sleep(0.05)
			GPIO.output(pin, GPIO.HIGH)


def destroy():
	for pin in pins:
		GPIO.output(pin, GPIO.HIGH)    # turn off all leds
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()


