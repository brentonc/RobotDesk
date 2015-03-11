import RPi.GPIO as GPIO
import time

class Actuator():

    def __init__(self, relay_a_pin, relay_b_pin, name):
        self.relay_a = relay_a_pin
        self.relay_b = relay_b_pin
        self.name = name

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.relay_a, GPIO.OUT)
        GPIO.setup(self.relay_b, GPIO.OUT)

    def extend(self):
        print(self.name +' extending')
        GPIO.output(self.relay_a, GPIO.LOW)
        GPIO.output(self.relay_b, GPIO.HIGH)

    def retract(self):
        print(self.name +' retracting')
        GPIO.output(self.relay_b, GPIO.LOW)
        GPIO.output(self.relay_a, GPIO.HIGH)

    def stop(self):
        print(self.name +' stopping')
        GPIO.output(self.relay_b, GPIO.LOW)
        GPIO.output(self.relay_a, GPIO.LOW)


class DeskController():

    def __init__(self, actuators):
        self.actuators = actuators
        if actuators is None:
            self.actuators = []

    def elevate(self, distance):
        extend_time = self.calculate_time(distance)
        for a in self.actuators:
            a.extend()
        
        time.sleep(extend_time)
        for a in self.actuators:
            a.stop()

    def lower(self, distance):
        lower_time = self.calculate_time(distance)
        for a in self.actuators:
            a.retract()
        
        time.sleep(lower_time)
        for a in self.actuators:
            a.stop()

    def reset(self):
        self.lower(20)

    def calculate_time(self, distance):
        RATE = .6
        return distance / RATE


def cleanup():
    GPIO.cleanup()


relay_0_a_signal = 23
relay_0_b_signal = 24
relay_1_a_signal = 20
relay_1_b_signal = 21
relay_2_a_signal = 5
relay_2_b_signal = 6

if __name__ == "__main__":
    try:
        #setup GPIO using BCM numbering
        #actuator = Actuator(relay_1_a_signal, relay_1_b_signal)
        #initialize()
        #time.sleep(3)
        #actuator.elevate(6)
        #time.sleep(5)
        #actuator.lower(6)

        actuators = [
            Actuator(relay_0_a_signal, relay_0_b_signal, "Leg#0"),
            Actuator(relay_1_a_signal, relay_1_b_signal, "Leg#1"),
            Actuator(relay_2_a_signal, relay_2_b_signal, "Leg#2")]
        desk = DeskController(actuators)
        desk.elevate(6)
        time.sleep(5)
        desk.lower(6)	

    finally:
        cleanup()



