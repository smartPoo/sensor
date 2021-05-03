import RPi.GPIO as GPIO
import time
import requests

url = ''

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

print('Distance measurement in progress')

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

while True:
    GPIO.output(TRIG, False)
    print("Waiting For Sensor To Settle")
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = (
        pulse_duration * 17150
    )
    distance = round(distance, 2)

    if distance < 400:
        print(
            "Distance:", distance - 0.5, "cm"
        )
        postDistance = distance - 0.5
    else:
        print("Out Of Range")

    occupied = True

    if(distance > 7):
        occupied = False

    requests.post(url, data={
        restroom_id: 29,
        toilet_no: 1,
        vacancy: occupied,
    })
