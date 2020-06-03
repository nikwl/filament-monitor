# filament_monitor
## Overview
Suplementary code for a filament monitor I designed for use with the Ender 3. In the past I've used some lower quality filaments that have a tendency to snap and ruin prints. I'm also continually frustrated by situations where the printer runs out of filament mid print. This system hopes to solve this by sending a notification to your phone when the filament runs out, so you can run on over and pause the print. It uses two rotary encoders and a raspberry pi to detect both when the printer is printing and when the filament has stopped. If the filament stops the pi sends a notification to a paired phone. See [here](https://www.thingiverse.com/thing:4414140) for the thingiverse model files and required parts. 

The idea for physical design of this project was to create as unobtrusive and reconfigurable a system as possible. Ideally both modules take up very little space and require very little material to print. The module monitoring printing state could easily be swapped out for a module that monitors the printhead fan or lights. The raspberry pi can also be mounted anywhere on the printer, given long enough cables.

## Installation
1. Setup notify-run for python. \
	Install:
	```bash
	pip install notify-run
	```
	Register your phone for notifications:
	```bash
	notify-run register
	```
2. Install cron to enable scripts to run on startup (you can use other methods as well). \
	Install:
	```bash
	sudo apt-get install cron
	```
	Set script to run on startup by running `crontab -e` and then adding the following line to the bottom of the file: 
	```bash
	@reboot  python /path/to/repo/filament_feeder.py &
	```
3. Run `python filament_feeder.py` (or reboot the pi) and see if you get a startup notification. If you don't, check the logfile.