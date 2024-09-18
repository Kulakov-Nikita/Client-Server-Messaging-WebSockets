import numpy as np
import json


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
    
    def get_parameter_querry(self) -> str:
        return str(json.dumps(self.get_header(packet_type=3)))
