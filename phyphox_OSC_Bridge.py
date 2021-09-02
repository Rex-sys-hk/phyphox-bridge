# import mido
# import mido.backends.rtmidi
"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time

from pythonosc import udp_client as osc_client

import requests
import time
import sys
import math

#Initialize and request the parameters
print("\n" * 100)
print("*** PHYPHOX MIDI BRIDGE ***")
print("")
print("Please follow these directions EXTREMELY carefully.")
print("")
print("The original purpose of this tool is to enable a VR piano experience")
print("powered by a smartphone used as an orientation sensor to trigger an")
print("immersive binaural soundstage that tracks with the pianist's head")
print("movement. To do this, a smartphone orientation sensor is connected")
print("to the modulation wheel MIDI controller in Kontakt, or other VI or DAW")
print("")
print("Currently, this app is untested on MacOS.  For Windows users, you will")
print("need the LoopMIDI utility")
print("")
print("To use it, you must have Phyphox installed on your phone to")
print("collect the sensor data. Windows users also should have LoopMIDI running")
print("on your computer to receive the data so that it can be routed to a VI or DAW.")
print("")
print("LoopMIDI should thus be set as an input to your VI or DAW (e.g. Kontakt)")
print("")
print("The basic data chain is like this:")
print("1. Phyphox collects sensor data and sends to your PC")
print("2. Phyphox MIDI bridge receives the data, converts to MIDI CC data")
print("3. Phyphox MIDI bridge sends the CC data to LoopMIDI")
print("4. LoopMIDI sends the CC data to your VI or DAW")
print("")
print("Before starting, please have LoopMIDI running and a Loopback")
print('midi port running. Loopback midi ports have names like "loopMIDI Port 2"')
print("")
dummy = input("Press Enter to continue")



#phyphox configuration
print("\n" * 100)
print("*** SETUP PHYPHOX PHONE CONNECTION")
print("")
print("1. Make sure that your phone and computer are on the same network")
print("2. Open the phyphox app on your phone, go to magnetometer screen")
print("3. Find and check the enable remote access box and note the ip address")
print("4. Press the play button to start the phone sensor transmitting")
print(" ")
PP_ADDRESS = input("Enter the ip address and port (default to be 192.168.25.103:80, press ENTER to continue): ")
if not PP_ADDRESS:
    PP_ADDRESS = '192.168.25.103:80'
PP_ADDRESS = "http://" + PP_ADDRESS

channel_dic = {
    1:["magX", "magY", "magZ"],
    2:["accX", "accY", "accZ"],
    3:["gyrX", "gyrY", "gyrZ"],
    4:["lat", "lon", "z"],
    5:["pressure"]
}
control_dic = {
    1:[1,2,3],
    2:[1,2,3],
    3:[1,2,3],
    4:[1,2,3],
    5:[1]
}

print("\n" * 100)
print("You are supposed to manually set up data type('1 - Magnetometer' by default): ")
print("1 - Magnetometer")
print("2 - Acceleration")
print("3 - Gyroscope")
print("4 - Location")
print("5 - Pressure")
Category = input("Enter the working sensor type(int): ")
M_CONTROLS = control_dic[int(Category)]
PP_CHANNELS = channel_dic[int(Category)]

print("\n" * 100)
print("***Please init OSC transmition by params***")
osc_localhost = input("please ENTER the localhost ip (default: 127.0.0.1): ")
if not osc_localhost:
    osc_localhost = '127.0.0.1'
osc_port = input("please ENTER the port you want to send (default: 8000): ")
if not osc_port:
    osc_port = 8000
client = osc_client.SimpleUDPClient(osc_localhost, int(osc_port))


counter = 0
mylist = []
while True:
    time.sleep(0.1)
    url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
    data = requests.get(url=url).json()
    input_values = []
    for i, control in enumerate(M_CONTROLS):
        input_values.append(data["buffer"][PP_CHANNELS[i]]["buffer"][0])
    print(input_values)
    """put your interface here"""
    try:
        client.send_message("/OSC/message/style", input_values[0])
        client.send_message("/Y", input_values[1])
        client.send_message("/Z", input_values[2])
    except:
        print("Data may not long enough")
        pass



