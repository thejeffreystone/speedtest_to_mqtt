# Speedtest to MQTT

This script was written to provide network speedtest results to a MQTT sensor in the [HomeAssistant](https://home-assistant.io) home automation platform. As expected the python speedtest-cli is resource intensive which makes the idea of running it on a system otehr than your main [HomeAssistant](https://home-assistant.io) a good idea. Not to mention if you are running [HomeAssistant](https://home-assistant.io) on a RaspberryPi you may be constrained by the Pi's network adapter. 

## Requirements
* You will need the ability to execute this script. 
* You will need a MQTT sever that you can publish to.
* if you want to use Splunk to log this script, jump to [You can Splunk it if you want to...](https://github.com/thejeffreystone/speedtest_to_mqtt#you-can-splunk-it-if-you-want-to-you-can-leave-your-friends-behind) 

## Installation
* Install the app by cloning this repo
 - `git clone https://github.com/thejeffreystone/speedtest_to_mqtt`
* Install the required python libraries:
 - `pip install paho-mqtt`
 - `pip install speedtest-cli`
 - `pip install python-dotenv`
* Edit the env-sample and saved as .env

## How To Use

This script is meant to run with something like supervisord, and has a default interval of 3600 seconds (1 hour). If you want to have this script to run speedtests continiously set the interval greater than zero. If interval is set to 0 the script will exit after running once. 

If you want to have cron or some other system mange the script execution then simply set the interval to 0 in the .env 

My use case for this was to update [HomeAssistant](https://home-assistant.io) sensors via MQTT. However, you can use this script to simply publish speedtests to your MQTT. 

## Features
* This script publishes speedtests to topic `hosue/speedtest/<test>` where test is either `download` or `upload`.
* This script utilizes the python `speedtest-cli` library and may not be accurate.
* This script is built to run continiously and will pause for the interval set in the `.env` file, but can be ran using cron or another system. In that case set `interval=0` in the .env file.
* The script has an app_mode set in the .env file. When app_mode is set to `debug` the script will output status messages to stdout. If you would like to supress these, change app_mode to somethign other than `debug`. Default app_mode is `prod`.   
* Log the script's results to Splunk using Splunk's HTTP Event Collector

## You can Splunk It if you want to. You can leave your friends behind...

I added the ability to log to [Splunk's HTTP Event Collector](https://docs.splunk.com/Documentation/Splunk/latest/Data/UsetheHTTPEventCollector) if you are like me and like to Splunk everything. The script leverages [George Starcher's Python Class](https://github.com/georgestarcher/Splunk-Class-httpevent).

If you want to use the Splunk component you will need to install [George Starcher's Python Class](https://github.com/georgestarcher/Splunk-Class-httpevent)
 - `pip install git+git://github.com/georgestarcher/Splunk-Class-httpevent.git`

The update your .env to include the details of your Splunk server:
```
# Splunk Server:
splunk_server=192.168.1.20
# Splunk HEC Port - Default is 8088:
splunk_hec_port=8088
# Splunk Hec SSL:
splunk_hec_ssl=False
# Splunk HEC Token:
splunk_hec_key=
# Splunk index:
splunk_index=main
# Splunk sourcetype:
splunk_sourcetype=speedtest
# Splunk Source:
splunk_source=speedtest_script
# Splunk host:
splunk_host=jarvis

```
If you don't set a token, the script will ignore the Splunk portion. 

If you are new to Splunk or the Splunk's HTTP Event Collector you can find more information at [Use Splunk's HTTP Event Collector](https://docs.splunk.com/Documentation/Splunk/latest/Data/UsetheHTTPEventCollector)

## Compatibility

This script was written and tested using python 3.7.2