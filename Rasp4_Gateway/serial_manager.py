import serial.tools.list_ports

class SerialManager:
    __serial_comm = None
    __message = ""

    @staticmethod
    def get_serial_ports():
        ports = serial.tools.list_ports.comports()
        N = len(ports)
        communication_ports = None
        for i in range (0, N):
            port = ports[i]
            str_port = str(port)
            print("Port: ", str_port)
            if "USB-SERIAL" in str_port:
                split_port = str_port.split(" ")
                communication_ports = split_port[0]
        return communication_ports
    
    def open_serial_port(self, baudrate, port=get_serial_ports()):
        print("Oppening serial port: ", port)
        if port is None:
            print("No serial port found")
            return
        self.__serial_comm = serial.Serial(port=port, baudrate=baudrate)
        print("Serial port opened")

    def write(self, data):
        self.__serial_comm.write((str(data) +"#").encode())

    def __init__(self):
        pass

    def process_data(self, data):
        # !1:TEMP:23.4#
        data = data.replace("!", "")
        data = data.replace("#", "")
        split_data = data.split(":")
        print("Data received: ", split_data)
        if len(split_data) != 3:
            return None, None, None
        return split_data[0], split_data[1], split_data[2]

    def read_data_serial(self):
        if self.__serial_comm is None:
            print("read_data_serial(self): Serial port is not open")
            return
        bytes_to_read = self.__serial_comm.in_waiting
        if (bytes_to_read > 0):
            self.__message = self.__message + self.__serial_comm.read(bytes_to_read).decode("UTF-8")
            while ("#" in self.__message) and ("!" in self.__message):
                start = self.__message.find("!")
                end = self.__message.find("#")
                new_message = self.__message[start:end + 1]
                id, value_type, value = self.process_data(new_message)
                print("ID: ", id, "Value type: ", value_type, "Value: ", value)
                if (end == len(self.__message)):
                    self.__message = ""
                else:
                    self.__message = self.__message[end + 1:]