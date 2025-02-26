# client side

import zmq

context = zmq.Context()
print("Connecting to request server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5000")

while True:
    city_request = input("city name to request weather data for: ")
    socket.send_string(city_request)

    
