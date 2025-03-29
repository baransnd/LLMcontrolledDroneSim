import Controller.DroneController.AirsimAdapter.object_detector
from Controller.DroneController.Utils.message import Roles
from Controller.DroneController.Utils.message import Message
from email import message
from PySide6.QtCore import Signal, QObject, QMetaObject, Qt, Q_ARG, Slot
import time

# Class that handles surveying the area.

class DroneSurveyor(QObject):
    display_signal = Signal(Message)

    def __init__(self, object_detector_container, view_controller):
        super().__init__()
        self.object_detector_container = object_detector_container
        self.view_controller = view_controller
        self.display_signal.connect(self.view_controller.display)       # Kolin: show the answers of the methods on the UI
        self.person_location = None
        self.person_detected = False
        self.person_found_by_drone_list = []
        self.start_gps = None
        self.drones_count = 1
        self.strips_count_drone_1 = 0                                          # Kolin: The count of the strips.
        self.strips_count_drone_2 = 0                                          # Kolin: The count of the strips.
        self.strips_count_drone_3 = 0                                          # Kolin: The count of the strips.
        self.strips_count_drone_4 = 0                                          # Kolin: The count of the strips.
        self.strips_count_drone_5 = 0                                          # Kolin: The count of the strips.
        self.strips_count_drone_6 = 0                                          # Kolin: The count of the strips.
        self.drones_arrives_count = 0



    """
    @Kolin: If the slot receives a "person found" signal from the object_detector, it changes the attribute "person_detected" to True.

    """  
    @Slot(list)        
    def person_found(self, person_location_and_relatived_drone):
        self.person_detected = True
        self.person_location = person_location_and_relatived_drone[0]
        self.person_found_by_drone_list.append(person_location_and_relatived_drone[1])
        
    def count(self, drone_name='Drone1'):
        if drone_name == "Drone1":
            self.strips_count_drone_1 += 1
            print(f"{drone_name} strips count: {self.strips_count_drone_1}")
            return self.strips_count_drone_1
        elif drone_name == "Drone2":
            self.strips_count_drone_2 += 1
            print(f"{drone_name} strips count: {self.strips_count_drone_2}")
            return self.strips_count_drone_2
        elif drone_name == "Drone3":
            self.strips_count_drone_3 += 1
            print(f"{drone_name} strips count: {self.strips_count_drone_3}")
            return self.strips_count_drone_3
        elif drone_name == "Drone4":
            self.strips_count_drone_4 += 1
            print(f"{drone_name} strips count: {self.strips_count_drone_4}")
            return self.strips_count_drone_4
        elif drone_name == "Drone5":
            self.strips_count_drone_5 += 1
            print(f"{drone_name} strips count: {self.strips_count_drone_5}")
            return self.strips_count_drone_5
        elif drone_name == "Drone6":
            self.strips_count_drone_6 += 1
            print(f"{drone_name} strips count: {self.strips_count_drone_6}")
            return self.strips_count_drone_6
            
        
        
    def calibrate(self, drone_name='Drone1'):
        if drone_name == "Drone1":
            self.strips_count_drone_1 = 0
        elif drone_name == "Drone2":
            self.strips_count_drone_2 = 0
        elif drone_name == "Drone3":
            self.strips_count_drone_3 = 0
        elif drone_name == "Drone4":
            self.strips_count_drone_4 = 0
        elif drone_name == "Drone5":
            self.strips_count_drone_5 = 0
        elif drone_name == "Drone6":
            self.strips_count_drone_6 = 0
            
    def calibrate_all(self):
        self.strips_count_drone_1 = 0
        self.strips_count_drone_2 = 0
        self.strips_count_drone_3 = 0
        self.strips_count_drone_4 = 0
        self.strips_count_drone_5 = 0
        self.strips_count_drone_6 = 0
            
    def set_start_gps(self, gps):
        self.start_gps = gps
        
    @Slot()
    def link_object_detector_to_self(self):
        for object_detector in self.object_detector_container:
            object_detector.person_detected_signal.connect(self.person_found)

    '''
    @Kolin: counter for the drone arrival report.
    '''
    @Slot(int)
    def start_drone_arrives_count(self, number):
        self.drones_arrives_count = 0

        while self.drones_arrives_count != number:
            time.sleep(2)

        message = f"All drones have got in position!"
        self.display_signal.emit(Message(Roles.SYSTEM, message))        
        print(message)
        
        self.drones_arrives_count = 0
        



