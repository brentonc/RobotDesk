import time
import sys
import getopt
import configparser
import json
import socket
from azure.servicebus import ServiceBusService, Message


class DeskController():
    """ The DeskController is responsible for issuing commands to the actuators, thereby
        causing the desk to move up and down.  It also tracks the current height of the desk.
    """

    def __init__(self,
                 notification_sender,
                 whatif=True,
                 relay_a=4,
                 relay_b=17,
                 ht_file="ht.rd",
                 max_height=18):
        """ Initializes the DeskController so that it is ready for operation.abs

            notification_sender -- the sender that should be use to transmit updates.
                                   Must contain method notify_height(height).
            whatif              -- indicates whether or not to run in 'what if' mode.
                                   'What if' mode causes most of the program to run, but does
                                   not actually signal the GPIO pins.
            relay_a             -- GPIO Pin number for the first relay
            relay_b             -- GPIO Pin number for the first relay
            ht_file             -- name of the file to use to track the desk height
            max_height          -- max height to allow the desk to move to.

        """

        self.whatif = whatif
        self.relay_a = relay_a
        self.relay_b = relay_b
        self.height_filename = ht_file
        self.resetting = False
        self.notification_sender = notification_sender
        self.max_height = max_height

        if self.whatif:
            print('Running in whatif mode')
        else:
            print('Running in GPIO mode')

        if not self.whatif:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.relay_a, GPIO.OUT)
            GPIO.setup(self.relay_b, GPIO.OUT)

    def cleanup(self):
        """ Tears down the application, including GPIO pin allocations. """
        print('cleaning up')
        if not self.whatif:
            import RPi.GPIO as GPIO
            GPIO.cleanup()

    def extend(self):
        """ Tells the actuators to extend """
        print('extending')
        if not self.whatif:
            import RPi.GPIO as GPIO
            GPIO.output(self.relay_a, GPIO.LOW)
            GPIO.output(self.relay_b, GPIO.HIGH)

    def retract(self):
        """ Tells the actuators to retract """
        print('retracting')
        if not self.whatif:
            import RPi.GPIO as GPIO
            GPIO.output(self.relay_b, GPIO.LOW)
            GPIO.output(self.relay_a, GPIO.HIGH)

    def stop(self):
        """ Tells the actuators to stop moving """
        print('stopping')
        if not self.whatif:
            import RPi.GPIO as GPIO
            GPIO.output(self.relay_b, GPIO.LOW)
            GPIO.output(self.relay_a, GPIO.LOW)

    def elevate(self, distance):
        """ Tells the actuators to extend a distance

        distance  -- the distance in inches to extend

        """
        extend_time = self.calculate_time(distance)
        self.extend()
        time.sleep(extend_time)
        self.stop()
        self.write_height(self.read_height() + distance)

    def lower(self, distance):
        """ Tells the actuators to retract a distance

            distance  -- the distance in inches to retract
        """
        lower_time = self.calculate_time(distance)
        self.retract()
        time.sleep(lower_time)
        self.stop()
        if not self.resetting:
            self.write_height(self.read_height() - distance)

    def move_to(self, height):
        """ Tells the actuators to move to a specific height.
        Can be higher or lower than the current location.

        height  -- the height above base in inches to move to.

        """
        if height > self.max_height:
            print('that is too high!')
            return
        current = self.where_am_i()
        distance = height - current
        print(("distance to move:" + str(distance)))
        if distance > 0:
            self.elevate(abs(distance))
        elif distance < 0:
            self.lower(abs(distance))

    def reset(self):
        """ Resets the desk height to 0"""
        self.resetting = True
        self.lower(self.max_height + 5)
        self.write_height(0)
        self.resetting = False

    def calculate_time(self, distance):
        """ calculates how long it will take to move the specified distance

            distance -- the distance in inches to calculate for
        """
        rate = .6
        return distance / rate

    def write_height(self, height):
        """ writes the height to disk so the program knows the height of the DeskController
            when it restarts

            height -- number to write to disk
        """
        if float(height) < 0:
            print(('WARNING: height ' + str(height) + ' less than zero, reset recommended.'))
            height = 0
        if float(height) > self.max_height:
            print(('WARNING: height' + str(height) + ' greater than max height (' + str(self.max_height) + '), reset recommended.'))
            height = self.max_height
        height_file = open(self.height_filename, 'w')
        height_file.write(str(height))
        height_file.close()

        if self.notification_sender is not None:
            self.notification_sender.notify_height(height)

    def read_height(self):
        """ reads the height from disk """
        height = "0"
        try:
            height_file = open(self.height_filename, 'r')
            height = height_file.read()
        except IOError:
            print('WARNING: height not known.  Reset recommended.')
            self.write_height(height)  # sets height to 0, may not be correct

        try:
            float_height = float(height)
        except:
            print('WARNING: height file corrupted.  Reset recommended.')
            float_height = 0
        return float_height

    def where_am_i(self):
        """returns the current height of the desk """
        height = self.read_height()
        return height


class AzureQueueClient:
    """ The AzureQueueClient provides the ability to notify 
        a Microsoft Azure Service Bus Queue with messages indicating
        the current height of the desk.

    """

    def __init__(self, key_name, key_value, namespace, queue_name, device_name):
        """initializes the object with the values needed to operate """
        self.key_name = key_name
        self.key_value = key_value
        self.namespace = namespace
        self.queue_name = queue_name
        self.device_name = device_name

    def notify_height(self, height):
        """
        Notifies of the current height

        height -- height to notify of
        """

        d = {}
        d['device_id'] = self.device_name
        d['command_text'] = ""
        d['to_height'] = "{:.9f}".format(height)
        d['move_initiate_time'] = time.strftime("%Y-%m-%dT%H:%M:%S")
        msgbody = json.dumps(d)
        msg = Message(str.encode(msgbody))

        sbs = ServiceBusService(self.namespace,
                                shared_access_key_name=self.key_name,
                                shared_access_key_value=self.key_value)
        print('sending...')

        sbs.send_queue_message(self.queue_name, msg)
        print('sent ' + msgbody)


def run(whatif, notify=True):
    """ Main program for robotdesk.py

        1) Loads configuration if needed
        2) Inializes a DeskController
        3) Provides the user input mechanism and translates to DeskController commands
    """
    azure = None
    if notify:
        # Load the config info from the config file
        config = configparser.ConfigParser()
        config.read("config.rd")

        # Make sure we have the items in the config
        try:
            azure_servicebus_keyname = config.get('Azure', 'servicebus_keyname')
            azure_servicebus_keyvalue = config.get('Azure', 'servicebus_keyvalue')
            azure_servicebus_namespace = config.get('Azure', 'servicebus_namespace')
            azure_servicebus_queue = config.get('Azure', 'servicebus_queue')

        except Exception:
            sys.exit("Invalid or missing config.txt file.")

        azure = AzureQueueClient(azure_servicebus_keyname,
                                 azure_servicebus_keyvalue,
                                 azure_servicebus_namespace,
                                 azure_servicebus_queue,
                                 socket.gethostname())

    desk = DeskController(azure, whatif)
    try:
        while True:
            print(('Height is ' + str(desk.where_am_i())))
            move_to_raw = input("Move to:")
            if move_to_raw == "reset":
                desk.reset()
            elif move_to_raw == "quit":
                break
            elif move_to_raw == "exit":
                break
            elif move_to_raw == "q":
                break
            else:
                try:
                    height = float(move_to_raw)
                    desk.move_to(height)
                except ValueError:
                    print('Unable to determine height to move to.')

    finally:
        desk.cleanup()


def testrun(whatif):
    """ Executes a test run. """
    try:
        desk = DeskController(whatif)
        desk.elevate(2)
        desk.where_am_i()
        desk.elevate(1)
        desk.where_am_i()
        desk.elevate(3)
        desk.where_am_i()
        time.sleep(2)
        desk.lower(6)
        desk.where_am_i()
    finally:
        desk.cleanup()


def main(argv):
    """ Main program.  Interprets arguments and initiates appropriate run mode"""

    whatif = False
    testrunmode = False
    notify = True
    opts, args = getopt.getopt(argv, "wtq", ["whatif", "testrun", "quiet"])
    for opt, arg in opts:
        if opt in ("-w", "--whatif"):
            whatif = True
        elif opt in ("-t", "--testrun"):
            testrunmode = True
        elif opt in ("-q", "--quiet"):
            notify = False

    if testrunmode:
        testrun(whatif)
    else:
        run(whatif, notify)

if __name__ == "__main__":
    main(sys.argv[1:])

