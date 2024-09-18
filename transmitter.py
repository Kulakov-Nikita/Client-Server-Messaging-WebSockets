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
            "signalFrequency": np.random.randint(0, 9223372036854775807, dtype=np.int64), # частота сигнала [Гц]
            "signalAmplitude": np.random.randint(), # амплитуда сигнала [от -150дБм до 20дБм]
            "signalWidth": np.random.randint(), # ширина сигнала [Гц]
            "signalDetectionType": np.random.choise([1,2]), # тип обнаружения [усл.ед.]
        }

    def get_uav_detection_data_frame(self, uav: UAV) -> str:
        frame = self.get_header(packet_type=1)
        frame.update(self.get_device_position_info())
        frame.update({"uav": uav.get_info()})
        return str(json.dumps(frame))

    def get_parameter_querry(self) -> str:
        return str(json.dumps(self.get_header(packet_type=3)))
