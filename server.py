from transmitter import Transmitter
import socket
import struct
import asyncio
import time
            
        

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 6000))
    server_socket.listen(1)
    print("Сервер запущен, ожидает подключения...")
    conn, addr = server_socket.accept()
    print(f"Подключено к {addr}")
    
    t1 = Transmitter(1, 1, conn)

    while True:
        message_type = int(input())
        if message_type == 1:
            t1.send_device_params_command()
        elif message_type == 2:
            t1.send_parameter_querry()
            print(t1.recv())
        elif message_type == 3:
            t1.send_error_message(1, "Hello")
            