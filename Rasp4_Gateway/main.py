import time
import global_manager
import serial_manager

if __name__ == '__main__':
    global_manager.myAwsMqtt.connect()
    global_manager.myAwsMqtt.subscribe()
    
    counter = 0
    
    # Open serial port 
    global_manager.mySerialManager = serial_manager.SerialManager()
    global_manager.mySerialManager.open_serial_port(baudrate=115200)

    while True:
        global_manager.mySerialManager.read_data_serial()
        time.sleep(1)