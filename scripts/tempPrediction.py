# Written by Savindu9x
# Version:1.0
# File No:0.2
# Source: https://github.com/Savindu9x/ECE4810/tree/main/Project

# .................... Instructions.............. #
# 1. change GPIO pin to your relevant DHT sensor pin


# Importing libraries
import Adafruit_DHT
import requests
import RPi.GPIO as GPIO
from time import sleep, strftime, time


#set the sensor type
sensor = Adafruit_DHT.AM2302
#Set GPIO pin for data_in
GPIO.setmode(GPIO.BOARD)
GPIO=4

def send_text(temp, hum):
    print("Sending to Telegram...")
    #convert int to string literals
    data_string = "Average Temperature: " + str(temp) + "\nAverage Humidity: " + str(hum)
    #Post a request with API key and relavent value field
    r = requests.post("https://maker.ifttt.com/trigger/send_text/with/key/dnoW4eyZ1pL-VgPXKgGHOS", json = {"value1":data_string})
    if r.status_code == 200: #return code if successful
        print("Message Sent Successfully")
    else: #rais an exception
        print("Error! sending texts to telegram")

# function to push data to Google Cloud platform
def push2Cloud():
    print("Data sent")

# function to measure the temperature and humidity
def tempMeasure():
    # Initiate variables for average calculation
    tot_temp = 0
    tot_hum = 0
    #Take the temp and humidity readings
    humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO)
    
    if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
            #send_text(temperature, humidity)
            tot_temp += temperature #calculate total temperature for average
            tot_hum += humidity #calculate total humidity for average
            humidity = round(humidity,2)
            temperature = round(temperature,2)
    else: # Reading doesn't always work! Just print error and we'll try again
        print("Failed to get reading from DHT. Try Again")
    
    with open("/home/pi/project/data_log.csv","a") as log:
        log.write("{0},{1},{2},{3}\n".format(strftime("%Y %m %d"),strftime("%H:%M:%S"),str(temperature),str(humidity)))
    #set time interval of 2 seconds for sensor to settle
    sleep(15)

while True:
    tempMeasure()