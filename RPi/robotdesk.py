import time


class DeskController():

    def __init__(self, use_gpio=True, relay_a=4, relay_b=17, ht_file="ht.rd"):

        self.use_gpio = use_gpio
        self.relay_a = relay_a
        self.relay_b = relay_b
        self.height_filename = ht_file
        self.resetting = False

        if self.use_gpio:
            print('Running in GPIO mode')
        else:
            print('Running in whatif mode')

        if self.use_gpio:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.relay_a, GPIO.OUT)
            GPIO.setup(self.relay_b, GPIO.OUT)

    def __del__(self):
        if self.use_gpio:
            import RPi.GPIO as GPIO
            GPIO.cleanup()

    def extend(self):
        print('extending')
        if self.use_gpio:
            import RPi.GPIO as GPIO
            GPIO.output(self.relay_a, GPIO.LOW)
            GPIO.output(self.relay_b, GPIO.HIGH)

    def retract(self):
        print('retracting')
        if self.use_gpio:
            import RPi.GPIO as GPIO
            GPIO.output(self.relay_b, GPIO.LOW)
            GPIO.output(self.relay_a, GPIO.HIGH)

    def stop(self):
        print('stopping')
        if self.use_gpio:
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
            print(('WARNING: height' + height + ' less than zero, reset recommended.'))
            height = 0

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
        print((self.read_height()))


if __name__ == "__main__":
    desk = DeskController(False)
    desk.elevate(2)
    desk.where_am_i()
    desk.elevate(1)
    desk.where_am_i()
    desk.elevate(3)
    desk.where_am_i()
    time.sleep(2)
    desk.lower(6)
    desk.where_am_i()
