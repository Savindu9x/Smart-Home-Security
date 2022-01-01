# Written by Savindu9x
# Version:1.0
# File No:0.3
# Source: https://github.com/Savindu9x/ECE4810/tree/main/Project


import time
from datetime import datetime as dt
import os, random, string
import requests
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)



def validateLogin(userName, password):
    #Connect the MySQL database here
    if userName == 'pasan':
        permission = True
        message = "Sending Verification Code..."
    else:
        permission = False
        message = "Invalid userName or Password\n 2 More attempts left"

    permission = userinSchedule(userName)

    return permission, message

# Sending User the generated verification code
def send_text(verify_key):
    print("Sending Verification code to Telegram...")
    #convert int to string literals
    data_string = "Your verification Key : " + str(verify_key)
    #Post a request with API key and relavent value field
    r = requests.post("https://maker.ifttt.com/trigger/send_text/with/key/dnoW4eyZ1pL-VgPXKgGHOS", json = {"value1":data_string})
    if r.status_code == 200: #return code if successful
        print("Verification code sent Successfully")
    else:
        print("Error! Failed to send verification code")


# function to generate password
def generateVerifyCode():
    length = 6
    chars = string.ascii_letters + string.digits + '!@#$*()'
    random.seed = (os.urandom(1024))
    verify_key = "".join(random.choice(chars) for i in range(length))
    send_text(verify_key)
    return verify_key

# function to compare the generated verify key and
# user entered verify key
def compareVerifyCode(verification_code, verify_key):
    if (verification_code == verify_key):
        permission = True
        message = "Successful ENTRY\n OPENING DOOR..."
    else:
        permission = False
        message = "Verification Failed\n TRY AGAIN"

    return permission, message


def userinSchedule(userName):
    # variable for current time
    now= dt.now()
    # dictionary for time schedule of Users.
    schedule = {'pasan': [dt(2021, 9, 1, 16, 0),dt(2021, 10, 30, 16, 0) ],
                'arief':[dt(2021, 10, 15, 5, 0), dt(2021, 10, 20,12, 0)],
                'dinidu':[dt(2021, 10, 4, 1, 0), dt(2021, 10, 31, 4, 0)]}
    # Checks the user is in schedule
    for k,v in schedule.items():
        if k == userName: # if yes, take the time intervals
            break
    # if the now time is in between the schedule time, grant access
    if (now > v[0]) and (now < v[1]):
        permission = True
    else: # raise exception.
        permission = False
        message = 'Access Denied: Not in the schedule'
        print(message)

    return permission


def doorUnlock():
    print("Door Unlocked")
    # Activate the relay, lock retract
    GPIO.setup(19, GPIO.OUT) # OPEN up the door for 15 secs.
    time.sleep(15)
    # Deactivate the relay, lock extends
    GPIO.setup(19, GPIO.IN)
    time.sleep(3)
    GPIO.cleanup()











