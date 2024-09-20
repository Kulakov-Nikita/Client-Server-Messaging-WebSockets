from transmitter import Transmitter
import socket
import struct

class Server:
    def __init__(self, socket: socket.socket) -> None:
        self.transmitter = Transmitter(2, 2, socket)

    def set_params(self) -> None:
        self.transmitter.send(self.transmitter.get_device_params_command())

    def ask_params(self) -> dict:
        self.transmitter.send(self.transmitter.get_parameter_querry())

if __name__ == '__main__':
    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 6000))
        server_socket.listen(1)
        print("Сервер запущен, ожидает подключения...")
        conn, addr = server_socket.accept()
        print(f"Подключено к {addr}")

        try:
            ser = Server(conn)
            ser.set_params()

            ser.ask_params()

            length = conn.recv(2)
            length = struct.unpack('>H', length)[0]
            message = conn.recv(length - 3)
            checksum = conn.recv(1)

            print(message)

        except Exception as e:
            print(e)
            conn.close()
            server_socket.close()