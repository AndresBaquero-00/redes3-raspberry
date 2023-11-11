import RPi.GPIO as GPIO

PIN = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(PIN, GPIO.IN)

def get_data() -> int:
    return GPIO.input(PIN)
