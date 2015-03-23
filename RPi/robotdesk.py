import time


class DeskController():

    def __init__(self, relay_a, relay_b, use_gpio):

        self.use_gpio = use_gpio
        self.relay_a = relay_a
        self.relay_b = relay_b

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

    def lower(self, distance):
        lower_time = self.calculate_time(distance)
        self.retract()

        time.sleep(lower_time)
        self.stop()

    def reset(self):
        self.lower(20)

    def calculate_time(self, distance):
        RATE = .6
        return distance / RATE



if __name__ == "__main__":
    relay_a_signal = 4
    relay_b_signal = 17

    desk = DeskController(relay_a_signal, relay_b_signal, False)
    desk.elevate(6)
    time.sleep(5)
    desk.lower(6)
