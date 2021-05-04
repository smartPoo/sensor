import RPi.GPIO as GPIO
import time
from datetime import datetime
import os
import requests

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

echoPin = [24, 27]
trigPin = [23, 22]

for j in range(2):
    GPIO.setup(trigPin[j], GPIO.OUT)
    GPIO.setup(echoPin[j], GPIO.IN)

    print(echoPin[j], trigPin[j])


def measure(echo, trig):
    GPIO.output(trig, False)
    time.sleep(0.5)
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    pulse_start = time.time()

    # save StartTime
    while GPIO.input(echo) == 0:
        pulse_start = time.time()

    # save time of arrival
    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    # time difference between start and arrival
    pulse_duration = pulse_end - pulse_start
    # mutiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = pulse_duration * 17150

    distance = round(distance, 2)

    return distance


print("press Ctrl+c to stop program")

occupied = 'init'
try:
    while True:
        for j in range(2):
            distance = measure(echoPin[j], trigPin[j])
            if(j == 0):
                print('1st Sensor', distance)
                visits = requests.get(
                    'http://139.59.226.250/api/restroom?id='+'2000').json()['data'][0]['visits']
                if(distance > 7):
                    occupied = 0
                else:
                    if (occupied == 0):
                        visits += 1
                    occupied = 1
            if(j == 1):
                print('2nd Sensor', distance)
                paper = 100 - (distance - 0.5)*100/10.00
        data = {
            'restroom_id': 2000,
            'toilet_no': 1,
            'status': occupied,
            'tissue': paper,
            'dustbin': 100,
            'visits': visits
        }
        print(data)
        requests.post('http://139.59.226.250/api/updateToilet', data=data)
        time.sleep(2)

except KeyboardInterrupt:
    print("Shutting Down ...")
    file.close()
