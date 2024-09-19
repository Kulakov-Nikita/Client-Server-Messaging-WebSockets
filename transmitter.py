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
    
    def get_device_params_command(self) -> str:
        frame = self.get_header(packet_type=2)
        frame.update({"supressMode": int(np.random.randint(100))})
        frame.update(self.get_device_params())
        return str(json.dumps(frame))

    def get_parameter_querry(self) -> str:
        return str(json.dumps(self.get_header(packet_type=3)))
    
    def get_device_params_data_frame(self) -> str:
        frame = self.get_header(packet_type=4)
        frame.update(self.get_device_mode())
        frame.update(self.get_device_params())
        return str(json.dumps(frame))
    
    def get_error_message(self, error_status: int, error_comment: str) -> str:
        frame = self.get_header(packet_type=20)
        frame.update({
            "deviceType": self.device_type,	# тип устройства
	        "deviceErrorStatus": error_status, # критичность ошибки
	        "deviceErrorComment": error_comment, # комментарий к ошибке
        })
        return str(json.dumps(frame))
