import time
import sys
import getopt


class DeskController():

    def __init__(self, whatif=True, relay_a=4, relay_b=17, ht_file="ht.rd"):

        self.whatif = whatif
        self.relay_a = relay_a
        self.relay_b = relay_b
        self.height_filename = ht_file
        self.resetting = False

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
        if not self.whatif:
            import RPi.GPIO as GPIO
            GPIO.cleanup()

    def extend(self):
        print('extending')
        if not self.whatif:
            import RPi.GPIO as GPIO
            GPIO.output(self.relay_a, GPIO.LOW)
            GPIO.output(self.relay_b, GPIO.HIGH)

    def retract(self):
        print('retracting')
        if not self.whatif:
            import RPi.GPIO as GPIO
            GPIO.output(self.relay_b, GPIO.LOW)
            GPIO.output(self.relay_a, GPIO.HIGH)

    def stop(self):
        print('stopping')
        if not self.whatif:
            import RPi.GPIO as GPIO
            GPIO.output(self.relay_b, GPIO.LOW)
            GPIO.output(self.relay_a, GPIO.LOW)

    def elevate(self, distance):
        extend_time = self.calculate_time(distance)
        self.extend()
        time.sleep(extend_time)
        self.stop()
        self.write_height(self.read_height() + distance)

    def lower(self, distance):
        lower_time = self.calculate_time(distance)
        self.retract()
        time.sleep(lower_time)
        self.stop()
        if not self.resetting:
            self.write_height(self.read_height() - distance)

    def move_to(self, ht):
        current = self.where_am_i()
        distance = ht - current
        print("distance to move:" + str(distance))
        if distance > 0:
            self.elevate(abs(distance))
        elif distance < 0:
            self.lower(abs(distance))

    def reset(self):
        self.resetting = True
        self.lower(20)
        self.write_height(0)
        self.resetting = False

    def calculate_time(self, distance):
        RATE = .6
        return distance / RATE

    def write_height(self, height):
        if float(height) < 0:
            print(('WARNING: height ' + str(height) + ' less than zero, reset recommended.'))
            height = 0
        if float(height) > 18:
            print(('WARNING: height' + str(height) + ' greater than max height (18), reset recommended.'))
            height = 18
        f = open(self.height_filename, 'w')
        f.write(str(height))
        f.close()

    def read_height(self):
        height = "0"
        try:
            f = open(self.height_filename, 'r')
            height = f.read()
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
        ht = self.read_height()
        return ht


def run(whatif):
    desk = DeskController(whatif)
    try:
        while(True):
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
                    ht = float(move_to_raw)
                    desk.move_to(ht)
                except ValueError:
                    print('Unable to determine height to move to.')

    finally:
        desk.cleanup()


def testrun(whatif):
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
    whatif = False
    testrunmode = False

    opts, args = getopt.getopt(argv, "wt")
    for opt, arg in opts:
        if opt == '-w':
            whatif = True
        elif opt == '-t':
            testrunmode = True

    if testrunmode:
        testrun(whatif)
    else:
        run(whatif)

if __name__ == "__main__":
    main(sys.argv[1:])

