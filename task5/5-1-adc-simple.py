import RPi.GPIO as GPIO
from time import sleep

dac    = [8, 11, 7, 1, 0, 5, 12, 6]
troyka = 13
comp   = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)

GPIO.setup(comp, GPIO.IN)


def dbl(number):
    binary_list = []
    while number > 0:
        remainder = number % 2
        binary_list.insert(0, remainder)
        number = number // 2
    while len(binary_list) < 8:
        binary_list.insert(0, 0)
    return binary_list


def adc():
    for i in range(256):
        GPIO.output(dac, dbl(i))
        tmp = GPIO.input(comp)
        sleep(0.01)
        if tmp:
            return i
    return 0


try:
    while True:
        i = 3.3 * adc() / 256.0
        if i:
            print("Текущее напряжение: ", i)
finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()
    print("EOP")
