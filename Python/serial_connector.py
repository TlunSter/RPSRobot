import serial

class SerialConnector:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None

    def connect(self):
        self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=0.01)

    def send(self, message):
        if self.serial_connection:
            self.serial_connection.write(message.encode())
    def receive(self):
        if self.serial_connection and self.serial_connection.in_waiting > 0 :
            return self.serial_connection.readline().decode().strip()
        return None

    def close(self):
        if self.serial_connection:
            self.serial_connection.close()