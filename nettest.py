#!/usr/bin/env python3
import speedtest
import os
import time
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
load_dotenv()

app_mode = os.getenv("app_mode")
interval = int(os.getenv("interval"))
broker = os.getenv("broker")
port = int(os.getenv("port"))
user = os.getenv("user")
password = os.getenv("password")



def testDownSpeed():
	speedtester = speedtest.Speedtest()
	speedtester.get_best_server()
	if app_mode == 'debug':
		print("Starting Download test...")
	speed = round(speedtester.download() / 1000 / 1000)
	if app_mode == 'debug':
		print("Publishing Download result {} to MQTT...".format(speed))
	publishToMqtt('down', speed)

def testUpSpeed():
	speedtester = speedtest.Speedtest()
	speedtester.get_best_server()
	if app_mode == 'debug':
		print("Starting Upload test...")
	speed = round(speedtester.upload() / 1000 / 1000)
	if app_mode == 'debug':
		print("Publishing Upload test result {} to MQTT...".format(speed))
	publishToMqtt('up', speed)

def on_publish(client,userdata,result):             
    pass

def publishToMqtt(test, speed):
	paho= mqtt.Client("speedtest") 
	paho.username_pw_set(user, password=password)                           
	paho.on_publish = on_publish                         
	paho.connect(broker,port)                                 
	ret= paho.publish("house/speedtest/{}".format(test),speed) 
	paho.disconnect()

def main(interval):
	while True:
		if app_mode == 'debug':
			print("Starting network tests....")
		testDownSpeed()
		testUpSpeed()
		if app_mode == 'debug':
			print("Tests completed....pausing for {} seconds...".format(interval))
		time.sleep(interval)

if __name__ == "__main__":
    main(interval)