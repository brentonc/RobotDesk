import RPi.GPIO as GPIO
import time


class Actuator():

    def __init__(self, relay_a_pin, relay_b_pin):
        self.relay_a = relay_a_pin
        self.relay_b = relay_b_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.relay_a, GPIO.OUT)
        GPIO.setup(self.relay_b, GPIO.OUT)

    def extend(self):
        GPIO.output(self.relay_a, GPIO.LOW)
        GPIO.output(self.relay_b, GPIO.HIGH)

    def retract(self):
        GPIO.output(self.relay_b, GPIO.LOW)
        GPIO.output(self.relay_a, GPIO.HIGH)

    def stop(self):
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


def cleanup():
    GPIO.cleanup()


relay_1_a_signal = 23
relay_1_b_signal = 24

if __name__ == "__main__":
    try:
        #setup GPIO using BCM numbering

        actuator = Actuator(relay_1_a_signal, relay_1_b_signal)
        #initialize()
        time.sleep(3)
        actuator.elevate(6)
        time.sleep(5)
        actuator.lower(6)

    finally:
        cleanup()







