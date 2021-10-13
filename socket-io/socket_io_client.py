import json
import socketio
import logging

logging.basicConfig()
with open("private/socket-io-des.json", "r") as f:
    socket_config = json.load(f)

base_url = socket_config["url"]

class Client():

    def __init__(self, args={}):
        self.sio = socketio.Client()
        for event in socket_config["listen"]:
            self.sio.on(event, self.print_on, namespace="/des")

        self.sio.connect(base_url, socketio_path=socket_config["path"], namespaces="/des")

    def print_on(self, data):
        print(f"receive message: {data}")

    def print_emit(self, data):
        print(f"return message: {data}")

    def start(self):
        for event in socket_config["emit"]:
            self.sio.emit(event["event"], callback=self.print_emit, namespace="/des")#, namespace="/des")

    def close(self):
        self.sio.disconnect()
        print("connection closed")


if __name__ == '__main__':
    client = Client()
    client.start()
    client.sio.wait()