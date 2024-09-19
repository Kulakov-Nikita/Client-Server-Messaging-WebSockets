from transmitter import Transmitter
import json
import socket


class Emulator:
    def __init__(self, device_id: int, socket: socket.socket) -> None:
        self.transmitter = Transmitter(device_id=device_id, device_type=1, socket=socket)
    
    def answer(self, message: str) -> None:
        message_packet_type = json.loads(message)['packetType']
        
        if message_packet_type == 3:
            self.transmitter.send(self.transmitter.get_device_params_data_frame())
        else:
            self.transmitter.send(self.transmitter.get_error_message(error_status=1, error_comment=f"packageType = {message_packet_type} isn't supported by this device"))
        
    

if __name__ == '__main__':
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 6000))
    except Exception as e:
        print(e)

try:
    t1 = Transmitter(1,1)
    em = Emulator(1)
    print(em.answer(t1.get_parameter_querry()))
except Exception as e:
    print(e)