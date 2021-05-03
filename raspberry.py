#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from datetime import datetime
import os

# GPIO setup
GPIO.setmode (GPIO.BCM)
GPIO.setwarnings(False)

# setup gpio for echo & trig
echopin = [24,17,22]
trigpin = [23,4,27]
 
for j in range(3):
    GPIO.setup(trigpin[j], GPIO.OUT)
    GPIO.setup(echopin[j], GPIO.IN)
    print j, echopin[j], trigpin[j]
    print " "
    


# Get reading from HC-SR04   
def ping(echo, trig):
    
    GPIO.output(trig, False)
    # Allow module to settle
    time.sleep(0.5)
    # Send 10us pulse to trigger
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

print " press Ctrl+c to stop program "
try:
    # main loop
    while True:
        # get distances and assemble data line for writing 
        results = str(datetime.now()) + ","
        for j in range(3):

            distance = ping(echopin[j], trigpin[j])
            if(j==0):
              if(distance > 7):
                occupied = False
              else:
                occupied = True
            if(j==1):
              dustbin = 100 - (distance - 0.5)*100/10.00
            if(j==2):
              paper = 100 - (distance - 0.5)*100/10.00
            
        requests.post(url, data={
          restroom_id: 29,
          toilet_no: 1,
          vacancy: occupied,
          dustbin: dustbin,
          paper: paper
        })      
        time.sleep (2)    
    
except KeyboardInterrupt:
    print("keyboard interrupt detected, File closed")       
    file.close()    
    
