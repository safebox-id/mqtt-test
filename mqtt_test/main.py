import os
import time
import sys
import paho.mqtt.client as mqtt
import json
from random import randint

def on_pre_connect(client,data):
    return

SERVER = '192.168.1.79'
# ACCESS_TOKEN = 'DHT22_DEMO_TOKEN'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=5

sensor_data = {'temperature': 0, 'humidity': 0}

next_reading = time.time()

client = mqtt.Client()
client.on_pre_connect=on_pre_connect

# Set access token
# client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(SERVER, 1883, 60)

client.loop_start()

try:
    while True:
        humidity = randint(80,85)
        temperature = randint(24,27)
        print(u"Temperature: {:g}\u00b0C, Humidity: {:g}%".format(temperature, humidity))
        sensor_data['t'] = temperature
        sensor_data['h'] = humidity

        # Sending humidity and temperature data to ThingsBoard
        client.publish('/home/lab/sensors', json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()