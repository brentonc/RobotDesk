# RobotDesk
This repository contains the software for a software-controlled adjustable desk.

##Background
Several years back I started using a standing desk at home and work.  My first standing desk was the [simple $22 Ikea standing desk build](http://iamnotaprogrammer.com/Ikea-Standing-desk-for-22-dollars.html).  It was great and got me hooked.

In 2014/2015 I considered buying a commercial electic standing desk but decided instead to build my own.  

You can see more about the build process on my blog (https://brentonc.com/tag/robot-desk/), including the hardware used and how to wire the actuators to the raspberry pi.

##
This repository contains the following:
* Arduino: an early attempt at the software using an Arduino board
* Design: sketchup files showing desk construction plan
* RPi: the software for the Raspberry pi.
  * robotdesk.py: this is the central raspberry pi software to control the desk via GPIO
  * robotdeskcloud.py: this program listens to a web service for remote commands (typically via Amazon Alexa voice service)

## Arguments
-w: 'whatif' mode.  Runs the code without actually turning GPIO pins.  Useful for testing on a non-raspberry pi device that doesn't have GPIO pins

-t 'test run' mode.  Exercises a specific set of actions to exercise the software

## Usage
Normal usage:
`sudo python3 robotdesk.py`

Whatif usage (useful for testing on a non-raspberry pi device that doesn't have GPIO)
`sudo python3 robotdesk.py -w`

Cloud command listener:
`sudo python3 robotdeskcloud.py`

## Dependencies
The RobotDesk program depends on the following external packages:
* Azure SDK (pip install azure)
