import numpy as np


class UAV:
    def __init__(self, uav_type: str, serial_number: str) -> None:
        self.uav_type: str = uav_type
        self.serial_number: str = serial_number

    def get_info(self) -> dict:
        return {
	        "uavType": self.uav_type, #  тип объекта
	        "serialNumber": self.serial_number, # серийный номер
	        "startUavLatitude": np.random.random(), # широта точки запуска БПЛА
	        "startUavLongitude": np.random.random(), # долгота точки запуска БПЛА
	        "uavLatitude": np.random.random(), # широта текущего положения БПЛА
	        "uavLongitude": np.random.random(), # долгота текущего положения БПЛА
	        "uavAltitude": np.random.random(), # высота текущего положения БПЛА
	        "operatorLatitude": np.random.random(), # широта положения оператора БПЛА
	        "operatorLongitude": np.random.random() #  долгота положения оператора БПЛА
	}
