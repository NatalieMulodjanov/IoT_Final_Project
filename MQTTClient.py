from paho.mqtt import client as mqtt
from queue import Queue
import time


#broker_address = "192.168.0.189";
broker_address = "10.0.0.248"


def subscribe(topic):

    # Callback method to get messages.
    def on_message(client, userdata, message):
         global received
         received = str(message.payload.decode("utf-8"))


    # Creating a new client instance.
    client = mqtt.Client("client")

    # Connnecting to the broker.
    client.connect(broker_address)

    # Subscribing to the topic.
    client.subscribe(topic)

    # Attaching callback to the client
    client.on_message=on_message

    # Looping the client enought time to get one message.
    client.loop_start()
    time.sleep(0.5)
    client.loop_stop()

    # Disconnecting the client.
    client.disconnect()

    # Returning the message
    return received