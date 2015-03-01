import RPi.GPIO as GPIO
import time


def extend_actuator(a, b):
    print("extending...")
    GPIO.output(a, GPIO.LOW)
    GPIO.output(b, GPIO.HIGH)


def retract_actuator(a, b):
    print("retracting...")
    GPIO.output(b, GPIO.LOW)
    GPIO.output(a, GPIO.HIGH)


def stop_actuator(a, b):
    GPIO.output(b, GPIO.LOW)
    GPIO.output(a, GPIO.LOW)


def elevate(distance):
    extend_time = calculate_time(distance)
    extend_actuator(relay_1_a_signal, relay_1_b_signal)
    time.sleep(extend_time)
    stop_actuator(relay_1_a_signal, relay_1_b_signal)


def lower(distance):
    lower_time = calculate_time(distance)
    retract_actuator(relay_1_a_signal, relay_1_b_signal)
    time.sleep(lower_time)
    stop_actuator(relay_1_a_signal, relay_1_b_signal)


def calculate_time(distance):
    RATE = .6
    return distance / RATE


def initialize():
    print("Setting up...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_1_a_signal, GPIO.OUT)
    GPIO.setup(relay_1_b_signal, GPIO.OUT)
    print("Done setting up")


if __name__ == "__main__":
    try:
        #setup GPIO using BCM numbering
        relay_1_a_signal = 23
        relay_1_b_signal = 24

        initialize()
        time.sleep(3)

        elevate(10)
        time.sleep(5)
        lower(10)

    finally:
        GPIO.cleanup()







