import numpy as np
import json

from uav import UAV


class Transmitter:
    def __init__(self, device_id: int, device_type: int) -> None:
        self.device_id: int = device_id
        self.device_type: int = device_type

    def get_gps_time(self) -> np.int64:
        return np.random.randint(0, 9223372036854775807, size=None, dtype=np.int64)
    
    def get_header(self, packet_type: int) -> dict:
        return {
                "time": int(self.get_gps_time()),
                "packetType": packet_type,
                "deviceId": self.device_id 
                }
    
    def get_device_position_info(self) -> dict:
        return {
            "deviceType": self.device_type, # тип устройства
            "deviceLatitude": np.random.random(), # широта привязки устройства
            "deviceLongitude": np.random.random(), # долгота привязки устройства
            "deviceAltitude": np.random.random(), # высота привязки устройства
        }
    
    def get_signal_info(self) -> dict:
        return {
            "signalType": np.random.choise([1,2,3,4,5,6,7,8,9,10,51,52]), # тип радиосигнала/принадлежность[усл.ед.]
            "signalFrequency": int(np.random.randint(0, 9223372036854775807, dtype=np.int64)), # частота сигнала [Гц]
            "signalAmplitude": int(np.random.randint(100)), # амплитуда сигнала [от -150дБм до 20дБм]
            "signalWidth": int(np.random.randint(100)), # ширина сигнала [Гц]
            "signalDetectionType": np.random.choise([1,2]), # тип обнаружения [усл.ед.]
        }
    
    def get_device_params(self) -> dict:
        return {
            "centerFrequency": int(np.random.randint(0, 9223372036854775807, dtype=np.int64)), # центральная частота сигнала [Гц]
			"receiveSensitivity": int(np.random.randint(100)), # коэффициент усиления[дБ] (0 – АРУ)
			"detectionBandwidth": int(np.random.randint(0, 9223372036854775807, dtype=np.int64)), # ширина полосы обнаружения [Гц]
		
			"idents": [{ 
					"signalType": "", # тип идентификации
					"signalDetectionType": "" # тип обнаружения
	 	   		}]
        }
        
    def get_device_mode(self) -> dict:
        return {
            "deviceType": self.device_type, # тип устройства 
	        "deviceStatus": int(np.random.choice([1,2,3])), # статус устройства 
	        "supressMode": int(np.random.randint(100)), # режим работы устройства обнаружения и идентификации [усл.ед.]
        }

    def get_uav_detection_data_frame(self, uav: UAV) -> str:
        frame = self.get_header(packet_type=1)
        frame.update(self.get_device_position_info())
        frame.update({"uav": uav.get_info()})
        return str(json.dumps(frame))
    
    def send_device_params_command(self) -> None:
        frame = self.get_header(packet_type=2)
        frame.update({"supressMode": int(np.random.randint(100))})
        frame.update(self.get_device_params())
        self.send(str(json.dumps(frame)))

    def send_parameter_querry(self) -> None:
        self.send(str(json.dumps(self.get_header(packet_type=3))))
    
    def send_device_params_data_frame(self) -> None:
        frame = self.get_header(packet_type=4)
        frame.update(self.get_device_mode())
        frame.update(self.get_device_params())
        self.send(str(json.dumps(frame)))
    
    def send_error_message(self, error_status: int, error_comment: str) -> None:
        frame = self.get_header(packet_type=20)
        frame.update({
            "deviceType": self.device_type,	# тип устройства
	        "deviceErrorStatus": error_status, # критичность ошибки
	        "deviceErrorComment": error_comment, # комментарий к ошибке
        })
        frame.update({
            "deviceErrorStatus": error_status,
            "deviceErrorComment": error_comment
        })
        self.send(str(json.dumps(frame)))
    
    def send(self, message: str) -> None:
        body = message.encode('utf-8')
        length = struct.pack('>H', len(body) + 3)
        checksum = struct.pack('B', sum(body) % 256)
        
        self.socket.sendall(length + body + checksum)

    def recv(self) -> dict:
        length = None
        while not length:
            length = self.socket.recv(2)
            
        length = struct.unpack('>H', length)[0]
        message = self.socket.recv(length - 3)
        checksum = self.socket.recv(1)
        if checksum == struct.pack('B', sum(message) % 256):
            return json.loads(message)
        else:
            self.send_error_message(error_status=1, error_comment="Checksum verification failed")
