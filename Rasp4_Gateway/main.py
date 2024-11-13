import aws_mqtt
import serial_manager
import serial
import time
import json
import random
from global_manager import myAwsMqtt

if __name__ == '__main__':
    myAwsMqtt.connect()
    myAwsMqtt.subscribe()
    
    counter = 0
    
    # Open serial port 
    mySerialManager = serial_manager.SerialManager()
    mySerialManager.open_serial_port(baudrate=115200)

    while True:
        mySerialManager.read_data_serial()
        time.sleep(1)