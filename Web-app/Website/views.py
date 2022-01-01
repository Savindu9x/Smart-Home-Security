from flask import Blueprint, render_template
from flask_login import login_required, logout_user, current_user
from sqlalchemy.sql.functions import user
from Website.auth import login

views  = Blueprint('views', __name__)

@views.route('/camera/on')
@login_required
def camera_feed():
    return render_template("camera_feed.html", user=current_user)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/<pin>/<action>")
@login_required
def action(pin, action):
   temperature = ''
   humidity = ''
   if pin == "pin1" and action == "on":
      #GPIO.output(led1, GPIO.HIGH)
      print()
    
   if pin == "pin1" and action == "off":
      #GPIO.output(led1, GPIO.LOW)
      print()
    
   if pin == "pin2" and action == "on":
      #GPIO.output(led2, GPIO.HIGH)
      print()
    
   if pin == "pin2" and action == "off":
      #GPIO.output(led2, GPIO.LOW)
      print()
 
   if pin == "dhtpin" and action == "get":
      print('ok')
   #     temp = 29.6
   #     humi = 89.1
   #     humi_ = 90.1
   #     temp_ = 28.7
   #  #   humi, temp = dht.read_retry(dht.DHT11, DHT11_pin)  # Reading humidity and temperature
   #     humi = '{0:0.1f}' .format(humi)
   #     temp = '{0:0.1f}' .format(temp)
   #     humi_ = '{0:0.1f}' .format(humi_)
   #     temp_ = '{0:0.1f}' .format(temp_)

   #     p_hum = humi_
   #     p_temp = temp_
   #     c_temp = temp
   #     c_hum = humi
 
   # templateData = {
   # 'c_temp' : c_temp,
   # 'p_temp' : p_temp,
   # 'c_hum': c_hum,
   # 'p_hum': p_hum
 
   return render_template('home.html',user=current_user) #, **templateData)