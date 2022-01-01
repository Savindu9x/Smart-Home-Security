# Written by Savindu9x
# Version:1.0
# File No:0.1
# Source: https://github.com/Savindu9x/ECE4810/tree/main/Project
# Modules: calculateDistance - objectDetect - sendVideo
# ............Instructions...............
# 1. Replace your IFTTT API KEY.
# 2.

# Importing libraries.
import os
import pickle5 as pickle
import RPi.GPIO as GPIO
import datetime as dt
import numpy as np
import csv
import time
import requests
import filestack
import picamera
from sklearn.neighbors import KNeighborsClassifier
from FaceRecognition import faceDetect

# Set GPIO pins for ultrasonic sensor A - movement detection/handgesture recognition
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
PIN_TRIGGER_A = 18
PIN_ECHO_A = 16
GPIO.setup(PIN_TRIGGER_A, GPIO.OUT)
GPIO.setup(PIN_ECHO_A, GPIO.IN)
# Set GPIO pins for ultrasonic sensor B - handgesture recognition
# PIN_TRIGGER_B = 22
# PIN_ECHO_B = 24
# GPIO.setup(PIN_TRIGGER_B, GPIO.OUT)
# GPIO.setup(PIN_ECHO_B, GPIO.IN)

# Define the user as Client with API Key
client = filestack.Client("ARecFiHv4Rb6Vc8MfGVuDz")
cmd = 'MP4Box -add in.h264 alert.mp4'
#define camera parameters
camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 30
#camera.iso = 800
camera.annotate_background = picamera.Color('black')
camera.annotate_text_size = 60
#camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# function to return distance with a interval of two seconds
def calculateDistance():
    time.sleep(1)
    print("Calculating distance...")
    GPIO.output(PIN_TRIGGER_A, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER_A, GPIO.LOW)
    while GPIO.input(PIN_ECHO_A) == 0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO_A) == 1:
        pulse_end_time = time.time()
    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    print("Distance:", distance, "cm")
    return distance
# Initiate lists for collecting
# distances and saving data to csv file
dist_array = []
save_array = []

# function to collect hand movement for recognition
# def collectDistance():
#     print("Six distances are measured")
#     time.sleep(2)
#     print("Calculating distance")
#     GPIO.output(PIN_TRIGGER_B, GPIO.HIGH)
#     time.sleep(0.00001)
#     GPIO.output(PIN_TRIGGER_B, GPIO.LOW)
#     while GPIO.input(PIN_ECHO_B) == 0:
#         pulse_start_time = time.time()
#     while GPIO.input(PIN_ECHO_B) == 1:
#         pulse_end_time = time.time()
#     pulse_duration = pulse_end_time - pulse_start_time
#     distance = round(pulse_duration * 17150, 2)
#     print("Distance:", distance, "cm")
#     return distance

# function to save data arrays to google sheet
# def saveCSV():
#     # opens an existing .csv file and pass as a file object
#     with open('distance_dataset.csv', 'a', newline='') as f:
#         # returns writer object to convert user data into delimited strings.
#         write = csv.writer(f)
#         # Write all elements in rows to the writer’s file object
#         write.writerows(save_array)

# function to send text messages to telegram bot
def sendtext(message,mode):
    print("Sending to Telegram...")
    #convert int to string literals
    if mode == 1:
        data_string = str(message) + " has entered the premise at " + str(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    elif mode == 2:
        data_string = str(message) + " has requested the access to premise at " + str(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    #Post a request with API key and relavent value field
    r = requests.post("https://maker.ifttt.com/trigger/send_text/with/key/dnoW4eyZ1pL-VgPXKgGHOS", json = {"value1":data_string})
    if r.status_code == 200: #return code if successful
        print("Message Sent Successfully")
    else: #rais an exception
        print("Error! sending texts to telegram")

#function to capture photo and send to telgram chat
def sendphoto():
    camera.capture("alert.jpg") 
    new_filelink = client.upload(filepath="alert.jpg") # upload the clip to filestack
    # Sending the upload link to IFTTT Telegram bot
    # Enter YOUR API KEY
    r = requests.post("https://maker.ifttt.com/trigger/trigger/with/key/dnoW4eyZ1pL-VgPXKgGHOS",
                      json={"value1": new_filelink.url})
    if r.status_code == 200: # Successfully video clip sent
        print("photo Sent")
    else: # raise an exception
        print("Error in sending photo to Telegram")

# function to record video and send to telegram chat
def sendVideo():
    camera.start_recording('in.h264')# Capturing a 30 seconds long video
    camera.wait_recording(10)
    camera.stop_recording()
    os.system(cmd)
    new_filelink = client.upload(filepath="alert.mp4") # upload the clip to filestack
    # Sending the upload link to IFTTT Telegram bot
    # Enter YOUR API KEY
    r = requests.post("https://maker.ifttt.com/trigger/send_video/with/key/dnoW4eyZ1pL-VgPXKgGHOS",
                      json={"value1": new_filelink.url})
    if r.status_code == 200: # Successfully video clip sent
        print("Video clip Sent")
    else: # raise an exception
        print("Error in sending video to Telegram")

# function to recognize the hand gesture
def handGesture():
    state = True
    while state:
     distance = calculateDistance()
     if distance <= 21:
         if len(dist_array) < 6:
             dist_array.append(distance)
         else:
             state = False
    print(dist_array)
    model = pickle.load(open('model_knn.pkl', 'rb'))
    data = [21.6, 20.21, 20.21, 18.63, 18.06, 17.30]
    data = dist_array
    data = (np.array(data)).reshape(1,-1)
    y_out = model.predict(data)
    print("Recognized Hand Gesture:" + y_out)
    return y_out

# function to detect any movements informant movements
def objectDetect():
    while True:
        distance = calculateDistance()
        if distance <= 20:
            name = faceDetect()
            print(str(name)+" is recognized in the frame.")
            if name == 'unknown':
                sendVideo()
            else:
                sendVideo()
                sendtext(name,1)

            # returns the recognized hand gesture
            gesture = handGesture()
            # if hand gesture is move_still, user requests action from owner.
            if gesture == 'move_still':
                print("User requesting action...")
                sendtext(name,2)
                break
            elif gesture == 'move_in':
                break
    
  

#objectDetect()
# calculateDistance()
# activate the relay, lock retract

