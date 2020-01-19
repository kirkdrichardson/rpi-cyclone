#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import enum


# Output led_pins associated with LED lights
led_pins = [11, 12, 13, 15, 16, 18, 22, 7, 35, 37]
reversed_led_pins = led_pins[::-1]

player_one_btn = 33


class Mode(enum.Enum):
	Off = 1
	Paused = 2
	Two_Player = 3


Current_Mode = Mode.Two_Player

Current_LED = None


def setup():
	print("Initializing")
	GPIO.setmode(GPIO.BOARD)        # Numbers GPIOs by physical location
	# Set player_one_btn mode to input, and pull up to high level(3.3V)
	GPIO.setup(player_one_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	for pin in led_pins:
		GPIO.setup(pin, GPIO.OUT)   # Set all led_pins' mode is output
		GPIO.output(pin, GPIO.HIGH)  # Set all led_pins to high(+3.3V) to off led


def handle_button_press(ev=None):
	global Current_Mode
	global Current_LED

	if Current_Mode == Mode.Paused:
		Current_Mode = Mode.Two_Player
	else:
		Current_Mode = Mode.Paused
	print('Detected Button Press - current LED is - ', Current_LED)


def loop():
	GPIO.add_event_detect(player_one_btn, GPIO.FALLING,
	                      callback=handle_button_press)  # wait for falling
	# Create ref to handle current pin sort order.
	current_led_pins = None

	global Current_LED

	while Current_Mode is not Mode.Off:
		# Toggle list to switch direction of LED lights
		current_led_pins = reversed_led_pins if (
			current_led_pins == led_pins) else led_pins

		# if GPIO.input(player_one_btn) == GPIO.LOW: # Check whether the button is pressed or not.
		# 	print('hey')

		if Current_Mode is not Mode.Paused:
			for pin in current_led_pins:
				Current_LED = pin
				GPIO.output(Current_LED, GPIO.LOW)
				time.sleep(0.05)
				GPIO.output(Current_LED, GPIO.HIGH)
		elif Current_LED is not None:
			print("inside elif - current LED is ", Current_LED)
			# Keep the current LED lit while paused
			GPIO.output(Current_LED, GPIO.LOW)
			time.sleep(0.05)
		else:
			GPIO.output(Current_LED, GPIO.HIGH)
			time.sleep(0.05)


def destroy():
	for pin in led_pins:
		GPIO.output(pin, GPIO.HIGH)    # turn off all leds
	GPIO.cleanup()                     # Release resource


if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
	except KeyboardInterrupt:
		destroy()
