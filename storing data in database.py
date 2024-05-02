import time
import datetime
import paho.mqtt.client as mqtt
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

data = 0

class Stopwatch:
    try:
        def __init__(self):
            self.start_time = None
            self.total_elapsed_time = 0
            self.running = False

        def start(self):
            if not self.running:
                self.start_time = time.time()
                self.running = True
                print("Stopwatch started")

        def stop(self):
            if self.running:
                self.total_elapsed_time += time.time() - self.start_time
                self.start_time = None
                self.running = False
                print("Stopwatch stopped")
                time.sleep(2.5)

        def resume(self):
            if not self.running:
                self.start_time = time.time()
                self.running = True
                print("Stopwatch resumed")

        def get_elapsed_time(self):
            if self.running:
                elapsed_time = self.total_elapsed_time + time.time() - self.start_time
            else:
                elapsed_time = self.total_elapsed_time
            return elapsed_time

        def display_time(self):
            elapsed_time = self.get_elapsed_time()
            minutes, seconds = divmod(elapsed_time, 60)
            hours, minutes = divmod(minutes, 60)
            print(f"{hours:02f}:{minutes:02f}:{seconds:05.2f}")

            cred = credentials.Certificate(r"#JSON file")


            firebase_admin.initialize_app(cred, {
                'databaseURL': '#Fire base URL'
            })


            ref = db.reference('/')



            data = {'time': f"{hours:02f}:{minutes:02f}:{seconds:05.2f}"}

            ref.push(data)
            print("Data uploaded successfully.")

    except Exception as e:
        print("Error: ", e)


try:
    def on_connect(client, userdata, flags, rc):

        client.subscribe("virtualnest")


    def on_message(client, userdata, msg):
        global ar_signal
        global data
        ar_signal = int(msg.payload.decode())
        if ar_signal == 1:
            if not stopwatch.running:
                stopwatch.start()
            else:
                stopwatch.resume()
        elif ar_signal == 0:
            stopwatch.stop()
            data = stopwatch.display_time()


    # MQTT broker configuration (replace with your broker details)
    broker_address = "mqtt-dashboard.com"
    broker_port = 1883

    # Create MQTT client
    client = mqtt.Client("#client ID from MQTT server")
    client.on_connect = on_connect
    client.on_message = on_message


    ar_signal = 0


    client.connect(broker_address, broker_port)


    stopwatch = Stopwatch()


    client.loop_forever()
except Exception as e:
    print("Error: ", e)
