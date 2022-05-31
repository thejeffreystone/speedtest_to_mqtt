#!/usr/bin/env python3
###############################################################################
#   @author         :   Jeffrey Stone 
#   @date           :   03/09/2019
#   @script        	:   nettest.py
#   @description    :   Script to run a network speedtest and publish the results to MQTT
###############################################################################
import sys
import speedtest
import os
import time
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
# set custom .env file-path if your file isn't found
load_dotenv("./env-sample.env")

app_mode = os.getenv("app_mode")
interval = int(os.getenv("interval"))
broker = os.getenv("broker")
port = int(os.getenv("port"))
topic = os.getenv("topic")
user = os.getenv("user")
password = os.getenv("password")
test_server = [] if os.getenv("test_server") == "False" else [int(os.getenv("test_server"))]
# Splunk env:
http_event_collector_key = os.getenv("splunk_hec_key")
http_event_collector_host = os.getenv("splunk_server")
http_event_collector_ssl = os.getenv("splunk_hec_ssl")
http_event_collector_port = int(os.getenv("splunk_hec_port"))
splunk_host = os.getenv("splunk_host")
splunk_source = os.getenv("splunk_source")
splunk_sourcetype = os.getenv("splunk_sourcetype")
splunk_index = os.getenv("splunk_index")

# if splunk hec key set in .env load the splunk libraries
if http_event_collector_key:
	import json
	from splunk_http_event_collector import http_event_collector
	if http_event_collector_ssl == "False":
		http_event_collector_ssl = False
	else:
		http_event_collector_ssl = True

def splunkIt(test,result,total_elapsed_time):
	if app_mode == 'debug':
		print("Time to Splunk It Yo...\n")
	logevent = http_event_collector(http_event_collector_key, http_event_collector_host, http_event_port = http_event_collector_port, http_event_server_ssl = http_event_collector_ssl)
	logevent.popNullFields = True

	payload = {}
	payload.update({"index":splunk_index})
	payload.update({"sourcetype":splunk_sourcetype})
	payload.update({"source":splunk_source})
	payload.update({"host":splunk_host})
	event = {}
	event.update({"action":"success"})
	event.update({"test":test})
	event.update({"total_elapsed_time":total_elapsed_time})
	event.update({"test_result":result})
	payload.update({"event":event})
	logevent.sendEvent(payload)
	logevent.flushBatch()
	if app_mode == 'debug':
		print("It has been Splunked...\n")


def testDownSpeed():
	if app_mode == 'debug':
		print("Starting Download test...")
	start = time.time()
	speedtester = speedtest.Speedtest()
	speedtester.get_servers(test_server)
	speedtester.get_best_server()
	speed = round(speedtester.download() / 1000 / 1000)
	end = time.time()
	total_elapsed_time = (end - start)
	if app_mode == 'debug':
		print("Publishing Download result {} to MQTT...".format(speed))
	publishToMqtt('down', speed)
	if http_event_collector_key:
		splunkIt('download',speed,total_elapsed_time)


def testUpSpeed():
	if app_mode == 'debug':
		print("Starting Upload test...")
	start = time.time()
	speedtester = speedtest.Speedtest()
	speedtester.get_servers(test_server)
	speedtester.get_best_server()
	speed = round(speedtester.upload() / 1000 / 1000)
	end = time.time()
	total_elapsed_time = (end - start)
	if app_mode == 'debug':
		print("Publishing Upload test result {} to MQTT...".format(speed))
	publishToMqtt('up', speed)
	if http_event_collector_key:
		splunkIt('upload',speed,total_elapsed_time)

def on_publish(client,userdata,result):             
    pass

def publishToMqtt(test, speed):
	paho= mqtt.Client("speedtest") 
	paho.username_pw_set(user, password=password)                           
	paho.on_publish = on_publish                         
	paho.connect(broker,port)                                 
	ret= paho.publish(topic+"{}".format(test),speed) 
	paho.disconnect()

def main(interval):
	while True:
		if app_mode == 'debug':
			print("Starting network tests....")
		testDownSpeed()
		testUpSpeed()
		if app_mode == 'debug':
			print("Tests completed...")
		if interval > 0:
			print("Time to sleep for {} seconds\n".format(interval))
			time.sleep(interval)
		else:
			if app_mode == 'debug':
				print("No Interval set...exiting...\n")
			sys.exit()

if __name__ == "__main__":
    main(interval)