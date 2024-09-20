from transmitter import Transmitter
import json
import socket
import struct


class Emulator:
    def __init__(self, device_id: int, socket: socket.socket) -> None:
        self.transmitter = Transmitter(device_id=device_id, device_type=1, socket=socket)
    
    def answer(self, message: str) -> None:
        message_packet_type = json.loads(message)['packetType']
        
        if message_packet_type == 3:
            self.transmitter.send(self.transmitter.get_device_params_data_frame())
        elif message_packet_type == 2:
            print(message)
        else:
            self.transmitter.send(self.transmitter.get_error_message(error_status=1, error_comment=f"packageType = {message_packet_type} isn't supported by this device"))
        
    

if __name__ == '__main__':
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', 6000))
            break
        except:
            pass

        
    em = Emulator(1, client_socket)

    while True:
        length = client_socket.recv(2)
        length = struct.unpack('>H', length)[0]
        message = client_socket.recv(length - 3)
        checksum = client_socket.recv(1)
        em.answer(message)
