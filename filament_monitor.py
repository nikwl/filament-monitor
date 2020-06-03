from RPi import GPIO
import time
import sys

from notify_run import Notify
import socket

clk_pin = 18
filament_pin = 17
stepper_pin = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(filament_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(stepper_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

printer_logfile = 'filament_feeder.log' # Here's where the errors will be printed

machine_running = False		# Is the machine currently printing?
filament_running = True		# Is the filament feeding?

epoch_length = 1			# Seconds/epoch

machine_paused_for = 0		# How many epochs the machine has been paused for, if any
machine_pause_max = 10		# After this many epochs, the machine is no longer running
filament_paused_for = 0		# How many epochs the filament has been paused for, if any
filament_pause_max = 30		# After this many epochs, the filament is no longer moving

notification_backoff = 10 * 60	# How long to backoff before sending another notification

notify = Notify()

# Note that erroring on the send will be caught and logged
try:
	notify.send('Notice: raspberry pi starting up with ip: ' + str(socket.gethostbyname(hostname)))
except:
	with open(printer_logfile, 'a+') as f:
		print(sys.exc_info()[0])

sent_notification = 0
try:
	clk_last_state = GPIO.input(clk_pin)

	while True:
		# Get updated states
		clk_state = GPIO.input(clk_pin)
		filament_state = GPIO.input(filament_pin)
		stepper_state = GPIO.input(stepper_pin)

		# Clock has been incremented
		if clk_state != clk_last_state:

				# The printer is moving
				if stepper_state != clk_state:
						machine_running = True
						machine_paused_for = 0
				
				# Else the printer isn't moving, increment
				else:
					machine_paused_for += 1
					if machine_paused_for >= machine_pause_max:
						machine_running = False
						filament_paused_for = 0

				# The filament is moving
				if filament_state != clk_state:
					filament_paused_for = 0
					filament_running = True
				
				# Else the filament isn't moving, increment
				else:
					if machine_running:
						filament_paused_for += 1
						if filament_paused_for >= filament_pause_max:
							filament_running = False

				# Should we notify?
				if not filament_running and machine_running and (time.time() - sent_notification) >= notification_backoff:
					try:
						notify.send('Notice: Ender 3 Filament has snapped.')
						sent_notification = time.time()
					except:
						with open(printer_logfile, 'a+') as f:
							print(sys.exc_info()[0])
		
		clk_last_state = clk_state
		time.sleep(epoch_length)
finally:
	GPIO.cleanup()
